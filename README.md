# Azure Functions & FastAPI 統合プロジェクト

このプロジェクトは、Azure FunctionsとFastAPIを統合した統一アプリケーションです。MySQL データベースと連携し、Azure Blob Storage、EventGrid、Assign-Kun APIを提供します。

## 🚀 主要機能

### 統合アプリケーション (`function_app.py`)
- **Azure Functions App** - EventGridトリガーとHTTPトリガー
- **FastAPI Application** - REST API、Swagger UI、管理画面
- **MySQL Database** - データ永続化とCRUD操作
- **Azure Blob Storage** - ファイル管理とストレージ
- **EventGrid** - イベント処理とリアルタイム通知

### API エンドポイント
- `/` - ホームページ（管理画面）
- `/docs` - Swagger UI
- `/health` - ヘルスチェック
- `/db-health` - データベース接続確認
- `/mysql/*` - MySQL CRUD操作
- `/blob/*` - Azure Blob Storage操作
- `/assign-kun/*` - Assign-Kun API
- `/eventgrid/*` - EventGrid操作
- `/csv/*` - CSV直接アップロード・処理
- `/csv-blob/*` - CSV Blob経由アップロード・処理

## 環境構成

### インストール済みツール
- **Python 3.11.13** - メイン開発言語
- **Azure Functions Core Tools v4** - ローカル開発とテスト用
- **Node.js LTS** - Azure Functions Core Toolsの依存関係
- **Azure CLI** - Azure リソースの管理用
- **Docker-in-Docker** - コンテナ開発用
- **MySQL 8.0** - データベース
- **SQLAlchemy** - ORM
- **aiomysql** - 非同期MySQL接続
- **VS Code 拡張機能**:
  - Azure Functions
  - Python
  - Pylance
  - Azure CLI
  - Black Formatter
  - Flake8
  - Jupyter
  - REST Client
  - YAML

### 設定済み機能
- Python仮想環境 (`.venv`)
- Azure Functions開発用のVS Codeタスク
- FastAPI開発用のVS Codeタスク
- デバッグ設定（Azure Functions & FastAPI）
- CORS設定
- ポートフォワーディング (7071, 8000, 8080)

## 使用方法

### Azure Functions

#### 1. Functions の起動
```bash
func start
```

#### 2. HTTPトリガーのテスト
```bash
curl http://localhost:7071/api/hello?name=World
```

#### 3. 新しい関数の追加
```bash
func new
```

### FastAPI

#### 1. FastAPIサーバーの起動
```bash
# 直接起動 (function_app.pyから起動)
python -m uvicorn function_app:fastapi_app --host 0.0.0.0 --port 8000 --reload

# またはVS Codeタスクから「FastAPI: Start Development Server」を実行
```

#### 2. FastAPIエンドポイントのテスト
```bash
# ヘルスチェック
curl http://localhost:8000/health

# データベースヘルスチェック
curl http://localhost:8000/db-health

# Swagger UI（ブラウザで開く）
http://localhost:8000/docs

# ホーム画面（ブラウザで開く）
http://localhost:8000/

# Assign-Kun API テスト
curl http://localhost:8000/assign-kun/assigns

# Blob Storage テスト
curl http://localhost:8000/blob/list?container=helloworld
```

#### 3. FastAPIテストの実行
```bash
pytest test_fastapi.py -v
```

#### 4. Docker Compose での起動
```bash
docker-compose up fastapi
```

### デバッグの開始
VS Codeで `F5` キーを押すか、「実行とデバッグ」パネルから以下を選択：
- **Azure Functions**: 「Attach to Python Functions」
- **FastAPI**: 「FastAPI: Debug」または「FastAPI: Run App」

## 利用可能なエンドポイント

### Azure Functions
- **http_trigger**: `http://localhost:7071/api/hello`
- **EventGridTrigger**: Event Gridイベント処理

### FastAPI（統合アプリケーション）
- **ホーム**: `http://localhost:8000/` - 管理画面
- **ヘルスチェック**: `http://localhost:8000/health`
- **データベースヘルスチェック**: `http://localhost:8000/db-health`

#### Assign-Kun API
- `GET /assign-kun/assigns` - アサインデータ一覧
- `GET /assign-kun/histograms` - ヒストグラムデータ一覧
- `GET /assign-kun/projects` - プロジェクトデータ一覧
- `GET /assign-kun/users` - ユーザーデータ一覧

