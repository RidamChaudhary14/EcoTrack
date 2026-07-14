from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, Field

T = TypeVar('T')

class PaginationResponse(BaseModel, Generic[T]):
    items: List[T] = Field(description="The items on the current page")
    total: int = Field(description="Total number of items")
    page: int = Field(description="Current page number")
    size: int = Field(description="Number of items per page")
    pages: int = Field(description="Total number of pages")

class APIResponse(BaseModel, Generic[T]):
    success: bool = Field(default=True, description="Indicates if the request was successful")
    message: str = Field(description="Response message")
    data: Optional[T] = Field(default=None, description="Response payload")
