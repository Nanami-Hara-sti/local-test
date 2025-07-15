from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import logging
import os

# 環境変数の読み込み
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenvがない場合はスキップ
    pass

# 分割したエンドポイントをインポート
import blob_endpoints
import blob_views
import assignkun_endpoints
import eventgrid_endpoints

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPIアプリケーション
app = FastAPI(
    title="Azure Blob Storage & Assign-Kun API", 
    version="2.0.0",
    description="Azure Blob Storage連携、EventGrid、Assign-Kun API統合アプリケーション"
)

# ルーターの登録
app.include_router(blob_endpoints.router, prefix="/blob", tags=["Blob Storage"])
app.include_router(blob_views.router, prefix="/blob", tags=["Blob Views"])
app.include_router(assignkun_endpoints.router, prefix="/assign-kun", tags=["Assign-Kun API"])
app.include_router(eventgrid_endpoints.router, prefix="/eventgrid", tags=["EventGrid"])

# 古いWebhookエンドポイントとの互換性のため
app.include_router(eventgrid_endpoints.router, prefix="/webhook", tags=["EventGrid Legacy"])


@app.get("/health")
def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy", "service": "Azure Blob Storage & Assign-Kun API"}


@app.get("/")
def read_root():
    """ホームページ"""
    return HTMLResponse(
        content="""
    <html>
        <head>
            <title>Azure Blob Storage & Assign-Kun API</title>
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
                .section-title {
                    color: #007acc;
                    font-size: 18px;
                    font-weight: bold;
                    margin: 20px 0 10px 0;
                    border-bottom: 2px solid #007acc;
                    padding-bottom: 5px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 Azure統合プラットフォーム</h1>
                    <p>Azure Blob Storage、EventGrid、Assign-Kun API</p>
                </div>
                
                <div class="links">
                    <div class="section-title">📊 Assign-Kun API</div>
                    
                    <a href="/assign-kun/histograms" class="link-button">
                        📊 ヒストグラムデータ
                        <div class="description">リソースヒストグラム表示・管理</div>
                    </a>
                    
                    <a href="/assign-kun/projects" class="link-button">
                        📋 プロジェクトデータ
                        <div class="description">プロジェクト情報表示・管理</div>
                    </a>
                    
                    <a href="/assign-kun/users" class="link-button">
                        👥 ユーザーデータ
                        <div class="description">メンバー情報表示・管理</div>
                    </a>
                    
                    <div class="section-title">💾 Azure Blob Storage</div>
                    
                    <a href="/blob/view" class="link-button">
                        📄 Blobテキスト表示
                        <div class="description">ファイルの内容を見やすく表示</div>
                    </a>
                    
                    <a href="/blob/list-view" class="link-button">
                        📁 ファイル一覧表示
                        <div class="description">コンテナ内のファイル一覧を表示</div>
                    </a>
                    
                    <div class="section-title">⚡ EventGrid</div>
                    
                    <a href="/eventgrid/events-view" class="link-button">
                        ⚡ EventGrid ダッシュボード
                        <div class="description">リアルタイムイベント監視</div>
                    </a>
                    
                    <a href="/eventgrid/test-ui" class="link-button">
                        🧪 EventGrid テストツール
                        <div class="description">ローカル環境でEventGridをテスト</div>
                    </a>
                    
                    <a href="/eventgrid/setup-guide" class="link-button">
                        🔧 EventGrid セットアップ
                        <div class="description">Azure Event Grid設定ガイド</div>
                    </a>
                    
                    <div class="section-title">📚 開発者向け</div>
                    
                    <a href="/docs" class="link-button">
                        📚 API文書 (Swagger UI)
                        <div class="description">インタラクティブなAPI文書</div>
                    </a>
                    
                    <a href="/redoc" class="link-button">
                        📖 API文書 (ReDoc)
                        <div class="description">きれいなAPI文書</div>
                    </a>
                </div>
                
                <div style="text-align: center; margin-top: 30px; color: #666;">
                    <small>FastAPI + Azure Blob Storage + EventGrid + Assign-Kun API v2.0</small>
                </div>
            </div>
        </body>
    </html>
    """
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