#### Blob Storage API
- `GET /blob/list` - Blob一覧取得
- `POST /blob/upload` - ファイルアップロード
- `DELETE /blob/delete` - ファイル削除
- `GET /blob/view` - ファイル内容表示
- `GET /blob/list-view` - ファイル一覧（Web画面）

#### CSV処理API
- `POST /csv/histograms/upload` - ヒストグラムCSV直接アップロード
- `POST /csv/projects/upload` - プロジェクトCSV直接アップロード
- `POST /csv/users/upload` - ユーザーCSV直接アップロード
- `POST /csv/assigns/upload` - アサインCSV直接アップロード
- `POST /csv-blob/histograms/upload` - ヒストグラムCSV Blobアップロード
- `POST /csv-blob/projects/upload` - プロジェクトCSV Blobアップロード
- `POST /csv-blob/users/upload` - ユーザーCSV Blobアップロード
- `POST /csv-blob/assigns/upload` - アサインCSV Blobアップロード

#### EventGrid API
- `POST /eventgrid/events` - EventGridイベント受信（Webhook）
- `GET /eventgrid/events` - イベント履歴取得
- `DELETE /eventgrid/events` - イベント履歴クリア
- `GET /eventgrid/events-view` - イベント履歴表示（Web画面）
- `GET /eventgrid/setup-guide` - EventGrid設定ガイド（Web画面）
- `GET /eventgrid/test-ui` - EventGridテスト用UI（Web画面）

#### MySQL API
- `GET /mysql/users` - MySQL ユーザー一覧
- `POST /mysql/users` - MySQL ユーザー作成
- `GET /mysql/users/{id}` - MySQL 特定ユーザー取得
- `PUT /mysql/users/{id}` - MySQL ユーザー更新
- `DELETE /mysql/users/{id}` - MySQL ユーザー削除

#### ドキュメント
- `http://localhost:8000/docs` - Swagger UI
- `http://localhost:8000/redoc` - ReDoc

## 開発のベストプラクティス

1. **依存関係の管理**: `requirements.txt` を使用してPythonパッケージを管理
2. **環境変数**: 
   - Azure Functions: `local.settings.json`
   - データベース設定: 環境変数またはlocal.settings.json
   - Azure Storage: 環境変数でAZURE_STORAGE_CONNECTION_STRING設定
3. **ログ**: `logging` モジュールを使用して適切なログを出力
4. **テスト**: 
   - Azure Functions: Azure Functions Core Toolsでテスト
   - FastAPI: pytest + TestClient でユニットテスト
   - API テスト: `tests.http` ファイルでREST Clientを使用
5. **コード品質**: Black（フォーマッター）+ Flake8（リンター）
6. **データベース**: 
   - Alembicでマイグレーション管理
   - SQLAlchemy 2.0の非同期セッション使用
7. **CSV処理**: 
   - 直接処理（`/csv/*`）: 小さなファイル、即座処理が必要な場合
   - Blob経由処理（`/csv-blob/*`）: 大きなファイル、非同期処理が可能な場合

## プロジェクト構造

```
.
├── .devcontainer/          # Dev Container設定
├── .vscode/               # VS Code設定
├── function_app.py        # Azure Functions + FastAPI 統合アプリ
├── fastapi_app.py         # FastAPI 単体アプリ（レガシー）
├── database.py            # データベース接続管理
├── db_models.py           # SQLAlchemy データベースモデル
├── db_crud.py             # データベースCRUD操作
├── models.py              # Pydantic モデル定義
├── assignkun_endpoints.py # Assign-Kun API エンドポイント
├── blob_endpoints.py      # Blob Storage API エンドポイント
├── blob_views.py          # Blob Storage Web UI
├── eventgrid_endpoints.py # EventGrid API エンドポイント
├── csv_endpoints.py       # CSV直接処理エンドポイント
├── csv_blob_endpoints.py  # CSV Blob経由処理エンドポイント
├── csv_processor.py       # CSV EventGrid処理ハンドラー
├── mysql_endpoints.py     # MySQL CRUD エンドポイント
├── test_fastapi.py        # FastAPIテスト
├── test_mysql.py          # MySQLテスト
├── tests.http             # HTTPリクエストテスト
├── requirements.txt       # Python依存関係
├── local.settings.json    # Azure Functions設定
├── host.json             # Azure Functions ホスト設定
├── setup.cfg             # Python設定
├── alembic.ini           # Alembic設定
├── alembic/              # データベースマイグレーション
├── mysql-init/           # MySQL初期化SQL
├── sample_*.csv          # サンプルCSVファイル
├── Dockerfile.fastapi    # FastAPI用Dockerfile
├── docker-compose.yml    # Docker Compose設定
└── README.md             # このファイル
```

