from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, Field

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T] = Field(description="The items on the current page")
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Number of items per page")
    total: int = Field(description="Total number of items")
    total_pages: int = Field(description="Total number of pages")
    has_next: bool = Field(description="Indicates if there is a next page")
    has_previous: bool = Field(description="Indicates if there is a previous page")

class APIResponse(BaseModel, Generic[T]):
    success: bool = Field(default=True, description="Indicates if the request was successful")
    message: str = Field(description="Response message")
    data: Optional[T] = Field(default=None, description="Response payload")
