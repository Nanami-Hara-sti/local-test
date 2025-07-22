"""
SQLAlchemy データベースモデル定義

このモジュールは以下のテーブルモデルを定義します：
- User: ユーザー情報
- Project: プロジェクト情報
- Assignment: 課題情報
- Notice: 通知情報
- BlobLog: Blob ログ情報
- Histogram: ヒストグラム情報
- AssignData: アサインデータ情報
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
    DECIMAL,
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


class AssignData(Base):
    """アサインデータテーブル"""

    __tablename__ = "assign_data"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100), nullable=False, comment="ユーザー名")
    assin_execution = Column(DECIMAL(10, 2), default=0.0, comment="実行アサイン")
    assin_maintenance = Column(DECIMAL(10, 2), default=0.0, comment="保守アサイン")
    assin_prospect = Column(DECIMAL(10, 2), default=0.0, comment="見込みアサイン")
    assin_common_cost = Column(DECIMAL(10, 2), default=0.0, comment="共通費アサイン")
    assin_most_com_ps = Column(DECIMAL(10, 2), default=0.0, comment="最も共通PS")
    assin_sales_mane = Column(DECIMAL(10, 2), default=0.0, comment="営業管理")
    assin_investigation = Column(DECIMAL(10, 2), default=0.0, comment="調査")
    assin_project_code = Column(Integer, nullable=False, comment="プロジェクトコード")
    assin_directly = Column(DECIMAL(10, 2), default=0.0, comment="直接")
    assin_common = Column(DECIMAL(10, 2), default=0.0, comment="共通")
    assin_sales_sup = Column(DECIMAL(10, 2), default=0.0, comment="営業支援")
    month_data = Column(JSON, comment="月ごとの合計データ")
    created_at = Column(DateTime, default=func.now(), comment="作成日時")
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), comment="更新日時"
    )


class HistogramData(Base):
    """ヒストグラムデータテーブル（Swagger準拠）"""

    __tablename__ = "histogram_data"

    id = Column(Integer, primary_key=True, index=True)
    histogram_ac_code = Column(String(30), nullable=False, comment="ACコード")
    histogram_ac_name = Column(String(100), nullable=False, comment="AC名称")
    histogram_pj_br_num = Column(String(30), nullable=False, comment="PJ枝番")
    histogram_pj_name = Column(String(100), nullable=False, comment="PJ名称")
    histogram_pj_contract_form = Column(
        String(30), nullable=False, comment="PJ契約形態"
    )
    histogram_costs_unit = Column(Integer, nullable=False, comment="工数単位")
    histogram_year = Column(Integer, nullable=False, comment="年")
    histogram_1month = Column(String(10), default="0.00", comment="1月")
    histogram_2month = Column(String(10), default="0.00", comment="2月")
    histogram_3month = Column(String(10), default="0.00", comment="3月")
    histogram_4month = Column(String(10), default="0.00", comment="4月")
    histogram_5month = Column(String(10), default="0.00", comment="5月")
    histogram_6month = Column(String(10), default="0.00", comment="6月")
    histogram_7month = Column(String(10), default="0.00", comment="7月")
    histogram_8month = Column(String(10), default="0.00", comment="8月")
    histogram_9month = Column(String(10), default="0.00", comment="9月")
    histogram_10month = Column(String(10), default="0.00", comment="10月")
    histogram_11month = Column(String(10), default="0.00", comment="11月")
    histogram_12month = Column(String(10), default="0.00", comment="12月")
    created_at = Column(DateTime, default=func.now(), comment="作成日時")
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), comment="更新日時"
    )


class ProjectData(Base):
    """プロジェクトデータテーブル（Swagger準拠）"""

    __tablename__ = "project_data"

    id = Column(Integer, primary_key=True, index=True)
    project_br_num = Column(
        String(30), nullable=False, unique=True, comment="PJコード枝番"
    )
    project_name = Column(String(100), nullable=False, comment="PJ名称")
    project_contract_form = Column(String(30), nullable=False, comment="PJ契約形態")
    project_sched_self = Column(String(20), nullable=False, comment="予定期間(自)")
    project_sched_to = Column(String(20), nullable=False, comment="予定期間(至)")
    project_type_name = Column(String(30), nullable=False, comment="PJタイプ名称")
    project_classification = Column(String(30), nullable=False, comment="PJ分類")
    project_budget_no = Column(String(30), nullable=False, comment="実行予算見積番号")
    project_valid_from = Column(String(20), comment="追加日")
    project_valid_to = Column(String(20), comment="有効期限")
    project_is_current = Column(Boolean, default=True, comment="現行PJフラグ")
    created_at = Column(DateTime, default=func.now(), comment="作成日時")
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), comment="更新日時"
    )


class UserData(Base):
    """ユーザーデータテーブル（Swagger準拠）"""

    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True, index=True)
    user_code = Column(
        String(30), nullable=False, unique=True, comment="ユーザーコード"
    )
    user_name = Column(String(30), nullable=False, comment="ユーザー名")
    user_team = Column(String(30), nullable=False, comment="所属チーム")
    user_type = Column(String(20), default="GENERAL", comment="ユーザータイプ")
    created_at = Column(DateTime, default=func.now(), comment="作成日時")
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), comment="更新日時"
    )
