from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import os
import logging

# ログ設定
logger = logging.getLogger(__name__)

# Blob Views用のルーター
router = APIRouter()


@router.get("/view")
def blob_view():
    """Blobの内容を表示するWebビュー"""
    return HTMLResponse(
        content="""
    <html>
        <head>
            <title>Blob テキスト表示</title>
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
                .form-group { 
                    margin-bottom: 20px; 
                }
                .form-group label { 
                    display: block; 
                    margin-bottom: 5px; 
                    font-weight: bold; 
                    color: #333; 
                }
                .form-group input, .form-group textarea { 
                    width: 100%; 
                    padding: 12px; 
                    border: 2px solid #ddd; 
                    border-radius: 6px; 
                    font-size: 14px; 
                    box-sizing: border-box; 
                }
                .form-group textarea { 
                    height: 200px; 
                    resize: vertical; 
                    font-family: 'Courier New', monospace; 
                }
                .btn { 
                    background-color: #007acc; 
                    color: white; 
                    padding: 12px 24px; 
                    border: none; 
                    border-radius: 6px; 
                    cursor: pointer; 
                    font-size: 14px; 
                    margin-right: 10px; 
                    margin-bottom: 10px; 
                }
                .btn:hover { 
                    background-color: #005a9e; 
                }
                .btn-danger { 
                    background-color: #dc3545; 
                }
                .btn-danger:hover { 
                    background-color: #c82333; 
                }
                #result { 
                    margin-top: 20px; 
                    padding: 15px; 
                    border-radius: 6px; 
                    display: none; 
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
                .back-link { 
                    display: inline-block; 
                    margin-bottom: 20px; 
                    color: #007acc; 
                    text-decoration: none; 
                }
                .back-link:hover { 
                    text-decoration: underline; 
                }
                pre { 
                    background-color: #f8f9fa; 
                    padding: 15px; 
                    border-radius: 6px; 
                    overflow-x: auto; 
                    white-space: pre-wrap; 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/" class="back-link">← ホームに戻る</a>
                <h1>📄 Blob テキスト表示</h1>
                
                <div class="form-group">
                    <label for="blobName">ファイル名:</label>
                    <input type="text" id="blobName" placeholder="例: sample.txt">
                </div>
                
                <button class="btn" onclick="readBlob()">📖 ファイル読み取り</button>
                <button class="btn" onclick="listBlobs()">📁 ファイル一覧表示</button>
                <button class="btn" onclick="downloadBlob()">⬇️ ダウンロード</button>
                <button class="btn btn-danger" onclick="deleteBlob()">🗑️ ファイル削除</button>
                
                <div class="form-group">
                    <label for="uploadContent">新しいテキストをアップロード:</label>
                    <textarea id="uploadContent" placeholder="ここにテキストを入力してください..."></textarea>
                </div>
                
                <button class="btn" onclick="uploadText()">⬆️ テキストアップロード</button>
                
                <div id="result"></div>
            </div>

            <script>
                function showResult(message, isSuccess = true) {
                    const result = document.getElementById('result');
                    result.innerHTML = message;
                    result.className = isSuccess ? 'success' : 'error';
                    result.style.display = 'block';
                }

                async function readBlob() {
                    const blobName = document.getElementById('blobName').value.trim();
                    if (!blobName) {
                        showResult('ファイル名を入力してください', false);
                        return;
                    }

                    try {
                        const response = await fetch(`/blob/read/${encodeURIComponent(blobName)}`);
                        if (response.ok) {
                            const data = await response.json();
                            showResult(`
                                <h3>📄 ${data.blob_name}</h3>
                                <p><strong>サイズ:</strong> ${data.size} bytes</p>
                                <p><strong>コンテンツタイプ:</strong> ${data.content_type || 'N/A'}</p>
                                <p><strong>最終更新:</strong> ${data.last_modified || 'N/A'}</p>
                                <h4>内容:</h4>
                                <pre>${data.content}</pre>
                            `);
                        } else {
                            const error = await response.json();
                            showResult(`エラー: ${error.detail}`, false);
                        }
                    } catch (error) {
                        showResult(`エラー: ${error.message}`, false);
                    }
                }

                async function listBlobs() {
                    try {
                        const response = await fetch('/blob/list');
                        if (response.ok) {
                            const data = await response.json();
                            let html = `
                                <h3>📁 ファイル一覧 (${data.container_name})</h3>
                                <p>合計: ${data.blob_count} ファイル</p>
                            `;
                            
                            if (data.blobs.length > 0) {
                                html += '<table style="width:100%; border-collapse: collapse; margin-top: 15px;">';
                                html += '<tr style="background-color: #f8f9fa;"><th style="border: 1px solid #ddd; padding: 8px;">ファイル名</th><th style="border: 1px solid #ddd; padding: 8px;">サイズ</th><th style="border: 1px solid #ddd; padding: 8px;">最終更新</th></tr>';
                                
                                data.blobs.forEach(blob => {
                                    html += `<tr>
                                        <td style="border: 1px solid #ddd; padding: 8px;">${blob.name}</td>
                                        <td style="border: 1px solid #ddd; padding: 8px;">${blob.size} bytes</td>
                                        <td style="border: 1px solid #ddd; padding: 8px;">${blob.last_modified || 'N/A'}</td>
                                    </tr>`;
                                });
                                
                                html += '</table>';
                            } else {
                                html += '<p>ファイルが見つかりません。</p>';
                            }
                            
                            showResult(html);
                        } else {
                            const error = await response.json();
                            showResult(`エラー: ${error.detail}`, false);
                        }
                    } catch (error) {
                        showResult(`エラー: ${error.message}`, false);
                    }
                }

                async function uploadText() {
                    const blobName = document.getElementById('blobName').value.trim();
                    const content = document.getElementById('uploadContent').value;
                    
                    if (!blobName) {
                        showResult('ファイル名を入力してください', false);
                        return;
                    }
                    
                    if (!content) {
                        showResult('アップロードするテキストを入力してください', false);
                        return;
                    }

                    try {
                        const response = await fetch('/blob/upload/text', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                blob_name: blobName,
                                content: content
                            })
                        });

                        if (response.ok) {
                            const data = await response.json();
                            showResult(`✅ ${data.message} (${data.size} bytes)`);
                            document.getElementById('uploadContent').value = '';
                        } else {
                            const error = await response.json();
                            showResult(`エラー: ${error.detail}`, false);
                        }
                    } catch (error) {
                        showResult(`エラー: ${error.message}`, false);
                    }
                }

                async function downloadBlob() {
                    const blobName = document.getElementById('blobName').value.trim();
                    if (!blobName) {
                        showResult('ファイル名を入力してください', false);
                        return;
                    }

                    try {
                        window.open(`/blob/download/${encodeURIComponent(blobName)}`, '_blank');
                        showResult(`📥 ${blobName} のダウンロードを開始しました`);
                    } catch (error) {
                        showResult(`エラー: ${error.message}`, false);
                    }
                }

                async function deleteBlob() {
                    const blobName = document.getElementById('blobName').value.trim();
                    if (!blobName) {
                        showResult('ファイル名を入力してください', false);
                        return;
                    }

                    if (!confirm(`"${blobName}" を削除してもよろしいですか？`)) {
                        return;
                    }

                    try {
                        const response = await fetch(`/blob/delete/${encodeURIComponent(blobName)}`, {
                            method: 'DELETE'
                        });

                        if (response.ok) {
                            const data = await response.json();
                            showResult(`✅ ${data.message}`);
                            document.getElementById('blobName').value = '';
                        } else {
                            const error = await response.json();
                            showResult(`エラー: ${error.detail}`, false);
                        }
                    } catch (error) {
                        showResult(`エラー: ${error.message}`, false);
                    }
                }
            </script>
        </body>
    </html>
    """
    )


