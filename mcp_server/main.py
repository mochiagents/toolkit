import logging
import os
from contextlib import asynccontextmanager
from typing import Dict, Any # Minimal imports needed at the top

from fastapi import FastAPI, HTTPException # Keep FastAPI
from dotenv import load_dotenv

# MCP Server specific models and registry
from .models import JsonRpcRequest, JsonRpcResponse, ServerSchemaResponse # Relative imports
from .tool_registry import (
    discover_and_register_tools,
    get_all_tool_definitions,
    call_tool
)

# Load environment variables from .env file (if your tools need them directly at init)
# Individual tools (like Tavily) are expected to load their own keys if they manage them
load_dotenv() 

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("MCP Server: Lifespan event - startup")
    # Discover and initialize tools from the specified directory
    # The actual path to tools needs to be correct from the execution context.
    # If main.py is in toolkit/mcp_server, and tools are in toolkit/available_tools,
    # the import path for discover_and_register_tools would be "toolkit.available_tools"
    await discover_and_register_tools()
    logger.info("Tool discovery and registration complete.")
    yield
    logger.info("MCP Server: Lifespan event - shutdown")
    # Add any global cleanup logic here if needed

app = FastAPI(
    title="Unified MCP Tool Server",
    description="Provides access to various tools via the MCP JSON-RPC interface.",
    version="1.0.0", # Updated version
    lifespan=lifespan
)

@app.post("/mcp", response_model=JsonRpcResponse, summary="MCP JSON-RPC Endpoint")
async def mcp_rpc_handler(request: JsonRpcRequest):
    logger.info(f"MCP Endpoint: Received JSON-RPC request with method: {request.method}, id: {request.id}")

    if request.method == "mcp_list_tools":
        tools_definitions = get_all_tool_definitions()
        # Pydantic models will be serialized to dicts by FastAPI/Pydantic
        return JsonRpcResponse(result=[td.model_dump() for td in tools_definitions], id=request.id)
    
    elif request.method == "mcp_call_tool":
        if not request.params or not isinstance(request.params, dict):
             return JsonRpcResponse(
                error={"code": -32602, "message": "Invalid params: 'params' must be an object for mcp_call_tool."},
                id=request.id
            )

        tool_name = request.params.get("tool_id") # MCP spec uses tool_id, but our registry uses tool_name
        inputs = request.params.get("inputs")

        if not tool_name or not isinstance(tool_name, str):
            return JsonRpcResponse(
                error={"code": -32602, "message": "Invalid params: 'tool_id' is missing or not a string."},
                id=request.id
            )
        if inputs is None or not isinstance(inputs, dict): # inputs can be an empty dict
            return JsonRpcResponse(
                error={"code": -32602, "message": "Invalid params: 'inputs' is missing or not an object."},
                id=request.id
            )

        tool_execution_payload = await call_tool(tool_name, inputs)

        if tool_execution_payload: # call_tool returns the payload directly
            return JsonRpcResponse(result=tool_execution_payload, id=request.id)
        else:
            # call_tool logs errors, but we need a specific JSON-RPC error here
            return JsonRpcResponse(
                error={"code": -32601, "message": f"Method not found or error: Tool with id '{tool_name}' is not available or failed execution."},
                id=request.id
            )
    else:
        logger.warning(f"MCP Endpoint: Method '{request.method}' not found.")
        return JsonRpcResponse(
            error={"code": -32601, "message": f"Method '{request.method}' not found."},
            id=request.id
        )

@app.get("/schema", response_model=ServerSchemaResponse, summary="Get Server and Tools Schema")
async def get_server_schema():
    tools_definitions = get_all_tool_definitions()
    return ServerSchemaResponse(
        name="Unified MCP Tool Server",
        description="Provides access to various tools via the MCP JSON-RPC interface. This schema describes the server and its available tools.",
        version=app.version,
        tools=tools_definitions # Already a list of ToolDefinition models
    )

if __name__ == "__main__":
    import uvicorn
    logger.info("Attempting to run Unified MCP Tool Server on http://localhost:8001")
    
    # Check for critical environment variables needed by tools if possible (though tools manage their own)
    # Example: if os.getenv("TAVILY_API_KEY") is None:
    #     logger.warning("TAVILY_API_KEY is not set. Some tools like Tavily search may not function.")

    uvicorn.run(
        "toolkit.mcp_server.main:app", 
        host="0.0.0.0", 
        port=8001, 
        reload=True, # Reload for development
        # reload_dirs=["toolkit"], # If you want to specify dirs for reload explicitly
    ) 