## 📂 実装されているコード全体の使い方ガイド

### 🏗️ コアファイルの役割

#### 1. `function_app.py` - メインアプリケーション
**統合エントリーポイント**: Azure Functions + FastAPI の統合アプリケーション

**主要機能**:
- Azure Functions（HTTPトリガー、EventGridトリガー）
- FastAPIアプリケーションの統合
- データベース初期化とヘルスチェック
- 全APIエンドポイントの統合

**起動方法**:
```bash
# FastAPI として起動（推奨）
python -m uvicorn function_app:fastapi_app --host 0.0.0.0 --port 8000 --reload

# Azure Functions として起動
func start
```

#### 2. `database.py` - データベース接続管理
**SQLAlchemy 2.0による非同期MySQL接続管理**

**使用方法**:
```python
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

async def my_function(db: AsyncSession = Depends(get_db)):
    # データベース操作
    pass
```

#### 3. `db_models.py` - データベースモデル定義
**定義されているテーブル**:
- `User` - ユーザー情報
- `Project` - プロジェクト情報
- `AssignData` - アサインデータ
- `HistogramData` - ヒストグラムデータ
- `BlobLog` - Blob操作ログ

#### 4. `models.py` - Pydanticモデル定義
**API用データ検証・シリアライゼーション**:
- `BlobResponse` - Blob操作レスポンス
- `CSVUploadResponse` - CSVアップロードレスポンス
- `HistogramResponse` - ヒストグラムデータレスポンス
- `EventGridEvent` - EventGridイベント

### 🎯 API エンドポイント詳細

#### 5. `assignkun_endpoints.py` - Assign-Kun API
**アサインデータ管理API**

**主要エンドポイント**:
```bash
# アサインデータ取得
GET /assign-kun/assigns
curl "http://localhost:8000/assign-kun/assigns"

# 月別データ取得
GET /assign-kun/assigns?month=7
curl "http://localhost:8000/assign-kun/assigns?month=7"

# ヒストグラムデータ取得
GET /assign-kun/histograms
curl "http://localhost:8000/assign-kun/histograms"

# プロジェクトデータ取得
GET /assign-kun/projects
curl "http://localhost:8000/assign-kun/projects"

# ユーザーデータ取得
GET /assign-kun/users
curl "http://localhost:8000/assign-kun/users"
```

#### 6. `blob_endpoints.py` - Blob Storage API
**Azure Blob Storage操作API**

**主要エンドポイント**:
```bash
# ファイル一覧取得
GET /blob/list?container=helloworld
curl "http://localhost:8000/blob/list?container=helloworld"

# ファイルアップロード
POST /blob/upload
curl -X POST "http://localhost:8000/blob/upload" \
  -F "file=@test.txt" \
  -F "container=helloworld"

# ファイル削除
DELETE /blob/delete?container=helloworld&blob=test.txt
curl -X DELETE "http://localhost:8000/blob/delete?container=helloworld&blob=test.txt"

# ファイル内容表示
GET /blob/view?container=helloworld&blob=test.txt
curl "http://localhost:8000/blob/view?container=helloworld&blob=test.txt"
```

#### 7. `blob_views.py` - Blob Storage Web UI
**ブラウザ用管理画面**:
- `GET /blob/list-view` - ファイル一覧（Web画面）
- `GET /blob/view` - ファイル表示（Web画面）

**アクセス方法**:
```
http://localhost:8000/blob/list-view?container=helloworld
```

#### 8. `eventgrid_endpoints.py` - EventGrid処理
**Azure EventGrid Webhook処理**

**主要エンドポイント**:
```bash
# EventGridイベント受信（Webhook）
POST /eventgrid/events
curl -X POST "http://localhost:8000/eventgrid/events" \
  -H "Content-Type: application/json" \
  -d '[{"eventType": "Microsoft.Storage.BlobCreated", "data": {...}}]'

# イベント履歴取得
GET /eventgrid/events
curl "http://localhost:8000/eventgrid/events"

# イベント履歴クリア
DELETE /eventgrid/events
curl -X DELETE "http://localhost:8000/eventgrid/events"
```

