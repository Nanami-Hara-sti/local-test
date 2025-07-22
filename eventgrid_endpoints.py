from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
import logging
import json
from datetime import datetime
from typing import List, Dict, Any

# CSV処理関連のインポートを追加
from csv_processor import process_csv_from_eventgrid

# ログ設定
logger = logging.getLogger(__name__)

# EventGrid用のルーター
router = APIRouter()

# イベントストレージ（メモリ内）
events_storage: List[Dict[str, Any]] = []


@router.post("/events")
async def handle_eventgrid_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Azure EventGridからのWebhookイベントを受信
    """
    try:
        # リクエストボディを取得
        body = await request.body()
        logger.info(f"Received EventGrid webhook: {body.decode()}")

        # JSONとしてパース
        events = json.loads(body.decode())

        # イベントが配列でない場合は配列にする
        if not isinstance(events, list):
            events = [events]

        # 各イベントを処理
        for event in events:
            # タイムスタンプを追加
            event["receivedAt"] = datetime.now().isoformat()

            # メモリストレージに保存
            events_storage.append(event)

            # ストレージサイズを制限（最新100件まで）
            if len(events_storage) > 100:
                events_storage.pop(0)

            # CSVファイルアップロードイベントかチェック
            if event.get("eventType") == "csvfile.uploaded":
                logger.info(f"CSV処理イベントを検出: {event.get('subject')}")
                # バックグラウンドでCSV処理を開始
                background_tasks.add_task(
                    process_csv_from_eventgrid, event.get("data", {})
                )

            logger.info(
                f"Processed event: {event.get('eventType', 'Unknown')} - {event.get('subject', 'No subject')}"
            )

        return {"status": "success", "processed_events": len(events)}

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in EventGrid webhook: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        logger.error(f"Error processing EventGrid webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events")
def get_events():
    """
    受信したEventGridイベントの一覧を取得
    """
    return {
        "events": events_storage,
        "total_count": len(events_storage),
        "last_updated": datetime.now().isoformat(),
    }


@router.delete("/events")
def clear_events():
    """
    保存されているイベントをクリア
    """
    event_count = len(events_storage)
    events_storage.clear()
    logger.info(f"Cleared {event_count} events from storage")
    return {"status": "cleared", "cleared_events": event_count}


@router.get("/events-view")
def events_view():
    """EventGridイベントを表示するWebビュー"""
    return HTMLResponse(
        content="""
    <html>
        <head>
            <title>EventGrid ダッシュボード</title>
            <meta charset="UTF-8">
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 20px; 
                    background-color: #f0f2f5; 
                }
                .container { 
                    max-width: 1200px; 
                    margin: 0 auto; 
                    background-color: white; 
                    border-radius: 8px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                    overflow: hidden; 
                }
                .header { 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; 
                    padding: 20px; 
                    text-align: center; 
                }
                .controls { 
                    padding: 20px; 
                    background-color: #f8f9fa; 
                    border-bottom: 1px solid #dee2e6; 
                }
                .btn { 
                    background-color: #007bff; 
                    color: white; 
                    border: none; 
                    padding: 10px 20px; 
                    border-radius: 5px; 
                    cursor: pointer; 
                    margin-right: 10px; 
                    font-weight: bold;
                }
                .btn:hover { 
                    background-color: #0056b3; 
                }
                .btn-danger { 
                    background-color: #dc3545; 
                }
                .btn-danger:hover { 
                    background-color: #c82333; 
                }
                .event-list { 
                    padding: 20px; 
                }
                .event-card { 
                    border: 1px solid #dee2e6; 
                    border-radius: 5px; 
                    margin-bottom: 15px; 
                    padding: 15px; 
                    background-color: #fff; 
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1); 
                }
                .event-header { 
                    display: flex; 
                    justify-content: space-between; 
                    align-items: center; 
                    margin-bottom: 10px; 
                }
                .event-type { 
                    background-color: #007bff; 
                    color: white; 
                    padding: 4px 8px; 
                    border-radius: 3px; 
                    font-size: 12px; 
                    font-weight: bold; 
                }
                .event-time { 
                    color: #6c757d; 
                    font-size: 12px; 
                }
                .event-subject { 
                    font-weight: bold; 
                    margin-bottom: 5px; 
                }
                .event-data { 
                    background-color: #f8f9fa; 
                    padding: 10px; 
                    border-radius: 3px; 
                    font-family: monospace; 
                    font-size: 12px; 
                    white-space: pre-wrap; 
                    max-height: 200px; 
                    overflow-y: auto; 
                }
                .stats { 
                    display: flex; 
                    justify-content: space-around; 
                    background-color: #e9ecef; 
                    padding: 15px; 
                    margin-bottom: 20px; 
                }
                .stat-item { 
                    text-align: center; 
                }
                .stat-value { 
                    font-size: 24px; 
                    font-weight: bold; 
                    color: #007bff; 
                }
                .stat-label { 
                    color: #6c757d; 
                    font-size: 12px; 
                }
                .no-events { 
                    text-align: center; 
                    color: #6c757d; 
                    padding: 40px; 
                    font-style: italic; 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚡ EventGrid ダッシュボード</h1>
                    <p>リアルタイムイベント監視・管理</p>
                </div>
                
                <div class="controls">
                    <button class="btn" onclick="refreshEvents()">🔄 更新</button>
                    <button class="btn btn-danger" onclick="clearEvents()">🗑️ イベントクリア</button>
                    <button class="btn" onclick="toggleAutoRefresh()">⏰ 自動更新 ON/OFF</button>
                </div>
                
                <div id="stats" class="stats">
                    <div class="stat-item">
                        <div class="stat-value" id="total-events">0</div>
                        <div class="stat-label">総イベント数</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="last-update">-</div>
                        <div class="stat-label">最終更新</div>
                    </div>
                </div>
                
                <div class="event-list" id="event-list">
                    <div class="no-events">イベントがありません</div>
                </div>
            </div>
            
            <script>
                let autoRefresh = false;
                let refreshInterval;
                
                async function refreshEvents() {
                    try {
                        const response = await fetch('/eventgrid/events');
                        const data = await response.json();
                        
                        // 統計更新
                        document.getElementById('total-events').textContent = data.total_count;
                        document.getElementById('last-update').textContent = 
                            new Date(data.last_updated).toLocaleTimeString();
                        
                        // イベント一覧更新
                        const eventList = document.getElementById('event-list');
                        
                        if (data.events.length === 0) {
                            eventList.innerHTML = '<div class="no-events">イベントがありません</div>';
                        } else {
                            eventList.innerHTML = data.events.reverse().map(event => `
                                <div class="event-card">
                                    <div class="event-header">
                                        <span class="event-type">${event.eventType || 'Unknown'}</span>
                                        <span class="event-time">${new Date(event.receivedAt).toLocaleString()}</span>
                                    </div>
                                    <div class="event-subject">${event.subject || 'No subject'}</div>
                                    <div class="event-data">${JSON.stringify(event, null, 2)}</div>
                                </div>
                            `).join('');
                        }
                    } catch (error) {
                        console.error('Error refreshing events:', error);
                        alert('イベントの取得に失敗しました');
                    }
                }
                
                async function clearEvents() {
                    if (confirm('すべてのイベントをクリアしますか？')) {
                        try {
                            await fetch('/eventgrid/events', { method: 'DELETE' });
                            refreshEvents();
                        } catch (error) {
                            console.error('Error clearing events:', error);
                            alert('イベントのクリアに失敗しました');
                        }
                    }
                }
                
                function toggleAutoRefresh() {
                    autoRefresh = !autoRefresh;
                    if (autoRefresh) {
                        refreshInterval = setInterval(refreshEvents, 5000);
                        alert('自動更新を開始しました（5秒間隔）');
                    } else {
                        clearInterval(refreshInterval);
                        alert('自動更新を停止しました');
                    }
                }
                
                // 初期読み込み
                refreshEvents();
            </script>
        </body>
    </html>
    """
    )


@router.get("/test-ui")
def test_ui():
    """EventGridテスト用のWebUI"""
    return HTMLResponse(
        content="""
    <html>
        <head>
            <title>EventGrid テストツール</title>
            <meta charset="UTF-8">
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 20px; 
                    background-color: #f5f5f5; 
                }
                .container { 
                    max-width: 800px; 
                    margin: 0 auto; 
                    background-color: white; 
                    padding: 30px; 
                    border-radius: 8px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                }
                .header { 
                    text-align: center; 
                    margin-bottom: 30px; 
                    color: #333; 
                }
                .form-group { 
                    margin-bottom: 20px; 
                }
                label { 
                    display: block; 
                    margin-bottom: 5px; 
                    font-weight: bold; 
                    color: #555; 
                }
                input, select, textarea { 
                    width: 100%; 
                    padding: 10px; 
                    border: 1px solid #ddd; 
                    border-radius: 4px; 
                    font-size: 14px; 
                }
                textarea { 
                    height: 150px; 
                    font-family: monospace; 
                }
                .btn { 
                    background-color: #007bff; 
                    color: white; 
                    padding: 12px 24px; 
                    border: none; 
                    border-radius: 4px; 
                    cursor: pointer; 
                    font-size: 16px; 
                    font-weight: bold; 
                }
                .btn:hover { 
                    background-color: #0056b3; 
                }
                .result { 
                    margin-top: 20px; 
                    padding: 15px; 
                    border-radius: 4px; 
                    font-family: monospace; 
                    white-space: pre-wrap; 
                }
                .success { 
                    background-color: #d4edda; 
                    border: 1px solid #c3e6cb; 
                    color: #155724; 
                }
                .error { 
                    background-color: #f8d7da; 
                    border: 1px solid #f5c6cb; 
                    color: #721c24; 
                }
                .preset-buttons { 
                    display: flex; 
                    gap: 10px; 
                    margin-bottom: 10px; 
                }
                .preset-btn { 
                    background-color: #6c757d; 
                    color: white; 
                    padding: 8px 16px; 
                    border: none; 
                    border-radius: 4px; 
                    cursor: pointer; 
                    font-size: 12px; 
                }
                .preset-btn:hover { 
                    background-color: #5a6268; 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧪 EventGrid テストツール</h1>
                    <p>ローカル環境でEventGridイベントをテスト</p>
                </div>
                
                <form id="test-form">
                    <div class="form-group">
                        <label for="event-type">イベントタイプ:</label>
                        <select id="event-type">
                            <option value="Microsoft.Storage.BlobCreated">Microsoft.Storage.BlobCreated</option>
                            <option value="Microsoft.Storage.BlobDeleted">Microsoft.Storage.BlobDeleted</option>
                            <option value="Microsoft.EventGrid.SubscriptionValidationEvent">Microsoft.EventGrid.SubscriptionValidationEvent</option>
                            <option value="Custom.Application.Test">Custom.Application.Test</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="subject">Subject:</label>
                        <input type="text" id="subject" placeholder="/blobServices/default/containers/sample/blobs/test.txt">
                    </div>
                    
                    <div class="form-group">
                        <label for="event-data">イベントデータ (JSON):</label>
                        <div class="preset-buttons">
                            <button type="button" class="preset-btn" onclick="loadPreset('blob-created')">Blob作成</button>
                            <button type="button" class="preset-btn" onclick="loadPreset('blob-deleted')">Blob削除</button>
                            <button type="button" class="preset-btn" onclick="loadPreset('custom')">カスタム</button>
                        </div>
                        <textarea id="event-data" placeholder="イベントデータをJSON形式で入力"></textarea>
                    </div>
                    
                    <button type="submit" class="btn">🚀 イベント送信</button>
                </form>
                
                <div id="result"></div>
            </div>
            
            <script>
                const presets = {
                    'blob-created': {
                        eventType: 'Microsoft.Storage.BlobCreated',
                        subject: '/blobServices/default/containers/sample/blobs/test.txt',
                        data: {
                            api: 'PutBlob',
                            requestId: '12345678-1234-1234-1234-123456789012',
                            eTag: '0x8D7EAF5D51C5E8E',
                            contentType: 'text/plain',
                            contentLength: 1024,
                            blobType: 'BlockBlob',
                            url: 'https://mystorageaccount.blob.core.windows.net/sample/test.txt',
                            sequencer: '00000000000000000000000000000000000000000000000001',
                            storageDiagnostics: {
                                batchId: '12345678-1234-1234-1234-123456789012'
                            }
                        }
                    },
                    'blob-deleted': {
                        eventType: 'Microsoft.Storage.BlobDeleted',
                        subject: '/blobServices/default/containers/sample/blobs/test.txt',
                        data: {
                            api: 'DeleteBlob',
                            requestId: '12345678-1234-1234-1234-123456789012',
                            contentType: 'text/plain',
                            blobType: 'BlockBlob',
                            url: 'https://mystorageaccount.blob.core.windows.net/sample/test.txt',
                            sequencer: '00000000000000000000000000000000000000000000000002',
                            storageDiagnostics: {
                                batchId: '12345678-1234-1234-1234-123456789012'
                            }
                        }
                    },
                    'custom': {
                        eventType: 'Custom.Application.Test',
                        subject: '/test/custom-event',
                        data: {
                            message: 'This is a test event',
                            timestamp: new Date().toISOString(),
                            customProperty: 'custom value'
                        }
                    }
                };
                
                function loadPreset(presetName) {
                    const preset = presets[presetName];
                    if (preset) {
                        document.getElementById('event-type').value = preset.eventType;
                        document.getElementById('subject').value = preset.subject;
                        document.getElementById('event-data').value = JSON.stringify(preset.data, null, 2);
                    }
                }
                
                document.getElementById('test-form').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    
                    const eventType = document.getElementById('event-type').value;
                    const subject = document.getElementById('subject').value;
                    const eventDataText = document.getElementById('event-data').value;
                    
                    let eventData;
                    try {
                        eventData = JSON.parse(eventDataText);
                    } catch (error) {
                        showResult('error', 'Invalid JSON format: ' + error.message);
                        return;
                    }
                    
                    const event = {
                        id: 'test-' + Date.now(),
                        eventType: eventType,
                        subject: subject,
                        eventTime: new Date().toISOString(),
                        data: eventData,
                        dataVersion: '1.0',
                        metadataVersion: '1',
                        topic: '/subscriptions/test/resourceGroups/test/providers/Microsoft.EventGrid/topics/test'
                    };
                    
                    try {
                        const response = await fetch('/eventgrid/events', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify([event])
                        });
                        
                        if (response.ok) {
                            const result = await response.json();
                            showResult('success', 'Event sent successfully: ' + JSON.stringify(result, null, 2));
                        } else {
                            const error = await response.text();
                            showResult('error', 'Error sending event: ' + error);
                        }
                    } catch (error) {
                        showResult('error', 'Network error: ' + error.message);
                    }
                });
                
                function showResult(type, message) {
                    const resultDiv = document.getElementById('result');
                    resultDiv.className = 'result ' + type;
                    resultDiv.textContent = message;
                }
                
                // 初期プリセット読み込み
                loadPreset('blob-created');
            </script>
        </body>
    </html>
    """
    )


@router.get("/setup-guide")
def setup_guide():
    """EventGrid設定ガイド"""
    return HTMLResponse(
        content="""
    <html>
        <head>
            <title>EventGrid セットアップガイド</title>
            <meta charset="UTF-8">
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 20px; 
                    background-color: #f5f5f5; 
                    line-height: 1.6; 
                }
                .container { 
                    max-width: 900px; 
                    margin: 0 auto; 
                    background-color: white; 
                    padding: 30px; 
                    border-radius: 8px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                }
                .header { 
                    text-align: center; 
                    margin-bottom: 30px; 
                    color: #333; 
                }
                .step { 
                    margin-bottom: 30px; 
                    padding: 20px; 
                    border: 1px solid #ddd; 
                    border-radius: 8px; 
                    background-color: #f8f9fa; 
                }
                .step-title { 
                    color: #007bff; 
                    font-size: 18px; 
                    font-weight: bold; 
                    margin-bottom: 10px; 
                }
                .code-block { 
                    background-color: #2d3748; 
                    color: #e2e8f0; 
                    padding: 15px; 
                    border-radius: 4px; 
                    font-family: monospace; 
                    margin: 10px 0; 
                    overflow-x: auto; 
                }
                .warning { 
                    background-color: #fff3cd; 
                    border: 1px solid #ffeaa7; 
                    color: #856404; 
                    padding: 15px; 
                    border-radius: 4px; 
                    margin: 10px 0; 
                }
                .info { 
                    background-color: #d1ecf1; 
                    border: 1px solid #bee5eb; 
                    color: #0c5460; 
                    padding: 15px; 
                    border-radius: 4px; 
                    margin: 10px 0; 
                }
                ul { 
                    margin-left: 20px; 
                }
                .endpoint-url { 
                    background-color: #e9ecef; 
                    padding: 10px; 
                    border-radius: 4px; 
                    font-family: monospace; 
                    border-left: 4px solid #007bff; 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔧 Azure EventGrid セットアップガイド</h1>
                    <p>Azure EventGridとの連携設定手順</p>
                </div>
                
                <div class="step">
                    <div class="step-title">📋 ステップ1: EventGridトピックの作成</div>
                    <p>Azure PortalでEventGridトピックを作成します。</p>
                    <div class="code-block">
# Azure CLIを使用する場合
az eventgrid topic create \\
  --name my-eventgrid-topic \\
  --location eastus \\
  --resource-group my-resource-group
                    </div>
                </div>
                
                <div class="step">
                    <div class="step-title">🔗 ステップ2: Webhookエンドポイントの設定</div>
                    <p>このアプリケーションのWebhookエンドポイントを設定します。</p>
                    <div class="endpoint-url">
Webhook URL: https://your-domain.com/eventgrid/events
                    </div>
                    <div class="info">
                        <strong>ローカル開発時:</strong> ngrokなどのトンネリングサービスを使用してローカルサーバーを外部に公開してください。
                    </div>
                </div>
                
                <div class="step">
                    <div class="step-title">📝 ステップ3: イベントサブスクリプションの作成</div>
                    <p>EventGridトピックにイベントサブスクリプションを作成します。</p>
                    <div class="code-block">
az eventgrid event-subscription create \\
  --name my-subscription \\
  --source-resource-id /subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.EventGrid/topics/{topic-name} \\
  --endpoint https://your-domain.com/eventgrid/events
                    </div>
                </div>
                
                <div class="step">
                    <div class="step-title">🔧 ステップ4: Azure Blob StorageでのEventGrid設定</div>
                    <p>Blob StorageイベントをEventGridに送信するように設定します。</p>
                    <ul>
                        <li>Azure PortalでBlobストレージアカウントを開く</li>
                        <li>「イベント」セクションに移動</li>
                        <li>「+ イベントサブスクリプション」をクリック</li>
                        <li>エンドポイントタイプで「Webhook」を選択</li>
                        <li>エンドポイントURLを設定: <code>https://your-domain.com/eventgrid/events</code></li>
                    </ul>
                </div>
                
                <div class="step">
                    <div class="step-title">🧪 ステップ5: テストとデバッグ</div>
                    <p>設定が正しく動作するかテストします。</p>
                    <ul>
                        <li><a href="/eventgrid/test-ui" target="_blank">EventGridテストツール</a>でローカルテスト</li>
                        <li><a href="/eventgrid/events-view" target="_blank">EventGridダッシュボード</a>でイベント監視</li>
                        <li>Blob Storageにファイルをアップロード/削除してイベントを確認</li>
                    </ul>
                </div>
                
                <div class="step">
                    <div class="step-title">⚙️ ステップ6: 本番環境での設定</div>
                    <div class="warning">
                        <strong>セキュリティ注意:</strong> 本番環境では以下の設定を必ず行ってください。
                    </div>
                    <ul>
                        <li>HTTPS通信の強制</li>
                        <li>EventGrid署名検証の実装</li>
                        <li>アクセス制御とファイアウォール設定</li>
                        <li>監視とログ記録の設定</li>
                    </ul>
                </div>
                
                <div class="step">
                    <div class="step-title">📊 ステップ7: 監視とメンテナンス</div>
                    <p>EventGridの動作を継続的に監視します。</p>
                    <ul>
                        <li>Azure Monitorでメトリクスを確認</li>
                        <li>配信エラーの監視</li>
                        <li>デッドレターキューの設定</li>
                        <li>再試行ポリシーの調整</li>
                    </ul>
                </div>
                
                <div class="info">
                    <strong>詳細情報:</strong> Azure EventGridの詳細については、
                    <a href="https://docs.microsoft.com/azure/event-grid/" target="_blank">Microsoft公式ドキュメント</a>
                    をご参照ください。
                </div>
            </div>
        </body>
    </html>
    """
    )
