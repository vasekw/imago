from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SearchByField(str, Enum):
    """Enum of searchable fields."""

    edited_image = "bearbeitet_bild"
    description = "description"
    search_text = "suchtext"
    title_field = "title"


class SortByField(str, Enum):
    """Enum of sortable fields."""

    date = "datum"
    width = "breite"
    height = "hoehe"
    photographer = "fotografen"
    db = "db"
    photo_number = "bildnummer"


class SortDirection(str, Enum):
    """Enum of sortable directions."""

    asc = "asc"
    desc = "desc"


class MediaItem(BaseModel):
    """Pydantic model for media item returned on search."""

    id: str = Field(..., description="Media ID")
    image_id: Optional[str] = Field(None, description="Image ID")
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
