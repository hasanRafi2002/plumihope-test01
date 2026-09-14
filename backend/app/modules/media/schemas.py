import uuid
from datetime import datetime

from pydantic import BaseModel

ALLOWED_MIME_TYPES: set[str] = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "application/pdf",
    "video/mp4",
}

MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB


class MediaPublic(BaseModel):
    id: uuid.UUID
    mime_type: str
    size_bytes: int
    visibility: str
    created_at: datetime

    model_config = {"from_attributes": True}
