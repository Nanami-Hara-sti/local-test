from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
import logging
import os
import json
from datetime import datetime
import httpx
from azure.storage.blob import BlobServiceClient
from models import (
    BlobResponse,
    BlobListResponse,
    UploadResponse,
    DeleteResponse,
    TextUploadRequest,
    EventGridEvent as EventGridEventModel,
    EventGridValidationEvent,
    EventGridResponse,
)

# 環境変数の読み込み
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # python-dotenvがない場合はスキップ
    pass

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Azure Blob Storage API", version="1.0.0")


@app.get("/health")
def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy", "service": "Azure Blob Storage API"}


@app.get("/")
def read_root():
    return HTMLResponse(
        content="""
    <html>
        <head>
            <title>Azure Blob Storage API</title>
            <meta charset="UTF-8">
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 40px; 
                    background-color: #f5f5f5; 
                }
                .container { 
                    background-color: white; 
                    padding: 30px; 
                    border-radius: 8px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                    max-width: 600px; 
                    margin: 0 auto; 
                }
                .header { 
                    text-align: center; 
                    border-bottom: 3px solid #007acc; 
                    padding-bottom: 20px; 
                    margin-bottom: 30px; 
                }
                .links { 
                    display: grid; 
                    gap: 15px; 
                }
                .link-button { 
                    display: block; 
                    color: #007acc; 
                    text-decoration: none; 
                    padding: 15px 20px; 
                    border: 2px solid #007acc; 
                    border-radius: 6px; 
                    text-align: center; 
                    transition: all 0.3s; 
                    font-weight: bold; 
                }
                .link-button:hover { 
                    background-color: #007acc; 
                    color: white; 
                    transform: translateY(-2px); 
                    box-shadow: 0 4px 12px rgba(0,122,204,0.3); 
                }
                .description { 
                    color: #666; 
                    font-size: 14px; 
                    margin-top: 5px; 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 Azure Blob Storage API</h1>
                    <p>FastAPIで作成されたAzure Blob Storage連携API</p>
                </div>
                
                <div class="links">
                    <a href="/blob/view" class="link-button">
                        📄 Blobテキスト表示
                        <div class="description">ファイルの内容を見やすく表示</div>
                    </a>
                    
                    <a href="/blob/list-view" class="link-button">
                        📁 ファイル一覧表示
                        <div class="description">コンテナ内のファイル一覧を表示</div>
                    </a>
                    
                    <a href="/docs" class="link-button">
                        📚 API文書 (Swagger UI)
                        <div class="description">インタラクティブなAPI文書</div>
                    </a>
                    
                    <a href="/redoc" class="link-button">
                        📖 API文書 (ReDoc)
                        <div class="description">きれいなAPI文書</div>
                    </a>
                    
                    <a href="/eventgrid/events-view" class="link-button">
                        ⚡ EventGrid ダッシュボード
                        <div class="description">リアルタイムイベント監視</div>
                    </a>
                    
                    <a href="/eventgrid/setup-guide" class="link-button">
                        🔧 EventGrid セットアップ
                        <div class="description">Azure Event Grid設定ガイド</div>
                    </a>
                </div>
                
                <div style="text-align: center; margin-top: 30px; color: #666;">
                    <small>FastAPI + Azure Blob Storage</small>
                </div>
            </div>
        </body>
    </html>
    """
    )


# Azure Blob Storageからテキストを取得するAPI
@app.get("/blob/text")
def get_blob_text(
    container: str = Query("helloworld", description="Container name"),
    blob: str = Query("helloworld.txt", description="Blob name"),
):
    logger.info("FastAPI function processed a request for blob text.")

    try:
        # 環境変数から接続文字列を取得
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

        if not connection_string:
            raise HTTPException(
                status_code=500,
                detail="Azure Storage connection string not found. Please set AZURE_STORAGE_CONNECTION_STRING environment variable.",
            )

        # BlobServiceClientを作成
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )

        # Blobクライアントを取得
        blob_client = blob_service_client.get_blob_client(
            container=container, blob=blob
        )

        # Blobの存在確認
        if not blob_client.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Blob '{blob}' not found in container '{container}'.",
            )

        # Blobからテキストを取得
        blob_data = blob_client.download_blob()
        blob_text = blob_data.readall().decode("utf-8")

        # プレーンテキストレスポンスを作成
        response_text = f"Blob Text Content:\n\n{blob_text}\n\n--- Blob Info ---\nContainer: {container}\nBlob: {blob}\nSize: {len(blob_text)} characters"

        # プレーンテキストとして返す（改行が正しく表示される）
        return PlainTextResponse(
            content=response_text, media_type="text/plain; charset=utf-8"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error accessing blob: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error accessing blob: {str(e)}")


# Azure Blob StorageからJSONレスポンスでテキストを取得するAPI
@app.get("/blob/json")
def get_blob_json(
    container: str = Query("helloworld", description="Container name"),
    blob: str = Query("helloworld.txt", description="Blob name"),
):
    logger.info("FastAPI function processed a request for blob JSON.")

    try:
        # 環境変数から接続文字列を取得
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

        if not connection_string:
            raise HTTPException(
                status_code=500, detail="Azure Storage connection string not found"
            )

        # BlobServiceClientを作成
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )

        # Blobクライアントを取得
        blob_client = blob_service_client.get_blob_client(
            container=container, blob=blob
        )

        # Blobの存在確認
        if not blob_client.exists():
            raise HTTPException(
                status_code=404,
                detail=f'Blob "{blob}" not found in container "{container}".',
            )

        # Blobからテキストを取得
        blob_data = blob_client.download_blob()
        blob_text = blob_data.readall().decode("utf-8")

        # Blobのプロパティを取得
        blob_properties = blob_client.get_blob_properties()

        # JSONレスポンスを作成
        response_data = {
            "success": True,
            "container": container,
            "blob": blob,
            "text": blob_text,
            "size": len(blob_text),
            "content_type": blob_properties.content_settings.content_type,
            "last_modified": (
                blob_properties.last_modified.isoformat()
                if blob_properties.last_modified
                else None
            ),
            "etag": blob_properties.etag,
            "message": "Successfully retrieved text from blob",
        }

        return response_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error accessing blob: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve text from blob",
            },
        )


# コンテナ内のBlob一覧を取得するAPI
@app.get("/blob/list")
def list_blobs(container: str = Query("helloworld", description="Container name")):
    logger.info("FastAPI function processed a request for blob list.")

    try:
        # 環境変数から接続文字列を取得
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

        if not connection_string:
            raise HTTPException(
                status_code=500, detail="Azure Storage connection string not found"
            )

        # BlobServiceClientを作成
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )

        # コンテナクライアントを取得
        container_client = blob_service_client.get_container_client(container)

        # コンテナの存在確認
        if not container_client.exists():
            raise HTTPException(
                status_code=404, detail=f'Container "{container}" not found.'
            )

        # Blob一覧を取得
        blobs = []
        for blob in container_client.list_blobs():
            blobs.append(
                {
                    "name": blob.name,
                    "size": blob.size,
                    "last_modified": (
                        blob.last_modified.isoformat() if blob.last_modified else None
                    ),
                    "content_type": (
                        blob.content_settings.content_type
                        if blob.content_settings
                        else None
                    ),
                }
            )

        # JSONレスポンスを作成
        response_data = {
            "success": True,
            "container": container,
            "blob_count": len(blobs),
            "blobs": blobs,
        }

        return response_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing blobs: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "message": "Failed to list blobs",
            },
        )


