"""
SQLAlchemy データベース接続管理

このモジュールはSQLAlchemy 2.0を使用してMySQLデータベースへの
非同期接続を管理します。
"""

import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import text
from db_models import Base


async def test_connection():
    """データベース接続をテスト"""
    try:
        # 環境変数からデータベース接続情報を取得
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "3306")
        db_name = os.getenv("DB_NAME", "assignkun_db")
        db_user = os.getenv("DB_USER", "assignkun")
        db_password = os.getenv("DB_PASSWORD", "assign")

        # MySQL接続URL (aiomysql使用)
        database_url = (
            f"mysql+aiomysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )

        # 一時的なエンジンを作成
        engine = create_async_engine(
            database_url,
            poolclass=NullPool,
            echo=False,
            pool_pre_ping=True,
        )

        # 接続テスト
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1 as test"))
            test_result = result.scalar()
            return test_result == 1

    except Exception as e:
        print(f"データベース接続エラー: {e}")
        return False
    finally:
        if "engine" in locals():
            await engine.dispose()


class DatabaseManager:
    """データベース接続管理クラス"""

    def __init__(self):
        self.engine = None
        self.async_session_maker = None
        self._initialized = False

    def initialize(self):
        """データベース接続の初期化"""
        if self._initialized:
            return

        # 環境変数からデータベース接続情報を取得
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "3306")
        db_name = os.getenv("DB_NAME", "assignkun_db")
        db_user = os.getenv("DB_USER", "assignkun")
        db_password = os.getenv("DB_PASSWORD", "assign")

        # MySQL接続URL (aiomysql使用)
        database_url = (
            f"mysql+aiomysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )

        # 非同期エンジンの作成
        self.engine = create_async_engine(
            database_url,
            poolclass=NullPool,  # Azure Functions用の設定
            echo=False,  # SQLログの出力 (開発時はTrueに設定)
            pool_pre_ping=True,  # 接続の健全性チェック
            pool_recycle=3600,  # 接続の再利用時間 (1時間)
        )

        # セッションメーカーの作成
        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        self._initialized = True

    async def create_tables(self):
        """テーブルの作成"""
        if not self._initialized:
            self.initialize()

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self):
        """テーブルの削除"""
        if not self._initialized:
            self.initialize()

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def get_session(self) -> AsyncSession:
        """非同期セッションの取得"""
        if not self._initialized:
            self.initialize()

        return self.async_session_maker()

    async def close(self):
        """データベース接続の終了"""
        if self.engine:
            await self.engine.dispose()


# グローバルなデータベースマネージャーインスタンス
db_manager = DatabaseManager()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI依存性注入用のデータベースセッション取得関数

    Yields:
        AsyncSession: 非同期データベースセッション
    """
    if not db_manager._initialized:
        db_manager.initialize()

    async with db_manager.async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """データベースの初期化"""
    await db_manager.create_tables()


async def close_db():
    """データベース接続の終了"""
    await db_manager.close()


# 互換性のためのエイリアス
async def get_database():
    """データベースセッションの取得 (互換性用)"""
    return await db_manager.get_session()


# init_database関数の追加（test_mysql.pyで使用）
async def init_database():
    """データベースの初期化 (test_mysql.py用)"""
    await db_manager.create_tables()
