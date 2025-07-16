"""
MySQL データベース API エンドポイント

このモジュールは以下のAPIエンドポイントを提供します：
- Users: ユーザー管理
- Projects: プロジェクト管理
- Assignments: 課題管理
- Notices: 通知管理
- BlobLogs: Blob ログ管理
- Histograms: ヒストグラム管理
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from db_crud import (
    UserCRUD,
    ProjectCRUD,
    AssignmentCRUD,
    NoticeCRUD,
    HistogramCRUD,
)
from models import (
    UserCreate,
    UserResponse,
    UserUpdate,
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
    AssignmentCreate,
    AssignmentResponse,
    NoticeCreate,
    NoticeResponse,
    HistogramCreate,
    HistogramResponse,
    HistogramStatsResponse,
)
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# ==============================================================================
# ユーザー関連エンドポイント
# ==============================================================================


@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """ユーザーを作成"""
    try:
        # ユーザー名の重複チェック
        existing_user = await UserCRUD.get_user_by_name(db, user.name)
        if existing_user:
            raise HTTPException(status_code=400, detail="ユーザー名が既に存在します")

        new_user = await UserCRUD.create_user(
            db=db, name=user.name, email=user.email, score=user.score or 0
        )
        return new_user
    except Exception as e:
        logger.error(f"ユーザー作成エラー: {e}")
        raise HTTPException(status_code=500, detail="ユーザー作成に失敗しました")


@router.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """ユーザー一覧を取得"""
    try:
        users = await UserCRUD.get_users(db, skip=skip, limit=limit)
        return users
    except Exception as e:
        logger.error(f"ユーザー一覧取得エラー: {e}")
        raise HTTPException(status_code=500, detail="ユーザー一覧取得に失敗しました")


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """ユーザーを取得"""
    try:
        user = await UserCRUD.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
        return user
    except Exception as e:
        logger.error(f"ユーザー取得エラー: {e}")
        raise HTTPException(status_code=500, detail="ユーザー取得に失敗しました")


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)
):
    """ユーザーを更新"""
    try:
        updated_user = await UserCRUD.update_user(
            db, user_id, **user.dict(exclude_unset=True)
        )
        if not updated_user:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
        return updated_user
    except Exception as e:
        logger.error(f"ユーザー更新エラー: {e}")
        raise HTTPException(status_code=500, detail="ユーザー更新に失敗しました")


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """ユーザーを削除"""
    try:
        deleted = await UserCRUD.delete_user(db, user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
        return {"message": "ユーザーが削除されました"}
    except Exception as e:
        logger.error(f"ユーザー削除エラー: {e}")
        raise HTTPException(status_code=500, detail="ユーザー削除に失敗しました")


# ==============================================================================
# プロジェクト関連エンドポイント
# ==============================================================================


@router.post("/projects", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    """プロジェクトを作成"""
    try:
        new_project = await ProjectCRUD.create_project(
            db=db,
            name=project.name,
            description=project.description,
            score=project.score or 0,
        )
        return new_project
    except Exception as e:
        logger.error(f"プロジェクト作成エラー: {e}")
        raise HTTPException(status_code=500, detail="プロジェクト作成に失敗しました")


@router.get("/projects", response_model=List[ProjectResponse])
async def get_projects(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """プロジェクト一覧を取得"""
    try:
        projects = await ProjectCRUD.get_projects(db, skip=skip, limit=limit)
        return projects
    except Exception as e:
        logger.error(f"プロジェクト一覧取得エラー: {e}")
        raise HTTPException(
            status_code=500, detail="プロジェクト一覧取得に失敗しました"
        )


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    """プロジェクトを取得"""
    try:
        project = await ProjectCRUD.get_project_by_id(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="プロジェクトが見つかりません")
        return project
    except Exception as e:
        logger.error(f"プロジェクト取得エラー: {e}")
        raise HTTPException(status_code=500, detail="プロジェクト取得に失敗しました")


@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int, project: ProjectUpdate, db: AsyncSession = Depends(get_db)
):
    """プロジェクトを更新"""
    try:
        updated_project = await ProjectCRUD.update_project(
            db, project_id, **project.dict(exclude_unset=True)
        )
        if not updated_project:
            raise HTTPException(status_code=404, detail="プロジェクトが見つかりません")
        return updated_project
    except Exception as e:
        logger.error(f"プロジェクト更新エラー: {e}")
        raise HTTPException(status_code=500, detail="プロジェクト更新に失敗しました")


@router.delete("/projects/{project_id}")
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    """プロジェクトを削除"""
    try:
        deleted = await ProjectCRUD.delete_project(db, project_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="プロジェクトが見つかりません")
        return {"message": "プロジェクトが削除されました"}
    except Exception as e:
        logger.error(f"プロジェクト削除エラー: {e}")
        raise HTTPException(status_code=500, detail="プロジェクト削除に失敗しました")


# ==============================================================================
# 課題関連エンドポイント
# ==============================================================================


@router.post("/assignments", response_model=AssignmentResponse)
async def create_assignment(
    assignment: AssignmentCreate, db: AsyncSession = Depends(get_db)
):
    """課題を作成"""
    try:
        new_assignment = await AssignmentCRUD.create_assignment(
            db=db, **assignment.dict()
        )
        return new_assignment
    except Exception as e:
        logger.error(f"課題作成エラー: {e}")
        raise HTTPException(status_code=500, detail="課題作成に失敗しました")


@router.get("/assignments", response_model=List[AssignmentResponse])
async def get_assignments(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """課題一覧を取得"""
    try:
        assignments = await AssignmentCRUD.get_assignments(db, skip=skip, limit=limit)
        return assignments
    except Exception as e:
        logger.error(f"課題一覧取得エラー: {e}")
        raise HTTPException(status_code=500, detail="課題一覧取得に失敗しました")


@router.get("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment(assignment_id: int, db: AsyncSession = Depends(get_db)):
    """課題を取得"""
    try:
        assignment = await AssignmentCRUD.get_assignment_by_id(db, assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="課題が見つかりません")
        return assignment
    except Exception as e:
        logger.error(f"課題取得エラー: {e}")
        raise HTTPException(status_code=500, detail="課題取得に失敗しました")


# ==============================================================================
# 通知関連エンドポイント
# ==============================================================================


@router.post("/notices", response_model=NoticeResponse)
async def create_notice(notice: NoticeCreate, db: AsyncSession = Depends(get_db)):
    """通知を作成"""
    try:
        new_notice = await NoticeCRUD.create_notice(db=db, **notice.dict())
        return new_notice
    except Exception as e:
        logger.error(f"通知作成エラー: {e}")
        raise HTTPException(status_code=500, detail="通知作成に失敗しました")


@router.get("/notices", response_model=List[NoticeResponse])
async def get_notices(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """通知一覧を取得"""
    try:
        notices = await NoticeCRUD.get_notices(db, skip=skip, limit=limit)
        return notices
    except Exception as e:
        logger.error(f"通知一覧取得エラー: {e}")
        raise HTTPException(status_code=500, detail="通知一覧取得に失敗しました")


# ==============================================================================
# ヒストグラム関連エンドポイント
# ==============================================================================


@router.post("/histograms", response_model=HistogramResponse)
async def create_histogram(
    histogram: HistogramCreate, db: AsyncSession = Depends(get_db)
):
    """ヒストグラムを作成"""
    try:
        new_histogram = await HistogramCRUD.create_histogram(db=db, **histogram.dict())
        return new_histogram
    except Exception as e:
        logger.error(f"ヒストグラム作成エラー: {e}")
        raise HTTPException(status_code=500, detail="ヒストグラム作成に失敗しました")


@router.get("/histograms", response_model=List[HistogramResponse])
async def get_histograms(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """ヒストグラム一覧を取得"""
    try:
        histograms = await HistogramCRUD.get_histograms(db, skip=skip, limit=limit)
        return histograms
    except Exception as e:
        logger.error(f"ヒストグラム一覧取得エラー: {e}")
        raise HTTPException(
            status_code=500, detail="ヒストグラム一覧取得に失敗しました"
        )


@router.get("/histograms/{histogram_id}", response_model=HistogramResponse)
async def get_histogram(histogram_id: int, db: AsyncSession = Depends(get_db)):
    """ヒストグラムを取得"""
    try:
        histogram = await HistogramCRUD.get_histogram_by_id(db, histogram_id)
        if not histogram:
            raise HTTPException(status_code=404, detail="ヒストグラムが見つかりません")
        return histogram
    except Exception as e:
        logger.error(f"ヒストグラム取得エラー: {e}")
        raise HTTPException(status_code=500, detail="ヒストグラム取得に失敗しました")


@router.get(
    "/histograms/resource/{resource_type}/{resource_id}",
    response_model=HistogramStatsResponse,
)
async def get_histogram_stats(
    resource_type: str, resource_id: int, db: AsyncSession = Depends(get_db)
):
    """リソース別ヒストグラム統計を取得"""
    try:
        stats = await HistogramCRUD.get_histogram_stats(db, resource_type, resource_id)
        return stats
    except Exception as e:
        logger.error(f"ヒストグラム統計取得エラー: {e}")
        raise HTTPException(
            status_code=500, detail="ヒストグラム統計取得に失敗しました"
        )
