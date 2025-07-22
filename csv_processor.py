"""
CSV EventGrid 処理ハンドラー

このモジュールは以下の機能を提供します：
- EventGridからのCSV処理イベントを受信
- BlobからCSVファイルをダウンロード
- CSVデータの解析とデータベース保存
- 処理ステータスの更新
"""

import csv
import io
import json
import logging
from datetime import datetime
from typing import List, Dict, Any
from azure.storage.blob import BlobServiceClient
from database import db_manager
from models import (
    HistogramCSVData,
    ProjectCSVData,
    UserCSVData,
    AssignDataCSVData,
)
from db_crud import (
    HistogramDataCRUD,
    ProjectDataCRUD,
    UserDataCRUD,
    AssignDataCSVCRUD,
)
import os

logger = logging.getLogger(__name__)

# Azure設定
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CSV_CONTAINER_NAME = os.getenv("CSV_CONTAINER_NAME", "csv-uploads")


def get_blob_service_client():
    """Blob Service Clientを取得"""
    if not AZURE_STORAGE_CONNECTION_STRING:
        raise Exception("Azure Storage connection string not configured")
    return BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)


async def download_csv_from_blob(blob_name: str) -> str:
    """BlobからCSVファイルをダウンロード"""
    try:
        blob_service_client = get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(
            container=CSV_CONTAINER_NAME, blob=blob_name
        )

        # Blobの内容をダウンロード
        blob_data = blob_client.download_blob()
        csv_content = blob_data.readall().decode("utf-8-sig")

        logger.info(f"CSVファイルをダウンロードしました: {blob_name}")
        return csv_content

    except Exception as e:
        logger.error(f"CSVダウンロードエラー: {str(e)}")
        raise


async def update_blob_metadata(blob_name: str, metadata_updates: Dict[str, str]):
    """Blobのメタデータを更新"""
    try:
        blob_service_client = get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(
            container=CSV_CONTAINER_NAME, blob=blob_name
        )

        # 現在のメタデータを取得
        blob_properties = blob_client.get_blob_properties()
        current_metadata = blob_properties.metadata or {}

        # メタデータを更新
        current_metadata.update(metadata_updates)

        # メタデータを設定
        blob_client.set_blob_metadata(current_metadata)

        logger.info(f"Blobメタデータを更新しました: {blob_name}")

    except Exception as e:
        logger.error(f"メタデータ更新エラー: {str(e)}")
        raise


async def parse_csv_content(csv_content: str) -> List[Dict[str, Any]]:
    """CSV内容を解析して辞書のリストに変換"""
    try:
        csv_reader = csv.DictReader(io.StringIO(csv_content))

        data_list = []
        for row_num, row in enumerate(csv_reader, start=1):
            if not any(row.values()):  # 空行をスキップ
                continue
            data_list.append(row)

        if not data_list:
            raise ValueError("CSVファイルにデータが含まれていません")

        return data_list

    except Exception as e:
        logger.error(f"CSV解析エラー: {str(e)}")
        raise


async def process_histogram_csv(blob_name: str, csv_content: str) -> int:
    """ヒストグラムCSVを処理"""
    try:
        # CSV解析
        csv_data = await parse_csv_content(csv_content)

        # データ検証とPydanticモデルに変換
        validated_data = []
        for row_num, row in enumerate(csv_data, start=1):
            try:
                histogram_data = HistogramCSVData(**row)
                validated_data.append(histogram_data.dict())
            except Exception as e:
                raise ValueError(f"行 {row_num}: データ形式エラー - {str(e)}")

        # データベース操作
        async with db_manager.async_session_maker() as db:
            try:
                # 既存データを削除
                await HistogramDataCRUD.clear_histogram_data(db)

                # 新しいデータを一括挿入
                records_processed = await HistogramDataCRUD.bulk_create_histogram_data(
                    db, validated_data
                )
                await db.commit()
            except Exception:
                await db.rollback()
                raise

        logger.info(f"ヒストグラムデータ処理完了: {records_processed}件")
        return records_processed

    except Exception as e:
        logger.error(f"ヒストグラムCSV処理エラー: {str(e)}")
        raise


async def process_project_csv(blob_name: str, csv_content: str) -> int:
    """プロジェクトCSVを処理"""
    try:
        # CSV解析
        csv_data = await parse_csv_content(csv_content)

        # データ検証とPydanticモデルに変換
        validated_data = []
        for row_num, row in enumerate(csv_data, start=1):
            try:
                project_data = ProjectCSVData(**row)
                validated_data.append(project_data.dict())
            except Exception as e:
                raise ValueError(f"行 {row_num}: データ形式エラー - {str(e)}")

        # データベース操作
        async with db_manager.async_session_maker() as db:
            try:
                # 既存データを削除
                await ProjectDataCRUD.clear_project_data(db)

                # 新しいデータを一括挿入
                records_processed = await ProjectDataCRUD.bulk_create_project_data(
                    db, validated_data
                )
                await db.commit()
            except Exception:
                await db.rollback()
                raise

        logger.info(f"プロジェクトデータ処理完了: {records_processed}件")
        return records_processed

    except Exception as e:
        logger.error(f"プロジェクトCSV処理エラー: {str(e)}")
        raise


