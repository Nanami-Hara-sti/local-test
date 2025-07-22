"""
統合アプリケーション: Azure Functions + FastAPI + MySQL

このファイルは以下の機能を統合します：
- Azure Functions (HTTPトリガー、EventGridトリガー)
- FastAPI アプリケーション
- MySQL データベース統合
- Azure Blob Storage
- EventGrid
- Assign-Kun API
"""

import logging
import azure.functions as func
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager

# データベース接続をインポート
from database import db_manager, test_connection, init_database

# 分割したエンドポイントをインポート
import blob_endpoints
import blob_views
import assignkun_endpoints
import eventgrid_endpoints
import csv_endpoints
import csv_blob_endpoints

# MySQLエンドポイントは条件付きインポート
try:
    import mysql_endpoints

    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

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

if not MYSQL_AVAILABLE:
    logger.warning("MySQL関連のモジュールが利用できません")


# ==============================================================================
# FastAPI アプリケーション設定
# ==============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションの起動・終了時の処理"""
    # 起動時
    logger.info("🚀 アプリケーション起動中...")

    # データベース接続テスト
    if await test_connection():
        logger.info("✅ データベース接続確認完了")
    else:
        logger.warning("⚠️  データベース接続に失敗しました")

    # データベース接続プールを作成
    try:
        db_manager.initialize()  # create_pool() ではなく initialize() を使用
        await init_database()
        logger.info("✅ データベース初期化完了")
    except Exception as e:
        logger.error(f"❌ データベース初期化エラー: {e}")

    yield

    # 終了時
    logger.info("🔄 アプリケーション終了中...")
    await db_manager.close()  # close_pool() ではなく close() を使用
    logger.info("✅ データベース接続を閉じました")


# FastAPIアプリケーション
fastapi_app = FastAPI(
    title="Azure統合プラットフォーム",
    version="2.0.0",
    description="Azure Functions + FastAPI + MySQL + Blob Storage + EventGrid + Assign-Kun API",
    lifespan=lifespan,
)

# ==============================================================================
# ルーター登録
# ==============================================================================

# APIエンドポイント
fastapi_app.include_router(
    assignkun_endpoints.router, prefix="/assign-kun", tags=["📊 Assign-Kun API"]
)
fastapi_app.include_router(
    blob_endpoints.router, prefix="/blob", tags=["� Blob Storage"]
)
fastapi_app.include_router(blob_views.router, prefix="/blob", tags=["� Blob Views"])
fastapi_app.include_router(
    eventgrid_endpoints.router, prefix="/eventgrid", tags=["⚡ EventGrid"]
)
fastapi_app.include_router(csv_endpoints.router, prefix="/csv", tags=["📂 CSV Upload"])
fastapi_app.include_router(
    csv_blob_endpoints.router, prefix="/csv-blob", tags=["📂 CSV Blob Storage"]
)

# MySQLエンドポイントは条件付きで登録
if MYSQL_AVAILABLE:
    fastapi_app.include_router(
        mysql_endpoints.router, prefix="/mysql", tags=["🗄️ MySQL Database"]
    )
    logger.info("MySQL エンドポイントが登録されました")
else:
    logger.warning("MySQL エンドポイントはスキップされました")

# 古いWebhookエンドポイントとの互換性のため
fastapi_app.include_router(
    eventgrid_endpoints.router, prefix="/webhook", tags=["⚡ EventGrid Legacy"]
)


# ==============================================================================
# ヘルスチェックエンドポイント
# ==============================================================================


@fastapi_app.get("/health")
def health_check():
    """システムヘルスチェック"""
    return {
        "status": "healthy",
        "service": "Azure統合プラットフォーム",
        "database": "MySQL",
        "version": "2.0.0",
    }


@fastapi_app.get("/db-health")
async def db_health_check():
    """データベース接続ヘルスチェック"""
    try:
        if await test_connection():
            return {
                "status": "healthy",
                "database": "MySQL",
                "connection": "OK",
                "timestamp": "2025-07-16",
            }
        else:
            return {"status": "unhealthy", "database": "MySQL", "connection": "Failed"}
    except Exception as e:
        return {"status": "error", "database": "MySQL", "error": str(e)}


# ==============================================================================
# ホームページ
# ==============================================================================


@fastapi_app.get("/")
def read_root():
    """統合プラットフォーム管理画面"""
    return HTMLResponse(content=get_homepage_html())