# Azure Blob Storageにテキストを書き込むAPI
@app.post("/blob/upload", response_model=UploadResponse)
def upload_blob_text(
    request_body: TextUploadRequest,
    container: str = Query("helloworld", description="Container name"),
    blob: str = Query("uploaded.txt", description="Blob name"),
):
    logger.info("FastAPI function processed a request for blob upload.")

    try:
        # 環境変数から接続文字列を取得
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

        if not connection_string:
            raise HTTPException(
                status_code=500, detail="Azure Storage connection string not found"
            )

        # BlobServiceClientを作成
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )

        # リクエストボディからテキストを取得
        text_content = request_body.text

        if not text_content:
            raise HTTPException(status_code=400, detail="No text content provided")

        # コンテナクライアントを取得
        container_client = blob_service_client.get_container_client(container)

        # コンテナが存在しない場合は作成
        if not container_client.exists():
            container_client.create_container()
            logger.info(f"Created container: {container}")

        # Blobクライアントを取得
        blob_client = blob_service_client.get_blob_client(
            container=container, blob=blob
        )

        # テキストをBlobにアップロード
        blob_client.upload_blob(
            text_content.encode("utf-8"),
            overwrite=True,
            content_settings={"content_type": "text/plain; charset=utf-8"},
        )

        # レスポンスを作成
        return UploadResponse(
            success=True,
            container=container,
            blob=blob,
            size=len(text_content),
            message="Successfully uploaded text to blob",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading blob: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "message": "Failed to upload text to blob",
            },
        )


# Azure Blob Storageからblobを削除するAPI
@app.delete("/blob/delete", response_model=DeleteResponse)
def delete_blob(
    container: str = Query("helloworld", description="Container name"),
    blob: str = Query(..., description="Blob name (required)"),
):
    logger.info("FastAPI function processed a request for blob deletion.")

    try:
        # 環境変数から接続文字列を取得
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

        if not connection_string:
            raise HTTPException(
                status_code=500, detail="Azure Storage connection string not found"
            )

        # BlobServiceClientを作成
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )

        # Blobクライアントを取得
        blob_client = blob_service_client.get_blob_client(
            container=container, blob=blob
        )

        # Blobの存在確認
        if not blob_client.exists():
            raise HTTPException(
                status_code=404,
                detail=f'Blob "{blob}" not found in container "{container}".',
            )

        # Blobを削除
        blob_client.delete_blob()

        # レスポンスを作成
        return DeleteResponse(
            success=True,
            container=container,
            blob=blob,
            message="Successfully deleted blob",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting blob: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "message": "Failed to delete blob",
            },
        )


