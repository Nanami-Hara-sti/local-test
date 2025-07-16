-- MySQL初期化スクリプト
-- データベースとユーザーの作成

-- データベース作成
CREATE DATABASE IF NOT EXISTS assignkun_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ユーザー作成と権限付与
CREATE USER IF NOT EXISTS 'assignkun'@'%' IDENTIFIED BY 'assignkun_password';
GRANT ALL PRIVILEGES ON assignkun_db.* TO 'assignkun'@'%';
FLUSH PRIVILEGES;

-- 初期データベースの使用
USE assignkun_db;

-- テーブル作成はSQLAlchemyが自動で行います
-- 必要に応じて追加の初期データを挿入できます

-- 例：管理者ユーザーの作成
-- INSERT INTO users (username, email, full_name, is_active) VALUES
-- ('admin', 'admin@example.com', 'Administrator', true);

-- 例：初期通知の作成
-- INSERT INTO notices (title, content, priority) VALUES
-- ('システム開始', 'AssignKun-MySQL統合システムが正常に開始されました', 'normal');
