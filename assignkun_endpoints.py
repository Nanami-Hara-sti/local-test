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