async def process_user_csv(blob_name: str, csv_content: str) -> int:
    """ユーザーCSVを処理"""
    try:
        # CSV解析
        csv_data = await parse_csv_content(csv_content)

        # データ検証とPydanticモデルに変換
        validated_data = []
        for row_num, row in enumerate(csv_data, start=1):
            try:
                user_data = UserCSVData(**row)
                validated_data.append(user_data.dict())
            except Exception as e:
                raise ValueError(f"行 {row_num}: データ形式エラー - {str(e)}")

        # データベース操作
        async with db_manager.async_session_maker() as db:
            try:
                # 既存データを削除
                await UserDataCRUD.clear_user_data(db)

                # 新しいデータを一括挿入
                records_processed = await UserDataCRUD.bulk_create_user_data(
                    db, validated_data
                )
                await db.commit()
            except Exception:
                await db.rollback()
                raise

        logger.info(f"ユーザーデータ処理完了: {records_processed}件")
        return records_processed

    except Exception as e:
        logger.error(f"ユーザーCSV処理エラー: {str(e)}")
        raise


async def process_assign_csv(blob_name: str, csv_content: str) -> int:
    """アサインCSVを処理"""
    try:
        # CSV解析
        csv_data = await parse_csv_content(csv_content)

        # データ検証とPydanticモデルに変換
        validated_data = []
        for row_num, row in enumerate(csv_data, start=1):
            try:
                assign_data = AssignDataCSVData(**row)
                # 辞書に変換し、SQLAlchemy モデルに不要なフィールドを除外
                data_dict = assign_data.dict()
                # AssignDataテーブルに存在するフィールドのみを抽出
                filtered_dict = {
                    k: v
                    for k, v in data_dict.items()
                    if k
                    in [
                        "user_name",
                        "assin_execution",
                        "assin_maintenance",
                        "assin_prospect",
                        "assin_common_cost",
                        "assin_most_com_ps",
                        "assin_sales_mane",
                        "assin_investigation",
                        "assin_project_code",
                        "assin_directly",
                        "assin_common",
                        "assin_sales_sup",
                    ]
                }
                validated_data.append(filtered_dict)
            except Exception as e:
                raise ValueError(f"行 {row_num}: データ形式エラー - {str(e)}")

        # データベース操作
        async with db_manager.async_session_maker() as db:
            try:
                # 既存データを削除
                await AssignDataCSVCRUD.clear_assign_data(db)

                # 新しいデータを一括挿入
                records_processed = await AssignDataCSVCRUD.bulk_create_assign_data(
                    db, validated_data
                )
                await db.commit()
            except Exception:
                await db.rollback()
                raise

        logger.info(f"アサインデータ処理完了: {records_processed}件")
        return records_processed

    except Exception as e:
        logger.error(f"アサインCSV処理エラー: {str(e)}")
        raise


async def process_csv_from_eventgrid(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """EventGridイベントからCSVファイルを処理"""
    try:
        blob_name = event_data.get("blobName")
        data_type = event_data.get("dataType")

        if not blob_name or not data_type:
            raise ValueError("blobNameまたはdataTypeが見つかりません")

        logger.info(f"CSV処理開始: {data_type} - {blob_name}")

        # 処理開始をメタデータに記録
        await update_blob_metadata(
            blob_name,
            {
                "processing_status": "processing",
                "processing_start_time": json.dumps(datetime.now().isoformat()),
            },
        )

        # BlobからCSVファイルをダウンロード
        csv_content = await download_csv_from_blob(blob_name)

        # データタイプに応じて処理
        records_processed = 0
        if data_type == "histograms":
            records_processed = await process_histogram_csv(blob_name, csv_content)
        elif data_type == "projects":
            records_processed = await process_project_csv(blob_name, csv_content)
        elif data_type == "users":
            records_processed = await process_user_csv(blob_name, csv_content)
        elif data_type == "assigns":
            records_processed = await process_assign_csv(blob_name, csv_content)
        else:
            raise ValueError(f"サポートされていないデータタイプ: {data_type}")

        # 処理完了をメタデータに記録
        await update_blob_metadata(
            blob_name,
            {
                "processing_status": "completed",
                "processed_records": str(records_processed),
                "processing_end_time": json.dumps(datetime.now().isoformat()),
            },
        )

        result = {
            "success": True,
            "blob_name": blob_name,
            "data_type": data_type,
            "records_processed": records_processed,
            "message": f"{data_type}データの処理が完了しました（{records_processed}件）",
        }

        logger.info(f"CSV処理完了: {result}")
        return result

    except Exception as e:
        error_message = str(e)
        logger.error(f"CSV処理エラー: {error_message}")

        # エラーをメタデータに記録
        if blob_name:
            try:
                await update_blob_metadata(
                    blob_name,
                    {
                        "processing_status": "error",
                        "error_message": error_message,
                        "processing_end_time": json.dumps(datetime.now().isoformat()),
                    },
                )
            except Exception as meta_error:
                logger.error(f"メタデータ更新エラー: {meta_error}")

        return {
            "success": False,
            "blob_name": blob_name,
            "data_type": data_type,
            "error_message": error_message,
            "message": f"CSV処理でエラーが発生しました: {error_message}",
        }
