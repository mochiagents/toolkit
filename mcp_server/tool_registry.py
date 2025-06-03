import importlib
import inspect
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable, Awaitable

# Assuming general MCP models are in toolkit.mcp_server.models
from toolkit.mcp_server.models import ToolDefinition
# Import directly from the available_tools package
from toolkit.available_tools import (
    TOOL_DEFINITIONS as AVAILABLE_TOOL_DEFINITIONS,
    TOOL_EXECUTORS as AVAILABLE_TOOL_EXECUTORS,
    initialize_all_tools as initialize_all_available_tools,
    get_all_tool_definitions as get_all_available_tool_definitions # If needed for direct passthrough
)

logger = logging.getLogger(__name__)

# Structure to hold loaded tool information
class RegisteredTool:
    name: str
    definition: ToolDefinition
    # initialize_func is handled by initialize_all_available_tools now
    execute_func: Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]

    def __init__(
        self,
        name: str,
        definition: ToolDefinition,
        execute_func: Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]],
        # initialize_func: Optional[Callable[[], None]] = None, # Removed
    ):
        self.name = name
        self.definition = definition
        # self.initialize_func = initialize_func # Removed
        self.execute_func = execute_func

_tool_registry: Dict[str, RegisteredTool] = {}

# Standardized function names expected in each tool module
GET_DEFINITION_FUNC_NAME = "get_tool_definition"  # e.g., get_tavily_search_tool_definition
EXECUTE_FUNC_NAME = "execute_tool"            # e.g., execute_tavily_search
INITIALIZE_FUNC_NAME = "initialize_tool"      # e.g., initialize_tavily_search_tool

async def discover_and_register_tools(): # Removed tools_base_path argument
    """
    Registers tools by using the centralized registration from toolkit.available_tools.
    Initializes all discovered tools.
    """
    global _tool_registry
    _tool_registry = {} # Reset registry

    logger.info("Starting tool registration using toolkit.available_tools...")

    try:
        # Initialize all tools (this will call their individual initializers)
        # This should be called ideally once at application startup.
        # If discover_and_register_tools can be called multiple times, ensure initialize_all_available_tools handles that gracefully (idempotent)
        initialize_all_available_tools() 
        logger.info("Successfully called initialize_all_available_tools.")

        for tool_name, definition in AVAILABLE_TOOL_DEFINITIONS.items():
            executor = AVAILABLE_TOOL_EXECUTORS.get(tool_name)
            if executor:
                if tool_name in _tool_registry:
                    logger.warning(f"Duplicate tool name '{tool_name}' encountered during registration. Overwriting.")
                
                _tool_registry[tool_name] = RegisteredTool(
                    name=tool_name,
                    definition=definition,
                    execute_func=executor
                )
                logger.info(f"Registered tool: '{tool_name}'")
            else:
                logger.warning(f"Executor not found for tool '{tool_name}' in AVAILABLE_TOOL_EXECUTORS. Skipping registration.")
        
        logger.info(f"Tool registration complete. {_tool_registry.keys().__len__()} tools registered: {list(_tool_registry.keys())}")

    except Exception as e:
        logger.error(f"Failed during tool registration from toolkit.available_tools: {e}", exc_info=True)
        # Depending on desired behavior, might re-raise or handle to allow server to start with no/few tools

def get_all_tool_definitions() -> List[ToolDefinition]:
    """Returns definitions of all successfully registered tools."""
    return [tool.definition for tool in _tool_registry.values()]

async def call_tool(tool_name: str, inputs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    tool = _tool_registry.get(tool_name)
    if tool and callable(tool.execute_func):
        logger.info(f"Calling tool: '{tool_name}' with inputs: {inputs}")
        try:
            return await tool.execute_func(inputs)
        except Exception as e:
            logger.error(f"Error executing tool '{tool_name}': {e}", exc_info=True)
            return {"status": "failure", "output": None, "error": f"Internal error during '{tool_name}' execution: {str(e)}"}
    
    logger.warning(f"Attempted to call unknown or non-executable tool: '{tool_name}'")
    # Consider returning a more specific error structure that conforms to tool execution payloads
    return {"status": "failure", "output": None, "error": f"Tool '{tool_name}' not found or not executable."}

# Ensure __all__ is appropriate if this module is imported elsewhere with 'from ... import *'
__all__ = [
    "discover_and_register_tools",
    "get_all_tool_definitions",
    "call_tool",
    "RegisteredTool" # If this class needs to be accessed from outside
]