# Azure Blob Storageからテキストを見やすく表示するAPI
@app.get("/blob/view")
def view_blob_text(
    container: str = Query("helloworld", description="Container name"),
    blob: str = Query("helloworld.txt", description="Blob name"),
):
    logger.info("FastAPI function processed a request for blob view.")

    try:
        # 環境変数から接続文字列を取得
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

        # デモ用のサンプルデータ（接続文字列がない場合または不正な場合）
        if not connection_string or connection_string.strip() == "" or "DefaultEndpointsProtocol=https;AccountName" not in connection_string:
            # デモ用のサンプルファイル内容
            if container == "helloworld" and blob == "helloworld.txt":
                demo_content = """Hello, World! 🌍

このファイルはAzure Blob Storageのデモ用サンプルファイルです。
実際のAzure Storage接続文字列が設定されていないため、
サンプルデータを表示しています。

📋 ファイル情報:
• コンテナ: helloworld
• ファイル名: helloworld.txt
• 作成日: 2025年7月14日
• サイズ: サンプルデータ

🚀 機能テスト項目:
✅ Blobテキスト表示
✅ Blob一覧表示
✅ EventGrid連携
✅ FastAPI + Azure Functions統合

💡 実際のAzure Blob Storageを使用するには:
1. Azure Storageアカウントを作成
2. AZURE_STORAGE_CONNECTION_STRING環境変数を設定
3. このエンドポイントを再実行

以上、デモファイルの内容でした！"""
                
                html_content = f"""
                <html>
                    <head>
                        <title>Blobテキスト表示 - {blob} (デモモード)</title>
                        <meta charset="UTF-8">
                        <style>
                            body {{ 
                                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                                margin: 40px; 
                                background-color: #f5f5f5; 
                            }}
                            .container {{ 
                                background-color: white; 
                                padding: 30px; 
                                border-radius: 8px; 
                                box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                                max-width: 800px; 
                                margin: 0 auto; 
                            }}
                            .header {{ 
                                border-bottom: 3px solid #007acc; 
                                padding-bottom: 20px; 
                                margin-bottom: 20px; 
                            }}
                            .demo-banner {{
                                background-color: #fff3cd;
                                padding: 15px;
                                border-radius: 5px;
                                border-left: 4px solid #ffc107;
                                margin-bottom: 20px;
                            }}
                            .info {{ 
                                background-color: #e8f4fd; 
                                padding: 15px; 
                                border-radius: 5px; 
                                margin-bottom: 20px; 
                                border-left: 4px solid #007acc; 
                            }}
                            .content {{ 
                                background-color: #f8f9fa; 
                                padding: 20px; 
                                border-radius: 5px; 
                                border: 1px solid #dee2e6; 
                                white-space: pre-wrap; 
                                font-family: 'Courier New', monospace; 
                                line-height: 1.6; 
                            }}
                            .links {{ 
                                margin-top: 20px; 
                                text-align: center; 
                            }}
                            .links a {{ 
                                color: #007acc; 
                                text-decoration: none; 
                                margin: 0 15px; 
                                padding: 8px 16px; 
                                border: 1px solid #007acc; 
                                border-radius: 4px; 
                                display: inline-block; 
                                transition: all 0.3s; 
                            }}
                            .links a:hover {{ 
                                background-color: #007acc; 
                                color: white; 
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">
                                <h1>📄 Azure Blob Storage ファイル表示</h1>
                            </div>
                            
                            <div class="demo-banner">
                                <h3>🚧 デモモード</h3>
                                <p>Azure Storage接続文字列が設定されていないため、サンプルデータを表示しています。</p>
                            </div>
                            
                            <div class="info">
                                <h3>📋 ファイル情報</h3>
                                <p><strong>🗂️ コンテナ:</strong> {container}</p>
                                <p><strong>📄 ファイル名:</strong> {blob}</p>
                                <p><strong>📏 サイズ:</strong> {len(demo_content):,} 文字</p>
                                <p><strong>🕒 最終更新:</strong> 2025年7月14日 (デモデータ)</p>
                                <p><strong>📁 コンテンツタイプ:</strong> text/plain</p>
                            </div>
                            
                            <h3>📖 ファイル内容</h3>
                            <div class="content">{demo_content}</div>
                            
                            <div class="links">
                                <a href="/blob/view">🔄 リロード</a>
                                <a href="/blob/json?container={container}&blob={blob}">🔗 JSON形式</a>
                                <a href="/blob/list?container={container}">📂 ファイル一覧</a>
                                <a href="/docs">📚 API文書</a>
                                <a href="/" style="color: red;">🏠 ホームに戻る</a>
                            </div>
                        </div>
                    </body>
                </html>
                """
                return HTMLResponse(content=html_content)
            
            else:
                # その他のファイルの場合
                html_content = f"""
                <html>
                    <head><title>ファイルが見つかりません (デモモード)</title></head>
                    <body style="font-family: Arial, sans-serif; margin: 40px;">
                        <h2 style="color: orange;">📄 ファイルが見つかりません</h2>
                        <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 15px 0;">
                            <strong>デモモード:</strong> Azure Storage接続文字列が設定されていません。
                        </div>
                        <p><strong>コンテナ:</strong> {container}</p>
                        <p><strong>Blob:</strong> {blob}</p>
                        <p>デモ用ファイルは helloworld/helloworld.txt のみ利用可能です。</p>
                        <a href="/blob/view?container=helloworld&blob=helloworld.txt" style="color: blue;">デモファイルを表示</a>
                        <a href="/" style="color: blue; margin-left: 15px;">ホームに戻る</a>
                    </body>
                </html>
                """
                return HTMLResponse(content=html_content, status_code=404)

        # BlobServiceClientを作成
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )

        # Blobクライアントを取得
        blob_client = blob_service_client.get_blob_client(
            container=container, blob=blob
        )

        # Blobの存在確認
        if not blob_client.exists():
            html_content = f"""
            <html>
                <head><title>ファイルが見つかりません</title></head>
                <body style="font-family: Arial, sans-serif; margin: 40px;">
                    <h2 style="color: orange;">📄 ファイルが見つかりません</h2>
                    <p><strong>コンテナ:</strong> {container}</p>
                    <p><strong>Blob:</strong> {blob}</p>
                    <p>指定されたファイルが存在しません。</p>
                    <a href="/blob/view" style="color: blue;">デフォルトファイルを表示</a>
                </body>
            </html>
            """
            return HTMLResponse(content=html_content, status_code=404)

        # Blobからテキストを取得
        blob_data = blob_client.download_blob()
        blob_text = blob_data.readall().decode("utf-8")

        # Blobのプロパティを取得
        blob_properties = blob_client.get_blob_properties()
        last_modified = (
            blob_properties.last_modified.strftime("%Y年%m月%d日 %H:%M:%S")
            if blob_properties.last_modified
            else "不明"
        )

        # 見やすいHTMLページを作成
        html_content = f"""
        <html>
            <head>
                <title>Blobテキスト表示 - {blob}</title>
                <meta charset="UTF-8">
                <style>
                    body {{ 
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                        margin: 40px; 
                        background-color: #f5f5f5; 
                    }}
                    .container {{ 
                        background-color: white; 
                        padding: 30px; 
                        border-radius: 8px; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                        max-width: 800px; 
                        margin: 0 auto; 
                    }}
                    .header {{ 
                        border-bottom: 3px solid #007acc; 
                        padding-bottom: 20px; 
                        margin-bottom: 20px; 
                    }}
                    .info {{ 
                        background-color: #e8f4fd; 
                        padding: 15px; 
                        border-radius: 5px; 
                        margin-bottom: 20px; 
                        border-left: 4px solid #007acc; 
                    }}
                    .content {{ 
                        background-color: #f8f9fa; 
                        padding: 20px; 
                        border-radius: 5px; 
                        border: 1px solid #dee2e6; 
                        white-space: pre-wrap; 
                        font-family: 'Courier New', monospace; 
                        line-height: 1.6; 
                    }}
                    .links {{ 
                        margin-top: 20px; 
                        text-align: center; 
                    }}
                    .links a {{ 
                        color: #007acc; 
                        text-decoration: none; 
                        margin: 0 15px; 
                        padding: 8px 16px; 
                        border: 1px solid #007acc; 
                        border-radius: 4px; 
                        display: inline-block; 
                        transition: all 0.3s; 
                    }}
                    .links a:hover {{ 
                        background-color: #007acc; 
                        color: white; 
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📄 Azure Blob Storage ファイル表示</h1>
                    </div>
                    
                    <div class="info">
                        <h3>📋 ファイル情報</h3>
                        <p><strong>🗂️ コンテナ:</strong> {container}</p>
                        <p><strong>📄 ファイル名:</strong> {blob}</p>
                        <p><strong>📏 サイズ:</strong> {len(blob_text):,} 文字</p>
                        <p><strong>🕒 最終更新:</strong> {last_modified}</p>
                        <p><strong>📁 コンテンツタイプ:</strong> {blob_properties.content_settings.content_type or 'text/plain'}</p>
                    </div>
                    
                    <h3>📖 ファイル内容</h3>
                    <div class="content">{blob_text}</div>
                    
                    <div class="links">
                        <a href="/blob/view">🔄 リロード</a>
                        <a href="/blob/json?container={container}&blob={blob}">🔗 JSON形式</a>
                        <a href="/blob/list?container={container}">📂 ファイル一覧</a>
                        <a href="/docs">📚 API文書</a>
                    </div>
                </div>
            </body>
        </html>
        """

        return HTMLResponse(content=html_content)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error accessing blob: {str(e)}")
        html_content = f"""
        <html>
            <head><title>エラー</title></head>
            <body style="font-family: Arial, sans-serif; margin: 40px;">
                <h2 style="color: red;">❌ エラーが発生しました</h2>
                <p><strong>エラー内容:</strong> {str(e)}</p>
                <a href="/blob/view" style="color: blue;">再試行</a>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=500)


# コンテナ内のBlob一覧を見やすく表示するAPI
@app.get("/blob/list-view")
def list_blobs_view(container: str = Query("helloworld", description="Container name")):
    logger.info("FastAPI function processed a request for blob list view.")

    try:
        # 環境変数から接続文字列を取得
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

        # デモ用のサンプルデータ（接続文字列がない場合または不正な場合）
        if not connection_string or connection_string.strip() == "" or "DefaultEndpointsProtocol=https;AccountName" not in connection_string:
            # デモ用のサンプルファイル一覧
            demo_blobs = [
                {
                    "name": "helloworld.txt",
                    "size": 421,
                    "last_modified": "2025年7月14日 12:00:00",
                    "content_type": "text/plain"
                },
                {
                    "name": "sample1.txt", 
                    "size": 256,
                    "last_modified": "2025年7月14日 11:30:00",
                    "content_type": "text/plain"
                },
                {
                    "name": "readme.md",
                    "size": 1024,
                    "last_modified": "2025年7月14日 10:00:00", 
                    "content_type": "text/markdown"
                }
            ]
            
            # Blob一覧のHTML行を作成（デモ用）
            blob_rows = ""
            for blob in demo_blobs:
                size_kb = blob["size"] / 1024
                # helloworld.txtのみリンクを有効にする
                if blob["name"] == "helloworld.txt":
                    blob_link = f'<a href="/blob/view?container={container}&blob={blob["name"]}" style="color: #007acc; text-decoration: none;">📄 {blob["name"]}</a>'
                    view_link = f'<a href="/blob/view?container={container}&blob={blob["name"]}" style="color: #28a745; text-decoration: none; margin-right: 10px;">👁️ 表示</a>'
                else:
                    blob_link = f'📄 {blob["name"]} <small>(デモファイル)</small>'
                    view_link = '<span style="color: #999;">👁️ デモファイル</span>'
                
                blob_rows += f"""
                <tr>
                    <td>{blob_link}</td>
                    <td>{size_kb:.1f} KB</td>
                    <td>{blob["last_modified"]}</td>
                    <td>{blob["content_type"]}</td>
                    <td>
                        {view_link}
                        <a href="/blob/json?container={container}&blob={blob["name"]}" style="color: #007acc; text-decoration: none;">🔗 JSON</a>
                    </td>
                </tr>
                """

            # 見やすいHTMLページを作成（デモ用）
            html_content = f"""
            <html>
                <head>
                    <title>Blobファイル一覧 - {container} (デモモード)</title>
                    <meta charset="UTF-8">
                    <style>
                        body {{ 
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                            margin: 40px; 
                            background-color: #f5f5f5; 
                        }}
                        .container {{ 
                            background-color: white; 
                            padding: 30px; 
                            border-radius: 8px; 
                            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                            max-width: 1000px; 
                            margin: 0 auto; 
                        }}
                        .header {{ 
                            border-bottom: 3px solid #007acc; 
                            padding-bottom: 20px; 
                            margin-bottom: 20px; 
                        }}
                        .demo-banner {{
                            background-color: #fff3cd;
                            padding: 15px;
                            border-radius: 5px;
                            border-left: 4px solid #ffc107;
                            margin-bottom: 20px;
                        }}
                        .info {{ 
                            background-color: #e8f4fd; 
                            padding: 15px; 
                            border-radius: 5px; 
                            margin-bottom: 20px; 
                            border-left: 4px solid #007acc; 
                        }}
                        table {{ 
                            width: 100%; 
                            border-collapse: collapse; 
                            margin-bottom: 20px; 
                        }}
                        th, td {{ 
                            border: 1px solid #dee2e6; 
                            padding: 12px; 
                            text-align: left; 
                        }}
                        th {{ 
                            background-color: #007acc; 
                            color: white; 
                            font-weight: bold; 
                        }}
                        tr:nth-child(even) {{ 
                            background-color: #f8f9fa; 
                        }}
                        tr:hover {{ 
                            background-color: #e8f4fd; 
                        }}
                        .links {{ 
                            margin-top: 20px; 
                            text-align: center; 
                        }}
                        .links a {{ 
                            color: #007acc; 
                            text-decoration: none; 
                            margin: 0 15px; 
                            padding: 8px 16px; 
                            border: 1px solid #007acc; 
                            border-radius: 4px; 
                            display: inline-block; 
                            transition: all 0.3s; 
                        }}
                        .links a:hover {{ 
                            background-color: #007acc; 
                            color: white; 
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>📁 Azure Blob Storage ファイル一覧</h1>
                        </div>
                        
                        <div class="demo-banner">
                            <h3>🚧 デモモード</h3>
                            <p>Azure Storage接続文字列が設定されていないため、サンプルデータを表示しています。</p>
                        </div>
                        
                        <div class="info">
                            <h3>📋 コンテナ情報</h3>
                            <p><strong>🗂️ コンテナ名:</strong> {container}</p>
                            <p><strong>📄 ファイル数:</strong> {len(demo_blobs)} 件 (デモデータ)</p>
                        </div>
                        
                        <table>
                            <thead>
                                <tr>
                                    <th>📄 ファイル名</th>
                                    <th>📏 サイズ</th>
                                    <th>🕒 最終更新</th>
                                    <th>📁 タイプ</th>
                                    <th>⚡ アクション</th>
                                </tr>
                            </thead>
                            <tbody>
                                {blob_rows}
                            </tbody>
                        </table>
                        
                        <div class="links">
                            <a href="/blob/list-view">🔄 リロード</a>
                            <a href="/blob/list?container={container}">🔗 JSON形式</a>
                            <a href="/docs">📚 API文書</a>
                            <a href="/" style="color: red;">🏠 ホームに戻る</a>
                        </div>
                    </div>
                </body>
            </html>
            """
            return HTMLResponse(content=html_content)

        # ...existing code... (Azure Storage接続がある場合の処理)

        # BlobServiceClientを作成
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )

        # コンテナクライアントを取得
        container_client = blob_service_client.get_container_client(container)

        # コンテナの存在確認
        if not container_client.exists():
            html_content = f"""
            <html>
                <head><title>コンテナが見つかりません</title></head>
                <body style="font-family: Arial, sans-serif; margin: 40px;">
                    <h2 style="color: orange;">📁 コンテナが見つかりません</h2>
                    <p><strong>コンテナ:</strong> {container}</p>
                    <a href="/blob/list-view">デフォルトコンテナを表示</a>
                </body>
            </html>
            """
            return HTMLResponse(content=html_content, status_code=404)

        # Blob一覧を取得
        blobs = []
        for blob in container_client.list_blobs():
            blobs.append(
                {
                    "name": blob.name,
                    "size": blob.size,
                    "last_modified": (
                        blob.last_modified.strftime("%Y年%m月%d日 %H:%M:%S")
                        if blob.last_modified
                        else "不明"
                    ),
                    "content_type": (
                        blob.content_settings.content_type
                        if blob.content_settings
                        else "text/plain"
                    ),
                }
            )

        # Blob一覧のHTML行を作成
        blob_rows = ""
        for blob in blobs:
            size_kb = blob["size"] / 1024 if blob["size"] else 0
            blob_rows += f"""
            <tr>
                <td><a href="/blob/view?container={container}&blob={blob['name']}" style="color: #007acc; text-decoration: none;">📄 {blob['name']}</a></td>
                <td>{size_kb:.1f} KB</td>
                <td>{blob['last_modified']}</td>
                <td>{blob['content_type']}</td>
                <td>
                    <a href="/blob/view?container={container}&blob={blob['name']}" style="color: #28a745; text-decoration: none; margin-right: 10px;">👁️ 表示</a>
                    <a href="/blob/json?container={container}&blob={blob['name']}" style="color: #007acc; text-decoration: none;">🔗 JSON</a>
                </td>
            </tr>
            """

        # 見やすいHTMLページを作成
        html_content = f"""
        <html>
            <head>
                <title>Blobファイル一覧 - {container}</title>
                <meta charset="UTF-8">
                <style>
                    body {{ 
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                        margin: 40px; 
                        background-color: #f5f5f5; 
                    }}
                    .container {{ 
                        background-color: white; 
                        padding: 30px; 
                        border-radius: 8px; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                        max-width: 1000px; 
                        margin: 0 auto; 
                    }}
                    .header {{ 
                        border-bottom: 3px solid #007acc; 
                        padding-bottom: 20px; 
                        margin-bottom: 20px; 
                    }}
                    .info {{ 
                        background-color: #e8f4fd; 
                        padding: 15px; 
                        border-radius: 5px; 
                        margin-bottom: 20px; 
                        border-left: 4px solid #007acc; 
                    }}
                    table {{ 
                        width: 100%; 
                        border-collapse: collapse; 
                        margin-bottom: 20px; 
                    }}
                    th, td {{ 
                        border: 1px solid #dee2e6; 
                        padding: 12px; 
                        text-align: left; 
                    }}
                    th {{ 
                        background-color: #007acc; 
                        color: white; 
                        font-weight: bold; 
                    }}
                    tr:nth-child(even) {{ 
                        background-color: #f8f9fa; 
                    }}
                    tr:hover {{ 
                        background-color: #e8f4fd; 
                    }}
                    .links {{ 
                        margin-top: 20px; 
                        text-align: center; 
                    }}
                    .links a {{ 
                        color: #007acc; 
                        text-decoration: none; 
                        margin: 0 15px; 
                        padding: 8px 16px; 
                        border: 1px solid #007acc; 
                        border-radius: 4px; 
                        display: inline-block; 
                        transition: all 0.3s; 
                    }}
                    .links a:hover {{ 
                        background-color: #007acc; 
                        color: white; 
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📁 Azure Blob Storage ファイル一覧</h1>
                    </div>
                    
                    <div class="info">
                        <h3>📋 コンテナ情報</h3>
                        <p><strong>🗂️ コンテナ名:</strong> {container}</p>
                        <p><strong>📄 ファイル数:</strong> {len(blobs)} 件</p>
                    </div>
                    
                    {f'''
                    <table>
                        <thead>
                            <tr>
                                <th>📄 ファイル名</th>
                                <th>📏 サイズ</th>
                                <th>🕒 最終更新</th>
                                <th>📁 タイプ</th>
                                <th>⚡ アクション</th>
                            </tr>
                        </thead>
                        <tbody>
                            {blob_rows}
                        </tbody>
                    </table>
                    ''' if blobs else '<p style="text-align: center; color: #666; font-size: 18px;">📭 このコンテナにはファイルがありません</p>'}
                    
                    <div class="links">
                        <a href="/blob/list-view">🔄 リロード</a>
                        <a href="/blob/list?container={container}">🔗 JSON形式</a>
                        <a href="/docs">📚 API文書</a>
                        <a href="/" style="color: red;">🏠 ホームに戻る</a>
                    </div>
                </div>
            </body>
        </html>
        """

        return HTMLResponse(content=html_content)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing blobs: {str(e)}")
        html_content = f"""
        <html>
            <head><title>エラー</title></head>
            <body style="font-family: Arial, sans-serif; margin: 40px;">
                <h2 style="color: red;">❌ エラーが発生しました</h2>
                <p><strong>エラー内容:</strong> {str(e)}</p>
                <a href="/blob/list-view" style="color: blue;">再試行</a>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=500)


# EventGrid Webhookエンドポイント
@app.post("/webhook/eventgrid")
async def handle_eventgrid_webhook(request: Request):
    """Azure Event Grid Webhookを処理するエンドポイント"""
    logger.info("EventGrid webhook received")
    
    try:
        # リクエストボディを取得
        body = await request.body()
        events_data = json.loads(body.decode('utf-8'))
        
        processed_events = []
        
        # 各イベントを処理
        for event_data in events_data:
            event_type = event_data.get('eventType', '')
            
            # SubscriptionValidationイベントの処理
            if event_type == 'Microsoft.EventGrid.SubscriptionValidationEvent':
                validation_code = event_data['data']['validationCode']
                logger.info(f"Received validation event with code: {validation_code}")
                # ValidationEventの場合は即座にvalidationResponseを返す
                return {"validationResponse": validation_code}
            
            # Blobストレージイベントの処理
            elif event_type.startswith('Microsoft.Storage.Blob'):
                blob_event = {
                    "id": event_data.get('id'),
                    "eventType": event_type,
                    "subject": event_data.get('subject', ''),
                    "eventTime": event_data.get('eventTime'),
                    "data": event_data.get('data', {}),
                    "processed_at": datetime.now().isoformat()
                }
                
                # Blobの詳細情報を取得
                if 'data' in event_data and 'url' in event_data['data']:
                    blob_url = event_data['data']['url']
                    logger.info(f"Processing blob event: {event_type} for {blob_url}")
                    
                    # URLからコンテナ名とBlob名を抽出
                    try:
                        # URL例: https://account.blob.core.windows.net/container/blob.txt
                        url_parts = blob_url.split('/')
                        if len(url_parts) >= 4:
                            container_name = url_parts[-2]
                            blob_name = url_parts[-1]
                            
                            blob_event['container_name'] = container_name
                            blob_event['blob_name'] = blob_name
                            
                            # 追加のBlob情報を取得（オプション）
                            try:
                                blob_info = await get_blob_info_from_event(container_name, blob_name)
                                blob_event['blob_info'] = blob_info
                            except Exception as e:
                                logger.warning(f"Could not get blob info: {str(e)}")
                                blob_event['blob_info_error'] = str(e)
                    
                    except Exception as e:
                        logger.error(f"Error parsing blob URL: {str(e)}")
                        blob_event['url_parse_error'] = str(e)
                
                processed_events.append(blob_event)
                logger.info(f"✅ Processed event: {event_type} for container:{blob_event.get('container_name', 'unknown')}/blob:{blob_event.get('blob_name', 'unknown')}")
                
                # コンソールに分かりやすく表示
                print("\n🔥 EventGrid Event Received:")
                print(f"   Event Type: {event_type}")
                print(f"   Container: {blob_event.get('container_name', 'unknown')}")
                print(f"   Blob: {blob_event.get('blob_name', 'unknown')}")
                print(f"   Time: {blob_event.get('eventTime', 'unknown')}")
                if 'blob_info' in blob_event:
                    if blob_event['blob_info'].get('exists'):
                        print(f"   Status: File exists ({blob_event['blob_info'].get('size', 0)} bytes)")
                    else:
                        print("   Status: File deleted or not found")
                print(f"   URL: {blob_url}")
                print("="*50)
            
            else:
                logger.info(f"Received unknown event type: {event_type}")
                processed_events.append({
                    "id": event_data.get('id'),
                    "eventType": event_type,
                    "processed_at": datetime.now().isoformat(),
                    "note": "Unknown event type"
                })
        
        return EventGridResponse(
            success=True,
            processed_events=len(processed_events),
            events=processed_events,
            message=f"Successfully processed {len(processed_events)} events"
        )
        
    except Exception as e:
        logger.error(f"Error processing EventGrid webhook: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "message": "Failed to process EventGrid webhook"
            }
        )


async def get_blob_info_from_event(container_name: str, blob_name: str) -> dict:
    """EventGridイベントからBlobの詳細情報を取得"""
    try:
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if not connection_string:
            return {"error": "No connection string available"}
        
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        if blob_client.exists():
            properties = blob_client.get_blob_properties()
            return {
                "exists": True,
                "size": properties.size,
                "last_modified": properties.last_modified.isoformat() if properties.last_modified else None,
                "content_type": properties.content_settings.content_type,
                "etag": properties.etag
            }
        else:
            return {"exists": False, "note": "Blob may have been deleted"}
            
    except Exception as e:
        return {"error": f"Could not retrieve blob info: {str(e)}"}


# EventGrid イベント履歴表示用エンドポイント
@app.get("/eventgrid/events-view")
def view_eventgrid_events():
    """EventGridイベントの履歴を表示（デモ用）"""
    
    html_content = """
    <html>
        <head>
            <title>EventGrid Events Dashboard</title>
            <meta charset="UTF-8">
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 40px; 
                    background-color: #f5f5f5; 
                }
                .container { 
                    background-color: white; 
                    padding: 30px; 
                    border-radius: 8px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                    max-width: 1000px; 
                    margin: 0 auto; 
                }
                .header { 
                    border-bottom: 3px solid #007acc; 
                    padding-bottom: 20px; 
                    margin-bottom: 20px; 
                }
                .info { 
                    background-color: #e8f4fd; 
                    padding: 15px; 
                    border-radius: 5px; 
                    margin-bottom: 20px; 
                    border-left: 4px solid #007acc; 
                }
                .webhook-url {
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 5px;
                    border: 1px solid #dee2e6;
                    font-family: monospace;
                    margin: 15px 0;
                }
                .setup-steps {
                    background-color: #fff3cd;
                    padding: 15px;
                    border-radius: 5px;
                    border-left: 4px solid #ffc107;
                    margin: 15px 0;
                }
                .links { 
                    margin-top: 30px; 
                    text-align: center; 
                }
                .links a { 
                    color: #007acc; 
                    text-decoration: none; 
                    margin: 0 15px; 
                    padding: 8px 16px; 
                    border: 1px solid #007acc; 
                    border-radius: 4px; 
                    display: inline-block; 
                    transition: all 0.3s; 
                }
                .links a:hover { 
                    background-color: #007acc; 
                    color: white; 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚡ Azure EventGrid イベントダッシュボード</h1>
                    <p>Blob StorageイベントをリアルタイムでキャッチするWebhookエンドポイント</p>
                </div>
                
                <div class="info">
                    <h3>📡 Webhookエンドポイント</h3>
                    <p>Azure Event GridがこのURLにイベントを送信します：</p>
                    <div class="webhook-url">
                        <strong>POST</strong> http://localhost:8000/webhook/eventgrid
                    </div>
                    <p><em>本番環境では、httpsでアクセス可能なパブリックURLが必要です。</em></p>
                </div>

                <div class="setup-steps">
                    <h3>🔧 EventGrid設定手順</h3>
                    <ol>
                        <li>Azure PortalでEvent Grid Subscriptionを作成</li>
                        <li>Event Typeで "Blob Created", "Blob Deleted" などを選択</li>
                        <li>Endpoint Typeを "Web Hook" に設定</li>
                        <li>Subscriber Endpointに上記のWebhook URLを設定</li>
                        <li>Blob Storageでファイルをアップロード/削除してテスト</li>
                    </ol>
                </div>

                <div class="info">
                    <h3>📊 サポートするイベントタイプ</h3>
                    <ul>
                        <li><strong>Microsoft.Storage.BlobCreated</strong> - Blobが作成された時</li>
                        <li><strong>Microsoft.Storage.BlobDeleted</strong> - Blobが削除された時</li>
                        <li><strong>Microsoft.EventGrid.SubscriptionValidationEvent</strong> - サブスクリプション検証</li>
                    </ul>
                </div>

                <div class="info">
                    <h3>🧪 テスト方法</h3>
                    <p>以下のコマンドでWebhookエンドポイントをテストできます：</p>
                    <div class="webhook-url">
curl -X POST http://localhost:8000/webhook/eventgrid \\<br/>
&nbsp;&nbsp;-H "Content-Type: application/json" \\<br/>
&nbsp;&nbsp;-d '[{"eventType": "Microsoft.Storage.BlobCreated", "subject": "/blobServices/default/containers/test/blobs/test.txt", "data": {"url": "https://test.blob.core.windows.net/test/test.txt"}}]'
                    </div>
                </div>
                
                <div class="links">
                    <a href="/docs">📚 API文書</a>
                    <a href="/blob/list-view">📁 Blob一覧</a>
                    <a href="/" style="color: red;">🏠 ホーム</a>
                </div>
            </div>
        </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)


# EventGrid Setup用エンドポイント
@app.get("/eventgrid/setup-guide")
def eventgrid_setup_guide():
    """EventGrid設定の詳細ガイド"""
    
    html_content = """
    <html>
        <head>
            <title>Azure EventGrid セットアップガイド</title>
            <meta charset="UTF-8">
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 40px; 
                    background-color: #f5f5f5; 
                }
                .container { 
                    background-color: white; 
                    padding: 30px; 
                    border-radius: 8px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                    max-width: 1200px; 
                    margin: 0 auto; 
                }
                .header { 
                    border-bottom: 3px solid #007acc; 
                    padding-bottom: 20px; 
                    margin-bottom: 20px; 
                }
                .step { 
                    background-color: #e8f4fd; 
                    padding: 20px; 
                    border-radius: 5px; 
                    margin: 20px 0; 
                    border-left: 4px solid #007acc; 
                }
                .command { 
                    background-color: #f8f9fa; 
                    padding: 15px; 
                    border-radius: 5px; 
                    border: 1px solid #dee2e6; 
                    font-family: 'Courier New', monospace; 
                    margin: 10px 0; 
                    overflow-x: auto;
                }
                .warning { 
                    background-color: #fff3cd; 
                    padding: 15px; 
                    border-radius: 5px; 
                    border-left: 4px solid #ffc107; 
                    margin: 15px 0; 
                }
                .success { 
                    background-color: #d4edda; 
                    padding: 15px; 
                    border-radius: 5px; 
                    border-left: 4px solid #28a745; 
                    margin: 15px 0; 
                }
                .links { 
                    margin-top: 30px; 
                    text-align: center; 
                }
                .links a { 
                    color: #007acc; 
                    text-decoration: none; 
                    margin: 0 15px; 
                    padding: 8px 16px; 
                    border: 1px solid #007acc; 
                    border-radius: 4px; 
                    display: inline-block; 
                    transition: all 0.3s; 
                }
                .links a:hover { 
                    background-color: #007acc; 
                    color: white; 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚡ Azure EventGrid セットアップガイド</h1>
                    <p>rgharaojtdev001ストレージアカウントでEventGridを設定し、Blobコンテナーの変更をリアルタイム監視</p>
                </div>

                <div class="step">
                    <h3>🔐 手順1: Azure CLIログイン</h3>
                    <p>まず、Azure CLIにログインします：</p>
                    <div class="command">az login</div>
                    <p>ブラウザが開くので、Azureアカウントでログインしてください。</p>
                </div>

                <div class="step">
                    <h3>🏗️ 手順2: リソース情報の確認</h3>
                    <p>ストレージアカウントの詳細を確認：</p>
                    <div class="command">az storage account show --name rgharaojtdev001 --query "id" --output tsv</div>
                    <p>リソースグループを確認：</p>
                    <div class="command">az storage account show --name rgharaojtdev001 --query "resourceGroup" --output tsv</div>
                </div>

                <div class="step">
                    <h3>🌐 手順3: パブリックURL設定（開発用）</h3>
                    <p>開発環境では、ngrokを使用してローカルサーバーを公開：</p>
                    <div class="command">
# ngrokをインストール（未インストールの場合）<br/>
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null<br/>
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list<br/>
sudo apt update && sudo apt install ngrok<br/><br/>

# 新しいターミナルでngrokを起動<br/>
ngrok http 8000
                    </div>
                    <div class="warning">
                        <strong>注意:</strong> ngrokの無料版では一時的なURLが生成されます。本番環境では固定のパブリックURLを使用してください。
                    </div>
                </div>

                <div class="step">
                    <h3>📡 手順4: Event Grid Subscription作成</h3>
                    <p>Event Grid Subscriptionを作成します（リソースグループ名は手順2で確認）：</p>
                    <div class="command">
RESOURCE_GROUP="your-resource-group"  # 手順2で確認したリソースグループ名<br/>
STORAGE_ACCOUNT="rgharaojtdev001"<br/>
WEBHOOK_URL="https://your-ngrok-url.ngrok.io/webhook/eventgrid"  # ngrokのURL<br/><br/>

az eventgrid event-subscription create \\<br/>
&nbsp;&nbsp;--name blob-storage-events \\<br/>
&nbsp;&nbsp;--source-resource-id "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Storage/storageAccounts/$STORAGE_ACCOUNT" \\<br/>
&nbsp;&nbsp;--endpoint "$WEBHOOK_URL" \\<br/>
&nbsp;&nbsp;--included-event-types Microsoft.Storage.BlobCreated Microsoft.Storage.BlobDeleted \\<br/>
&nbsp;&nbsp;--subject-begins-with "/blobServices/default/containers/helloworld/"
                    </div>
                </div>

                <div class="step">
                    <h3>🧪 手順5: テストとして新しいファイルをアップロード</h3>
                    <p>Event Grid動作確認のため、Blobファイルをアップロード：</p>
                    <div class="command">
# テキストファイルを作成<br/>
echo "EventGrid Test File - $(date)" > test-eventgrid.txt<br/><br/>

# Azure Blob Storageにアップロード<br/>
az storage blob upload \\<br/>
&nbsp;&nbsp;--account-name rgharaojtdev001 \\<br/>
&nbsp;&nbsp;--container-name helloworld \\<br/>
&nbsp;&nbsp;--name "test-eventgrid.txt" \\<br/>
&nbsp;&nbsp;--file test-eventgrid.txt \\<br/>
&nbsp;&nbsp;--connection-string os.getenv("AZURE_STORAGE_CONNECTION_STRING")
                    </div>
                </div>

                <div class="success">
                    <h3>✅ 動作確認</h3>
                    <p>ファイルをアップロードすると、以下でEventGridイベントが受信されます：</p>
                    <ul>
                        <li>FastAPIコンソールログ</li>
                        <li>WebhookエンドポイントのJSONレスポンス</li>
                        <li>自動的にBlob詳細情報の取得</li>
                    </ul>
                </div>

                <div class="step">
                    <h3>🔧 手順6: Azure Portal での設定（GUI方式）</h3>
                    <p>Azure Portalでの設定も可能です：</p>
                    <ol>
                        <li>Azure Portal → Storage Accounts → rgharaojtdev001</li>
                        <li>左メニュー「Events」を選択</li>
                        <li>「+ Event Subscription」をクリック</li>
                        <li>設定項目：
                            <ul>
                                <li><strong>Name:</strong> blob-storage-events</li>
                                <li><strong>Event Types:</strong> Blob Created, Blob Deleted</li>
                                <li><strong>Endpoint Type:</strong> Web Hook</li>
                                <li><strong>Endpoint:</strong> https://your-ngrok-url.ngrok.io/webhook/eventgrid</li>
                                <li><strong>Subject Filters:</strong> Subject begins with: /blobServices/default/containers/helloworld/</li>
                            </ul>
                        </li>
                        <li>「Create」をクリック</li>
                    </ol>
                </div>

                <div class="warning">
                    <h3>🚨 本番環境での注意事項</h3>
                    <ul>
                        <li>本番環境では、HTTPSでアクセス可能な固定URLを使用</li>
                        <li>適切な認証とセキュリティ設定を実装</li>
                        <li>Event Grid Subscriptionのフィルタリング設定を適切に</li>
                        <li>コストを考慮したイベントの頻度とサイズ</li>
                    </ul>
                </div>

                <div class="links">
                    <a href="/webhook/eventgrid">🧪 Webhook テスト</a>
                    <a href="/blob/view">📄 Blob表示</a>
                    <a href="/blob/list-view">📁 ファイル一覧</a>
                    <a href="/docs">📚 API文書</a>
                    <a href="/" style="color: red;">🏠 ホーム</a>
                </div>
            </div>
        </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)


# EventGrid シミュレーター用エンドポイント
@app.post("/eventgrid/simulate")
async def simulate_eventgrid_event(
    container: str = Query("helloworld", description="Container name"),
    blob: str = Query("test-file.txt", description="Blob name"),
    event_type: str = Query("Microsoft.Storage.BlobCreated", description="Event type")
):
    """EventGridイベントをシミュレートする（開発用）"""
    logger.info(f"Simulating EventGrid event: {event_type}")
    
    # シミュレートイベントを作成
    simulated_event = {
        "id": f"sim-{int(datetime.now().timestamp())}",
        "eventType": event_type,
        "subject": f"/blobServices/default/containers/{container}/blobs/{blob}",
        "eventTime": datetime.now().isoformat() + "Z",
        "data": {
            "api": "PutBlob" if "Created" in event_type else "DeleteBlob",
            "clientRequestId": f"sim-client-{int(datetime.now().timestamp())}",
            "requestId": f"sim-request-{int(datetime.now().timestamp())}",
            "eTag": f"sim-etag-{int(datetime.now().timestamp())}",
            "contentType": "text/plain",
            "contentLength": 100,
            "blobType": "BlockBlob",
            "url": f"https://rgharaojtdev001.blob.core.windows.net/{container}/{blob}",
            "sequencer": f"sim-seq-{int(datetime.now().timestamp())}"
        },
        "dataVersion": "1.0",
        "metadataVersion": "1",
        "topic": "/subscriptions/sim-sub/resourcegroups/sim-rg/providers/Microsoft.Storage/storageAccounts/rgharaojtdev001"
    }
    
    # 作成したイベントをWebhookエンドポイントに送信
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/webhook/eventgrid",
                json=[simulated_event],
                headers={"Content-Type": "application/json"}
            )
            webhook_result = response.json()
        
        return {
            "success": True,
            "message": f"Successfully simulated {event_type} event",
            "simulated_event": simulated_event,
            "webhook_response": webhook_result
        }
    
    except Exception as e:
        logger.error(f"Error simulating event: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "simulated_event": simulated_event
        }


