from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MediaItem(BaseModel):
    """Pydantic model for media item returned on search."""

    id: str = Field(..., description="Media ID")
    image_id: str = Field(..., description="Image ID")
    title: Optional[str] = Field(None, description="Media title")
    description: Optional[str] = Field(None, description="Media description")
    db: str = Field(..., description="Database source, e.g., 'st' or 'sp'")
    date: Optional[datetime] = Field(None, description="Media date")
    photographer: Optional[str] = Field(None, description="Media photographer")
    width: Optional[int] = Field(None, description="Media width")
    height: Optional[int] = Field(None, description="Media height")
    thumbnail_url: str = Field(..., description="URL to the thumbnail image")


class SearchResponse(BaseModel):
    """Pydantic model for search response."""

    results: list[MediaItem]
    total: int
