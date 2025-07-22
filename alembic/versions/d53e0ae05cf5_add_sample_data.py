"""add sample data

Revision ID: d53e0ae05cf5
Revises: c84698d55337
Create Date: 2025-07-17 12:00:00.000000

"""
from alembic import op
from sqlalchemy import Float, Integer, String
from sqlalchemy.sql import column, table

# revision identifiers, used by Alembic.
revision = 'd53e0ae05cf5'
down_revision = 'c84698d55337'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """テーブルにサンプルデータを投入"""
    # users テーブル
    users_table = table(
        'users',
        column('id', Integer),
        column('user_code', String),
        column('name', String),
        column('user_team', String),
        column('user_type', String),
    )
    op.bulk_insert(users_table, [
        {'id': 1, 'user_code': 'U001', 'name': '田中太郎', 'user_team': '開発チーム', 'user_type': 'GENERAL'},
        {'id': 2, 'user_code': 'U002', 'name': '佐藤花子', 'user_team': '開発チーム', 'user_type': 'GENERAL'},
        {'id': 3, 'user_code': 'U003', 'name': '鈴木次郎', 'user_team': 'テストチーム', 'user_type': 'GENERAL'},
    ])

    # projects テーブル
    projects_table = table(
        'projects',
        column('id', Integer),
        column('project_br_num', String),
        column('name', String),
        column('project_contract_form', String),
        column('project_sched_self', String),
        column('project_sched_to', String),
        column('project_type_name', String),
        column('project_classification', String),
        column('project_budget_no', String),
    )
    op.bulk_insert(projects_table, [
        {'id': 1, 'project_br_num': 'PJ001', 'name': 'Webシステム開発', 'project_contract_form': '請負', 'project_sched_self': '2025-01-01', 'project_sched_to': '2025-12-31', 'project_type_name': 'システム開発', 'project_classification': '新規開発', 'project_budget_no': 'B2025001'},
        {'id': 2, 'project_br_num': 'PJ002', 'name': 'データ分析システム', 'project_contract_form': '派遣', 'project_sched_self': '2025-02-01', 'project_sched_to': '2025-08-31', 'project_type_name': 'データ分析', 'project_classification': '新規開発', 'project_budget_no': 'B2025002'},
        {'id': 3, 'project_br_num': 'PJ003', 'name': 'モバイルアプリ開発', 'project_contract_form': '請負', 'project_sched_self': '2025-03-01', 'project_sched_to': '2025-09-30', 'project_type_name': 'アプリ開発', 'project_classification': '新規開発', 'project_budget_no': 'B2025003'},
    ])

    # assigns テーブル (assignkun_endpoints.py の assigns に対応)
    # このテーブルのスキーマは不明なため、db_models.py に基づいて作成します。
    # 実際のカラム名に合わせて調整してください。
    assigns_table = table(
        'assigns',
        column('id', Integer),
        column('user_name', String),
        column('assin_execution', Float),
        column('assin_maintenance', Float),
        column('assin_prospect', Float),
        column('assin_common_cost', Float),
        column('assin_most_com_ps', Float),
        column('assin_sales_mane', Float),
        column('assin_investigation', Float),
        column('assin_project_code', Integer),
        column('assin_directly', Float),
        column('assin_common', Float),
        column('assin_sales_sup', Float),
    )
    op.bulk_insert(assigns_table, [
        {
            'id': 1,
            "user_name": "田中太郎",
            "assin_execution": 120.0,
            "assin_maintenance": 20.0,
            "assin_prospect": 10.0,
            "assin_common_cost": 5.0,
            "assin_most_com_ps": 3.0,
            "assin_sales_mane": 2.0,
            "assin_investigation": 0.0,
            "assin_project_code": 1,
            "assin_directly": 140.0,
            "assin_common": 15.0,
            "assin_sales_sup": 5.0,
        }
    ])

    # histograms テーブル
    histograms_table = table(
        'histograms',
        column('id', Integer),
        column('histogram_ac_code', String),
        column('histogram_ac_name', String),
        column('histogram_pj_br_num', String),
        column('histogram_pj_name', String),
        column('histogram_pj_contract_form', String),
        column('histogram_costs_unit', Integer),
        column('histogram_year', Integer),
        column('histogram_01month', Float),
        column('histogram_02month', Float),
        column('histogram_03month', Float),
        column('histogram_04month', Float),
        column('histogram_05month', Float),
        column('histogram_06month', Float),
        column('histogram_07month', Float),
        column('histogram_08month', Float),
        column('histogram_09month', Float),
        column('histogram_10month', Float),
        column('histogram_11month', Float),
        column('histogram_12month', Float),
    )
    op.bulk_insert(histograms_table, [
        {'id': 1, 'histogram_ac_code': 'AC001', 'histogram_ac_name': 'アカウント1', 'histogram_pj_br_num': 'PJ001', 'histogram_pj_name': 'プロジェクト1', 'histogram_pj_contract_form': '請負', 'histogram_costs_unit': 1, 'histogram_year': 2025, 'histogram_01month': 1.2, 'histogram_02month': 1.5, 'histogram_03month': 1.8, 'histogram_04month': 1.5, 'histogram_05month': 2.0, 'histogram_06month': 1.8, 'histogram_07month': 2.2, 'histogram_08month': 1.9, 'histogram_09month': 2.1, 'histogram_10month': 1.7, 'histogram_11month': 1.6, 'histogram_12month': 1.4},
        {'id': 2, 'histogram_ac_code': 'AC002', 'histogram_ac_name': 'アカウント2', 'histogram_pj_br_num': 'PJ002', 'histogram_pj_name': 'プロジェクト2', 'histogram_pj_contract_form': '派遣', 'histogram_costs_unit': 1, 'histogram_year': 2025, 'histogram_01month': 0.8, 'histogram_02month': 1.0, 'histogram_03month': 1.2, 'histogram_04month': 1.1, 'histogram_05month': 1.3, 'histogram_06month': 1.5, 'histogram_07month': 1.4, 'histogram_08month': 1.6, 'histogram_09month': 1.2, 'histogram_10month': 1.0, 'histogram_11month': 0.9, 'histogram_12month': 0.8},
        {'id': 3, 'histogram_ac_code': 'AC003', 'histogram_ac_name': 'アカウント3', 'histogram_pj_br_num': 'PJ003', 'histogram_pj_name': 'プロジェクト3', 'histogram_pj_contract_form': '請負', 'histogram_costs_unit': 1, 'histogram_year': 2025, 'histogram_01month': 2.1, 'histogram_02month': 2.3, 'histogram_03month': 2.0, 'histogram_04month': 2.5, 'histogram_05month': 2.8, 'histogram_06month': 2.4, 'histogram_07month': 2.6, 'histogram_08month': 2.2, 'histogram_09month': 2.0, 'histogram_10month': 1.9, 'histogram_11month': 2.1, 'histogram_12month': 2.3},
    ])

    # notices テーブル
    notices_table = table(
        'notices',
        column('id', Integer),
        column('notice_time', String),
        column('user_name', String),
        column('notice_text', String),
        column('project_name', String),
        column('notice_type', String),
    )
    op.bulk_insert(notices_table, [
        {'id': 1, 'notice_time': '2025-07-08T10:00:00Z', 'user_name': '田中太郎', 'notice_text': 'プロジェクトPJ001の工事進行基準が達成されました', 'project_name': 'Webシステム開発', 'notice_type': '工事進行基準案件'},
        {'id': 2, 'notice_time': '2025-07-08T09:30:00Z', 'user_name': '佐藤花子', 'notice_text': 'システムメンテナンスが完了しました', 'project_name': None, 'notice_type': 'システムメンテナンス'},
        {'id': 3, 'notice_time': '2025-07-08T09:00:00Z', 'user_name': '鈴木次郎', 'notice_text': 'データ更新が完了しました', 'project_name': 'データ分析システム', 'notice_type': 'データ更新'},
    ])


def downgrade() -> None:
    # サンプルデータを削除
    op.execute('DELETE FROM notices')
    op.execute('DELETE FROM histograms')
    op.execute('DELETE FROM assigns')
    op.execute('DELETE FROM projects')
    op.execute('DELETE FROM users')
