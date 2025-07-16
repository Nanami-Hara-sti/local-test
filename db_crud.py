"""
データベース CRUD 操作

このモジュールは以下のデータベース操作クラスを提供します：
- UserCRUD: ユーザー操作
- ProjectCRUD: プロジェクト操作
- AssignmentCRUD: 課題操作
- NoticeCRUD: 通知操作
- BlobLogCRUD: Blob ログ操作
- HistogramCRUD: ヒストグラム操作
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db_models import User, Project, Assignment, Notice, BlobLog, Histogram
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


# ==============================================================================
# ユーザー操作クラス
# ==============================================================================


class UserCRUD:
    """ユーザー操作"""

    @staticmethod
    async def create_user(
        db: AsyncSession, name: str, email: str = None, score: int = 0
    ) -> User:
        """ユーザーを作成"""
        user = User(name=name, email=email, score=score)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """IDでユーザーを取得"""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_name(db: AsyncSession, name: str) -> Optional[User]:
        """ユーザー名でユーザーを取得"""
        result = await db.execute(select(User).where(User.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_users(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[User]:
        """ユーザー一覧を取得"""
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, **kwargs) -> Optional[User]:
        """ユーザーを更新"""
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            await db.commit()
            await db.refresh(user)
        return user

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        """ユーザーを削除"""
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            await db.delete(user)
            await db.commit()
            return True
        return False


# ==============================================================================
# プロジェクト操作クラス
# ==============================================================================


class ProjectCRUD:
    """プロジェクト操作"""

    @staticmethod
    async def create_project(
        db: AsyncSession, name: str, description: str = None, score: int = 0
    ) -> Project:
        """プロジェクトを作成"""
        project = Project(name=name, description=description, score=score)
        db.add(project)
        await db.commit()
        await db.refresh(project)
        return project

    @staticmethod
    async def get_project_by_id(db: AsyncSession, project_id: int) -> Optional[Project]:
        """IDでプロジェクトを取得"""
        result = await db.execute(
            select(Project)
            .options(selectinload(Project.assignments))
            .where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_project_by_name(db: AsyncSession, name: str) -> Optional[Project]:
        """プロジェクト名でプロジェクトを取得"""
        result = await db.execute(select(Project).where(Project.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_projects(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """プロジェクト一覧を取得"""
        result = await db.execute(
            select(Project)
            .options(selectinload(Project.assignments))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def update_project(
        db: AsyncSession, project_id: int, **kwargs
    ) -> Optional[Project]:
        """プロジェクトを更新"""
        result = await db.execute(select(Project).where(Project.id == project_id))
        project = result.scalar_one_or_none()
        if project:
            for key, value in kwargs.items():
                if hasattr(project, key):
                    setattr(project, key, value)
            await db.commit()
            await db.refresh(project)
        return project

    @staticmethod
    async def delete_project(db: AsyncSession, project_id: int) -> bool:
        """プロジェクトを削除"""
        result = await db.execute(select(Project).where(Project.id == project_id))
        project = result.scalar_one_or_none()
        if project:
            await db.delete(project)
            await db.commit()
            return True
        return False


class AssignmentCRUD:
    """課題操作"""

    @staticmethod
    async def create_assignment(db: AsyncSession, **kwargs) -> Assignment:
        """課題を作成"""
        assignment = Assignment(**kwargs)
        db.add(assignment)
        await db.commit()
        await db.refresh(assignment)
        return assignment

    @staticmethod
    async def get_assignment_by_id(
        db: AsyncSession, assignment_id: int
    ) -> Optional[Assignment]:
        """IDで課題を取得"""
        result = await db.execute(
            select(Assignment).where(Assignment.id == assignment_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_assignments(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Assignment]:
        """課題一覧を取得"""
        result = await db.execute(
            select(Assignment)
            .options(selectinload(Assignment.project))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_assignments_by_project(
        db: AsyncSession, project_id: int
    ) -> List[Assignment]:
        """プロジェクトIDで課題一覧を取得"""
        result = await db.execute(
            select(Assignment)
            .options(selectinload(Assignment.project))
            .where(Assignment.project_id == project_id)
        )
        return result.scalars().all()

    @staticmethod
    async def update_assignment(
        db: AsyncSession, assignment_id: int, **kwargs
    ) -> Optional[Assignment]:
        """課題を更新"""
        result = await db.execute(
            select(Assignment).where(Assignment.id == assignment_id)
        )
        assignment = result.scalar_one_or_none()
        if assignment:
            for key, value in kwargs.items():
                if hasattr(assignment, key):
                    setattr(assignment, key, value)
            await db.commit()
            await db.refresh(assignment)
        return assignment

    @staticmethod
    async def delete_assignment(db: AsyncSession, assignment_id: int) -> bool:
        """課題を削除"""
        result = await db.execute(
            select(Assignment).where(Assignment.id == assignment_id)
        )
        assignment = result.scalar_one_or_none()
        if assignment:
            await db.delete(assignment)
            await db.commit()
            return True
        return False


# ==============================================================================
# 通知操作クラス
# ==============================================================================


class NoticeCRUD:
    """通知操作"""

    @staticmethod
    async def create_notice(db: AsyncSession, **kwargs) -> Notice:
        """通知を作成"""
        notice = Notice(**kwargs)
        db.add(notice)
        await db.commit()
        await db.refresh(notice)
        return notice

    @staticmethod
    async def get_notice_by_id(db: AsyncSession, notice_id: int) -> Optional[Notice]:
        """IDで通知を取得"""
        result = await db.execute(select(Notice).where(Notice.id == notice_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_notices(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Notice]:
        """通知一覧を取得"""
        result = await db.execute(
            select(Notice)
            .options(selectinload(Notice.user))
            .order_by(Notice.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_unread_notices(db: AsyncSession, user_id: int = None) -> List[Notice]:
        """未読通知を取得"""
        query = select(Notice).where(Notice.is_read.is_(False))
        if user_id:
            query = query.where(Notice.user_id == user_id)
        query = query.order_by(Notice.created_at.desc())

        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def mark_as_read(db: AsyncSession, notice_id: int) -> bool:
        """通知を既読にする"""
        result = await db.execute(select(Notice).where(Notice.id == notice_id))
        notice = result.scalar_one_or_none()
        if notice:
            notice.is_read = True
            await db.commit()
            return True
        return False

    @staticmethod
    async def update_notice(
        db: AsyncSession, notice_id: int, **kwargs
    ) -> Optional[Notice]:
        """通知を更新"""
        result = await db.execute(select(Notice).where(Notice.id == notice_id))
        notice = result.scalar_one_or_none()
        if notice:
            for key, value in kwargs.items():
                if hasattr(notice, key):
                    setattr(notice, key, value)
            await db.commit()
            await db.refresh(notice)
        return notice

    @staticmethod
    async def delete_notice(db: AsyncSession, notice_id: int) -> bool:
        """通知を削除"""
        result = await db.execute(select(Notice).where(Notice.id == notice_id))
        notice = result.scalar_one_or_none()
        if notice:
            await db.delete(notice)
            await db.commit()
            return True
        return False


# ==============================================================================
# Blob ログ操作クラス
# ==============================================================================


class BlobLogCRUD:
    """Blobログ操作"""

    @staticmethod
    async def create_blob_log(db: AsyncSession, **kwargs) -> BlobLog:
        """Blobログを作成"""
        blob_log = BlobLog(**kwargs)
        db.add(blob_log)
        await db.commit()
        await db.refresh(blob_log)
        return blob_log

    @staticmethod
    async def get_blob_log_by_id(db: AsyncSession, log_id: int) -> Optional[BlobLog]:
        """IDでBlobログを取得"""
        result = await db.execute(select(BlobLog).where(BlobLog.id == log_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_blob_logs(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[BlobLog]:
        """Blobログ一覧を取得"""
        result = await db.execute(
            select(BlobLog)
            .options(selectinload(BlobLog.user))
            .order_by(BlobLog.operation_time.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_blob_logs_by_container(
        db: AsyncSession, container_name: str
    ) -> List[BlobLog]:
        """コンテナ名でBlobログを取得"""
        result = await db.execute(
            select(BlobLog)
            .where(BlobLog.container_name == container_name)
            .order_by(BlobLog.operation_time.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def update_blob_log(
        db: AsyncSession, log_id: int, **kwargs
    ) -> Optional[BlobLog]:
        """Blobログを更新"""
        result = await db.execute(select(BlobLog).where(BlobLog.id == log_id))
        blob_log = result.scalar_one_or_none()
        if blob_log:
            for key, value in kwargs.items():
                if hasattr(blob_log, key):
                    setattr(blob_log, key, value)
            await db.commit()
            await db.refresh(blob_log)
        return blob_log

    @staticmethod
    async def delete_blob_log(db: AsyncSession, log_id: int) -> bool:
        """Blobログを削除"""
        result = await db.execute(select(BlobLog).where(BlobLog.id == log_id))
        blob_log = result.scalar_one_or_none()
        if blob_log:
            await db.delete(blob_log)
            await db.commit()
            return True
        return False


# ==============================================================================
# ヒストグラム操作クラス
# ==============================================================================


class HistogramCRUD:
    """ヒストグラム操作"""

    @staticmethod
    async def create_histogram(db: AsyncSession, **kwargs) -> Histogram:
        """ヒストグラムを作成"""
        try:
            histogram = Histogram(**kwargs)
            db.add(histogram)
            await db.commit()
            await db.refresh(histogram)
            return histogram
        except Exception as e:
            await db.rollback()
            raise e

    @staticmethod
    async def get_histogram_by_id(
        db: AsyncSession, histogram_id: int
    ) -> Optional[Histogram]:
        """IDでヒストグラムを取得"""
        result = await db.execute(select(Histogram).where(Histogram.id == histogram_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_histograms(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Histogram]:
        """ヒストグラム一覧を取得"""
        result = await db.execute(
            select(Histogram)
            .order_by(Histogram.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_histograms_by_resource(
        db: AsyncSession, resource_type: str, resource_id: int
    ) -> List[Histogram]:
        """リソース別ヒストグラムを取得"""
        result = await db.execute(
            select(Histogram)
            .where(Histogram.resource_type == resource_type)
            .where(Histogram.resource_id == resource_id)
            .order_by(Histogram.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_histogram_stats(
        db: AsyncSession, resource_type: str, resource_id: int
    ):
        """ヒストグラム統計を取得"""
        histograms = await HistogramCRUD.get_histograms_by_resource(
            db, resource_type, resource_id
        )

        if not histograms:
            return None

        total_count = sum(h.count for h in histograms)
        bin_count = len(histograms)
        values = [h.bin_value for h in histograms]
        average_value = sum(values) / len(values) if values else 0
        min_value = min(values) if values else 0
        max_value = max(values) if values else 0

        return {
            "resource_type": resource_type,
            "resource_id": resource_id,
            "total_count": total_count,
            "bin_count": bin_count,
            "average_value": average_value,
            "min_value": min_value,
            "max_value": max_value,
            "histograms": histograms,
        }

    @staticmethod
    async def update_histogram(
        db: AsyncSession, histogram_id: int, **kwargs
    ) -> Optional[Histogram]:
        """ヒストグラムを更新"""
        try:
            result = await db.execute(
                select(Histogram).where(Histogram.id == histogram_id)
            )
            histogram = result.scalar_one_or_none()

            if histogram:
                for key, value in kwargs.items():
                    if hasattr(histogram, key):
                        setattr(histogram, key, value)
                await db.commit()
                await db.refresh(histogram)
                return histogram
            return None
        except Exception as e:
            await db.rollback()
            raise e

    @staticmethod
    async def delete_histogram(db: AsyncSession, histogram_id: int) -> bool:
        """ヒストグラムを削除"""
        try:
            result = await db.execute(
                select(Histogram).where(Histogram.id == histogram_id)
            )
            histogram = result.scalar_one_or_none()

            if histogram:
                await db.delete(histogram)
                await db.commit()
                return True
            return False
        except Exception as e:
            await db.rollback()
            raise e
