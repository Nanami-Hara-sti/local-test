from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi.responses import HTMLResponse
import logging
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from models import (
    HistogramResponse,
    ProjectResponse,
    UserResponse,
)
from database import get_db
from db_crud import AssignDataCRUD
from db_models import AssignData

# ログ設定
logger = logging.getLogger(__name__)

# Assign-Kun API用のルーター
router = APIRouter()


@router.get("/assigns")
async def get_assign_data(
    month: Optional[int] = Query(
        None, description="基準月（指定月の前後1ヶ月分のデータを取得）", ge=1, le=12
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    ホーム画面アサインデータ取得API
    ホーム画面に必要なアサインデータを取得して返却します
    ユーザー名が同じデータについては、assin_total, assin_executionを集計します
    """
    logger.info(f"Assign data requested for month: {month}")

    try:
        # データベースからアサインデータを取得
        assign_data_list = await AssignDataCRUD.get_all_assign_data(db)

        # データがなければデモデータを使用して初期化
        if not assign_data_list:
            logger.info("No assign data found in database, initializing with demo data")
            # デモ用のサンプルアサインデータ
            demo_assigns = [
                {
                    "user_name": "田中太郎",
                    "assin_execution": 120.0,
                    "assin_maintenance": 20.0,
                    "assin_prospect": 10.0,
                    "assin_common_cost": 5.0,
                    "assin_most_com_ps": 3.0,
                    "assin_sales_mane": 2.0,
                    "assin_investigation": 0.0,
                    "month_totals": {
                        "previous_month": {"month": 4, "total_assin": 150.5},
                        "current_month": {"month": 5, "total_assin": 160.0},
                        "next_month": {"month": 6, "total_assin": 155.8},
                    },
                    "assin_project_code": 1,
                    "assin_directly": 140.0,
                    "assin_common": 15.0,
                    "assin_sales_sup": 5.0,
                },
                {
                    "user_name": "田中太郎",  # 同じユーザーの別プロジェクト
                    "assin_execution": 80.0,
                    "assin_maintenance": 10.0,
                    "assin_prospect": 5.0,
                    "assin_common_cost": 2.0,
                    "assin_most_com_ps": 1.0,
                    "assin_sales_mane": 1.0,
                    "assin_investigation": 0.0,
                    "month_totals": {
                        "previous_month": {"month": 4, "total_assin": 90.5},
                        "current_month": {"month": 5, "total_assin": 99.0},
                        "next_month": {"month": 6, "total_assin": 95.8},
                    },
                    "assin_project_code": 2,
                    "assin_directly": 90.0,
                    "assin_common": 8.0,
                    "assin_sales_sup": 2.0,
                },
            ]

            # デモデータをデータベースに保存
            for assign in demo_assigns:
                # JSON形式の月別データを作成
                month_data = {
                    "previous_month": assign["month_totals"]["previous_month"],
                    "current_month": assign["month_totals"]["current_month"],
                    "next_month": assign["month_totals"]["next_month"],
                }

                # データベースに保存
                await AssignDataCRUD.create_assign_data(
                    db,
                    user_name=assign["user_name"],
                    assin_execution=assign["assin_execution"],
                    assin_maintenance=assign["assin_maintenance"],
                    assin_prospect=assign["assin_prospect"],
                    assin_common_cost=assign["assin_common_cost"],
                    assin_most_com_ps=assign["assin_most_com_ps"],
                    assin_sales_mane=assign["assin_sales_mane"],
                    assin_investigation=assign["assin_investigation"],
                    assin_project_code=assign["assin_project_code"],
                    assin_directly=assign["assin_directly"],
                    assin_common=assign["assin_common"],
                    assin_sales_sup=assign["assin_sales_sup"],
                    month_data=month_data,
                )

            # 保存後に再取得
            assign_data_list = await AssignDataCRUD.get_all_assign_data(db)

        # データベースから取得したデータをdict形式に変換
        assigns = []
        for data in assign_data_list:
            assign = {
                "user_name": data.user_name,
                "assin_execution": float(data.assin_execution),
                "assin_maintenance": float(data.assin_maintenance),
                "assin_prospect": float(data.assin_prospect),
                "assin_common_cost": float(data.assin_common_cost),
                "assin_most_com_ps": float(data.assin_most_com_ps),
                "assin_sales_mane": float(data.assin_sales_mane),
                "assin_investigation": float(data.assin_investigation),
                "assin_project_code": data.assin_project_code,
                "assin_directly": float(data.assin_directly),
                "assin_common": float(data.assin_common),
                "assin_sales_sup": float(data.assin_sales_sup),
                "month_totals": data.month_data,
            }
            assigns.append(assign)

        # ユーザー名でグループ化して集計
        user_totals = {}
        for assign in assigns:
            user_name = assign["user_name"]
            if user_name not in user_totals:
                user_totals[user_name] = {
                    "user_name": user_name,
                    "assin_execution_total": 0.0,
                    "assin_maintenance_total": 0.0,
                    "assin_prospect_total": 0.0,
                    "assin_common_cost_total": 0.0,
                    "assin_most_com_ps_total": 0.0,
                    "assin_sales_mane_total": 0.0,
                    "assin_investigation_total": 0.0,
                    "assin_directly_total": 0.0,
                    "assin_common_total": 0.0,
                    "assin_sales_sup_total": 0.0,
                    "month_totals": {
                        "previous_month": {"month": 0, "total_assin": 0.0},
                        "current_month": {"month": 0, "total_assin": 0.0},
                        "next_month": {"month": 0, "total_assin": 0.0},
                    },
                    "projects": [],  # プロジェクトごとの詳細を保存
                }

            totals = user_totals[user_name]
            totals["assin_execution_total"] += assign["assin_execution"]
            totals["assin_maintenance_total"] += assign["assin_maintenance"]
            totals["assin_prospect_total"] += assign["assin_prospect"]
            totals["assin_common_cost_total"] += assign["assin_common_cost"]
            totals["assin_most_com_ps_total"] += assign["assin_most_com_ps"]
            totals["assin_sales_mane_total"] += assign["assin_sales_mane"]
            totals["assin_investigation_total"] += assign["assin_investigation"]
            totals["assin_directly_total"] += assign["assin_directly"]
            totals["assin_common_total"] += assign["assin_common"]
            totals["assin_sales_sup_total"] += assign["assin_sales_sup"]

            # プロジェクトごとの詳細を保存
            totals["projects"].append(
                {
                    "assin_project_code": assign["assin_project_code"],
                    "assin_execution": assign["assin_execution"],
                    "assin_directly": assign["assin_directly"],
                }
            )

        # 集計結果をリストに変換
        aggregated_assigns = list(user_totals.values())

        return {"assigns": aggregated_assigns, "total_users": len(aggregated_assigns)}

    except Exception as e:
        logger.error(f"Error retrieving assign data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve assign data: {str(e)}"
        )


@router.get("/histograms", response_model=list[HistogramResponse])
def get_histograms(
    month: Optional[int] = Query(
        None, description="基準月（指定月のデータを取得）", ge=1, le=12
    )
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
                    "histogram_12month": 1.4,
                },
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
                    "histogram_12month": 0.8,
                },
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
                    "histogram_12month": 2.3,
                },
            },
        ]

        # 月指定がある場合のフィルタリング（デモでは全データを返す）
        if month:
            logger.info(f"Filtering data for month: {month}")
            # 実際の実装では、指定月のデータをフィルタリング

        return demo_histograms

    except Exception as e:
        logger.error(f"Error retrieving histogram data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve histogram data: {str(e)}"
        )


@router.get("/projects", response_model=list[ProjectResponse])
def get_projects():
    """
    プロジェクトデータ取得API
    プロジェクト一覧を取得して返却します
    """
    logger.info("Project data requested")

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
                "project_budget_no": "B2025001",
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
                "project_budget_no": "B2025002",
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
                "project_budget_no": "B2025003",
            },
        ]

        return demo_projects

    except Exception as e:
        logger.error(f"Error retrieving project data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve project data: {str(e)}"
        )


@router.get("/users", response_model=list[UserResponse])
def get_users():
    """
    ユーザーデータ取得API
    メンバーリストを取得して返却します
    """
    logger.info("User data requested")

    try:
        # デモ用のサンプルユーザーデータ
        demo_users = [
            {
                "user_id": 1,
                "user_code": "U001",
                "user_name": "田中太郎",
                "user_team": "開発チーム",
                "user_type": "GENERAL",
            },
            {
                "user_id": 2,
                "user_code": "U002",
                "user_name": "佐藤花子",
                "user_team": "開発チーム",
                "user_type": "GENERAL",
            },
            {
                "user_id": 3,
                "user_code": "U003",
                "user_name": "鈴木次郎",
                "user_team": "テストチーム",
                "user_type": "GENERAL",
            },
        ]

        return demo_users

    except Exception as e:
        logger.error(f"Error retrieving user data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve user data: {str(e)}"
        )


@router.get("/informations")
def get_information(
    month: int = Query(
        ..., description="基準月（前後1ヶ月分の合計値を取得）", ge=1, le=12
    ),
    year: Optional[int] = Query(None, description="対象年", ge=1900, le=2100),
):
    """
    情報表示画面API
    総計情報を取得します
    """
    logger.info(f"Information data requested for month: {month}, year: {year}")

    try:
        if year is None:
            year = 2025

        # デモ用のサンプル総計データ
        demo_data = {
            "base_month": month,
            "target_year": year,
            "month_totals": {
                "previous_month": {
                    "month": month - 1 if month > 1 else 12,
                    "total_amount": 1250.75,
                },
                "current_month": {"month": month, "total_amount": 1400.50},
                "next_month": {
                    "month": month + 1 if month < 12 else 1,
                    "total_amount": 1325.25,
                },
            },
            "totals": [
                {
                    "total_year": str(year),
                    "total_month": month,
                    "total_execution": 800.0,
                    "total_maintenance": 150.0,
                    "total_prospect": 100.0,
                    "total_common_cost": 50.0,
                    "total_most_com_ps": 30.0,
                    "total_sales_mane": 20.0,
                    "total_investigation": 10.0,
                    "total_directly": 900.0,
                    "total_common": 180.0,
                    "total_sales_sup": 25.0,
                }
            ],
        }

        return demo_data

    except Exception as e:
        logger.error(f"Error retrieving information data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve information data: {str(e)}"
        )


@router.get("/notices", response_model=dict)
def get_notices(
    page: int = Query(1, description="ページ番号", ge=1),
    limit: int = Query(20, description="1ページあたりの件数", ge=1, le=100),
):
    """
    通知一覧取得API
    ユーザーの通知一覧を取得します
    """
    logger.info(f"Notice data requested - page: {page}, limit: {limit}")

    try:
        # デモ用のサンプル通知データ
        demo_notices = [
            {
                "notice_time": "2025-07-08T10:00:00Z",
                "user_name": "田中太郎",
                "notice_text": "プロジェクトPJ001の工事進行基準が達成されました",
                "project_name": "Webシステム開発",
                "notice_type": "工事進行基準案件",
            },
            {
                "notice_time": "2025-07-08T09:30:00Z",
                "user_name": "佐藤花子",
                "notice_text": "システムメンテナンスが完了しました",
                "project_name": None,
                "notice_type": "システムメンテナンス",
            },
            {
                "notice_time": "2025-07-08T09:00:00Z",
                "user_name": "鈴木次郎",
                "notice_text": "データ更新が完了しました",
                "project_name": "データ分析システム",
                "notice_type": "データ更新",
            },
        ]

        # ページネーション処理
        total_count = len(demo_notices)
        start_index = (page - 1) * limit
        end_index = start_index + limit
        paged_notices = demo_notices[start_index:end_index]

        return {
            "notice": paged_notices,
            "pagination": {
                "current_page": page,
                "total_pages": (total_count + limit - 1) // limit,
                "total_count": total_count,
                "limit": limit,
                "has_next": end_index < total_count,
                "has_previous": page > 1,
            },
        }

    except Exception as e:
        logger.error(f"Error retrieving notice data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve notice data: {str(e)}"
        )


@router.get("/", response_class=HTMLResponse)
def get_home():
    """
    ホーム画面
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Assign-Kun API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            h1 { color: #333; }
            .endpoint { margin: 20px 0; padding: 15px; background: #f5f5f5; border-radius: 5px; }
            .method { font-weight: bold; color: #007bff; }
            .url { font-family: monospace; background: #fff; padding: 5px; border-radius: 3px; }
            .description { margin-top: 10px; color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Assign-Kun API</h1>
            <p>アサインメント管理システムのAPI</p>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="url">/assigns</div>
                <div class="description">ホーム画面アサインデータ取得</div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="url">/histograms</div>
                <div class="description">ヒストグラムデータ取得</div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="url">/projects</div>
                <div class="description">プロジェクトデータ取得</div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="url">/users</div>
                <div class="description">ユーザーデータ取得</div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="url">/notices</div>
                <div class="description">通知一覧取得</div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="url">/informations</div>
                <div class="description">情報表示画面データ取得</div>
            </div>
        </div>
    </body>
    </html>
    """