# EventGrid テスト用UI
@app.get("/eventgrid/test-ui")
def eventgrid_test_ui():
    """EventGrid テスト用インターフェース"""
    
    html_content = """
    <html>
        <head>
            <title>EventGrid テストツール</title>
            <meta charset="UTF-8">
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 40px; 
                    background-color: #f5f5f5; 
                }
                .container { 
                    background-color: white; 
                    padding: 30px; 
                    border-radius: 8px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                    max-width: 800px; 
                    margin: 0 auto; 
                }
                .header { 
                    border-bottom: 3px solid #007acc; 
                    padding-bottom: 20px; 
                    margin-bottom: 20px; 
                }
                .form-group { 
                    margin: 15px 0; 
                }
                .form-group label { 
                    display: block; 
                    margin-bottom: 5px; 
                    font-weight: bold; 
                }
                .form-group input, .form-group select { 
                    width: 100%; 
                    padding: 10px; 
                    border: 1px solid #ddd; 
                    border-radius: 4px; 
                    font-size: 14px; 
                }
                .btn { 
                    background-color: #007acc; 
                    color: white; 
                    padding: 12px 24px; 
                    border: none; 
                    border-radius: 4px; 
                    cursor: pointer; 
                    font-size: 16px; 
                    margin: 10px 5px; 
                }
                .btn:hover { 
                    background-color: #005a9e; 
                }
                .btn-secondary { 
                    background-color: #6c757d; 
                }
                .btn-secondary:hover { 
                    background-color: #545b62; 
                }
                .result { 
                    background-color: #f8f9fa; 
                    padding: 15px; 
                    border-radius: 4px; 
                    margin-top: 20px; 
                    border: 1px solid #dee2e6; 
                    white-space: pre-wrap; 
                    font-family: 'Courier New', monospace; 
                    font-size: 12px; 
                }
                .links { 
                    margin-top: 20px; 
                    text-align: center; 
                }
                .links a { 
                    color: #007acc; 
                    text-decoration: none; 
                    margin: 0 10px; 
                    padding: 8px 16px; 
                    border: 1px solid #007acc; 
                    border-radius: 4px; 
                    display: inline-block; 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧪 EventGrid テストツール</h1>
                    <p>ローカル環境でEventGridイベントをシミュレートしてテストします</p>
                </div>
                
                <form id="eventForm">
                    <div class="form-group">
                        <label for="container">コンテナ名:</label>
                        <input type="text" id="container" name="container" value="helloworld">
                    </div>
                    
                    <div class="form-group">
                        <label for="blob">Blob名:</label>
                        <input type="text" id="blob" name="blob" value="test-file.txt">
                    </div>
                    
                    <div class="form-group">
                        <label for="eventType">イベントタイプ:</label>
                        <select id="eventType" name="eventType">
                            <option value="Microsoft.Storage.BlobCreated">Blob Created (ファイル作成)</option>
                            <option value="Microsoft.Storage.BlobDeleted">Blob Deleted (ファイル削除)</option>
                        </select>
                    </div>
                    
                    <button type="button" class="btn" onclick="simulateEvent()">🚀 イベント送信</button>
                    <button type="button" class="btn btn-secondary" onclick="clearResult()">🗑️ クリア</button>
                </form>
                
                <div id="result" class="result" style="display: none;"></div>
                
                <div class="links">
                    <a href="/eventgrid/setup-guide">🔧 セットアップガイド</a>
                    <a href="/blob/view">📄 Blob表示</a>
                    <a href="/blob/list-view">📁 ファイル一覧</a>
                    <a href="/" style="color: red;">🏠 ホーム</a>
                </div>
            </div>
            
            <script>
                async function simulateEvent() {
                    const container = document.getElementById('container').value;
                    const blob = document.getElementById('blob').value;
                    const eventType = document.getElementById('eventType').value;
                    const resultDiv = document.getElementById('result');
                    
                    resultDiv.style.display = 'block';
                    resultDiv.textContent = '送信中...';
                    
                    try {
                        const response = await fetch(`/eventgrid/simulate?container=${encodeURIComponent(container)}&blob=${encodeURIComponent(blob)}&event_type=${encodeURIComponent(eventType)}`, {
                            method: 'POST'
                        });
                        
                        const result = await response.json();
                        resultDiv.textContent = JSON.stringify(result, null, 2);
                        
                        if (result.success) {
                            resultDiv.style.borderColor = '#28a745';
                            resultDiv.style.backgroundColor = '#d4edda';
                        } else {
                            resultDiv.style.borderColor = '#dc3545';
                            resultDiv.style.backgroundColor = '#f8d7da';
                        }
                    } catch (error) {
                        resultDiv.textContent = 'エラー: ' + error.message;
                        resultDiv.style.borderColor = '#dc3545';
                        resultDiv.style.backgroundColor = '#f8d7da';
                    }
                }
                
                function clearResult() {
                    const resultDiv = document.getElementById('result');
                    resultDiv.style.display = 'none';
                    resultDiv.style.borderColor = '#dee2e6';
                    resultDiv.style.backgroundColor = '#f8f9fa';
                }
            </script>
        </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