**Web UI**:
- `GET /eventgrid/events-view` - イベント履歴表示
- `GET /eventgrid/setup-guide` - 設定ガイド
- `GET /eventgrid/test-ui` - テスト用UI

### 📂 CSV処理システム

#### 9. `csv_endpoints.py` - 直接CSV処理
**CSVファイルの即座アップロードと処理**

**主要エンドポイント**:
```bash
# ヒストグラムCSVアップロード
POST /csv/histograms/upload
curl -X POST "http://localhost:8000/csv/histograms/upload" \
  -F "file=@sample_histogram.csv"

# プロジェクトCSVアップロード
POST /csv/projects/upload
curl -X POST "http://localhost:8000/csv/projects/upload" \
  -F "file=@sample_projects.csv"

# ユーザーCSVアップロード
POST /csv/users/upload
curl -X POST "http://localhost:8000/csv/users/upload" \
  -F "file=@sample_users.csv"

# アサインCSVアップロード
POST /csv/assigns/upload
curl -X POST "http://localhost:8000/csv/assigns/upload" \
  -F "file=@sample_assigns.csv"
```

#### 10. `csv_blob_endpoints.py` - Blob経由CSV処理
**CSVファイルをBlobに保存してEventGrid経由で非同期処理**

**主要エンドポイント**:
```bash
# ヒストグラムCSV Blobアップロード
POST /csv-blob/histograms/upload
curl -X POST "http://localhost:8000/csv-blob/histograms/upload" \
  -F "file=@sample_histogram.csv"

# プロジェクトCSV Blobアップロード
POST /csv-blob/projects/upload
curl -X POST "http://localhost:8000/csv-blob/projects/upload" \
  -F "file=@sample_projects.csv"

# ユーザーCSV Blobアップロード
POST /csv-blob/users/upload
curl -X POST "http://localhost:8000/csv-blob/users/upload" \
  -F "file=@sample_users.csv"

# アサインCSV Blobアップロード
POST /csv-blob/assigns/upload
curl -X POST "http://localhost:8000/csv-blob/assigns/upload" \
  -F "file=@sample_assigns.csv"
```

#### 11. `csv_processor.py` - CSV EventGrid処理
**EventGridからのCSV処理要求を受信して実際の処理を実行**

**主な機能**:
- BlobからCSVダウンロード
- CSVデータ解析・検証
- データベース保存
- エラーハンドリング

### 🔧 開発・テスト・運用

#### 12. `test_fastapi.py` - FastAPIテスト
**APIエンドポイントの単体テスト**

**実行方法**:
```bash
# 全テスト実行
pytest test_fastapi.py -v

# 特定テスト実行
pytest test_fastapi.py::test_health_check -v

# カバレッジ付きテスト
pytest --cov=. test_fastapi.py
```

#### 13. `tests.http` - HTTPリクエストテスト
**VS Code REST Client用テストファイル**

**使用方法**:
1. VS Codeで `tests.http` を開く
2. 各リクエストの上にある「Send Request」をクリック
3. レスポンスを確認

#### 14. `alembic/` - データベースマイグレーション
**データベーススキーマのバージョン管理**

**使用方法**:
```bash
# マイグレーション生成
alembic revision --autogenerate -m "マイグレーション名"

# マイグレーション実行
alembic upgrade head

# マイグレーション履歴確認
alembic history
```

### 🚀 典型的な使用フロー

#### CSV処理フロー（直接）
1. CSVファイルを準備
2. `/csv/{type}/upload` エンドポイントにPOST
3. 即座にデータベースに保存
4. `/assign-kun/{type}` でデータ確認

#### CSV処理フロー（Blob経由）
1. CSVファイルを準備
2. `/csv-blob/{type}/upload` エンドポイントにPOST
3. BlobストレージにCSVファイル保存
4. EventGridイベント発行
5. バックグラウンドでCSV処理
6. `/assign-kun/{type}` でデータ確認

#### EventGrid連携フロー
1. Azure Blob Storageにファイルアップロード
2. EventGridがイベント発行
3. `/eventgrid/events` でWebhook受信
4. 自動処理実行

#### API利用フロー
1. http://localhost:8000/docs でSwagger UI確認
2. HTTPクライアントでリクエスト送信
3. レスポンスデータを確認

### 🌐 Web画面アクセス

