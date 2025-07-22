"""
CSV Blob Storage エンドポイント

このモジュールは以下のCSV専用Blob Storage機能を提供します：
- CSVファイルのBlobストレージへのアップロード
- EventGridトリガーによる非同期処理
- CSVファイルのメタデータ管理
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from azure.storage.blob import BlobServiceClient, ContentSettings
import httpx
import logging
import os

from models import CSVUploadResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["CSV Blob Storage"])

# Azure設定
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CSV_CONTAINER_NAME = os.getenv("CSV_CONTAINER_NAME", "csv-uploads")
EVENTGRID_TOPIC_ENDPOINT = os.getenv("EVENTGRID_TOPIC_ENDPOINT")
EVENTGRID_ACCESS_KEY = os.getenv("EVENTGRID_ACCESS_KEY")


def get_blob_service_client():
    """Blob Service Clientを取得"""
    if not AZURE_STORAGE_CONNECTION_STRING:
        raise HTTPException(
            status_code=500, detail="Azure Storage connection string not configured"
        )
    return BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)


async def publish_csv_processing_event(blob_info: Dict[str, Any], data_type: str):
    """CSVファイル処理のEventGridイベントをHTTPで発行"""
    try:
        if not EVENTGRID_TOPIC_ENDPOINT or not EVENTGRID_ACCESS_KEY:
            logger.warning("EventGrid設定が不完全です - イベント発行をスキップします")
            return

        # イベントデータを構築
        event_data = {
            "blobName": blob_info["blob_name"],
            "containerName": blob_info["container_name"],
            "blobUrl": blob_info["blob_url"],
            "dataType": data_type,
            "fileSize": blob_info["file_size"],
            "metadata": blob_info["metadata"],
            "processingStatus": "pending",
        }

        # EventGridイベントを作成
        event = {
            "id": str(uuid.uuid4()),
            "eventType": "csvfile.uploaded",
            "subject": f"csv/{data_type}/{blob_info['blob_name']}",
            "eventTime": datetime.now().isoformat() + "Z",
            "data": event_data,
            "dataVersion": "1.0",
        }

        # HTTPでイベントを発行
        headers = {
            "aeg-sas-key": EVENTGRID_ACCESS_KEY,
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                EVENTGRID_TOPIC_ENDPOINT, json=[event], headers=headers, timeout=30.0
            )
            response.raise_for_status()

        logger.info(
            f"EventGridイベントを発行しました: {data_type} - {blob_info['blob_name']}"
        )

    except Exception as e:
        logger.error(f"EventGrid発行エラー: {str(e)}")
        # EventGridの失敗は処理を停止させない
        pass


async def upload_csv_to_blob(
    file: UploadFile, data_type: str, metadata: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """CSVファイルをBlobストレージにアップロード"""
    try:
        # ファイル名を生成（重複を避けるためUUIDを使用）
        file_extension = ".csv"
        if file.filename and file.filename.endswith(".csv"):
            original_name = file.filename[:-4]  # .csvを除去
        else:
            original_name = file.filename or "unknown"

        unique_filename = f"{data_type}/{datetime.now().strftime('%Y%m%d')}/{uuid.uuid4().hex}_{original_name}{file_extension}"

        # ファイル内容を読み取り
        file_content = await file.read()
        await file.seek(0)  # ファイルポインタをリセット

        # Blobクライアントを取得
        blob_service_client = get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(
            container=CSV_CONTAINER_NAME, blob=unique_filename
        )

        # メタデータを準備
        blob_metadata = {
            "data_type": data_type,
            "original_filename": file.filename or "unknown",
            "upload_timestamp": datetime.now().isoformat(),
            "file_size": str(len(file_content)),
            "processing_status": "pending",
        }

        if metadata:
            blob_metadata.update(metadata)

        # Content Settingsを設定
        content_settings = ContentSettings(
            content_type="text/csv", content_encoding="utf-8"
        )

        # Blobにアップロード
        blob_client.upload_blob(
            file_content,
            overwrite=True,
            metadata=blob_metadata,
            content_settings=content_settings,
        )

        logger.info(f"CSVファイルがBlobにアップロードされました: {unique_filename}")

        return {
            "blob_name": unique_filename,
            "container_name": CSV_CONTAINER_NAME,
            "blob_url": blob_client.url,
            "file_size": len(file_content),
            "metadata": blob_metadata,
        }

    except Exception as e:
        logger.error(f"Blobアップロードエラー: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Blobアップロードに失敗しました: {str(e)}"
        )


@router.post("/histograms/upload", response_model=CSVUploadResponse)
async def upload_histogram_csv_to_blob(
    background_tasks: BackgroundTasks, file: UploadFile = File(...)
):
    """ヒストグラムCSVをBlobにアップロードしてEventGridで処理"""
    try:
        # ファイル形式チェック
        if not file.filename or not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=415, detail="CSVファイルのみアップロード可能です"
            )

        # Blobにアップロード
        blob_info = await upload_csv_to_blob(file, "histograms")

        # バックグラウンドでEventGridイベントを発行
        background_tasks.add_task(publish_csv_processing_event, blob_info, "histograms")

        return CSVUploadResponse(
            message="ヒストグラムCSVファイルがアップロードされ、処理待ちです",
            type="histograms",
            filename=file.filename,
            records_processed=0,  # まだ処理していないので0
            updated_by="システム",
            blob_name=blob_info["blob_name"],
            processing_status="pending",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ヒストグラムCSVアップロードエラー: {str(e)}")
        raise HTTPException(
            status_code=500, detail="ヒストグラムCSVアップロードに失敗しました"
        )


@router.post("/projects/upload", response_model=CSVUploadResponse)
async def upload_project_csv_to_blob(
    background_tasks: BackgroundTasks, file: UploadFile = File(...)
):
    """プロジェクトCSVをBlobにアップロードしてEventGridで処理"""
    try:
        # ファイル形式チェック
        if not file.filename or not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=415, detail="CSVファイルのみアップロード可能です"
            )

        # Blobにアップロード
        blob_info = await upload_csv_to_blob(file, "projects")

        # バックグラウンドでEventGridイベントを発行
        background_tasks.add_task(publish_csv_processing_event, blob_info, "projects")

        return CSVUploadResponse(
            message="プロジェクトCSVファイルがアップロードされ、処理待ちです",
            type="projects",
            filename=file.filename,
            records_processed=0,
            updated_by="システム",
            blob_name=blob_info["blob_name"],
            processing_status="pending",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"プロジェクトCSVアップロードエラー: {str(e)}")
        raise HTTPException(
            status_code=500, detail="プロジェクトCSVアップロードに失敗しました"
        )


@router.post("/users/upload", response_model=CSVUploadResponse)
async def upload_user_csv_to_blob(
    background_tasks: BackgroundTasks, file: UploadFile = File(...)
):
    """ユーザーCSVをBlobにアップロードしてEventGridで処理"""
    try:
        # ファイル形式チェック
        if not file.filename or not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=415, detail="CSVファイルのみアップロード可能です"
            )

        # Blobにアップロード
        blob_info = await upload_csv_to_blob(file, "users")

        # バックグラウンドでEventGridイベントを発行
        background_tasks.add_task(publish_csv_processing_event, blob_info, "users")

        return CSVUploadResponse(
            message="ユーザーCSVファイルがアップロードされ、処理待ちです",
            type="users",
            filename=file.filename,
            records_processed=0,
            updated_by="システム",
            blob_name=blob_info["blob_name"],
            processing_status="pending",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ユーザーCSVアップロードエラー: {str(e)}")
        raise HTTPException(
            status_code=500, detail="ユーザーCSVアップロードに失敗しました"
        )


@router.post("/assigns/upload", response_model=CSVUploadResponse)
async def upload_assign_csv_to_blob(
    background_tasks: BackgroundTasks, file: UploadFile = File(...)
):
    """アサインCSVをBlobにアップロードしてEventGridで処理"""
    try:
        # ファイル形式チェック
        if not file.filename or not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=415, detail="CSVファイルのみアップロード可能です"
            )

        # Blobにアップロード
        blob_info = await upload_csv_to_blob(file, "assigns")

        # バックグラウンドでEventGridイベントを発行
        background_tasks.add_task(publish_csv_processing_event, blob_info, "assigns")

        return CSVUploadResponse(
            message="アサインCSVファイルがアップロードされ、処理待ちです",
            type="assigns",
            filename=file.filename,
            records_processed=0,
            updated_by="システム",
            blob_name=blob_info["blob_name"],
            processing_status="pending",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"アサインCSVアップロードエラー: {str(e)}")
        raise HTTPException(
            status_code=500, detail="アサインCSVアップロードに失敗しました"
        )


@router.get("/status/{blob_name}")
async def get_csv_processing_status(blob_name: str):
    """CSV処理ステータスを取得"""
    try:
        blob_service_client = get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(
            container=CSV_CONTAINER_NAME, blob=blob_name
        )

        # Blobのメタデータを取得
        blob_properties = blob_client.get_blob_properties()
        metadata = blob_properties.metadata

        return {
            "blob_name": blob_name,
            "processing_status": metadata.get("processing_status", "unknown"),
            "data_type": metadata.get("data_type", "unknown"),
            "upload_timestamp": metadata.get("upload_timestamp"),
            "original_filename": metadata.get("original_filename"),
            "file_size": metadata.get("file_size"),
            "processed_records": metadata.get("processed_records", "0"),
            "error_message": metadata.get("error_message"),
        }

    except Exception as e:
        logger.error(f"ステータス取得エラー: {str(e)}")
        raise HTTPException(
            status_code=500, detail="処理ステータスの取得に失敗しました"
        )
