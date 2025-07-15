from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import HTMLResponse
import logging
from datetime import datetime
from typing import Optional
from models import Histogram, ProjectData, ProjectListResponse, UserData, UserListResponse

# ログ設定
logger = logging.getLogger(__name__)

# Assign-Kun API用のルーター
router = APIRouter()


@router.get("/histograms", response_model=list[Histogram])
def get_histograms(
    month: Optional[int] = Query(None, description="基準月（指定月のデータを取得）", ge=1, le=12)
):
    """
    ヒストグラムデータ取得API
    リソースヒストグラム一覧を取得して返却します
    """
    logger.info(f"Histogram data requested for month: {month}")
    
    try:
        # デモ用のサンプルヒストグラムデータ
        demo_histograms = [
            {
                "histogram_id": 1,
                "histogram_ac_code": "AC001",
                "histogram_ac_name": "アカウント1",
                "histogram_pj_br_num": "PJ001",
                "histogram_pj_name": "プロジェクト1",
                "histogram_pj_contract_form": "請負",
                "histogram_costs_unit": 1,
                "histogram_year": 2025,
                "annual_data": {
                    "histogram_01month": 1.2,
                    "histogram_02month": 1.5,
                    "histogram_03month": 1.8,
                    "histogram_04month": 1.5,
                    "histogram_05month": 2.0,
                    "histogram_06month": 1.8,
                    "histogram_07month": 2.2,
                    "histogram_08month": 1.9,
                    "histogram_09month": 2.1,
                    "histogram_10month": 1.7,
                    "histogram_11month": 1.6,
                    "histogram_12month": 1.4
                }
            },
            {
                "histogram_id": 2,
                "histogram_ac_code": "AC002",
                "histogram_ac_name": "アカウント2",
                "histogram_pj_br_num": "PJ002",
                "histogram_pj_name": "プロジェクト2",
                "histogram_pj_contract_form": "派遣",
                "histogram_costs_unit": 1,
                "histogram_year": 2025,
                "annual_data": {
                    "histogram_01month": 0.8,
                    "histogram_02month": 1.0,
                    "histogram_03month": 1.2,
                    "histogram_04month": 1.1,
                    "histogram_05month": 1.3,
                    "histogram_06month": 1.5,
                    "histogram_07month": 1.4,
                    "histogram_08month": 1.6,
                    "histogram_09month": 1.2,
                    "histogram_10month": 1.0,
                    "histogram_11month": 0.9,
                    "histogram_12month": 0.8
                }
            },
            {
                "histogram_id": 3,
                "histogram_ac_code": "AC003",
                "histogram_ac_name": "アカウント3",
                "histogram_pj_br_num": "PJ003",
                "histogram_pj_name": "プロジェクト3",
                "histogram_pj_contract_form": "請負",
                "histogram_costs_unit": 1,
                "histogram_year": 2025,
                "annual_data": {
                    "histogram_01month": 2.1,
                    "histogram_02month": 2.3,
                    "histogram_03month": 2.0,
                    "histogram_04month": 2.5,
                    "histogram_05month": 2.8,
                    "histogram_06month": 2.4,
                    "histogram_07month": 2.6,
                    "histogram_08month": 2.2,
                    "histogram_09month": 2.0,
                    "histogram_10month": 1.9,
                    "histogram_11month": 2.1,
                    "histogram_12month": 2.3
                }
            }
        ]
        
        # 月指定がある場合のフィルタリング（デモでは全データを返す）
        if month:
            logger.info(f"Filtering data for month: {month}")
            # 実際の実装では、指定月のデータをフィルタリング
        
        return demo_histograms
        
    except Exception as e:
        logger.error(f"Error retrieving histogram data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve histogram data: {str(e)}")


