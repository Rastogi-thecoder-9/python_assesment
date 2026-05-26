from pydantic import BaseModel, Field
from typing import Optional
from src.constants import summary_cache_prefix


class DocumentCreate(BaseModel):
    user_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=10)


class DocumentResponse(BaseModel):
    document_id: str
    status: str


class DocumentStatusResponse(BaseModel):
    document_id: str
    status: str
    summary_cache_prefix: Optional[str] = None