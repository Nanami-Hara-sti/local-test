from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import HTMLResponse
import logging
from datetime import datetime
from typing import Optional
from models import (
    Histogram, HistogramArray, Project, ProjectArray, User, UserArray, 
    Notice, NoticeArray, NotificationCreateRequest, Assin, AssinArray, 
    Total, TotalArray, MonthTotals
)

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


@router.get("/projects", response_model=ProjectArray)
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
                "project_br_num": "PJ001",
                "project_name": "Webシステム開発",
                "project_contract_form": "請負",
                "project_sched_self": "2025-01-01",
                "project_sched_to": "2025-12-31",
                "project_type_name": "システム開発",
                "project_classification": "新規開発",
                "project_budget_no": "B2025001"
            },
            {
                "project_id": 2,
                "project_br_num": "PJ002",
                "project_name": "データ分析システム",
                "project_contract_form": "派遣",
                "project_sched_self": "2025-02-01",
                "project_sched_to": "2025-08-31",
                "project_type_name": "データ分析",
                "project_classification": "新規開発",
                "project_budget_no": "B2025002"
            },
            {
                "project_id": 3,
                "project_br_num": "PJ003",
                "project_name": "モバイルアプリ開発",
                "project_contract_form": "請負",
                "project_sched_self": "2025-03-01",
                "project_sched_to": "2025-09-30",
                "project_type_name": "アプリ開発",
                "project_classification": "新規開発",
                "project_budget_no": "B2025003"
            }
        # フィルタリング処理
        filtered_projects = demo_projects
        
        # 月指定がある場合のフィルタリング（デモでは全データを返す）
        if month:
            logger.info(f"Filtering data for month: {month}")
            # 実際の実装では、指定月のプロジェクトをフィルタリング
        
        return demo_projects
        
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