**管理画面**:
- **ホーム画面**: http://localhost:8000/
- **API文書**: http://localhost:8000/docs
- **Blob管理**: http://localhost:8000/blob/list-view
- **EventGrid履歴**: http://localhost:8000/eventgrid/events-view
- **EventGrid設定**: http://localhost:8000/eventgrid/setup-guide
- **EventGridテスト**: http://localhost:8000/eventgrid/test-ui

### 📋 環境変数設定

**必要な環境変数** (`local.settings.json`):
```json
{
  "IsEncrypted": false,
  "Values": {
    "AZURE_STORAGE_CONNECTION_STRING": "DefaultEndpointsProtocol=https;AccountName=...",
    "DB_HOST": "localhost",
    "DB_PORT": "3306",
    "DB_NAME": "assignkun_db",
    "DB_USER": "assignkun",
    "DB_PASSWORD": "assign",
    "CSV_CONTAINER_NAME": "csv-uploads",
    "EVENTGRID_TOPIC_ENDPOINT": "https://...",
    "EVENTGRID_ACCESS_KEY": "..."
  }
}
```

### 🔄 データベース初期化

**初回セットアップ**:
```bash
# データベース初期化
python init_database.py

# マイグレーション実行
alembic upgrade head

# サンプルデータ投入（オプション）
# CSVファイルからサンプルデータをアップロード
```

## トラブルシューティング

### ポートが使用中の場合
```bash
# Azure Functions (7071)
pkill -f func

# FastAPI (8000)
pkill -f uvicorn
```

### 依存関係の再インストール
```bash
pip install -r requirements.txt
```

### データベース接続エラー
```bash
# データベースヘルスチェック
curl http://localhost:8000/db-health

# MySQL接続確認
python -c "from database import test_connection; import asyncio; print(asyncio.run(test_connection()))"

# データベース初期化
python init_database.py
```

### Azure Storage接続エラー
```bash
# 環境変数確認
echo $AZURE_STORAGE_CONNECTION_STRING

# または local.settings.json の設定確認
cat local.settings.json
```

### CSV処理エラー
```bash
# CSVサンプルファイル確認
ls sample_*.csv

# CSV処理ログ確認（サーバーコンソール）
# FastAPIサーバーの起動コンソールでログを確認
```

### EventGrid連携エラー
```bash
# EventGrid履歴確認
curl http://localhost:8000/eventgrid/events

# EventGridテスト
curl -X POST "http://localhost:8000/eventgrid/events" \
  -H "Content-Type: application/json" \
  -d '[{"eventType": "Microsoft.Storage.BlobCreated", "data": {}}]'
```

### Docker関連の問題
```bash
docker-compose down
docker-compose up --build
```

## デプロイ

### Azure Functions
```bash
# Azure CLIでデプロイ
func azure functionapp publish <app-name>

# 設定値をAzureに反映
func azure functionapp config appsettings set --name <app-name> --setting "AZURE_STORAGE_CONNECTION_STRING=..."
```

### FastAPI (Azure Container Instances)
```bash
# Dockerイメージのビルド
docker build -f Dockerfile.fastapi -t fastapi-app .

# Azure Container Registryにプッシュ
az acr build --registry <registry-name> --image fastapi-app .

# Azure Container Instancesにデプロイ
az container create --resource-group <rg-name> --name fastapi-app --image <registry>.azurecr.io/fastapi-app:latest
```

### FastAPI (Azure App Service)
```bash
# Azure App Serviceにデプロイ
az webapp up --name <app-name> --resource-group <rg-name> --runtime PYTHON:3.11

# 設定値をAzureに反映
az webapp config appsettings set --name <app-name> --resource-group <rg-name> --settings \
  AZURE_STORAGE_CONNECTION_STRING="..." \
  DB_HOST="..." \
  DB_NAME="..." \
  DB_USER="..." \
  DB_PASSWORD="..."
```

### データベース（Azure Database for MySQL）
```bash
# Azure Database for MySQLの作成
az mysql flexible-server create --name <server-name> --resource-group <rg-name> --admin-user <admin-user> --admin-password <admin-password>

# ファイアウォール設定
az mysql flexible-server firewall-rule create --name <server-name> --resource-group <rg-name> --rule-name AllowAzureServices --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0

# データベース作成
az mysql flexible-server db create --server-name <server-name> --resource-group <rg-name> --database-name assignkun_db
```