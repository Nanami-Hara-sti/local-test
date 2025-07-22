#!/usr/bin/env python3
"""
MySQLデータベース接続テストスクリプト
"""

import asyncio
import sys
import os
import logging

# 現在のディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import test_connection, db_manager, init_database
from sqlalchemy import text

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 環境変数設定
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "3306"
os.environ["DB_NAME"] = "assignkun_db"
os.environ["DB_USER"] = "assignkun"
os.environ["DB_PASSWORD"] = "assign"


async def test_database_operations():
    """データベース操作のテスト"""

    # 接続テスト
    logger.info("=== データベース接続テスト ===")
    if await test_connection():
        logger.info("✅ データベース接続成功")
    else:
        logger.error("❌ データベース接続失敗")
        return False

    # データベース初期化
    logger.info("=== データベース初期化 ===")
    try:
        await init_database()
        logger.info("✅ データベース初期化成功")
    except Exception as e:
        logger.error(f"❌ データベース初期化失敗: {e}")
        return False

    # CRUD操作テスト
    logger.info("=== CRUD操作テスト ===")
    try:
        # データベースセッションを使用したテスト
        db_manager.initialize()
        async with db_manager.async_session_maker() as session:

            # 簡単なクエリテスト
            result = await session.execute(text("SELECT 1 as test"))
            test_result = result.scalar()
            logger.info(f"✅ 基本クエリテスト成功: {test_result}")

            # テーブル確認
            result = await session.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            table_names = [table[0] for table in tables]
            logger.info(f"✅ テーブル一覧取得成功: {table_names}")

    except Exception as e:
        logger.error(f"❌ CRUD操作テスト失敗: {e}")
        return False

    # 接続終了
    logger.info("=== 接続終了 ===")
    await db_manager.close()
    logger.info("✅ 接続終了成功")

    return True


async def main():
    """メイン関数"""
    logger.info("🚀 MySQLデータベーステスト開始")

    success = await test_database_operations()

    if success:
        logger.info("🎉 すべてのテストが成功しました！")
        return 0
    else:
        logger.error("💥 テストに失敗しました")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