@router.get("/Noticess", response_model=NoticesListResponse)
def get_Noticess(
    page: int = Query(1, description="ページ番号", ge=1),
    per_page: int = Query(10, description="1ページあたりの項目数", ge=1, le=100),
    Notices_type: Optional[str] = Query(None, description="通知タイプ"),
    priority: Optional[str] = Query(None, description="優先度"),
    is_read: Optional[bool] = Query(None, description="読み取り状態"),
    category: Optional[str] = Query(None, description="カテゴリー")
):
    """
    通知一覧取得API
    通知リストを取得して返却します
    """
    logger.info(f"Notices data requested - page: {page}, per_page: {per_page}, type: {Notices_type}, priority: {priority}")
    
    try:
        # デモ用のサンプル通知データ
        demo_Noticess = [
            {
                "Notices_id": 1,
                "title": "プロジェクト開始通知",
                "message": "プロジェクト「Webアプリケーション開発」が開始されました。",
                "Notices_type": "INFO",
                "priority": "MEDIUM",
                "sender": "system",
                "recipient": "U001",
                "is_read": False,
                "created_at": "2025-07-15T09:00:00+09:00",
                "read_at": None,
                "related_project_id": 1,
                "related_user_id": 1,
                "category": "PROJECT"
            },
            {
                "Notices_id": 2,
                "title": "締切リマインダー",
                "message": "プロジェクト「データ分析システム」の中間報告締切が近づいています。",
                "Notices_type": "WARNING",
                "priority": "HIGH",
                "sender": "system",
                "recipient": "U002",
                "is_read": True,
                "created_at": "2025-07-14T15:30:00+09:00",
                "read_at": "2025-07-14T16:00:00+09:00",
                "related_project_id": 2,
                "related_user_id": 2,
                "category": "DEADLINE"
            },
            {
                "Notices_id": 3,
                "title": "システムメンテナンス",
                "message": "7月20日21:00-23:00にシステムメンテナンスを実施します。",
                "Notices_type": "INFO",
                "priority": "LOW",
                "sender": "admin",
                "recipient": "ALL",
                "is_read": False,
                "created_at": "2025-07-13T10:00:00+09:00",
                "read_at": None,
                "related_project_id": None,
                "related_user_id": None,
                "category": "SYSTEM"
            },
            {
                "Notices_id": 4,
                "title": "タスク完了",
                "message": "タスク「データベース設計」が完了しました。",
                "Notices_type": "SUCCESS",
                "priority": "MEDIUM",
                "sender": "U003",
                "recipient": "U004",
                "is_read": False,
                "created_at": "2025-07-12T14:20:00+09:00",
                "read_at": None,
                "related_project_id": 3,
                "related_user_id": 3,
                "category": "TASK"
            },
            {
                "Notices_id": 5,
                "title": "エラー発生",
                "message": "プロジェクト「インフラ構築」でエラーが発生しました。確認してください。",
                "Notices_type": "ERROR",
                "priority": "HIGH",
                "sender": "system",
                "recipient": "U004",
                "is_read": True,
                "created_at": "2025-07-11T11:15:00+09:00",
                "read_at": "2025-07-11T11:30:00+09:00",
                "related_project_id": 4,
                "related_user_id": 4,
                "category": "ERROR"
            },
            {
                "Notices_id": 6,
                "title": "新メンバー参加",
                "message": "新しいメンバーが「AIチーム」に参加しました。",
                "Notices_type": "INFO",
                "priority": "LOW",
                "sender": "HR",
                "recipient": "U006",
                "is_read": False,
                "created_at": "2025-07-10T09:45:00+09:00",
                "read_at": None,
                "related_project_id": None,
                "related_user_id": 11,
                "category": "TEAM"
            },
            {
                "Notices_id": 7,
                "title": "予算承認",
                "message": "プロジェクト「セキュリティ強化」の予算が承認されました。",
                "Notices_type": "SUCCESS",
                "priority": "MEDIUM",
                "sender": "finance",
                "recipient": "U005",
                "is_read": False,
                "created_at": "2025-07-09T16:00:00+09:00",
                "read_at": None,
                "related_project_id": 5,
                "related_user_id": 5,
                "category": "BUDGET"
            },
            {
                "Notices_id": 8,
                "title": "会議招集",
                "message": "7月18日14:00から週次定例会議を開催します。",
                "Notices_type": "INFO",
                "priority": "MEDIUM",
                "sender": "U002",
                "recipient": "TEAM",
                "is_read": True,
                "created_at": "2025-07-08T12:00:00+09:00",
                "read_at": "2025-07-08T12:30:00+09:00",
                "related_project_id": None,
                "related_user_id": None,
                "category": "MEETING"
            },
            {
                "Notices_id": 9,
                "title": "リリース完了",
                "message": "プロジェクト「モバイルアプリ開発」のベータ版がリリースされました。",
                "Notices_type": "SUCCESS",
                "priority": "HIGH",
                "sender": "U003",
                "recipient": "ALL",
                "is_read": False,
                "created_at": "2025-07-07T18:30:00+09:00",
                "read_at": None,
                "related_project_id": 3,
                "related_user_id": 3,
                "category": "RELEASE"
            },
            {
                "Notices_id": 10,
                "title": "パフォーマンス警告",
                "message": "システムのパフォーマンスが低下しています。調査が必要です。",
                "Notices_type": "WARNING",
                "priority": "HIGH",
                "sender": "monitoring",
                "recipient": "U004",
                "is_read": False,
                "created_at": "2025-07-06T22:45:00+09:00",
                "read_at": None,
                "related_project_id": None,
                "related_user_id": None,
                "category": "MONITORING"
            }
        ]
        
        # フィルタリング処理
        filtered_Noticess = demo_Noticess
        
        if Notices_type:
            filtered_Noticess = [n for n in filtered_Noticess if n["Notices_type"] == Notices_type]
            logger.info(f"Filtered by Notices_type '{Notices_type}': {len(filtered_Noticess)} Noticess")
        
        if priority:
            filtered_Noticess = [n for n in filtered_Noticess if n["priority"] == priority]
            logger.info(f"Filtered by priority '{priority}': {len(filtered_Noticess)} Noticess")
        
        if is_read is not None:
            filtered_Noticess = [n for n in filtered_Noticess if n["is_read"] == is_read]
            logger.info(f"Filtered by is_read '{is_read}': {len(filtered_Noticess)} Noticess")
            
        if category:
            filtered_Noticess = [n for n in filtered_Noticess if n["category"] == category]
            logger.info(f"Filtered by category '{category}': {len(filtered_Noticess)} Noticess")
        
        # ページネーション処理
        total_count = len(filtered_Noticess)
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paged_Noticess = filtered_Noticess[start_index:end_index]
        
        # 未読通知数を計算
        unread_count = len([n for n in demo_Noticess if not n["is_read"]])
        
        return NoticesListResponse(
            Noticess=paged_Noticess,
            total_count=total_count,
            page=page,
            per_page=per_page,
            unread_count=unread_count
        )
        
    except Exception as e:
        logger.error(f"Error retrieving Notices data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve Notices data: {str(e)}")


