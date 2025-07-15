from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse
import logging
import os
import json
from datetime import datetime
from typing import Optional
import httpx
from azure.storage.blob import BlobServiceClient
from models import (
    BlobResponse,
    BlobListResponse,
    UploadResponse,
    DeleteResponse,
    TextUploadRequest
)

# ログ設定
logger = logging.getLogger(__name__)

# Blob Storage用のルーター
router = APIRouter()

# Azure Blob Storage設定
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME", "testcontainer")

def get_blob_service_client():
    """Blob Service Clientを取得"""
    if not AZURE_STORAGE_CONNECTION_STRING:
        raise HTTPException(
            status_code=500, 
            detail="Azure Storage connection string not configured"
        )
    return BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)


@router.get("/list", response_model=BlobListResponse)
def list_blobs():
    """コンテナ内のblob一覧を取得"""
    try:
        blob_service_client = get_blob_service_client()
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        
        blobs = []
        for blob in container_client.list_blobs():
            blobs.append({
                "name": blob.name,
                "size": blob.size,
                "last_modified": blob.last_modified.isoformat() if blob.last_modified else None,
                "content_type": blob.content_settings.content_type if blob.content_settings else None
            })
        
        return BlobListResponse(
            container_name=CONTAINER_NAME,
            blob_count=len(blobs),
            blobs=blobs
        )
    except Exception as e:
        logger.error(f"Error listing blobs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list blobs: {str(e)}")


@router.get("/read/{blob_name}", response_model=BlobResponse)
def read_blob(blob_name: str):
    """指定されたblobの内容を読み取り"""
    try:
        blob_service_client = get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(
            container=CONTAINER_NAME, 
            blob=blob_name
        )
        
        # Blobの存在確認
        if not blob_client.exists():
            raise HTTPException(status_code=404, detail=f"Blob '{blob_name}' not found")
        
        # Blobの内容を読み取り
        content = blob_client.download_blob().readall()
        
        # Blobのプロパティを取得
        properties = blob_client.get_blob_properties()
        
        return BlobResponse(
            blob_name=blob_name,
            content=content.decode('utf-8'),
            size=properties.size,
            content_type=properties.content_settings.content_type,
            last_modified=properties.last_modified.isoformat() if properties.last_modified else None
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading blob {blob_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read blob: {str(e)}")


@router.post("/upload/text", response_model=UploadResponse)
def upload_text(request: TextUploadRequest):
    """テキストコンテンツをblobとしてアップロード"""
    try:
        blob_service_client = get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(
            container=CONTAINER_NAME, 
            blob=request.blob_name
        )
        
        # テキストをUTF-8でエンコードしてアップロード
        blob_client.upload_blob(
            data=request.content.encode('utf-8'),
            overwrite=True,
            content_settings={
                "content_type": "text/plain; charset=utf-8"
            }
        )
        
        return UploadResponse(
            blob_name=request.blob_name,
            status="success",
            message=f"Text content uploaded to {request.blob_name}",
            size=len(request.content.encode('utf-8'))
        )
    except Exception as e:
        logger.error(f"Error uploading text to {request.blob_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload text: {str(e)}")


@router.delete("/delete/{blob_name}", response_model=DeleteResponse)
def delete_blob(blob_name: str):
    """指定されたblobを削除"""
    try:
        blob_service_client = get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(
            container=CONTAINER_NAME, 
            blob=blob_name
        )
        
        # Blobの存在確認
        if not blob_client.exists():
            raise HTTPException(status_code=404, detail=f"Blob '{blob_name}' not found")
        
        # Blobを削除
        blob_client.delete_blob()
        
        return DeleteResponse(
            blob_name=blob_name,
            status="success",
            message=f"Blob {blob_name} deleted successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting blob {blob_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete blob: {str(e)}")


@router.get("/download/{blob_name}")
def download_blob(blob_name: str):
    """指定されたblobをダウンロード"""
    try:
        blob_service_client = get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(
            container=CONTAINER_NAME, 
            blob=blob_name
        )
        
        # Blobの存在確認
        if not blob_client.exists():
            raise HTTPException(status_code=404, detail=f"Blob '{blob_name}' not found")
        
        # Blobの内容とプロパティを取得
        content = blob_client.download_blob().readall()
        properties = blob_client.get_blob_properties()
        
        return PlainTextResponse(
            content=content.decode('utf-8'),
            headers={
                "Content-Disposition": f'attachment; filename="{blob_name}"',
                "Content-Type": properties.content_settings.content_type or "text/plain"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading blob {blob_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to download blob: {str(e)}")
