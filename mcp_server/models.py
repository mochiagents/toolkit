from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

# --- Pydantic Models for MCP Schema ---

class ToolInputSchema(BaseModel):
    name: str = Field(..., description="Name of the input parameter.")
    description: str = Field(..., description="Description of the input parameter.")
    type: str = Field(..., description="Data type of the input parameter (e.g., 'string', 'integer', 'boolean').")
    required: bool = Field(..., description="Whether the input parameter is required.")
    example: Optional[Any] = Field(None, description="An example value for the input.")

class ToolOutputSchemaDefinition(BaseModel):
    type: str = Field(..., description="Data type of the output (e.g., 'array', 'object', 'string').")
    description: Optional[str] = Field(None, description="Description of the output.")
    properties: Optional[Dict[str, Dict[str, Any]]] = Field(None, description="If type is 'object', this describes its properties.")
    items: Optional[Dict[str, Any]] = Field(None, description="If type is 'array', this describes the items in the array.")
    example: Optional[Any] = Field(None, description="An example value for the output.")

class ToolDefinition(BaseModel):
    tool_name: str = Field(..., description="The unique name of the tool.")
    description: str = Field(..., description="A human-readable description of what the tool does.")
    inputs: List[ToolInputSchema] = Field(..., description="A list of input parameters the tool accepts.")
    output: ToolOutputSchemaDefinition = Field(..., description="The schema of the output the tool produces.")

class ServerSchemaResponse(BaseModel):
    name: str = Field(..., description="The name of the MCP server.")
    description: str = Field(..., description="A human-readable description of the server and its capabilities.")
    version: str = Field(..., description="The version of the server.")
    tools: List[ToolDefinition] = Field(..., description="A list of tools provided by this server.")

# --- MCP JSON-RPC Models ---
class JsonRpcRequest(BaseModel):
    jsonrpc: str = Field("2.0", Literal=True)
    method: str
    params: Optional[Union[Dict[str, Any], List[Any]]] = None
    id: Optional[Union[str, int]] = None

class JsonRpcResponse(BaseModel):
    jsonrpc: str = Field("2.0", Literal=True)
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None # Based on JSON-RPC spec for error object
    id: Union[str, int, None]

# --- General Error Models (can be used by direct HTTP endpoints too) ---
class ErrorDetail(BaseModel):
    type: str = Field(..., description="Type of error.")
    message: str = Field(..., description="Detailed error message.")

class ErrorResponse(BaseModel):
    status: str = Field("error", description="Status of the operation.")
    error: ErrorDetail = Field(..., description="Details of the error.") 