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
class Project(BaseModel):
    """プロジェクトデータ"""
    project_id: Optional[int] = None
    project_br_num: str
    project_name: str
    project_contract_form: str
    project_sched_self: str
    project_sched_to: str
    project_type_name: str
    project_classification: str
    project_budget_no: str
    project_estimate_num: Optional[str] = None
    project_valid_from: Optional[str] = None
    project_valid_to: Optional[str] = None
    project_is_current: Optional[bool] = None


class ProjectArray(BaseModel):
    """プロジェクト一覧のレスポンス"""
    projects: list[Project]


# ユーザーデータ用のモデル
class User(BaseModel):
    """ユーザーデータ"""
    user_id: Optional[int] = None
    user_code: str
    user_name: str
    user_team: str
    user_type: Optional[str] = "GENERAL"


class UserArray(BaseModel):
    """ユーザー一覧のレスポンス"""
    users: list[User]


# 通知データ用のモデル
class Notice(BaseModel):
    """通知データ"""
    notice_id: Optional[int] = None
    notice_time: str
    notice_text: str
    user_name: str
    project_name: Optional[str] = None
    notice_type: str


class NoticeArray(BaseModel):
    """通知一覧のレスポンス"""
    notices: list[Notice]


class NotificationCreateRequest(BaseModel):
    """通知作成リクエスト"""
    notice_text: str
    user_name: str
    project_name: Optional[str] = None
    notice_type: str


# アサインデータ用のモデル
class MonthTotal(BaseModel):
    """月合計データ"""
    month: int
    total_assin: Optional[float] = None


class AssignMonthTotals(BaseModel):
    """アサインの月合計データ"""
    previous_month: MonthTotal
    current_month: MonthTotal
    next_month: MonthTotal


class Assin(BaseModel):
    """アサインデータ"""
    assins_id: Optional[int] = None
    user_name: str
    assin_execution: Optional[float] = None
    assin_maintenance: Optional[float] = None
    assin_prospect: Optional[float] = None
    assin_common_cost: Optional[float] = None
    assin_most_com_ps: Optional[float] = None
    assin_sales_mane: Optional[float] = None
    assin_investigation: Optional[float] = None
    month_totals: AssignMonthTotals
    assin_project_code: Optional[int] = None
    assin_directly: Optional[float] = None
    assin_common: Optional[float] = None
    assin_sales_sup: Optional[float] = None


class AssinArray(BaseModel):
    """アサイン一覧"""
    assigns: list[Assin]


# 総計データ用のモデル
class MonthTotals(BaseModel):
    """月合計データ"""
    previous_month: MonthTotal
    current_month: MonthTotal
    next_month: MonthTotal


class Total(BaseModel):
    """総計データ"""
    total_year: str
    total_month: int
    total_execution: Optional[float] = None
    total_maintenance: Optional[float] = None
    total_prospect: Optional[float] = None
    total_common_cost: Optional[float] = None
    total_most_com_ps: Optional[float] = None
    total_sales_mane: Optional[float] = None
    total_investigation: Optional[float] = None
    total_directly: Optional[float] = None
    total_common: Optional[float] = None
    total_sales_sup: Optional[float] = None


class TotalArray(BaseModel):
    """総計一覧"""
    totals: list[Total]