@router.get("/histograms/view")
def histogram_view():
    """ヒストグラムデータ表示用のWebビュー"""
    return HTMLResponse(
        content="""
    <html>
        <head>
            <title>📊 ヒストグラムデータ</title>
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
                .back-link { 
                    display: inline-block; 
                    margin-bottom: 20px; 
                    color: #007acc; 
                    text-decoration: none; 
                }
                .back-link:hover { 
                    text-decoration: underline; 
                }
                .controls { 
                    margin-bottom: 20px; 
                    padding: 15px; 
                    background-color: #f8f9fa; 
                    border-radius: 6px; 
                }
                .form-group { 
                    display: inline-block; 
                    margin-right: 15px; 
                }
                .form-group label { 
                    display: block; 
                    margin-bottom: 5px; 
                    font-weight: bold; 
                    color: #333; 
                }
                .form-group select, .form-group input { 
                    padding: 8px; 
                    border: 2px solid #ddd; 
                    border-radius: 4px; 
                    font-size: 14px; 
                }
                .btn { 
                    background-color: #007acc; 
                    color: white; 
                    padding: 10px 20px; 
                    border: none; 
                    border-radius: 6px; 
                    cursor: pointer; 
                    font-size: 14px; 
                    margin-right: 10px; 
                }
                .btn:hover { 
                    background-color: #005a9e; 
                }
                table { 
                    width: 100%; 
                    border-collapse: collapse; 
                    margin-top: 20px; 
                    font-size: 14px; 
                }
                th, td { 
                    border: 1px solid #ddd; 
                    padding: 8px; 
                    text-align: left; 
                }
                th { 
                    background-color: #007acc; 
                    color: white; 
                    font-weight: bold; 
                    position: sticky
                    top: 0
                }
                tr:nth-child(even) { 
                    background-color: #f8f9fa; 
                }
                tr:hover { 
                    background-color: #e3f2fd; 
                }
                .month-header { 
                    background-color: #e3f2fd !important; 
                    font-weight: bold; 
                    text-align: center; 
                }
                .loading { 
                    text-align: center; 
                    color: #666; 
                    padding: 20px; 
                }
                .error { 
                    background-color: #f8d7da; 
                    border: 1px solid #f5c6cb; 
                    color: #721c24; 
                    padding: 15px; 
                    border-radius: 6px; 
                    margin: 20px 0; 
                }
                .success { 
                    background-color: #d4edda; 
                    border: 1px solid #c3e6cb; 
                    color: #155724; 
                    padding: 15px; 
                    border-radius: 6px; 
                    margin: 20px 0; 
                }
                .table-container { 
                    overflow-x: auto; 
                    margin-top: 20px; 
                }
                .summary { 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                    gap: 15px; 
                    margin-bottom: 20px; 
                }
                .summary-card { 
                    background-color: #f8f9fa; 
                    padding: 15px; 
                    border-radius: 6px; 
                    text-align: center; 
                }
                .summary-card h3 { 
                    margin: 0 0 10px 0; 
                    color: #007acc; 
                }
                .summary-card .value { 
                    font-size: 24px; 
                    font-weight: bold; 
                    color: #333; 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/" class="back-link">← ホームに戻る</a>
                <h1>📊 Assign-Kun ヒストグラムデータ</h1>
                
                <div class="controls">
                    <div class="form-group">
                        <label for="monthFilter">月フィルタ:</label>
                        <select id="monthFilter">
                            <option value="">全ての月</option>
                            <option value="1">1月</option>
                            <option value="2">2月</option>
                            <option value="3">3月</option>
                            <option value="4">4月</option>
                            <option value="5">5月</option>
                            <option value="6">6月</option>
                            <option value="7">7月</option>
                            <option value="8">8月</option>
                            <option value="9">9月</option>
                            <option value="10">10月</option>
                            <option value="11">11月</option>
                            <option value="12">12月</option>
                        </select>
                    </div>
                    
                    <button class="btn" onclick="loadHistogramData()">🔄 データ更新</button>
                    <button class="btn" onclick="exportToCSV()">📁 CSV出力</button>
                </div>
                
                <div id="summary" class="summary" style="display: none;"></div>
                
                <div id="histogramData">
                    <div class="loading">データを読み込み中...</div>
                </div>
            </div>

            <script>
                let currentData = []

                function showMessage(message, isSuccess = true) {
                    const messageDiv = document.createElement('div')
                    messageDiv.className = isSuccess ? 'success' : 'error'
                    messageDiv.innerHTML = message
                    
                    const container = document.querySelector('.container')
                    const existingMessage = container.querySelector('.success, .error')
                    if (existingMessage) {
                        existingMessage.remove()
                    }
                    
                    container.insertBefore(messageDiv, container.querySelector('#summary'))
                    
                    setTimeout(() => {
                        messageDiv.remove()
                    }, 5000)
                }

                async function loadHistogramData() {
                    const dataDiv = document.getElementById('histogramData')
                    const summaryDiv = document.getElementById('summary')
                    
                    dataDiv.innerHTML = '<div class="loading">データを読み込み中...</div>'
                    summaryDiv.style.display = 'none'

                    try {
                        const monthFilter = document.getElementById('monthFilter').value
                        const url = monthFilter ? 
                            `/assign-kun/histograms?month=${monthFilter}` : 
                            '/assign-kun/histograms'
                        
                        const response = await fetch(url)
                        if (response.ok) {
                            const data = await response.json()
                            currentData = data
                            displayHistogramData(data)
                            displaySummary(data)
                            showMessage(`✅ ヒストグラムデータを正常に読み込みました (${data.length}件)`)
                        } else {
                            const error = await response.json()
                            dataDiv.innerHTML = `<div class="error">エラー: ${error.detail}</div>`
                            showMessage(`エラー: ${error.detail}`, false)
                        }
                    } catch (error) {
                        dataDiv.innerHTML = `<div class="error">エラー: ${error.message}</div>`
                        showMessage(`エラー: ${error.message}`, false)
                    }
                }

                function displaySummary(data) {
                    const summaryDiv = document.getElementById('summary')
                    
                    if (data.length === 0) {
                        summaryDiv.style.display = 'none'
                        return
                    }

                    const totalProjects = data.length
                    const contractForms = [...new Set(data.map(d => d.histogram_pj_contract_form))]
                    const totalAccounts = [...new Set(data.map(d => d.histogram_ac_code))].length
                    
                    // 年間の平均値を計算
                    const averageValues = data.map(d => {
                        const annualData = d.annual_data
                        const values = Object.values(annualData)
                        return values.reduce((sum, val) => sum + val, 0) / values.length
                    })
                    const overallAverage = averageValues.reduce((sum, avg) => sum + avg, 0) / averageValues.length

                    summaryDiv.innerHTML = `
                        <div class="summary-card">
                            <h3>プロジェクト数</h3>
                            <div class="value">${totalProjects}</div>
                        </div>
                        <div class="summary-card">
                            <h3>アカウント数</h3>
                            <div class="value">${totalAccounts}</div>
                        </div>
                        <div class="summary-card">
                            <h3>契約形態</h3>
                            <div class="value">${contractForms.join(', ')}</div>
                        </div>
                        <div class="summary-card">
                            <h3>平均値</h3>
                            <div class="value">${overallAverage.toFixed(2)}</div>
                        </div>
                    `
                    
                    summaryDiv.style.display = 'grid'
                }

                function displayHistogramData(data) {
                    const dataDiv = document.getElementById('histogramData')
                    
                    if (data.length === 0) {
                        dataDiv.innerHTML = '<p>データが見つかりません。</p>'
                        return
                    }

                    let html = `
                        <div class="table-container">
                            <table>
                                <thead>
                                    <tr>
                                        <th rowspan="2">ID</th>
                                        <th rowspan="2">アカウントコード</th>
                                        <th rowspan="2">アカウント名</th>
                                        <th rowspan="2">プロジェクト番号</th>
                                        <th rowspan="2">プロジェクト名</th>
                                        <th rowspan="2">契約形態</th>
                                        <th rowspan="2">年度</th>
                                        <th colspan="12" class="month-header">月別データ</th>
                                    </tr>
                                    <tr>
                                        <th class="month-header">1月</th>
                                        <th class="month-header">2月</th>
                                        <th class="month-header">3月</th>
                                        <th class="month-header">4月</th>
                                        <th class="month-header">5月</th>
                                        <th class="month-header">6月</th>
                                        <th class="month-header">7月</th>
                                        <th class="month-header">8月</th>
                                        <th class="month-header">9月</th>
                                        <th class="month-header">10月</th>
                                        <th class="month-header">11月</th>
                                        <th class="month-header">12月</th>
                                    </tr>
                                </thead>
                                <tbody>
                    `
                    
                    data.forEach(histogram => {
                        const annualData = histogram.annual_data
                        html += `
                            <tr>
                                <td>${histogram.histogram_id}</td>
                                <td>${histogram.histogram_ac_code}</td>
                                <td>${histogram.histogram_ac_name}</td>
                                <td>${histogram.histogram_pj_br_num}</td>
                                <td>${histogram.histogram_pj_name}</td>
                                <td>${histogram.histogram_pj_contract_form}</td>
                                <td>${histogram.histogram_year}</td>
                                <td>${annualData.histogram_01month}</td>
                                <td>${annualData.histogram_02month}</td>
                                <td>${annualData.histogram_03month}</td>
                                <td>${annualData.histogram_04month}</td>
                                <td>${annualData.histogram_05month}</td>
                                <td>${annualData.histogram_06month}</td>
                                <td>${annualData.histogram_07month}</td>
                                <td>${annualData.histogram_08month}</td>
                                <td>${annualData.histogram_09month}</td>
                                <td>${annualData.histogram_10month}</td>
                                <td>${annualData.histogram_11month}</td>
                                <td>${annualData.histogram_12month}</td>
                            </tr>
                        `
                    })
                    
                    html += `
                                </tbody>
                            </table>
                        </div>
                    `
                    
                    dataDiv.innerHTML = html
                }

                function exportToCSV() {
                    if (currentData.length === 0) {
                        showMessage('エクスポートするデータがありません', false)
                        return
                    }

                    let csv = 'ID,アカウントコード,アカウント名,プロジェクト番号,プロジェクト名,契約形態,年度,1月,2月,3月,4月,5月,6月,7月,8月,9月,10月,11月,12月\\n'
                    
                    currentData.forEach(histogram => {
                        const annualData = histogram.annual_data
                        csv += `${histogram.histogram_id},${histogram.histogram_ac_code},"${histogram.histogram_ac_name}",${histogram.histogram_pj_br_num},"${histogram.histogram_pj_name}","${histogram.histogram_pj_contract_form}",${histogram.histogram_year},${annualData.histogram_01month},${annualData.histogram_02month},${annualData.histogram_03month},${annualData.histogram_04month},${annualData.histogram_05month},${annualData.histogram_06month},${annualData.histogram_07month},${annualData.histogram_08month},${annualData.histogram_09month},${annualData.histogram_10month},${annualData.histogram_11month},${annualData.histogram_12month}\\n`
                    })

                    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
                    const link = document.createElement('a')
                    const url = URL.createObjectURL(blob)
                    link.setAttribute('href', url)
                    link.setAttribute('download', `histogram_data_${new Date().toISOString().split('T')[0]}.csv`)
                    link.style.visibility = 'hidden'
                    document.body.appendChild(link)
                    link.click()
                    document.body.removeChild(link)
                    
                    showMessage('✅ CSVファイルをダウンロードしました')
                }

                // ページ読み込み時にデータを取得
                window.onload = loadHistogramData
            </script>
        </body>
    </html>
    """
    )


