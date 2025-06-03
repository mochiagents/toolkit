from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    query: str = Field(..., description="The search query string.")
    max_results: Optional[int] = Field(5, ge=1, le=20, description="Maximum number of search results to return.")

class SearchResultItem(BaseModel):
    title: str = Field(..., description="The title of the search result.")
    url: str = Field(..., description="The URL of the search result.")
    content: str = Field(..., description="A snippet or summary of the search result content.")
    score: Optional[float] = Field(None, description="The relevance score of the search result, if available.")
    raw_content: Optional[str] = Field(None, description="The raw content of the search result, if available.")

class SearchResponse(BaseModel):
    status: str = Field("success", description="Status of the search operation.")
    results: List[SearchResultItem] = Field(..., description="A list of search results.") 