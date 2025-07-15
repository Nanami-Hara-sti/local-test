from pydantic import BaseModel
from typing import Optional


class BlobResponse(BaseModel):
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
    name: str
    size: int
    last_modified: Optional[str] = None
    content_type: Optional[str] = None


class BlobListResponse(BaseModel):
    success: bool
    container: str
    blob_count: int
    blobs: list[BlobInfo]


class UploadResponse(BaseModel):
    success: bool
    container: str
    blob: str
    size: int
    message: str


class DeleteResponse(BaseModel):
    success: bool
    container: str
    blob: str
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: str


class TextUploadRequest(BaseModel):
    text: str


# EventGrid用のモデル
class EventGridData(BaseModel):
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
    id: str
    eventType: str
    subject: str
    eventTime: str
    data: EventGridData
    dataVersion: str
    metadataVersion: str
    topic: str


class EventGridValidationEvent(BaseModel):
    id: str
    eventType: str
    subject: str
    eventTime: str
    data: dict
    dataVersion: str
    metadataVersion: str
    topic: str


class EventGridResponse(BaseModel):
    success: bool
    processed_events: int
    events: list[dict]
    message: str


# Assign-Kun API用のモデル

class AnnualData(BaseModel):
    """年間ヒストグラムデータ（1-12月分）"""
    histogram_01month: Optional[float] = None
    histogram_02month: Optional[float] = None  
    histogram_03month: Optional[float] = None
    histogram_04month: Optional[float] = None
    histogram_05month: Optional[float] = None
    histogram_06month: Optional[float] = None
    histogram_07month: Optional[float] = None
    histogram_08month: Optional[float] = None
    histogram_09month: Optional[float] = None
    histogram_10month: Optional[float] = None
    histogram_11month: Optional[float] = None
    histogram_12month: Optional[float] = None


class Histogram(BaseModel):
    """ヒストグラムデータ"""
    histogram_id: Optional[int] = None
    histogram_ac_code: str
    histogram_ac_name: str
    histogram_pj_br_num: str
    histogram_pj_name: str
    histogram_pj_contract_form: str
    histogram_costs_unit: int
    histogram_year: int
    annual_data: AnnualData


class HistogramArray(BaseModel):
    """ヒストグラムデータ配列のレスポンス"""
    histograms: list[Histogram]


class MonthValue(BaseModel):
    """月単位の値"""
    month: int
    value: Optional[float] = None


class MonthData(BaseModel):
    """前月・当月・翌月のデータ"""
    previous_month: MonthValue
    current_month: MonthValue 
    next_month: MonthValue


# プロジェクトデータ用のモデル
class ProjectData(BaseModel):
    """プロジェクトデータ"""
    project_id: Optional[int] = None
    project_code: str
    project_name: str
    account_code: str
    account_name: str
    contract_form: str
    start_date: str
    end_date: Optional[str] = None
    status: str
    manager_name: Optional[str] = None
    team_size: Optional[int] = None
    budget: Optional[float] = None
    description: Optional[str] = None


class ProjectListResponse(BaseModel):
    """プロジェクト一覧のレスポンス"""
    projects: list[ProjectData]
    total_count: int
    page: int
    per_page: int


# ユーザーデータ用のモデル
class UserData(BaseModel):
    """ユーザーデータ"""
    user_id: Optional[int] = None
    user_code: str
    user_name: str
    user_team: str
    user_type: Optional[str] = "GENERAL"


class UserListResponse(BaseModel):
    """ユーザー一覧のレスポンス"""
    users: list[UserData]
    total_count: int
    page: int
    per_page: int