def get_homepage_html():
    """ホームページのHTMLコンテンツを生成"""
    return """
    <!DOCTYPE html>
    <html lang="ja">
        <head>
            <title>Azure統合プラットフォーム</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }
                
                .container { 
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    max-width: 800px;
                    margin: 0 auto;
                    overflow: hidden;
                }
                
                .header { 
                    background: linear-gradient(135deg, #007acc 0%, #0056b3 100%);
                    color: white;
                    padding: 40px 30px;
                    text-align: center;
                }
                
                .header h1 {
                    font-size: 2.5em;
                    margin-bottom: 10px;
                    font-weight: 300;
                }
                
                .header p {
                    font-size: 1.1em;
                    opacity: 0.9;
                }
                
                .content {
                    padding: 40px 30px;
                }
                
                .section {
                    margin-bottom: 40px;
                }
                
                .section-title {
                    color: #333;
                    font-size: 1.4em;
                    font-weight: 600;
                    margin-bottom: 20px;
                    padding-bottom: 10px;
                    border-bottom: 3px solid #007acc;
                    display: flex;
                    align-items: center;
                }
                
                .section-title::before {
                    content: '';
                    display: inline-block;
                    width: 4px;
                    height: 20px;
                    background: #007acc;
                    margin-right: 10px;
                }
                
                .links {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 15px;
                }
                
                .link-button {
                    display: block;
                    color: #333;
                    text-decoration: none;
                    padding: 20px;
                    border: 2px solid #e0e0e0;
                    border-radius: 10px;
                    transition: all 0.3s ease;
                    background: #f8f9fa;
                    position: relative;
                    overflow: hidden;
                }
                
                .link-button::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: -100%;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
                    transition: left 0.5s;
                }
                
                .link-button:hover::before {
                    left: 100%;
                }
                
                .link-button:hover {
                    border-color: #007acc;
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(0,122,204,0.15);
                    background: #fff;
                }
                
                .link-button h3 {
                    font-size: 1.1em;
                    margin-bottom: 8px;
                    color: #007acc;
                }
                
                .link-button p {
                    color: #666;
                    font-size: 0.9em;
                    line-height: 1.4;
                }
                
                .footer {
                    background: #f8f9fa;
                    padding: 30px;
                    text-align: center;
                    border-top: 1px solid #e0e0e0;
                }
                
                .footer p {
                    color: #666;
                    font-size: 0.9em;
                }
                
                .status-badge {
                    display: inline-block;
                    background: #28a745;
                    color: white;
                    padding: 4px 8px;
                    border-radius: 12px;
                    font-size: 0.8em;
                    margin-left: 10px;
                }
                
                @media (max-width: 768px) {
                    .header h1 {
                        font-size: 2em;
                    }
                    .content {
                        padding: 30px 20px;
                    }
                    .links {
                        grid-template-columns: 1fr;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 Azure統合プラットフォーム</h1>
                    <p>Azure Functions + FastAPI + MySQL + Blob Storage + EventGrid</p>
                    <span class="status-badge">ONLINE</span>
                </div>
                
                <div class="content">
                    <div class="section">
                        <h2 class="section-title">📊 Assign-Kun API</h2>
                        <div class="links">
                            <a href="/assign-kun/assigns" class="link-button">
                                <h3>📊 アサインデータ</h3>
                                <p>ホーム画面アサインデータ取得・管理</p>
                            </a>
                            <a href="/assign-kun/histograms" class="link-button">
                                <h3>� ヒストグラムデータ</h3>
                                <p>リソースヒストグラム表示・分析</p>
                            </a>
                            <a href="/assign-kun/projects" class="link-button">
                                <h3>📋 プロジェクト管理</h3>
                                <p>プロジェクト情報表示・管理</p>
                            </a>
                            <a href="/assign-kun/users" class="link-button">
                                <h3>👥 ユーザー管理</h3>
                                <p>メンバー情報表示・管理</p>
                            </a>
                            <a href="/assign-kun/notices" class="link-button">
                                <h3>🔔 通知管理</h3>
                                <p>通知一覧表示・管理</p>
                            </a>
                            <a href="/assign-kun/informations" class="link-button">
                                <h3>📊 情報ダッシュボード</h3>
                                <p>総計情報表示・分析</p>
                            </a>
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2 class="section-title">🗄️ MySQL Database</h2>
                        <div class="links">
                            <a href="/mysql/users" class="link-button">
                                <h3>👥 ユーザー管理</h3>
                                <p>ユーザー情報のCRUD操作</p>
                            </a>
                            <a href="/mysql/projects" class="link-button">
                                <h3>📋 プロジェクト管理</h3>
                                <p>プロジェクト情報のCRUD操作</p>
                            </a>
                            <a href="/mysql/assignments" class="link-button">
                                <h3>📊 アサインメント管理</h3>
                                <p>アサインメント情報のCRUD操作</p>
                            </a>
                            <a href="/mysql/notices" class="link-button">
                                <h3>🔔 通知管理</h3>
                                <p>通知情報のCRUD操作</p>
                            </a>
                            <a href="/mysql/histograms" class="link-button">
                                <h3>� ヒストグラム管理</h3>
                                <p>ヒストグラムデータのCRUD操作</p>
                            </a>
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2 class="section-title">💾 Azure Blob Storage</h2>
                        <div class="links">
                            <a href="/blob/view" class="link-button">
                                <h3>📄 Blobテキスト表示</h3>
                                <p>ファイル内容の表示・確認</p>
                            </a>
                            <a href="/blob/list-view" class="link-button">
                                <h3>📁 ファイル一覧</h3>
                                <p>コンテナ内のファイル一覧表示</p>
                            </a>
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2 class="section-title">⚡ EventGrid</h2>
                        <div class="links">
                            <a href="/eventgrid/events-view" class="link-button">
                                <h3>⚡ EventGrid ダッシュボード</h3>
                                <p>リアルタイムイベント監視</p>
                            </a>
                            <a href="/eventgrid/test-ui" class="link-button">
                                <h3>🧪 EventGrid テストツール</h3>
                                <p>ローカル環境でのEventGridテスト</p>
                            </a>
                            <a href="/eventgrid/setup-guide" class="link-button">
                                <h3>🔧 EventGrid セットアップ</h3>
                                <p>Azure Event Grid設定ガイド</p>
                            </a>
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2 class="section-title">📚 開発者向けツール</h2>
                        <div class="links">
                            <a href="/docs" class="link-button">
                                <h3>📚 API文書 (Swagger UI)</h3>
                                <p>インタラクティブなAPI文書</p>
                            </a>
                            <a href="/redoc" class="link-button">
                                <h3>📖 API文書 (ReDoc)</h3>
                                <p>きれいなAPI文書</p>
                            </a>
                            <a href="/health" class="link-button">
                                <h3>🔍 システムヘルスチェック</h3>
                                <p>システム状態確認</p>
                            </a>
                            <a href="/db-health" class="link-button">
                                <h3>🔍 データベースヘルスチェック</h3>
                                <p>MySQL接続状態確認</p>
                            </a>
                        </div>
                    </div>
                </div>
                
                <div class="footer">
                    <p><strong>Azure統合プラットフォーム v2.0</strong></p>
                    <p>FastAPI + Azure Functions + MySQL + Blob Storage + EventGrid</p>
                </div>
            </div>
        </body>
    </html>
    """


