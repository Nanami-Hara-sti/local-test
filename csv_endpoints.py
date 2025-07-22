"""
CSV アップロード エンドポイント

このモジュールは以下のCSVアップロード機能を提供します：
- ヒストグラムデータのCSVアップロード
- プロジェクトデータのCSVアップロード
- ユーザーデータのCSVアップロード
- アサインデータのCSVアップロード
"""

import csv
import io
from typing import List, Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import (
    CSVUploadResponse,
    HistogramCSVData,
    ProjectCSVData,
    UserCSVData,
    AssignDataCSVData,
)
from db_crud import (
    HistogramDataCRUD,
    ProjectDataCRUD,
    UserDataCRUD,
    AssignDataCSVCRUD,
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["CSV Upload"])


async def parse_csv_file(file: UploadFile) -> List[Dict[str, Any]]:
    """CSVファイルを解析して辞書のリストに変換"""
    try:
        # ファイルサイズチェック（10MB上限）
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=413, detail="ファイルサイズが10MBを超えています"
            )

        # CSVとして解析
        csv_text = content.decode("utf-8-sig")  # BOMを処理
        csv_reader = csv.DictReader(io.StringIO(csv_text))

        data_list = []
        for row_num, row in enumerate(csv_reader, start=1):
            if not any(row.values()):  # 空行をスキップ
                continue
            data_list.append(row)

        if not data_list:
            raise HTTPException(
                status_code=422, detail="CSVファイルにデータが含まれていません"
            )

        return data_list

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=422,
            detail="ファイルのエンコーディングが不正です（UTF-8を使用してください）",
        )
    except csv.Error as e:
        raise HTTPException(
            status_code=422, detail=f"CSVファイルの形式が不正です: {str(e)}"
        )
    except Exception as e:
        logger.error(f"CSV解析エラー: {str(e)}")
        raise HTTPException(status_code=500, detail="CSVファイルの解析に失敗しました")


@router.post("/histograms", response_model=CSVUploadResponse)
async def upload_histogram_csv(
    file: UploadFile = File(...), db: AsyncSession = Depends(get_db)
):
    """ヒストグラムCSVファイルアップロード"""
    try:
        # ファイル形式チェック
        if not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=415, detail="CSVファイルのみアップロード可能です"
            )

        # CSV解析
        csv_data = await parse_csv_file(file)

        # データ検証とPydanticモデルに変換
        validated_data = []
        for row_num, row in enumerate(csv_data, start=1):
            try:
                histogram_data = HistogramCSVData(**row)
                validated_data.append(histogram_data.dict())
            except Exception as e:
                raise HTTPException(
                    status_code=422, detail=f"行 {row_num}: データ形式エラー - {str(e)}"
                )

        # 既存データを削除
        await HistogramDataCRUD.clear_histogram_data(db)

        # 新しいデータを一括挿入
        records_processed = await HistogramDataCRUD.bulk_create_histogram_data(
            db, validated_data
        )

        return CSVUploadResponse(
            message="ヒストグラムデータが正常にアップロードされました",
            type="histograms",
            filename=file.filename,
            records_processed=records_processed,
            updated_by="システム",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ヒストグラムCSVアップロードエラー: {str(e)}")
        raise HTTPException(
            status_code=500, detail="ヒストグラムデータのアップロードに失敗しました"
        )


@router.post("/projects", response_model=CSVUploadResponse)
async def upload_project_csv(
    file: UploadFile = File(...), db: AsyncSession = Depends(get_db)
):
    """プロジェクトCSVファイルアップロード"""
    try:
        # ファイル形式チェック
        if not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=415, detail="CSVファイルのみアップロード可能です"
            )

        # CSV解析
        csv_data = await parse_csv_file(file)

        # データ検証とPydanticモデルに変換
        validated_data = []
        for row_num, row in enumerate(csv_data, start=1):
            try:
                project_data = ProjectCSVData(**row)
                validated_data.append(project_data.dict())
            except Exception as e:
                raise HTTPException(
                    status_code=422, detail=f"行 {row_num}: データ形式エラー - {str(e)}"
                )

        # 既存データを削除
        await ProjectDataCRUD.clear_project_data(db)

        # 新しいデータを一括挿入
        records_processed = await ProjectDataCRUD.bulk_create_project_data(
            db, validated_data
        )

        return CSVUploadResponse(
            message="プロジェクトデータが正常にアップロードされました",
            type="projects",
            filename=file.filename,
            records_processed=records_processed,
            updated_by="システム",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"プロジェクトCSVアップロードエラー: {str(e)}")
        raise HTTPException(
            status_code=500, detail="プロジェクトデータのアップロードに失敗しました"
        )