@router.get("/projects", response_model=ProjectListResponse)
def get_projects(
    page: int = Query(1, description="ページ番号", ge=1),
    per_page: int = Query(10, description="1ページあたりの項目数", ge=1, le=100),
    status: Optional[str] = Query(None, description="プロジェクトステータス"),
    account_code: Optional[str] = Query(None, description="アカウントコード"),
    contract_form: Optional[str] = Query(None, description="契約形態")
):
    """
    プロジェクトデータ取得API
    プロジェクト一覧を取得して返却します
    """
    logger.info(f"Project data requested - page: {page}, per_page: {per_page}, status: {status}")
    
    try:
        # デモ用のサンプルプロジェクトデータ
        demo_projects = [
            {
                "project_id": 1,
                "project_code": "PJ001",
                "project_name": "Webアプリケーション開発",
                "account_code": "AC001",
                "account_name": "株式会社ABC",
                "contract_form": "請負",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "status": "進行中",
                "manager_name": "田中太郎",
                "team_size": 5,
                "budget": 10000000.0,
                "description": "ECサイト構築プロジェクト"
            },
            {
                "project_id": 2,
                "project_code": "PJ002",
                "project_name": "データ分析システム",
                "account_code": "AC002",
                "account_name": "株式会社XYZ",
                "contract_form": "派遣",
                "start_date": "2025-02-01",
                "end_date": "2025-08-31",
                "status": "進行中",
                "manager_name": "佐藤花子",
                "team_size": 3,
                "budget": 8000000.0,
                "description": "売上分析ダッシュボード開発"
            },
            {
                "project_id": 3,
                "project_code": "PJ003",
                "project_name": "モバイルアプリ開発",
                "account_code": "AC003",
                "account_name": "株式会社DEF",
                "contract_form": "請負",
                "start_date": "2025-03-01",
                "end_date": "2025-09-30",
                "status": "進行中",
                "manager_name": "鈴木次郎",
                "team_size": 4,
                "budget": 12000000.0,
                "description": "iOS/Androidアプリ開発"
            },
            {
                "project_id": 4,
                "project_code": "PJ004",
                "project_name": "インフラ構築",
                "account_code": "AC001",
                "account_name": "株式会社ABC",
                "contract_form": "請負",
                "start_date": "2024-10-01",
                "end_date": "2025-01-31",
                "status": "完了",
                "manager_name": "高橋三郎",
                "team_size": 6,
                "budget": 15000000.0,
                "description": "クラウドインフラ構築・移行"
            },
            {
                "project_id": 5,
                "project_code": "PJ005",
                "project_name": "セキュリティ強化",
                "account_code": "AC004",
                "account_name": "株式会社GHI",
                "contract_form": "派遣",
                "start_date": "2025-04-01",
                "end_date": "2025-06-30",
                "status": "計画中",
                "manager_name": "山田五郎",
                "team_size": 2,
                "budget": 5000000.0,
                "description": "セキュリティ監査・改善"
            },
            {
                "project_id": 6,
                "project_code": "PJ006",
                "project_name": "AI導入支援",
                "account_code": "AC005",
                "account_name": "株式会社JKL",
                "contract_form": "請負",
                "start_date": "2025-05-01",
                "end_date": "2025-11-30",
                "status": "計画中",
                "manager_name": "松本六郎",
                "team_size": 7,
                "budget": 20000000.0,
                "description": "機械学習システム導入"
            }
        ]
        
        # フィルタリング処理
        filtered_projects = demo_projects
        
        if status:
            filtered_projects = [p for p in filtered_projects if p["status"] == status]
            logger.info(f"Filtered by status '{status}': {len(filtered_projects)} projects")
        
        if account_code:
            filtered_projects = [p for p in filtered_projects if p["account_code"] == account_code]
            logger.info(f"Filtered by account_code '{account_code}': {len(filtered_projects)} projects")
        
        if contract_form:
            filtered_projects = [p for p in filtered_projects if p["contract_form"] == contract_form]
            logger.info(f"Filtered by contract_form '{contract_form}': {len(filtered_projects)} projects")
        
        # ページネーション処理
        total_count = len(filtered_projects)
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paged_projects = filtered_projects[start_index:end_index]
        
        return ProjectListResponse(
            projects=paged_projects,
            total_count=total_count,
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        logger.error(f"Error retrieving project data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve project data: {str(e)}")


@router.get("/projects/{project_id}", response_model=ProjectData)
def get_project(project_id: int):
    """
    プロジェクト詳細取得API
    指定されたIDのプロジェクト詳細を取得します
    """
    logger.info(f"Project detail requested for ID: {project_id}")
    
    try:
        # デモ用のサンプルプロジェクトデータ（上記と同じデータを使用）
        demo_projects = [
            {
                "project_id": 1,
                "project_code": "PJ001",
                "project_name": "Webアプリケーション開発",
                "account_code": "AC001",
                "account_name": "株式会社ABC",
                "contract_form": "請負",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "status": "進行中",
                "manager_name": "田中太郎",
                "team_size": 5,
                "budget": 10000000.0,
                "description": "ECサイト構築プロジェクト"
            },
            {
                "project_id": 2,
                "project_code": "PJ002",
                "project_name": "データ分析システム",
                "account_code": "AC002",
                "account_name": "株式会社XYZ",
                "contract_form": "派遣",
                "start_date": "2025-02-01",
                "end_date": "2025-08-31",
                "status": "進行中",
                "manager_name": "佐藤花子",
                "team_size": 3,
                "budget": 8000000.0,
                "description": "売上分析ダッシュボード開発"
            },
            {
                "project_id": 3,
                "project_code": "PJ003",
                "project_name": "モバイルアプリ開発",
                "account_code": "AC003",
                "account_name": "株式会社DEF",
                "contract_form": "請負",
                "start_date": "2025-03-01",
                "end_date": "2025-09-30",
                "status": "進行中",
                "manager_name": "鈴木次郎",
                "team_size": 4,
                "budget": 12000000.0,
                "description": "iOS/Androidアプリ開発"
            },
            {
                "project_id": 4,
                "project_code": "PJ004",
                "project_name": "インフラ構築",
                "account_code": "AC001",
                "account_name": "株式会社ABC",
                "contract_form": "請負",
                "start_date": "2024-10-01",
                "end_date": "2025-01-31",
                "status": "完了",
                "manager_name": "高橋三郎",
                "team_size": 6,
                "budget": 15000000.0,
                "description": "クラウドインフラ構築・移行"
            },
            {
                "project_id": 5,
                "project_code": "PJ005",
                "project_name": "セキュリティ強化",
                "account_code": "AC004",
                "account_name": "株式会社GHI",
                "contract_form": "派遣",
                "start_date": "2025-04-01",
                "end_date": "2025-06-30",
                "status": "計画中",
                "manager_name": "山田五郎",
                "team_size": 2,
                "budget": 5000000.0,
                "description": "セキュリティ監査・改善"
            },
            {
                "project_id": 6,
                "project_code": "PJ006",
                "project_name": "AI導入支援",
                "account_code": "AC005",
                "account_name": "株式会社JKL",
                "contract_form": "請負",
                "start_date": "2025-05-01",
                "end_date": "2025-11-30",
                "status": "計画中",
                "manager_name": "松本六郎",
                "team_size": 7,
                "budget": 20000000.0,
                "description": "機械学習システム導入"
            }
        ]
        
        # 指定されたIDのプロジェクトを検索
        project = next((p for p in demo_projects if p["project_id"] == project_id), None)
        
        if not project:
            raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
        
        return ProjectData(**project)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving project detail: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve project detail: {str(e)}")


@router.get("/projects/view")
def projects_view():
    """プロジェクトデータ表示用のWebビュー"""
    return HTMLResponse(
        content="""
    <html>
        <head>
            <title>📁 プロジェクトデータ</title>
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
                .back-link { 
                    display: inline-block; 
                    margin-bottom: 20px; 
                    color: #007acc; 
                    text-decoration: none; 
                }
                .back-link:hover { 
                    text-decoration: underline; 
                }
                .controls { 
                    margin-bottom: 20px; 
                    padding: 15px; 
                    background-color: #f8f9fa; 
                    border-radius: 6px; 
                }
                .form-group { 
                    display: inline-block; 
                    margin-right: 15px; 
                }
                .form-group label { 
                    display: block; 
                    margin-bottom: 5px; 
                    font-weight: bold; 
                    color: #333; 
                }
                .form-group select, .form-group input { 
                    padding: 8px; 
                    border: 2px solid #ddd; 
                    border-radius: 4px; 
                    font-size: 14px; 
                }
                .btn { 
                    background-color: #007acc; 
                    color: white; 
                    padding: 10px 20px; 
                    border: none; 
                    border-radius: 6px; 
                    cursor: pointer; 
                    font-size: 14px; 
                    margin-right: 10px; 
                }
                .btn:hover { 
                    background-color: #005a9e; 
                }
                .pagination { 
                    margin: 20px 0; 
                    text-align: center; 
                }
                .pagination button { 
                    background-color: #007acc; 
                    color: white; 
                    padding: 8px 16px; 
                    border: none; 
                    border-radius: 4px; 
                    cursor: pointer; 
                    margin: 0 5px; 
                }
                .pagination button:hover { 
                    background-color: #005a9e; 
                }
                .pagination button:disabled { 
                    background-color: #ccc; 
                    cursor: not-allowed; 
                }
                .pagination .current { 
                    background-color: #005a9e; 
                }
                .project-card { 
                    border: 1px solid #ddd; 
                    border-radius: 6px; 
                    padding: 15px; 
                    margin: 10px 0; 
                    background-color: #f9f9f9; 
                }
                .project-card:hover { 
                    background-color: #e3f2fd; 
                }
                .project-header { 
                    display: flex; 
                    justify-content: space-between; 
                    align-items: center; 
                    margin-bottom: 10px; 
                }
                .project-name { 
                    font-size: 18px; 
                    font-weight: bold; 
                    color: #007acc; 
                }
                .project-code { 
                    background-color: #007acc; 
                    color: white; 
                    padding: 4px 8px; 
                    border-radius: 4px; 
                    font-size: 12px; 
                }
                .project-details { 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                    gap: 10px; 
                    margin-top: 10px; 
                }
                .detail-item { 
                    font-size: 14px; 
                }
                .detail-label { 
                    font-weight: bold; 
                    color: #555; 
                }
                .status-badge { 
                    padding: 4px 8px; 
                    border-radius: 4px; 
                    font-size: 12px; 
                    font-weight: bold; 
                }
                .status-progress { 
                    background-color: #28a745; 
                    color: white; 
                }
                .status-completed { 
                    background-color: #6c757d; 
                    color: white; 
                }
                .status-planned { 
                    background-color: #ffc107; 
                    color: black; 
                }
                .loading { 
                    text-align: center; 
                    color: #666; 
                    padding: 20px; 
                }
                .error { 
                    background-color: #f8d7da; 
                    border: 1px solid #f5c6cb; 
                    color: #721c24; 
                    padding: 15px; 
                    border-radius: 6px; 
                    margin: 20px 0; 
                }
                .success { 
                    background-color: #d4edda; 
                    border: 1px solid #c3e6cb; 
                    color: #155724; 
                    padding: 15px; 
                    border-radius: 6px; 
                    margin: 20px 0; 
                }
                .summary { 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                    gap: 15px; 
                    margin-bottom: 20px; 
                }
                .summary-card { 
                    background-color: #f8f9fa; 
                    padding: 15px; 
                    border-radius: 6px; 
                    text-align: center; 
                }
                .summary-card h3 { 
                    margin: 0 0 10px 0; 
                    color: #007acc; 
                }
                .summary-card .value { 
                    font-size: 24px; 
                    font-weight: bold; 
                    color: #333; 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/" class="back-link">← ホームに戻る</a>
                <h1>📁 Assign-Kun プロジェクトデータ</h1>
                
                <div class="controls">
                    <div class="form-group">
                        <label for="statusFilter">ステータス:</label>
                        <select id="statusFilter">
                            <option value="">全てのステータス</option>
                            <option value="進行中">進行中</option>
                            <option value="完了">完了</option>
                            <option value="計画中">計画中</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="contractFilter">契約形態:</label>
                        <select id="contractFilter">
                            <option value="">全ての契約形態</option>
                            <option value="請負">請負</option>
                            <option value="派遣">派遣</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="accountFilter">アカウントコード:</label>
                        <input type="text" id="accountFilter" placeholder="AC001">
                    </div>
                    
                    <div class="form-group">
                        <label for="perPageSelect">表示件数:</label>
                        <select id="perPageSelect">
                            <option value="5">5件</option>
                            <option value="10" selected>10件</option>
                            <option value="20">20件</option>
                        </select>
                    </div>
                    
                    <button class="btn" onclick="loadProjectData()">🔄 データ更新</button>
                </div>
                
                <div id="summary" class="summary" style="display: none;"></div>
                
                <div id="projectData">
                    <div class="loading">データを読み込み中...</div>
                </div>
                
                <div id="pagination" class="pagination" style="display: none;"></div>
            </div>

            <script>
                let currentData = []
                let currentPage = 1
                let totalPages = 1
                let totalCount = 0

                function showMessage(message, isSuccess = true) {
                    const messageDiv = document.createElement('div')
                    messageDiv.className = isSuccess ? 'success' : 'error'
                    messageDiv.innerHTML = message
                    
                    const container = document.querySelector('.container')
                    const existingMessage = container.querySelector('.success, .error')
                    if (existingMessage) {
                        existingMessage.remove()
                    }
                    
                    container.insertBefore(messageDiv, container.querySelector('#summary'))
                    
                    setTimeout(() => {
                        messageDiv.remove()
                    }, 5000)
                }

                async function loadProjectData(page = 1) {
                    const dataDiv = document.getElementById('projectData')
                    const summaryDiv = document.getElementById('summary')
                    const paginationDiv = document.getElementById('pagination')
                    
                    dataDiv.innerHTML = '<div class="loading">データを読み込み中...</div>'
                    summaryDiv.style.display = 'none'
                    paginationDiv.style.display = 'none'

                    try {
                        const statusFilter = document.getElementById('statusFilter').value
                        const contractFilter = document.getElementById('contractFilter').value
                        const accountFilter = document.getElementById('accountFilter').value
                        const perPage = document.getElementById('perPageSelect').value
                        
                        let url = `/assign-kun/projects?page=${page}&per_page=${perPage}`
                        if (statusFilter) url += `&status=${encodeURIComponent(statusFilter)}`
                        if (contractFilter) url += `&contract_form=${encodeURIComponent(contractFilter)}`
                        if (accountFilter) url += `&account_code=${encodeURIComponent(accountFilter)}`
                        
                        const response = await fetch(url)
                        if (response.ok) {
                            const data = await response.json()
                            currentData = data.projects
                            currentPage = data.page
                            totalCount = data.total_count
                            totalPages = Math.ceil(totalCount / data.per_page)
                            
                            displayProjectData(data.projects)
                            displaySummary(data.projects)
                            displayPagination()
                            showMessage(`✅ プロジェクトデータを正常に読み込みました (${totalCount}件中 ${data.projects.length}件を表示)`)
                        } else {
                            const error = await response.json()
                            dataDiv.innerHTML = `<div class="error">エラー: ${error.detail}</div>`
                            showMessage(`エラー: ${error.detail}`, false)
                        }
                    } catch (error) {
                        dataDiv.innerHTML = `<div class="error">エラー: ${error.message}</div>`
                        showMessage(`エラー: ${error.message}`, false)
                    }
                }

                function displaySummary(projects) {
                    const summaryDiv = document.getElementById('summary')
                    
                    if (projects.length === 0) {
                        summaryDiv.style.display = 'none'
                        return
                    }

                    const statusCounts = {}
                    const contractCounts = {}
                    let totalBudget = 0
                    let totalTeamSize = 0
                    
                    projects.forEach(project => {
                        statusCounts[project.status] = (statusCounts[project.status] || 0) + 1
                        contractCounts[project.contract_form] = (contractCounts[project.contract_form] || 0) + 1
                        totalBudget += project.budget
                        totalTeamSize += project.team_size
                    })

                    summaryDiv.innerHTML = `
                        <div class="summary-card">
                            <h3>プロジェクト総数</h3>
                            <div class="value">${totalCount}</div>
                        </div>
                        <div class="summary-card">
                            <h3>表示中</h3>
                            <div class="value">${projects.length}</div>
                        </div>
                        <div class="summary-card">
                            <h3>総予算</h3>
                            <div class="value">¥${totalBudget.toLocaleString()}</div>
                        </div>
                        <div class="summary-card">
                            <h3>平均チーム規模</h3>
                            <div class="value">${(totalTeamSize / projects.length).toFixed(1)}人</div>
                        </div>
                    `
                    
                    summaryDiv.style.display = 'grid'
                }

                function displayProjectData(projects) {
                    const dataDiv = document.getElementById('projectData')
                    
                    if (projects.length === 0) {
                        dataDiv.innerHTML = '<p>条件に一致するプロジェクトが見つかりません。</p>'
                        return
                    }

                    let html = ''
                    
                    projects.forEach(project => {
                        const statusClass = project.status === '進行中' ? 'status-progress' : 
                                           project.status === '完了' ? 'status-completed' : 'status-planned'
                        
                        html += `
                            <div class="project-card">
                                <div class="project-header">
                                    <div class="project-name">${project.project_name}</div>
                                    <div class="project-code">${project.project_code}</div>
                                </div>
                                <div class="project-details">
                                    <div class="detail-item">
                                        <span class="detail-label">アカウント:</span> 
                                        ${project.account_name} (${project.account_code})
                                    </div>
                                    <div class="detail-item">
                                        <span class="detail-label">契約形態:</span> 
                                        ${project.contract_form}
                                    </div>
                                    <div class="detail-item">
                                        <span class="detail-label">ステータス:</span> 
                                        <span class="status-badge ${statusClass}">${project.status}</span>
                                    </div>
                                    <div class="detail-item">
                                        <span class="detail-label">期間:</span> 
                                        ${project.start_date} ～ ${project.end_date}
                                    </div>
                                    <div class="detail-item">
                                        <span class="detail-label">マネージャー:</span> 
                                        ${project.manager_name}
                                    </div>
                                    <div class="detail-item">
                                        <span class="detail-label">チーム規模:</span> 
                                        ${project.team_size}人
                                    </div>
                                    <div class="detail-item">
                                        <span class="detail-label">予算:</span> 
                                        ¥${project.budget.toLocaleString()}
                                    </div>
                                    <div class="detail-item" style="grid-column: 1 / -1;">
                                        <span class="detail-label">概要:</span> 
                                        ${project.description}
                                    </div>
                                </div>
                            </div>
                        `
                    })
                    
                    dataDiv.innerHTML = html
                }

                function displayPagination() {
                    const paginationDiv = document.getElementById('pagination')
                    
                    if (totalPages <= 1) {
                        paginationDiv.style.display = 'none'
                        return
                    }

                    let html = ''
                    
                    // Previous button
                    html += `<button onclick="loadProjectData(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>← 前</button>`
                    
                    // Page numbers
                    for (let i = 1; i <= totalPages; i++) {
                        if (i === currentPage) {
                            html += `<button class="current" disabled>${i}</button>`
                        } else {
                            html += `<button onclick="loadProjectData(${i})">${i}</button>`
                        }
                    }
                    
                    // Next button
                    html += `<button onclick="loadProjectData(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>次 →</button>`
                    
                    paginationDiv.innerHTML = html
                    paginationDiv.style.display = 'block'
                }

                // ページ読み込み時にデータを取得
                window.onload = () => loadProjectData(1)
            </script>
        </body>
    </html>
    """
    )


@router.get("/users", response_model=UserListResponse)
def get_users(
    page: int = Query(1, description="ページ番号", ge=1),
    per_page: int = Query(10, description="1ページあたりの項目数", ge=1, le=100),
    team: Optional[str] = Query(None, description="チーム名"),
    user_type: Optional[str] = Query(None, description="ユーザータイプ")
):
    """
    ユーザーデータ取得API
    メンバーリストを取得して返却します
    """
    logger.info(f"User data requested - page: {page}, per_page: {per_page}, team: {team}, user_type: {user_type}")
    
    try:
        # デモ用のサンプルユーザーデータ
        demo_users = [
            {
                "user_id": 1,
                "user_code": "U001",
                "user_name": "田中太郎",
                "user_team": "開発チーム",
                "user_type": "GENERAL"
            },
            {
                "user_id": 2,
                "user_code": "U002",
                "user_name": "佐藤花子",
                "user_team": "開発チーム",
                "user_type": "MANAGER"
            },
            {
                "user_id": 3,
                "user_code": "U003",
                "user_name": "鈴木次郎",
                "user_team": "テストチーム",
                "user_type": "GENERAL"
            },
            {
                "user_id": 4,
                "user_code": "U004",
                "user_name": "高橋三郎",
                "user_team": "インフラチーム",
                "user_type": "MANAGER"
            },
            {
                "user_id": 5,
                "user_code": "U005",
                "user_name": "山田五郎",
                "user_team": "セキュリティチーム",
                "user_type": "GENERAL"
            },
            {
                "user_id": 6,
                "user_code": "U006",
                "user_name": "松本六郎",
                "user_team": "AIチーム",
                "user_type": "MANAGER"
            },
            {
                "user_id": 7,
                "user_code": "U007",
                "user_name": "渡辺七子",
                "user_team": "開発チーム",
                "user_type": "GENERAL"
            },
            {
                "user_id": 8,
                "user_code": "U008",
                "user_name": "伊藤八郎",
                "user_team": "テストチーム",
                "user_type": "GENERAL"
            },
            {
                "user_id": 9,
                "user_code": "U009",
                "user_name": "加藤九子",
                "user_team": "デザインチーム",
                "user_type": "GENERAL"
            },
            {
                "user_id": 10,
                "user_code": "U010",
                "user_name": "吉田十郎",
                "user_team": "営業チーム",
                "user_type": "MANAGER"
            }
        ]
        
        # フィルタリング処理
        filtered_users = demo_users
        
        if team:
            filtered_users = [u for u in filtered_users if u["user_team"] == team]
            logger.info(f"Filtered by team '{team}': {len(filtered_users)} users")
        
        if user_type:
            filtered_users = [u for u in filtered_users if u["user_type"] == user_type]
            logger.info(f"Filtered by user_type '{user_type}': {len(filtered_users)} users")
        
        # ページネーション処理
        total_count = len(filtered_users)
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paged_users = filtered_users[start_index:end_index]
        
        return UserListResponse(
            users=paged_users,
            total_count=total_count,
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        logger.error(f"Error retrieving user data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user data: {str(e)}")


@router.get("/users/{user_id}", response_model=UserData)
def get_user(user_id: int):
    """
    ユーザー詳細取得API
    指定されたIDのユーザー詳細を取得します
    """
    logger.info(f"User detail requested for ID: {user_id}")
    
    try:
        # デモ用のサンプルユーザーデータ（上記と同じデータを使用）
        demo_users = [
            {
                "user_id": 1,
                "user_code": "U001",
                "user_name": "田中太郎",
                "user_team": "開発チーム",
                "user_type": "GENERAL"
            },
            {
                "user_id": 2,
                "user_code": "U002",
                "user_name": "佐藤花子",
                "user_team": "開発チーム",
                "user_type": "MANAGER"
            },
            {
                "user_id": 3,
                "user_code": "U003",
                "user_name": "鈴木次郎",
                "user_team": "テストチーム",
                "user_type": "GENERAL"
            },
            {
                "user_id": 4,
                "user_code": "U004",
                "user_name": "高橋三郎",
                "user_team": "インフラチーム",
                "user_type": "MANAGER"
            },
            {
                "user_id": 5,
                "user_code": "U005",
                "user_name": "山田五郎",
                "user_team": "セキュリティチーム",
                "user_type": "GENERAL"
            },
            {
                "user_id": 6,
                "user_code": "U006",
                "user_name": "松本六郎",
                "user_team": "AIチーム",
                "user_type": "MANAGER"
            },
            {
                "user_id": 7,
                "user_code": "U007",
                "user_name": "渡辺七子",
                "user_team": "開発チーム",
                "user_type": "GENERAL"
            },
            {
                "user_id": 8,
                "user_code": "U008",
                "user_name": "伊藤八郎",
                "user_team": "テストチーム",
                "user_type": "GENERAL"
            },
            {
                "user_id": 9,
                "user_code": "U009",
                "user_name": "加藤九子",
                "user_team": "デザインチーム",
                "user_type": "GENERAL"
            },
            {
                "user_id": 10,
                "user_code": "U010",
                "user_name": "吉田十郎",
                "user_team": "営業チーム",
                "user_type": "MANAGER"
            }
        ]
        
        # 指定されたIDのユーザーを検索
        user = next((u for u in demo_users if u["user_id"] == user_id), None)
        
        if not user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        
        return UserData(**user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user detail: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user detail: {str(e)}")


@router.get("/users/view")
def users_view():
    """ユーザーデータ表示用のWebビュー"""
    return HTMLResponse(
        content="""
    <html>
        <head>
            <title>👥 ユーザーデータ</title>
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
                .back-link { 
                    display: inline-block; 
                    margin-bottom: 20px; 
                    color: #007acc; 
                    text-decoration: none; 
                }
                .back-link:hover { 
                    text-decoration: underline; 
                }
                .controls { 
                    margin-bottom: 20px; 
                    padding: 15px; 
                    background-color: #f8f9fa; 
                    border-radius: 6px; 
                }
                .form-group { 
                    display: inline-block; 
                    margin-right: 15px; 
                }
                .form-group label { 
                    display: block; 
                    margin-bottom: 5px; 
                    font-weight: bold; 
                    color: #333; 
                }
                .form-group select, .form-group input { 
                    padding: 8px; 
                    border: 2px solid #ddd; 
                    border-radius: 4px; 
                    font-size: 14px; 
                }
                .btn { 
                    background-color: #007acc; 
                    color: white; 
                    padding: 10px 20px; 
                    border: none; 
                    border-radius: 6px; 
                    cursor: pointer; 
                    font-size: 14px; 
                    margin-right: 10px; 
                }
                .btn:hover { 
                    background-color: #005a9e; 
                }
                .pagination { 
                    margin: 20px 0; 
                    text-align: center; 
                }
                .pagination button { 
                    background-color: #007acc; 
                    color: white; 
                    padding: 8px 16px; 
                    border: none; 
                    border-radius: 4px; 
                    cursor: pointer; 
                    margin: 0 5px; 
                }
                .pagination button:hover { 
                    background-color: #005a9e; 
                }
                .pagination button:disabled { 
                    background-color: #ccc; 
                    cursor: not-allowed; 
                }
                .pagination .current { 
                    background-color: #005a9e; 
                }
                .user-card { 
                    border: 1px solid #ddd; 
                    border-radius: 6px; 
                    padding: 15px; 
                    margin: 10px 0; 
                    background-color: #f9f9f9; 
                    display: flex; 
                    justify-content: space-between; 
                    align-items: center; 
                }
                .user-card:hover { 
                    background-color: #e3f2fd; 
                }
                .user-info { 
                    flex: 1; 
                }
                .user-name { 
                    font-size: 18px; 
                    font-weight: bold; 
                    color: #007acc; 
                    margin-bottom: 5px; 
                }
                .user-code { 
                    background-color: #6c757d; 
                    color: white; 
                    padding: 4px 8px; 
                    border-radius: 4px; 
                    font-size: 12px; 
                    margin-right: 10px; 
                }
                .user-team { 
                    background-color: #28a745; 
                    color: white; 
                    padding: 4px 8px; 
                    border-radius: 4px; 
                    font-size: 12px; 
                    margin-right: 10px; 
                }
                .user-type { 
                    padding: 4px 8px; 
                    border-radius: 4px; 
                    font-size: 12px; 
                    font-weight: bold; 
                }
                .type-manager { 
                    background-color: #dc3545; 
                    color: white; 
                }
                .type-general { 
                    background-color: #17a2b8; 
                    color: white; 
                }
                .loading { 
                    text-align: center; 
                    color: #666; 
                    padding: 20px; 
                }
                .error { 
                    background-color: #f8d7da; 
                    border: 1px solid #f5c6cb; 
                    color: #721c24; 
                    padding: 15px; 
                    border-radius: 6px; 
                    margin: 20px 0; 
                }
                .success { 
                    background-color: #d4edda; 
                    border: 1px solid #c3e6cb; 
                    color: #155724; 
                    padding: 15px; 
                    border-radius: 6px; 
                    margin: 20px 0; 
                }
                .summary { 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                    gap: 15px; 
                    margin-bottom: 20px; 
                }
                .summary-card { 
                    background-color: #f8f9fa; 
                    padding: 15px; 
                    border-radius: 6px; 
                    text-align: center; 
                }
                .summary-card h3 { 
                    margin: 0 0 10px 0; 
                    color: #007acc; 
                }
                .summary-card .value { 
                    font-size: 24px; 
                    font-weight: bold; 
                    color: #333; 
                }
                .team-list { 
                    display: flex; 
                    flex-wrap: wrap; 
                    gap: 5px; 
                }
                .team-tag { 
                    background-color: #007acc; 
                    color: white; 
                    padding: 2px 6px; 
                    border-radius: 3px; 
                    font-size: 10px; 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/" class="back-link">← ホームに戻る</a>
                <h1>👥 Assign-Kun ユーザーデータ</h1>
                
                <div class="controls">
                    <div class="form-group">
                        <label for="teamFilter">チーム:</label>
                        <select id="teamFilter">
                            <option value="">全てのチーム</option>
                            <option value="開発チーム">開発チーム</option>
                            <option value="テストチーム">テストチーム</option>
                            <option value="インフラチーム">インフラチーム</option>
                            <option value="セキュリティチーム">セキュリティチーム</option>
                            <option value="AIチーム">AIチーム</option>
                            <option value="デザインチーム">デザインチーム</option>
                            <option value="営業チーム">営業チーム</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="typeFilter">ユーザータイプ:</label>
                        <select id="typeFilter">
                            <option value="">全てのタイプ</option>
                            <option value="MANAGER">マネージャー</option>
                            <option value="GENERAL">一般</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="perPageSelect">表示件数:</label>
                        <select id="perPageSelect">
                            <option value="5">5件</option>
                            <option value="10" selected>10件</option>
                            <option value="20">20件</option>
                        </select>
                    </div>
                    
                    <button class="btn" onclick="loadUserData()">🔄 データ更新</button>
                </div>
                
                <div id="summary" class="summary" style="display: none;"></div>
                
                <div id="userData">
                    <div class="loading">データを読み込み中...</div>
                </div>
                
                <div id="pagination" class="pagination" style="display: none;"></div>
            </div>

            <script>
                let currentData = []
                let currentPage = 1
                let totalPages = 1
                let totalCount = 0

                function showMessage(message, isSuccess = true) {
                    const messageDiv = document.createElement('div')
                    messageDiv.className = isSuccess ? 'success' : 'error'
                    messageDiv.innerHTML = message
                    
                    const container = document.querySelector('.container')
                    const existingMessage = container.querySelector('.success, .error')
                    if (existingMessage) {
                        existingMessage.remove()
                    }
                    
                    container.insertBefore(messageDiv, container.querySelector('#summary'))
                    
                    setTimeout(() => {
                        messageDiv.remove()
                    }, 5000)
                }

                async function loadUserData(page = 1) {
                    const dataDiv = document.getElementById('userData')
                    const summaryDiv = document.getElementById('summary')
                    const paginationDiv = document.getElementById('pagination')
                    
                    dataDiv.innerHTML = '<div class="loading">データを読み込み中...</div>'
                    summaryDiv.style.display = 'none'
                    paginationDiv.style.display = 'none'

                    try {
                        const teamFilter = document.getElementById('teamFilter').value
                        const typeFilter = document.getElementById('typeFilter').value
                        const perPage = document.getElementById('perPageSelect').value
                        
                        let url = `/assign-kun/users?page=${page}&per_page=${perPage}`
                        if (teamFilter) url += `&team=${encodeURIComponent(teamFilter)}`
                        if (typeFilter) url += `&user_type=${encodeURIComponent(typeFilter)}`
                        
                        const response = await fetch(url)
                        if (response.ok) {
                            const data = await response.json()
                            currentData = data.users
                            currentPage = data.page
                            totalCount = data.total_count
                            totalPages = Math.ceil(totalCount / data.per_page)
                            
                            displayUserData(data.users)
                            displaySummary(data.users)
                            displayPagination()
                            showMessage(`✅ ユーザーデータを正常に読み込みました (${totalCount}件中 ${data.users.length}件を表示)`)
                        } else {
                            const error = await response.json()
                            dataDiv.innerHTML = `<div class="error">エラー: ${error.detail}</div>`
                            showMessage(`エラー: ${error.detail}`, false)
                        }
                    } catch (error) {
                        dataDiv.innerHTML = `<div class="error">エラー: ${error.message}</div>`
                        showMessage(`エラー: ${error.message}`, false)
                    }
                }

                function displaySummary(users) {
                    const summaryDiv = document.getElementById('summary')
                    
                    if (users.length === 0) {
                        summaryDiv.style.display = 'none'
                        return
                    }

                    const teamCounts = {}
                    const typeCounts = {}
                    
                    users.forEach(user => {
                        teamCounts[user.user_team] = (teamCounts[user.user_team] || 0) + 1
                        typeCounts[user.user_type] = (typeCounts[user.user_type] || 0) + 1
                    })

                    const uniqueTeams = Object.keys(teamCounts)
                    const managerCount = typeCounts['MANAGER'] || 0
                    const generalCount = typeCounts['GENERAL'] || 0

                    summaryDiv.innerHTML = `
                        <div class="summary-card">
                            <h3>ユーザー総数</h3>
                            <div class="value">${totalCount}</div>
                        </div>
                        <div class="summary-card">
                            <h3>表示中</h3>
                            <div class="value">${users.length}</div>
                        </div>
                        <div class="summary-card">
                            <h3>チーム数</h3>
                            <div class="value">${uniqueTeams.length}</div>
                        </div>
                        <div class="summary-card">
                            <h3>マネージャー / 一般</h3>
                            <div class="value">${managerCount} / ${generalCount}</div>
                        </div>
                    `
                    
                    summaryDiv.style.display = 'grid'
                }

                function displayUserData(users) {
                    const dataDiv = document.getElementById('userData')
                    
                    if (users.length === 0) {
                        dataDiv.innerHTML = '<p>条件に一致するユーザーが見つかりません。</p>'
                        return
                    }

                    let html = ''
                    
                    users.forEach(user => {
                        const typeClass = user.user_type === 'MANAGER' ? 'type-manager' : 'type-general'
                        const typeText = user.user_type === 'MANAGER' ? 'マネージャー' : '一般'
                        
                        html += `
                            <div class="user-card">
                                <div class="user-info">
                                    <div class="user-name">${user.user_name}</div>
                                    <div>
                                        <span class="user-code">${user.user_code}</span>
                                        <span class="user-team">${user.user_team}</span>
                                        <span class="user-type ${typeClass}">${typeText}</span>
                                    </div>
                                </div>
                            </div>
                        `
                    })
                    
                    dataDiv.innerHTML = html
                }

                function displayPagination() {
                    const paginationDiv = document.getElementById('pagination')
                    
                    if (totalPages <= 1) {
                        paginationDiv.style.display = 'none'
                        return
                    }

                    let html = ''
                    
                    // Previous button
                    html += `<button onclick="loadUserData(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>← 前</button>`
                    
                    // Page numbers
                    for (let i = 1; i <= totalPages; i++) {
                        if (i === currentPage) {
                            html += `<button class="current" disabled>${i}</button>`
                        } else {
                            html += `<button onclick="loadUserData(${i})">${i}</button>`
                        }
                    }
                    
                    // Next button
                    html += `<button onclick="loadUserData(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>次 →</button>`
                    
                    paginationDiv.innerHTML = html
                    paginationDiv.style.display = 'block'
                }

                // ページ読み込み時にデータを取得
                window.onload = () => loadUserData(1)
            </script>
        </body>
    </html>
    """
    )

