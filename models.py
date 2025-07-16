"""
Pydantic モデル定義

このモジュールは以下のモデルを定義します：
- Azure Blob Storage 関連モデル
- EventGrid 関連モデル
- Assign-Kun API 関連モデル
- MySQL データベース関連モデル
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ==============================================================================
# Azure Blob Storage 関連モデル
# ==============================================================================


class BlobResponse(BaseModel):
    """Blob操作のレスポンス"""

    success: bool
    container: str
    blob: str
    text: str
    size: int
    content_type: Optional[str] = None
    last_modified: Optional[str] = None
    etag: Optional[str] = None
    message: str


class BlobInfo(BaseModel):
    """Blob情報"""

    name: str
    size: int
    last_modified: Optional[str] = None
    content_type: Optional[str] = None


class BlobListResponse(BaseModel):
    """Blob一覧のレスポンス"""

    success: bool
    container: str
    blob_count: int
    blobs: List[BlobInfo]


class UploadResponse(BaseModel):
    """アップロードレスポンス"""

    success: bool
    container: str
    blob: str
    size: int
    message: str


class DeleteResponse(BaseModel):
    """削除レスポンス"""

    success: bool
    container: str
    blob: str
    message: str


class ErrorResponse(BaseModel):
    """エラーレスポンス"""

    success: bool = False
    error: str
    message: str


class TextUploadRequest(BaseModel):
    """テキストアップロードリクエスト"""

    text: str


# ==============================================================================
# EventGrid 関連モデル
# ==============================================================================


class EventGridData(BaseModel):
    """EventGridイベントデータ"""

    api: str
    clientRequestId: str
    requestId: str
    eTag: str
    contentType: str
    contentLength: int
    blobType: str
    url: str
    sequencer: str
    storageDiagnostics: dict


class EventGridEvent(BaseModel):
    """EventGridイベント"""

    id: str
    eventType: str
    subject: str
    eventTime: str
    data: EventGridData
    dataVersion: str
    metadataVersion: str
    topic: str


class EventGridValidationEvent(BaseModel):
    """EventGrid検証イベント"""

    id: str
    eventType: str
    subject: str
    eventTime: str
    data: dict
    dataVersion: str
    metadataVersion: str
    topic: str


class EventGridResponse(BaseModel):
    """EventGridレスポンス"""

    success: bool
    processed_events: int
    events: List[dict]
    message: str


# ==============================================================================
# Assign-Kun API 関連モデル
# ==============================================================================


class AssignKunRequest(BaseModel):
    """Assign-Kun API リクエスト"""

    userName: str
    projectName: str
    assignmentName: str
    level: str
    isCorrect: bool


class AssignKunResponse(BaseModel):
    """Assign-Kun API レスポンス"""

    success: bool
    message: str
    userId: Optional[int] = None
    projectId: Optional[int] = None
    assignmentId: Optional[int] = None
    userScore: Optional[int] = None
    projectScore: Optional[int] = None
    assignmentScore: Optional[int] = None


# ==============================================================================
# MySQL データベース関連モデル
# ==============================================================================


class UserBase(BaseModel):
    """ユーザー基底モデル"""

    name: str
    email: Optional[str] = None
    score: Optional[int] = 0


class UserCreate(UserBase):
    """ユーザー作成モデル"""

    pass


class UserUpdate(BaseModel):
    """ユーザー更新モデル"""

    name: Optional[str] = None
    email: Optional[str] = None
    score: Optional[int] = None


class UserResponse(UserBase):
    """ユーザーレスポンスモデル"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    """プロジェクト基底モデル"""

    name: str
    description: Optional[str] = None
    score: Optional[int] = 0


class ProjectCreate(ProjectBase):
    """プロジェクト作成モデル"""

    pass


class ProjectUpdate(BaseModel):
    """プロジェクト更新モデル"""

    name: Optional[str] = None
    description: Optional[str] = None
    score: Optional[int] = None


class ProjectResponse(ProjectBase):
    """プロジェクトレスポンスモデル"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AssignmentBase(BaseModel):
    """課題基底モデル"""

    name: str
    description: Optional[str] = None
    project_id: int
    difficulty_level: str
    max_score: Optional[int] = 100
    is_active: Optional[bool] = True


class AssignmentCreate(AssignmentBase):
    """課題作成モデル"""

    pass


class AssignmentUpdate(BaseModel):
    """課題更新モデル"""

    name: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[int] = None
    difficulty_level: Optional[str] = None
    max_score: Optional[int] = None
    is_active: Optional[bool] = None


class AssignmentResponse(AssignmentBase):
    """課題レスポンスモデル"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NoticeBase(BaseModel):
    """通知基底モデル"""

    title: str
    content: str
    user_id: int
    is_read: Optional[bool] = False
    priority: Optional[str] = "normal"


class NoticeCreate(NoticeBase):
    """通知作成モデル"""

    pass


class NoticeUpdate(BaseModel):
    """通知更新モデル"""

    title: Optional[str] = None
    content: Optional[str] = None
    is_read: Optional[bool] = None
    priority: Optional[str] = None


class NoticeResponse(NoticeBase):
    """通知レスポンスモデル"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BlobLogBase(BaseModel):
    """Blob ログ基底モデル"""

    operation_type: str
    container_name: str
    blob_name: str
    file_size: Optional[int] = None
    content_type: Optional[str] = None
    status: str
    user_id: Optional[int] = None
    error_message: Optional[str] = None


class BlobLogCreate(BlobLogBase):
    """Blob ログ作成モデル"""

    pass


class BlobLogUpdate(BaseModel):
    """Blob ログ更新モデル"""

    operation_type: Optional[str] = None
    container_name: Optional[str] = None
    blob_name: Optional[str] = None
    file_size: Optional[int] = None
    content_type: Optional[str] = None
    status: Optional[str] = None
    user_id: Optional[int] = None
    error_message: Optional[str] = None


class BlobLogResponse(BlobLogBase):
    """Blob ログレスポンスモデル"""

    id: int
    operation_time: datetime

    class Config:
        from_attributes = True


class HistogramBase(BaseModel):
    """ヒストグラム基底モデル"""

    resource_type: str
    resource_id: int
    bin_label: str
    bin_value: int
    count: int
    percentage: Optional[float] = None
    additional_data: Optional[dict] = None


class HistogramCreate(HistogramBase):
    """ヒストグラム作成モデル"""

    pass


class HistogramUpdate(BaseModel):
    """ヒストグラム更新モデル"""

    resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    bin_label: Optional[str] = None
    bin_value: Optional[int] = None
    count: Optional[int] = None
    percentage: Optional[float] = None
    additional_data: Optional[dict] = None


class HistogramResponse(HistogramBase):
    """ヒストグラムレスポンスモデル"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class HistogramStatsResponse(BaseModel):
    """ヒストグラム統計レスポンスモデル"""

    resource_type: str
    resource_id: int
    total_count: int
    bin_count: int
    average_value: float
    min_value: int
    max_value: int
    histograms: List[HistogramResponse]

    class Config:
        from_attributes = True