@router.post("/users", response_model=CSVUploadResponse)
async def upload_user_csv(
    file: UploadFile = File(...), db: AsyncSession = Depends(get_db)
):
    """ユーザーCSVファイルアップロード"""
    try:
        # ファイル形式チェック
        if not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=415, detail="CSVファイルのみアップロード可能です"
            )

        # CSV解析
        csv_data = await parse_csv_file(file)

        # データ検証とPydanticモデルに変換
        validated_data = []
        for row_num, row in enumerate(csv_data, start=1):
            try:
                user_data = UserCSVData(**row)
                validated_data.append(user_data.dict())
            except Exception as e:
                raise HTTPException(
                    status_code=422, detail=f"行 {row_num}: データ形式エラー - {str(e)}"
                )

        # 既存データを削除
        await UserDataCRUD.clear_user_data(db)

        # 新しいデータを一括挿入
        records_processed = await UserDataCRUD.bulk_create_user_data(db, validated_data)

        return CSVUploadResponse(
            message="ユーザーデータが正常にアップロードされました",
            type="users",
            filename=file.filename,
            records_processed=records_processed,
            updated_by="システム",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ユーザーCSVアップロードエラー: {str(e)}")
        raise HTTPException(
            status_code=500, detail="ユーザーデータのアップロードに失敗しました"
        )


@router.post("/assigns", response_model=CSVUploadResponse)
async def upload_assign_csv(
    file: UploadFile = File(...), db: AsyncSession = Depends(get_db)
):
    """アサインデータCSVファイルアップロード"""
    try:
        # ファイル形式チェック
        if not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=415, detail="CSVファイルのみアップロード可能です"
            )

        # CSV解析
        csv_data = await parse_csv_file(file)

        # データ検証とPydanticモデルに変換
        validated_data = []
        for row_num, row in enumerate(csv_data, start=1):
            try:
                assign_data = AssignDataCSVData(**row)
                # 辞書に変換し、SQLAlchemy モデルに不要なフィールドを除外
                data_dict = assign_data.dict()
                # AssignDataテーブルに存在するフィールドのみを抽出
                filtered_dict = {
                    k: v
                    for k, v in data_dict.items()
                    if k
                    in [
                        "user_name",
                        "assin_execution",
                        "assin_maintenance",
                        "assin_prospect",
                        "assin_common_cost",
                        "assin_most_com_ps",
                        "assin_sales_mane",
                        "assin_investigation",
                        "assin_project_code",
                        "assin_directly",
                        "assin_common",
                        "assin_sales_sup",
                    ]
                }
                validated_data.append(filtered_dict)
            except Exception as e:
                raise HTTPException(
                    status_code=422, detail=f"行 {row_num}: データ形式エラー - {str(e)}"
                )

        # 既存データを削除
        await AssignDataCSVCRUD.clear_assign_data(db)

        # 新しいデータを一括挿入
        records_processed = await AssignDataCSVCRUD.bulk_create_assign_data(
            db, validated_data
        )

        return CSVUploadResponse(
            message="アサインデータが正常にアップロードされました",
            type="assigns",
            filename=file.filename,
            records_processed=records_processed,
            updated_by="システム",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"アサインCSVアップロードエラー: {str(e)}")
        raise HTTPException(
            status_code=500, detail="アサインデータのアップロードに失敗しました"
        )
