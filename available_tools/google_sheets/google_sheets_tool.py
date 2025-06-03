import os
import logging
from typing import Dict, Any, Optional, List

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from toolkit.mcp_server.models import ToolDefinition, ToolInputSchema, ToolOutputSchemaDefinition
from .google_sheets_models import AppendRequest, AppendResponse, ReadRequest, ReadResponse, UpdateRequest, UpdateResponse

logger = logging.getLogger(__name__)

# Global Google Sheets service client instance
google_sheets_service: Optional[Any] = None

def initialize_google_sheets_tool():
    """Initializes the Google Sheets API client if not already initialized."""
    global google_sheets_service
    if google_sheets_service:
        return

    try:
        creds, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/spreadsheets'])
        google_sheets_service = build("sheets", "v4", credentials=creds)
        logger.info("Google Sheets client initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Google Sheets client: {e}", exc_info=True)
        google_sheets_service = None

# --- Append Tool --- #
def get_google_sheets_append_tool_definition() -> ToolDefinition:
    return ToolDefinition(
        tool_name="google_sheets_append",
        description="Appends values to a Google Sheet. Finds a table in the specified range and appends data after the last row.",
        inputs=[
            ToolInputSchema(name="spreadsheet_id", description="The ID of the spreadsheet.", type="string", required=True),
            ToolInputSchema(name="range", description="The A1 notation of a range (e.g., 'Sheet1!A1:C2' or 'Sheet1'). Values are appended after the last row of the table found in this range.", type="string", required=True),
            ToolInputSchema(name="values", description="A list of rows to append. Each row is a list of cell values (e.g., [['data1', 'data2'], ['data3', 'data4']]).", type="array", items_type="array", required=True),
            ToolInputSchema(name="value_input_option", description="How input data is interpreted. Options: 'RAW', 'USER_ENTERED'. Default: 'USER_ENTERED'.", type="string", required=False),
            ToolInputSchema(name="insert_data_option", description="How data is inserted. Options: 'OVERWRITE', 'INSERT_ROWS'. Default: Appends after table, may overwrite.", type="string", required=False)
        ],
        output=ToolOutputSchemaDefinition(
            type="object",
            description="Result of the append operation.",
            properties={
                "spreadsheet_id": {"type": "string", "description": "ID of the spreadsheet."},
                "table_range": {"type": "string", "description": "The range the data was appended to (e.g., 'Sheet1!A1:D5')."},
                "updates": {"type": "object", "description": "Details of the update (updatedCells, updatedRange, etc.)."},
            }
        )
    )

async def execute_google_sheets_append(inputs: Dict[str, Any]) -> Dict[str, Any]:
    global google_sheets_service
    if not google_sheets_service:
        initialize_google_sheets_tool()
        if not google_sheets_service:
             return {"status": "failure", "output": None, "error": "Tool error: Google Sheets client not initialized."}
    try:
        append_request = AppendRequest(**inputs)
    except Exception as e:
        return {"status": "failure", "output": None, "error": f"Invalid input for append: {str(e)}"}

    body = {"values": append_request.values}
    try:
        request_params = {
            "spreadsheetId": append_request.spreadsheet_id,
            "range": append_request.range,
            "valueInputOption": append_request.value_input_option,
            "body": body,
        }
        if append_request.insert_data_option:
            request_params["insertDataOption"] = append_request.insert_data_option
        
        result = google_sheets_service.spreadsheets().values().append(**request_params).execute()
        output_response = {
            "spreadsheet_id": result.get("spreadsheetId"),
            "table_range": result.get("updates", {}).get("updatedRange"),
            "updates": result.get("updates")
        }
        return {"status": "success", "output": output_response, "error": None}
    except HttpError as error:
        return {"status": "failure", "output": None, "error": f"API error (append): {error.resp.status} - {error._get_reason()}. Details: {error.content.decode() if error.content else 'N/A'}"}
    except Exception as e:
        return {"status": "failure", "output": None, "error": f"Tool execution error (append): {str(e)}"}

# --- Read Tool --- #
def get_google_sheets_read_tool_definition() -> ToolDefinition:
    return ToolDefinition(
        tool_name="google_sheets_read",
        description="Reads values from a Google Sheet.",
        inputs=[
            ToolInputSchema(name="spreadsheet_id", description="The ID of the spreadsheet.", type="string", required=True),
            ToolInputSchema(name="range", description="The A1 notation of the range to read (e.g., 'Sheet1!A1:B5').", type="string", required=True),
            ToolInputSchema(name="major_dimension", description="ROWS or COLUMNS for result. Default: ROWS.", type="string", required=False),
            ToolInputSchema(name="value_render_option", description="How values are rendered (e.g., FORMATTED_VALUE). Default: FORMATTED_VALUE", type="string", required=False),
            ToolInputSchema(name="date_time_render_option", description="How date/time is rendered (e.g., SERIAL_NUMBER). Default: SERIAL_NUMBER", type="string", required=False)
        ],
        output=ToolOutputSchemaDefinition(
            type="object",
            description="The data read from the sheet.",
            properties={
                "spreadsheet_id": {"type": "string", "description": "ID of the spreadsheet."},
                "range": {"type": "string", "description": "The A1 range that was read."},
                "major_dimension": {"type": "string", "description": "Major dimension of the values (ROWS or COLUMNS)."},
                "values": {"type": "array", "items_type": "array", "description": "The data read from the sheet as a list of rows (or columns if major_dimension is COLUMNS)."}
            }
        )
    )

