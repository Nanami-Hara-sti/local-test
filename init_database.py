#!/usr/bin/env python3
"""
データベーステーブル作成・初期化スクリプト
"""

import asyncio
import sys
import os
import logging

# 現在のディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import db_manager
from sqlalchemy import text

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Docker環境用のデータベース接続設定
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "3306"
os.environ["DB_NAME"] = "assignkun_db"
os.environ["DB_USER"] = "assignkun"
os.environ["DB_PASSWORD"] = "assign"


async def create_tables():
    """データベーステーブルを作成"""
    logger.info("=== データベーステーブル作成 ===")
    
    try:
        # データベースマネージャーを初期化
        db_manager.initialize()
        logger.info("✅ データベースマネージャー初期化完了")
        
        # テーブルを作成
        logger.info("テーブルを作成中...")
        await db_manager.create_tables()
        logger.info("✅ テーブル作成完了")
        
        # テーブル一覧を確認
        logger.info("作成されたテーブルを確認中...")
        async with db_manager.async_session_maker() as session:
            result = await session.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            table_names = [table[0] for table in tables]
            logger.info(f"✅ 作成されたテーブル: {table_names}")
            
            # 各テーブルの構造を確認
            for table_name in table_names:
                result = await session.execute(text(f"DESCRIBE {table_name}"))
                columns = result.fetchall()
                logger.info(f"📋 {table_name} テーブル構造:")
                for col in columns:
                    logger.info(f"  - {col[0]}: {col[1]} ({col[2]})")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ テーブル作成エラー: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await db_manager.close()


async def insert_sample_data():
    """サンプルデータを挿入"""
    logger.info("=== サンプルデータ挿入 ===")
    
    try:
        db_manager.initialize()
        
        async with db_manager.async_session_maker() as session:
            # ユーザーサンプルデータ
            from db_models import User, Project, Assignment, Notice
            
            # サンプルユーザーを作成
            user1 = User(name="テストユーザー1", email="test1@example.com", score=100)
            user2 = User(name="テストユーザー2", email="test2@example.com", score=150)
            
            session.add(user1)
            session.add(user2)
            await session.commit()
            await session.refresh(user1)
            await session.refresh(user2)
            
            # サンプルプロジェクトを作成
            project1 = Project(name="テストプロジェクト1", description="テスト用プロジェクト", score=200)
            project2 = Project(name="テストプロジェクト2", description="別のテストプロジェクト", score=300)
            
            session.add(project1)
            session.add(project2)
            await session.commit()
            await session.refresh(project1)
            await session.refresh(project2)
            
            # サンプル課題を作成
            assignment1 = Assignment(
                name="テスト課題1",
                description="テスト用の課題",
                project_id=project1.id,
                difficulty_level="easy",
                max_score=50
            )
            assignment2 = Assignment(
                name="テスト課題2",
                description="難しいテスト課題",
                project_id=project2.id,
                difficulty_level="hard",
                max_score=100
            )
            
            session.add(assignment1)
            session.add(assignment2)
            await session.commit()
            
            # サンプル通知を作成
            notice1 = Notice(
                title="テスト通知1",
                content="これはテスト通知です",
                user_id=user1.id,
                priority="normal"
            )
            notice2 = Notice(
                title="重要な通知",
                content="重要なお知らせです",
                user_id=user2.id,
                priority="high"
            )
            
            session.add(notice1)
            session.add(notice2)
            await session.commit()
            
            logger.info("✅ サンプルデータ挿入完了")
            
            # データ確認
            result = await session.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.scalar()
            logger.info(f"📊 ユーザー数: {user_count}")
            
            result = await session.execute(text("SELECT COUNT(*) FROM projects"))
            project_count = result.scalar()
            logger.info(f"📊 プロジェクト数: {project_count}")
            
            result = await session.execute(text("SELECT COUNT(*) FROM assignments"))
            assignment_count = result.scalar()
            logger.info(f"📊 課題数: {assignment_count}")
            
            result = await session.execute(text("SELECT COUNT(*) FROM notices"))
            notice_count = result.scalar()
            logger.info(f"📊 通知数: {notice_count}")
            
        return True
        
    except Exception as e:
        logger.error(f"❌ サンプルデータ挿入エラー: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await db_manager.close()


async def main():
    """メイン関数"""
    logger.info("🚀 データベーステーブル作成・初期化開始")
    
    # テーブル作成
    if await create_tables():
        logger.info("✅ テーブル作成成功")
        
        # サンプルデータ挿入
        if await insert_sample_data():
            logger.info("✅ サンプルデータ挿入成功")
            logger.info("🎉 データベース初期化完了！")
            return 0
        else:
            logger.error("❌ サンプルデータ挿入失敗")
            return 1
    else:
        logger.error("❌ テーブル作成失敗")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