@router.get("/Noticess/{Notices_id}", response_model=NoticesData)
def get_Notices(Notices_id: int):
    """
    通知詳細取得API
    指定されたIDの通知詳細を取得します
    """
    logger.info(f"Notices detail requested for ID: {Notices_id}")
    
    try:
        # デモ用のサンプル通知データ（上記と同じデータを使用）
        demo_Noticess = [
            {
                "Notices_id": 1,
                "title": "プロジェクト開始通知",
                "message": "プロジェクト「Webアプリケーション開発」が開始されました。",
                "Notices_type": "INFO",
                "priority": "MEDIUM",
                "sender": "system",
                "recipient": "U001",
                "is_read": False,
                "created_at": "2025-07-15T09:00:00+09:00",
                "read_at": None,
                "related_project_id": 1,
                "related_user_id": 1,
                "category": "PROJECT"
            },
            {
                "Notices_id": 2,
                "title": "締切リマインダー",
                "message": "プロジェクト「データ分析システム」の中間報告締切が近づいています。",
                "Notices_type": "WARNING",
                "priority": "HIGH",
                "sender": "system",
                "recipient": "U002",
                "is_read": True,
                "created_at": "2025-07-14T15:30:00+09:00",
                "read_at": "2025-07-14T16:00:00+09:00",
                "related_project_id": 2,
                "related_user_id": 2,
                "category": "DEADLINE"
            },
            {
                "Notices_id": 3,
                "title": "システムメンテナンス",
                "message": "7月20日21:00-23:00にシステムメンテナンスを実施します。",
                "Notices_type": "INFO",
                "priority": "LOW",
                "sender": "admin",
                "recipient": "ALL",
                "is_read": False,
                "created_at": "2025-07-13T10:00:00+09:00",
                "read_at": None,
                "related_project_id": None,
                "related_user_id": None,
                "category": "SYSTEM"
            },
            {
                "Notices_id": 4,
                "title": "タスク完了",
                "message": "タスク「データベース設計」が完了しました。",
                "Notices_type": "SUCCESS",
                "priority": "MEDIUM",
                "sender": "U003",
                "recipient": "U004",
                "is_read": False,
                "created_at": "2025-07-12T14:20:00+09:00",
                "read_at": None,
                "related_project_id": 3,
                "related_user_id": 3,
                "category": "TASK"
            },
            {
                "Notices_id": 5,
                "title": "エラー発生",
                "message": "プロジェクト「インフラ構築」でエラーが発生しました。確認してください。",
                "Notices_type": "ERROR",
                "priority": "HIGH",
                "sender": "system",
                "recipient": "U004",
                "is_read": True,
                "created_at": "2025-07-11T11:15:00+09:00",
                "read_at": "2025-07-11T11:30:00+09:00",
                "related_project_id": 4,
                "related_user_id": 4,
                "category": "ERROR"
            },
            {
                "Notices_id": 6,
                "title": "新メンバー参加",
                "message": "新しいメンバーが「AIチーム」に参加しました。",
                "Notices_type": "INFO",
                "priority": "LOW",
                "sender": "HR",
                "recipient": "U006",
                "is_read": False,
                "created_at": "2025-07-10T09:45:00+09:00",
                "read_at": None,
                "related_project_id": None,
                "related_user_id": 11,
                "category": "TEAM"
            },
            {
                "Notices_id": 7,
                "title": "予算承認",
                "message": "プロジェクト「セキュリティ強化」の予算が承認されました。",
                "Notices_type": "SUCCESS",
                "priority": "MEDIUM",
                "sender": "finance",
                "recipient": "U005",
                "is_read": False,
                "created_at": "2025-07-09T16:00:00+09:00",
                "read_at": None,
                "related_project_id": 5,
                "related_user_id": 5,
                "category": "BUDGET"
            },
            {
                "Notices_id": 8,
                "title": "会議招集",
                "message": "7月18日14:00から週次定例会議を開催します。",
                "Notices_type": "INFO",
                "priority": "MEDIUM",
                "sender": "U002",
                "recipient": "TEAM",
                "is_read": True,
                "created_at": "2025-07-08T12:00:00+09:00",
                "read_at": "2025-07-08T12:30:00+09:00",
                "related_project_id": None,
                "related_user_id": None,
                "category": "MEETING"
            },
            {
                "Notices_id": 9,
                "title": "リリース完了",
                "message": "プロジェクト「モバイルアプリ開発」のベータ版がリリースされました。",
                "Notices_type": "SUCCESS",
                "priority": "HIGH",
                "sender": "U003",
                "recipient": "ALL",
                "is_read": False,
                "created_at": "2025-07-07T18:30:00+09:00",
                "read_at": None,
                "related_project_id": 3,
                "related_user_id": 3,
                "category": "RELEASE"
            },
            {
                "Notices_id": 10,
                "title": "パフォーマンス警告",
                "message": "システムのパフォーマンスが低下しています。調査が必要です。",
                "Notices_type": "WARNING",
                "priority": "HIGH",
                "sender": "monitoring",
                "recipient": "U004",
                "is_read": False,
                "created_at": "2025-07-06T22:45:00+09:00",
                "read_at": None,
                "related_project_id": None,
                "related_user_id": None,
                "category": "MONITORING"
            }
        ]
        
        # 指定されたIDの通知を検索
        Notices = next((n for n in demo_Noticess if n["Notices_id"] == Notices_id), None)
        
        if not Notices:
            raise HTTPException(status_code=404, detail=f"Notices with ID {Notices_id} not found")
        
        return NoticesData(**Notices)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving Notices detail: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve Notices detail: {str(e)}")