async def execute_google_sheets_read(inputs: Dict[str, Any]) -> Dict[str, Any]:
    global google_sheets_service
    if not google_sheets_service:
        initialize_google_sheets_tool()
        if not google_sheets_service:
            return {"status": "failure", "output": None, "error": "Tool error: Google Sheets client not initialized."}
    try:
        read_request = ReadRequest(**inputs)
    except Exception as e:
        return {"status": "failure", "output": None, "error": f"Invalid input for read: {str(e)}"}

    try:
        request_params = {
            "spreadsheetId": read_request.spreadsheet_id,
            "range": read_request.range,
        }
        if read_request.major_dimension:
            request_params["majorDimension"] = read_request.major_dimension
        if read_request.value_render_option:
            request_params["valueRenderOption"] = read_request.value_render_option
        if read_request.date_time_render_option:
            request_params["dateTimeRenderOption"] = read_request.date_time_render_option

        result = google_sheets_service.spreadsheets().values().get(**request_params).execute()
        output_values = result.get("values", [])
        
        if not output_values:
            return {"status": "failure", "error": "Empty spreadsheet data"}

        has_meaningful_data = any(
            any(cell not in [None, "", " "] for cell in row)
            for row in output_values
        )
        
        if not has_meaningful_data:
            return {
                "status": "failure",
                "output": None,
                "error": "No meaningful data found in spreadsheet range. Check: "
                        f"1. Range includes sheet name (e.g., 'Sheet1!A1:Z100')\n"
                        f"2. Cells contain non-empty values\n"
                        f"3. Range contains actual data (current range: {read_request.range})"
            }

        output_response = {
            "spreadsheet_id": read_request.spreadsheet_id,
            "range": result.get("range"),
            "major_dimension": result.get("majorDimension"),
            "values": output_values
        }
        return {"status": "success", "output": output_response, "error": None}
    except HttpError as error:
        return {"status": "failure", "output": None, "error": f"API error (read): {error.resp.status} - {error._get_reason()}. Details: {error.content.decode() if error.content else 'N/A'}"}
    except Exception as e:
        return {"status": "failure", "output": None, "error": f"Tool execution error (read): {str(e)}"}

# --- Update Tool --- #
def get_google_sheets_update_tool_definition() -> ToolDefinition:
    return ToolDefinition(
        tool_name="google_sheets_update",
        description="Updates (writes) values to a specific range in a Google Sheet.",
        inputs=[
            ToolInputSchema(name="spreadsheet_id", description="The ID of the spreadsheet.", type="string", required=True),
            ToolInputSchema(name="range", description="The A1 notation of the range to write (e.g., 'Sheet1!A1:B2').", type="string", required=True),
            ToolInputSchema(name="values", description="A list of rows to write. Each row is a list of cell values (e.g., [['newA1', 'newB1'], ['newA2', 'newB2']]).", type="array", items_type="array", required=True),
            ToolInputSchema(name="value_input_option", description="How input data is interpreted. Options: 'RAW', 'USER_ENTERED'. Default: 'USER_ENTERED'.", type="string", required=False)
        ],
        output=ToolOutputSchemaDefinition(
            type="object",
            description="Result of the update operation.",
            properties={
                "spreadsheet_id": {"type": "string", "description": "ID of the spreadsheet."},
                "updated_range": {"type": "string", "description": "The A1 range that was updated."},
                "updated_rows": {"type": "integer", "description": "Number of rows updated."},
                "updated_columns": {"type": "integer", "description": "Number of columns updated."},
                "updated_cells": {"type": "integer", "description": "Total cells updated."}
            }
        )
    )

async def execute_google_sheets_update(inputs: Dict[str, Any]) -> Dict[str, Any]:
    global google_sheets_service
    if not google_sheets_service:
        initialize_google_sheets_tool()
        if not google_sheets_service:
            return {"status": "failure", "output": None, "error": "Tool error: Google Sheets client not initialized."}
    try:
        update_request = UpdateRequest(**inputs)
    except Exception as e:
        return {"status": "failure", "output": None, "error": f"Invalid input for update: {str(e)}"}

    body = {"values": update_request.values}
    try:
        request_params = {
            "spreadsheetId": update_request.spreadsheet_id,
            "range": update_request.range,
            "valueInputOption": update_request.value_input_option,
            "body": body,
        }
        result = google_sheets_service.spreadsheets().values().update(**request_params).execute()
        output_response = {
            "spreadsheet_id": result.get("spreadsheetId"),
            "updated_range": result.get("updatedRange"),
            "updated_rows": result.get("updatedRows"),
            "updated_columns": result.get("updatedColumns"),
            "updated_cells": result.get("updatedCells")
        }
        return {"status": "success", "output": output_response, "error": None}
    except HttpError as error:
        return {"status": "failure", "output": None, "error": f"API error (update): {error.resp.status} - {error._get_reason()}. Details: {error.content.decode() if error.content else 'N/A'}"}
    except Exception as e:
        return {"status": "failure", "output": None, "error": f"Tool execution error (update): {str(e)}"}
