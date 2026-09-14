import uuid

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.modules.media import storage
from app.modules.media.models import Media
from app.modules.media.schemas import ALLOWED_MIME_TYPES, MAX_FILE_SIZE_BYTES


def upload_media(db: Session, owner_id: uuid.UUID, file: UploadFile, visibility: str = "RESTRICTED") -> Media:
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unsupported file type: {file.content_type}",
        )

    file_bytes = file.file.read()
    size_bytes = len(file_bytes)

    if size_bytes == 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Empty file")

    if size_bytes > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="File exceeds maximum allowed size")

    object_key = storage.build_object_key(owner_id, file.filename or "upload")
    storage.upload_file(object_key, file_bytes, file.content_type)

    media = Media(
        owner_id=owner_id,
        object_key=object_key,
        mime_type=file.content_type,
        size_bytes=size_bytes,
        visibility=visibility,
    )
    db.add(media)
    db.commit()
    db.refresh(media)
    return media


def get_media_or_404(db: Session, media_id: uuid.UUID) -> Media:
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")
    return media
