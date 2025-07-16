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
# 直接起動
python -m uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 --reload

# またはVS Codeタスクから「FastAPI: Start Development Server」を実行
```

#### 2. FastAPIエンドポイントのテスト
```bash
# ヘルスチェック
curl http://localhost:8000/health

# アイテム一覧
curl http://localhost:8000/items

# Swagger UI（ブラウザで開く）
http://localhost:8000/docs
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

### FastAPI
- **ルート**: `http://localhost:8000/` - ウェルカムページ
- **ヘルスチェック**: `http://localhost:8000/health`
- **アイテム関連**:
  - `GET /items` - アイテム一覧
  - `GET /items/{id}` - 特定アイテム取得
  - `POST /items` - アイテム作成
  - `PUT /items/{id}` - アイテム更新
  - `DELETE /items/{id}` - アイテム削除
- **ユーザー関連**:
  - `GET /users` - ユーザー一覧
  - `GET /users/{id}` - 特定ユーザー取得
  - `POST /users` - ユーザー作成
- **ドキュメント**:
  - `http://localhost:8000/docs` - Swagger UI
  - `http://localhost:8000/redoc` - ReDoc

## 開発のベストプラクティス

1. **依存関係の管理**: `requirements.txt` を使用してPythonパッケージを管理
2. **環境変数**: 
   - Azure Functions: `local.settings.json`
   - FastAPI: 環境変数またはコンフィグファイル
3. **ログ**: `logging` モジュールを使用して適切なログを出力
4. **テスト**: 
   - Azure Functions: Azure Functions Core Toolsでテスト
   - FastAPI: pytest + TestClient でユニットテスト
5. **コード品質**: Black（フォーマッター）+ Flake8（リンター）
6. **API テスト**: `tests.http` ファイルでREST Clientを使用

## プロジェクト構造

```
.
├── .devcontainer/          # Dev Container設定
├── .vscode/               # VS Code設定
├── function_app.py        # Azure Functions アプリ
├── fastapi_app.py         # FastAPI アプリ
├── test_fastapi.py        # FastAPIテスト
├── tests.http             # HTTPリクエストテスト
├── requirements.txt       # Python依存関係
├── local.settings.json    # Azure Functions設定
├── host.json             # Azure Functions ホスト設定
├── Dockerfile.fastapi    # FastAPI用Dockerfile
├── docker-compose.yml    # Docker Compose設定
└── README.md             # このファイル
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
```

### FastAPI
```bash
# Dockerイメージのビルドとデプロイ
docker build -f Dockerfile.fastapi -t fastapi-app .
docker run -p 8000:8000 fastapi-app
```