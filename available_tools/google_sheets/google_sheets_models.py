from typing import List, Optional, Any
from pydantic import BaseModel, Field

class AppendRequest(BaseModel):
    spreadsheet_id: str = Field(..., description="The ID of the spreadsheet.")
    range: str = Field(..., description="The A1 notation of a range to search for a logical table of data. Values will be appended after the last row of the table.")
    value_input_option: str = Field("USER_ENTERED", description="How the input data should be interpreted.")
    values: List[List[Any]] = Field(..., description="The data to append. A list of rows, where each row is a list of cell values.")
    insert_data_option: Optional[str] = Field(None, description="How the input data should be inserted. (e.g., INSERT_ROWS, OVERWRITE)")


class AppendResponse(BaseModel):
    spreadsheet_id: str = Field(..., description="The ID of the spreadsheet.")
    table_range: Optional[str] = Field(None, description="The range the data was appended to.")
    updates: Optional[dict] = Field(None, description="Information about the updates that were applied.")
    updated_cells: Optional[int] = Field(None, description="The number of cells appended.")


class ReadRequest(BaseModel):
    spreadsheet_id: str = Field(..., description="The ID of the spreadsheet.")
    range: str = Field(..., description="The A1 notation of the range to read.")
    major_dimension: Optional[str] = Field(None, description="The major dimension that results should use. ROWS or COLUMNS.")
    value_render_option: Optional[str] = Field(None, description="How values should be represented in the output. FORMATTED_VALUE, UNFORMATTED_VALUE, FORMULA.")
    date_time_render_option: Optional[str] = Field(None, description="How dates, times, and durations should be represented. SERIAL_NUMBER or FORMATTED_STRING.")


class ReadResponse(BaseModel):
    spreadsheet_id: str = Field(..., description="The ID of the spreadsheet.")
    range: str = Field(..., description="The range the data was read from.")
    major_dimension: Optional[str] = Field(None, description="The major dimension of the values.")
    values: Optional[List[List[Any]]] = Field(None, description="The data that was read.")


class UpdateRequest(BaseModel):
    spreadsheet_id: str = Field(..., description="The ID of the spreadsheet.")
    range: str = Field(..., description="The A1 notation of the range to write.")
    values: List[List[Any]] = Field(..., description="The data to write. A list of rows, where each row is a list of cell values.")
    value_input_option: Optional[str] = Field("USER_ENTERED", description="How the input data should be interpreted. RAW or USER_ENTERED.")
    # Sheets API v4 update method does not directly use majorDimension in the same way as batchUpdate in the request body,
    # it's more about the structure of the 'values' array. The 'body' for update is a ValueRange.


class UpdateResponse(BaseModel):
    spreadsheet_id: str = Field(..., description="The ID of the spreadsheet.")
    updated_range: str = Field(..., description="The A1 notation of the range that was updated.")
    updated_rows: int = Field(..., description="The number of rows updated.")
    updated_columns: int = Field(..., description="The number of columns updated.")
    updated_cells: int = Field(..., description="The total number of cells updated.") 