@router.get("/list-view")
def blob_list_view():
    """Blobの一覧を表示するWebビュー"""
    return HTMLResponse(
        content="""
    <html>
        <head>
            <title>ファイル一覧表示</title>
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
                .back-link { 
                    display: inline-block; 
                    margin-bottom: 20px; 
                    color: #007acc; 
                    text-decoration: none; 
                }
                .back-link:hover { 
                    text-decoration: underline; 
                }
                .btn { 
                    background-color: #007acc; 
                    color: white; 
                    padding: 12px 24px; 
                    border: none; 
                    border-radius: 6px; 
                    cursor: pointer; 
                    font-size: 14px; 
                    margin-right: 10px; 
                    margin-bottom: 20px; 
                }
                .btn:hover { 
                    background-color: #005a9e; 
                }
                table { 
                    width: 100%; 
                    border-collapse: collapse; 
                    margin-top: 20px; 
                }
                th, td { 
                    border: 1px solid #ddd; 
                    padding: 12px; 
                    text-align: left; 
                }
                th { 
                    background-color: #f8f9fa; 
                    font-weight: bold; 
                }
                tr:nth-child(even) { 
                    background-color: #f8f9fa; 
                }
                .action-btn { 
                    background-color: #007acc; 
                    color: white; 
                    padding: 6px 12px; 
                    border: none; 
                    border-radius: 4px; 
                    cursor: pointer; 
                    font-size: 12px; 
                    margin-right: 5px; 
                }
                .action-btn:hover { 
                    background-color: #005a9e; 
                }
                .action-btn.danger { 
                    background-color: #dc3545; 
                }
                .action-btn.danger:hover { 
                    background-color: #c82333; 
                }
                #result { 
                    margin-top: 20px; 
                    padding: 15px; 
                    border-radius: 6px; 
                    display: none; 
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
                .loading { 
                    text-align: center; 
                    color: #666; 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/" class="back-link">← ホームに戻る</a>
                <h1>📁 ファイル一覧表示</h1>
                
                <button class="btn" onclick="loadFileList()">🔄 一覧を更新</button>
                
                <div id="fileList">
                    <div class="loading">読み込み中...</div>
                </div>
                
                <div id="result"></div>
            </div>

            <script>
                function showResult(message, isSuccess = true) {
                    const result = document.getElementById('result');
                    result.innerHTML = message;
                    result.className = isSuccess ? 'success' : 'error';
                    result.style.display = 'block';
                }

                function formatFileSize(bytes) {
                    if (bytes === 0) return '0 Bytes';
                    const k = 1024;
                    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
                    const i = Math.floor(Math.log(bytes) / Math.log(k));
                    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
                }

                function formatDate(dateString) {
                    if (!dateString || dateString === 'N/A') return 'N/A';
                    const date = new Date(dateString);
                    return date.toLocaleString('ja-JP');
                }

                async function loadFileList() {
                    const fileListDiv = document.getElementById('fileList');
                    fileListDiv.innerHTML = '<div class="loading">読み込み中...</div>';

                    try {
                        const response = await fetch('/blob/list');
                        if (response.ok) {
                            const data = await response.json();
                            
                            let html = `
                                <h3>📁 コンテナ: ${data.container_name}</h3>
                                <p>合計ファイル数: ${data.blob_count}</p>
                            `;
                            
                            if (data.blobs.length > 0) {
                                html += `
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>ファイル名</th>
                                                <th>サイズ</th>
                                                <th>コンテンツタイプ</th>
                                                <th>最終更新</th>
                                                <th>操作</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                `;
                                
                                data.blobs.forEach(blob => {
                                    html += `
                                        <tr>
                                            <td>${blob.name}</td>
                                            <td>${formatFileSize(blob.size)}</td>
                                            <td>${blob.content_type || 'N/A'}</td>
                                            <td>${formatDate(blob.last_modified)}</td>
                                            <td>
                                                <button class="action-btn" onclick="viewFile('${blob.name}')">📖 表示</button>
                                                <button class="action-btn" onclick="downloadFile('${blob.name}')">⬇️ DL</button>
                                                <button class="action-btn danger" onclick="deleteFile('${blob.name}')">🗑️ 削除</button>
                                            </td>
                                        </tr>
                                    `;
                                });
                                
                                html += `
                                        </tbody>
                                    </table>
                                `;
                            } else {
                                html += '<p>ファイルが見つかりません。</p>';
                            }
                            
                            fileListDiv.innerHTML = html;
                        } else {
                            const error = await response.json();
                            fileListDiv.innerHTML = `<div class="error">エラー: ${error.detail}</div>`;
                        }
                    } catch (error) {
                        fileListDiv.innerHTML = `<div class="error">エラー: ${error.message}</div>`;
                    }
                }

                async function viewFile(fileName) {
                    try {
                        const response = await fetch(`/blob/read/${encodeURIComponent(fileName)}`);
                        if (response.ok) {
                            const data = await response.json();
                            showResult(`
                                <h3>📄 ${data.blob_name}</h3>
                                <p><strong>サイズ:</strong> ${formatFileSize(data.size)}</p>
                                <p><strong>コンテンツタイプ:</strong> ${data.content_type || 'N/A'}</p>
                                <p><strong>最終更新:</strong> ${formatDate(data.last_modified)}</p>
                                <h4>内容:</h4>
                                <pre style="background-color: #f8f9fa; padding: 15px; border-radius: 6px; overflow-x: auto; white-space: pre-wrap; max-height: 400px; overflow-y: auto;">${data.content}</pre>
                            `);
                        } else {
                            const error = await response.json();
                            showResult(`エラー: ${error.detail}`, false);
                        }
                    } catch (error) {
                        showResult(`エラー: ${error.message}`, false);
                    }
                }

                function downloadFile(fileName) {
                    try {
                        window.open(`/blob/download/${encodeURIComponent(fileName)}`, '_blank');
                        showResult(`📥 ${fileName} のダウンロードを開始しました`);
                    } catch (error) {
                        showResult(`エラー: ${error.message}`, false);
                    }
                }

                async function deleteFile(fileName) {
                    if (!confirm(`"${fileName}" を削除してもよろしいですか？`)) {
                        return;
                    }

                    try {
                        const response = await fetch(`/blob/delete/${encodeURIComponent(fileName)}`, {
                            method: 'DELETE'
                        });

                        if (response.ok) {
                            const data = await response.json();
                            showResult(`✅ ${data.message}`);
                            // ファイル一覧を再読み込み
                            loadFileList();
                        } else {
                            const error = await response.json();
                            showResult(`エラー: ${error.detail}`, false);
                        }
                    } catch (error) {
                        showResult(`エラー: ${error.message}`, false);
                    }
                }

                // ページ読み込み時にファイル一覧を取得
                window.onload = loadFileList;
            </script>
        </body>
    </html>
    """
    )
