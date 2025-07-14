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