@router.get("/Noticess/view")
def Noticess_view():
    """通知データ表示用のWebビュー"""
    return HTMLResponse(
        content="""
    <html>
        <head>
            <title>🔔 通知一覧</title>
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
                .Notices-card { 
                    border: 1px solid #ddd; 
                    border-radius: 6px; 
                    padding: 15px; 
                    margin: 10px 0; 
                    background-color: #f9f9f9; 
                    position: relative; 
                }
                .Notices-card:hover { 
                    background-color: #e3f2fd; 
                }
                .Notices-card.unread { 
                    border-left: 4px solid #007acc; 
                    background-color: #f0f8ff; 
                }
                .Notices-header { 
                    display: flex; 
                    justify-content: space-between; 
                    align-items: center; 
                    margin-bottom: 10px; 
                }
                .Notices-title { 
                    font-size: 16px; 
                    font-weight: bold; 
                    color: #333; 
                }
                .Notices-meta { 
                    font-size: 12px; 
                    color: #666; 
                }
                .Notices-type { 
                    padding: 4px 8px; 
                    border-radius: 4px; 
                    font-size: 11px; 
                    font-weight: bold; 
                    margin-right: 10px; 
                }
                .type-info { 
                    background-color: #17a2b8; 
                    color: white; 
                }
                .type-warning { 
                    background-color: #ffc107; 
                    color: black; 
                }
                .type-error { 
                    background-color: #dc3545; 
                    color: white; 
                }
                .type-success { 
                    background-color: #28a745; 
                    color: white; 
                }
                .priority-badge { 
                    padding: 3px 6px; 
                    border-radius: 3px; 
                    font-size: 10px; 
                    font-weight: bold; 
                }
                .priority-low { 
                    background-color: #6c757d; 
                    color: white; 
                }
                .priority-medium { 
                    background-color: #fd7e14; 
                    color: white; 
                }
                .priority-high { 
                    background-color: #dc3545; 
                    color: white; 
                }
                .Notices-message { 
                    margin: 10px 0; 
                    line-height: 1.4; 
                }
                .Notices-footer { 
                    display: flex; 
                    justify-content: space-between; 
                    align-items: center; 
                    margin-top: 10px; 
                    font-size: 12px; 
                    color: #666; 
                }
                .unread-badge { 
                    background-color: #007acc; 
                    color: white; 
                    padding: 2px 6px; 
                    border-radius: 10px; 
                    font-size: 10px; 
                    font-weight: bold; 
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
                .category-badge { 
                    background-color: #e9ecef; 
                    color: #495057; 
                    padding: 2px 6px; 
                    border-radius: 3px; 
                    font-size: 10px; 
                    font-weight: bold; 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/" class="back-link">← ホームに戻る</a>
                <h1>🔔 Assign-Kun 通知一覧</h1>
                
                <div class="controls">
                    <div class="form-group">
                        <label for="typeFilter">通知タイプ:</label>
                        <select id="typeFilter">
                            <option value="">全てのタイプ</option>
                            <option value="INFO">情報</option>
                            <option value="WARNING">警告</option>
                            <option value="ERROR">エラー</option>
                            <option value="SUCCESS">成功</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="priorityFilter">優先度:</label>
                        <select id="priorityFilter">
                            <option value="">全ての優先度</option>
                            <option value="LOW">低</option>
                            <option value="MEDIUM">中</option>
                            <option value="HIGH">高</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="readFilter">読み取り状態:</label>
                        <select id="readFilter">
                            <option value="">全て</option>
                            <option value="false">未読</option>
                            <option value="true">既読</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="categoryFilter">カテゴリー:</label>
                        <select id="categoryFilter">
                            <option value="">全てのカテゴリー</option>
                            <option value="PROJECT">プロジェクト</option>
                            <option value="TASK">タスク</option>
                            <option value="DEADLINE">締切</option>
                            <option value="SYSTEM">システム</option>
                            <option value="TEAM">チーム</option>
                            <option value="MEETING">会議</option>
                            <option value="RELEASE">リリース</option>
                            <option value="ERROR">エラー</option>
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
                    
                    <button class="btn" onclick="loadNoticesData()">🔄 データ更新</button>
                </div>
                
                <div id="summary" class="summary" style="display: none;"></div>
                
                <div id="NoticesData">
                    <div class="loading">データを読み込み中...</div>
                </div>
                
                <div id="pagination" class="pagination" style="display: none;"></div>
            </div>

            <script>
                let currentData = []
                let currentPage = 1
                let totalPages = 1
                let totalCount = 0
                let unreadCount = 0

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

                async function loadNoticesData(page = 1) {
                    const dataDiv = document.getElementById('NoticesData')
                    const summaryDiv = document.getElementById('summary')
                    const paginationDiv = document.getElementById('pagination')
                    
                    dataDiv.innerHTML = '<div class="loading">データを読み込み中...</div>'
                    summaryDiv.style.display = 'none'
                    paginationDiv.style.display = 'none'

                    try {
                        const typeFilter = document.getElementById('typeFilter').value
                        const priorityFilter = document.getElementById('priorityFilter').value
                        const readFilter = document.getElementById('readFilter').value
                        const categoryFilter = document.getElementById('categoryFilter').value
                        const perPage = document.getElementById('perPageSelect').value
                        
                        let url = `/assign-kun/Noticess?page=${page}&per_page=${perPage}`
                        if (typeFilter) url += `&Notices_type=${encodeURIComponent(typeFilter)}`
                        if (priorityFilter) url += `&priority=${encodeURIComponent(priorityFilter)}`
                        if (readFilter) url += `&is_read=${readFilter}`
                        if (categoryFilter) url += `&category=${encodeURIComponent(categoryFilter)}`
                        
                        const response = await fetch(url)
                        if (response.ok) {
                            const data = await response.json()
                            currentData = data.Noticess
                            currentPage = data.page
                            totalCount = data.total_count
                            unreadCount = data.unread_count
                            totalPages = Math.ceil(totalCount / data.per_page)
                            
                            displayNoticesData(data.Noticess)
                            displaySummary(data.Noticess, data.unread_count)
                            displayPagination()
                            showMessage(`✅ 通知データを正常に読み込みました (${totalCount}件中 ${data.Noticess.length}件を表示)`)
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

                function displaySummary(Noticess, unreadCount) {
                    const summaryDiv = document.getElementById('summary')
                    
                    if (Noticess.length === 0) {
                        summaryDiv.style.display = 'none'
                        return
                    }

                    const typeCounts = {}
                    const priorityCounts = {}
                    
                    Noticess.forEach(Notices => {
                        typeCounts[Notices.Notices_type] = (typeCounts[Notices.Notices_type] || 0) + 1
                        priorityCounts[Notices.priority] = (priorityCounts[Notices.priority] || 0) + 1
                    })

                    const highPriorityCount = priorityCounts['HIGH'] || 0

                    summaryDiv.innerHTML = `
                        <div class="summary-card">
                            <h3>通知総数</h3>
                            <div class="value">${totalCount}</div>
                        </div>
                        <div class="summary-card">
                            <h3>未読通知</h3>
                            <div class="value">${unreadCount}</div>
                        </div>
                        <div class="summary-card">
                            <h3>高優先度</h3>
                            <div class="value">${highPriorityCount}</div>
                        </div>
                        <div class="summary-card">
                            <h3>表示中</h3>
                            <div class="value">${Noticess.length}</div>
                        </div>
                    `
                    
                    summaryDiv.style.display = 'grid'
                }

                function displayNoticesData(Noticess) {
                    const dataDiv = document.getElementById('NoticesData')
                    
                    if (Noticess.length === 0) {
                        dataDiv.innerHTML = '<p>条件に一致する通知が見つかりません。</p>'
                        return
                    }

                    let html = ''
                    
                    Noticess.forEach(Notices => {
                        const typeClass = `type-${Notices.Notices_type.toLowerCase()}`
                        const priorityClass = `priority-${Notices.priority.toLowerCase()}`
                        const unreadClass = !Notices.is_read ? 'unread' : ''
                        
                        const createdDate = new Date(Notices.created_at).toLocaleString('ja-JP')
                        const readDate = Notices.read_at ? new Date(Notices.read_at).toLocaleString('ja-JP') : null
                        
                        html += `
                            <div class="Notices-card ${unreadClass}">
                                <div class="Notices-header">
                                    <div class="Notices-title">${Notices.title}</div>
                                    <div class="Notices-meta">
                                        <span class="Notices-type ${typeClass}">${Notices.Notices_type}</span>
                                        <span class="priority-badge ${priorityClass}">${Notices.priority}</span>
                                        ${!Notices.is_read ? '<span class="unread-badge">未読</span>' : ''}
                                    </div>
                                </div>
                                <div class="Notices-message">${Notices.message}</div>
                                <div class="Notices-footer">
                                    <div>
                                        <span class="category-badge">${Notices.category || 'その他'}</span>
                                        <span>送信者: ${Notices.sender}</span>
                                    </div>
                                    <div>
                                        <div>作成: ${createdDate}</div>
                                        ${readDate ? `<div>読み取り: ${readDate}</div>` : ''}
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
                    html += `<button onclick="loadNoticesData(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>← 前</button>`
                    
                    // Page numbers
                    for (let i = 1; i <= totalPages; i++) {
                        if (i === currentPage) {
                            html += `<button class="current" disabled>${i}</button>`
                        } else {
                            html += `<button onclick="loadNoticesData(${i})">${i}</button>`
                        }
                    }
                    
                    // Next button
                    html += `<button onclick="loadNoticesData(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>次 →</button>`
                    
                    paginationDiv.innerHTML = html
                    paginationDiv.style.display = 'block'
                }

                // ページ読み込み時にデータを取得
                window.onload = () => loadNoticesData(1)
            </script>
        </body>
    </html>
    """
    )