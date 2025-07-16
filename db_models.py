"""
SQLAlchemy データベースモデル定義

このモジュールは以下のテーブルモデルを定義します：
- User: ユーザー情報
- Project: プロジェクト情報
- Assignment: 課題情報
- Notice: 通知情報
- BlobLog: Blob ログ情報
- Histogram: ヒストグラム情報
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func


# ==============================================================================
# Base クラス
# ==============================================================================


class Base(DeclarativeBase):
    """SQLAlchemy 2.0対応のベースクラス"""

    pass


# ==============================================================================
# データベースモデル
# ==============================================================================


class User(Base):
    """ユーザーテーブル"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="ユーザー名")
    email = Column(String(100), unique=True, index=True, comment="メールアドレス")
    score = Column(Integer, default=0, comment="スコア")
    created_at = Column(DateTime, default=func.now(), comment="作成日時")
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), comment="更新日時"
    )

    # リレーション
    notices = relationship("Notice", back_populates="user")
    blob_logs = relationship("BlobLog", back_populates="user")


class Project(Base):
    """プロジェクトテーブル"""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="プロジェクト名")
    description = Column(Text, comment="説明")
    score = Column(Integer, default=0, comment="スコア")
    created_at = Column(DateTime, default=func.now(), comment="作成日時")
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), comment="更新日時"
    )

    # リレーション
    assignments = relationship("Assignment", back_populates="project")


class Assignment(Base):
    """課題テーブル"""

    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="課題名")
    description = Column(Text, comment="説明")
    project_id = Column(
        Integer, ForeignKey("projects.id"), nullable=False, comment="プロジェクトID"
    )
    difficulty_level = Column(String(20), nullable=False, comment="難易度")
    max_score = Column(Integer, default=100, comment="最大スコア")
    is_active = Column(Boolean, default=True, comment="有効フラグ")
    created_at = Column(DateTime, default=func.now(), comment="作成日時")
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), comment="更新日時"
    )

    # リレーション
    project = relationship("Project", back_populates="assignments")


class Notice(Base):
    """通知テーブル"""

    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="タイトル")
    content = Column(Text, nullable=False, comment="内容")
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, comment="ユーザーID"
    )
    is_read = Column(Boolean, default=False, comment="読了フラグ")
    priority = Column(String(20), default="normal", comment="優先度")
    created_at = Column(DateTime, default=func.now(), comment="作成日時")
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), comment="更新日時"
    )

    # リレーション
    user = relationship("User", back_populates="notices")


class BlobLog(Base):
    """Blob ログテーブル"""

    __tablename__ = "blob_logs"

    id = Column(Integer, primary_key=True, index=True)
    operation_type = Column(String(50), nullable=False, comment="操作タイプ")
    container_name = Column(String(100), nullable=False, comment="コンテナ名")
    blob_name = Column(String(500), nullable=False, comment="Blob名")
    file_size = Column(Integer, comment="ファイルサイズ")
    content_type = Column(String(100), comment="コンテンツタイプ")
    status = Column(String(20), nullable=False, comment="ステータス")
    user_id = Column(Integer, ForeignKey("users.id"), comment="ユーザーID")
    error_message = Column(Text, comment="エラーメッセージ")
    operation_time = Column(DateTime, default=func.now(), comment="操作時間")

    # リレーション
    user = relationship("User", back_populates="blob_logs")


class Histogram(Base):
    """ヒストグラムテーブル"""

    __tablename__ = "histograms"

    id = Column(Integer, primary_key=True, index=True)
    resource_type = Column(String(50), nullable=False, comment="リソースタイプ")
    resource_id = Column(Integer, nullable=False, comment="リソースID")
    bin_label = Column(String(100), nullable=False, comment="ビンラベル")
    bin_value = Column(Integer, nullable=False, comment="ビン値")
    count = Column(Integer, nullable=False, comment="カウント")
    percentage = Column(String(10), comment="パーセンテージ")
    additional_data = Column(JSON, comment="追加データ")
    created_at = Column(DateTime, default=func.now(), comment="作成日時")
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), comment="更新日時"
    )