# ==============================================================================
# Azure Functions
# ==============================================================================

# Azure Functions App
app = func.FunctionApp()


@app.route(route="hello")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Functions HTTPトリガー"""
    logging.info("🔄 Azure Functions HTTP trigger が呼び出されました")

    name = req.params.get("name")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get("name")

    if name:
        return func.HttpResponse(
            f"こんにちは、{name}さん！Azure Functions HTTP トリガーが正常に実行されました。"
        )
    else:
        return func.HttpResponse(
            "Azure Functions HTTP トリガーが正常に実行されました。"
            "パーソナライズされたレスポンスを取得するには、"
            "クエリ文字列またはリクエスト本文で名前を渡してください。",
            status_code=200,
        )


@app.event_grid_trigger(arg_name="azeventgrid")
def EventGridTrigger(azeventgrid: func.EventGridEvent):
    """Azure Functions EventGridトリガー"""
    logging.info("⚡ Azure Functions EventGrid trigger が呼び出されました")

    # EventGridイベントをログに記録
    logging.info(f"📋 Event Type: {azeventgrid.event_type}")
    logging.info(f"📋 Event Subject: {azeventgrid.subject}")
    logging.info(f"📋 Event Data: {azeventgrid.get_json()}")

    # 必要に応じて、MySQLデータベースにイベントログを記録
    # 例: イベントをデータベースに保存
    try:
        # 非同期処理の場合は適切に処理する必要があります
        # 実際の実装では、バックグラウンドタスクやメッセージキューを使用
        logging.info("✅ EventGrid イベントの処理が完了しました")
    except Exception as e:
        logging.error(f"❌ EventGrid処理エラー: {e}")


# ==============================================================================
# アプリケーションエイリアス
# ==============================================================================

# FastAPIアプリケーション用のエイリアス（既存のコードとの互換性のため）
app_fastapi = fastapi_app
