from typing import Dict, Callable, Coroutine, Any, List, Optional

from toolkit.mcp_server.models import ToolDefinition
from .tavily_search.tavily_search_tool import get_tavily_search_tool_definition, execute_tavily_search, initialize_tavily_search_tool
from .google_sheets.google_sheets_tool import (
    get_google_sheets_append_tool_definition,
    execute_google_sheets_append,
    get_google_sheets_read_tool_definition,
    execute_google_sheets_read,
    get_google_sheets_update_tool_definition,
    execute_google_sheets_update,
    initialize_google_sheets_tool
)

# Dictionary to hold tool definitions
TOOL_DEFINITIONS: Dict[str, ToolDefinition] = {}

# Dictionary to hold tool execution functions
TOOL_EXECUTORS: Dict[str, Callable[[Dict[str, Any]], Coroutine[Any, Any, Dict[str, Any]]]] = {}

# List of initialization functions for all tools
TOOL_INITIALIZERS: List[Callable[[], None]] = []

def register_tool(
    tool_name: str,
    definition_getter: Callable[[], ToolDefinition],
    executor: Callable[[Dict[str, Any]], Coroutine[Any, Any, Dict[str, Any]]],
    initializer: Optional[Callable[[], None]] = None,
    is_initializer_shared: bool = False
):
    """Registers a tool's definition, executor, and optional initializer."""
    definition = definition_getter()
    if tool_name != definition.tool_name:
        raise ValueError(f"Tool name mismatch for {tool_name}: definition has {definition.tool_name}")
    
    TOOL_DEFINITIONS[tool_name] = definition
    TOOL_EXECUTORS[tool_name] = executor
    if initializer and (not is_initializer_shared or initializer not in TOOL_INITIALIZERS):
        TOOL_INITIALIZERS.append(initializer)

# Register Tavily Search tool
register_tool(
    tool_name="tavily_search",
    definition_getter=get_tavily_search_tool_definition,
    executor=execute_tavily_search,
    initializer=initialize_tavily_search_tool
)

# Register Google Sheets Append tool
register_tool(
    tool_name="google_sheets_append",
    definition_getter=get_google_sheets_append_tool_definition,
    executor=execute_google_sheets_append,
    initializer=initialize_google_sheets_tool,
    is_initializer_shared=True
)

# Register Google Sheets Read tool
register_tool(
    tool_name="google_sheets_read",
    definition_getter=get_google_sheets_read_tool_definition,
    executor=execute_google_sheets_read,
    initializer=initialize_google_sheets_tool,
    is_initializer_shared=True
)

# Register Google Sheets Update tool
register_tool(
    tool_name="google_sheets_update",
    definition_getter=get_google_sheets_update_tool_definition,
    executor=execute_google_sheets_update,
    initializer=initialize_google_sheets_tool,
    is_initializer_shared=True
)

def get_all_tool_definitions() -> List[ToolDefinition]:
    """Returns a list of all registered tool definitions."""
    return list(TOOL_DEFINITIONS.values())

def get_tool_executor(tool_name: str) -> Optional[Callable[[Dict[str, Any]], Coroutine[Any, Any, Dict[str, Any]]]]:
    """Returns the executor for a given tool name."""
    return TOOL_EXECUTORS.get(tool_name)

def initialize_all_tools():
    """Initializes all registered tools."""
    unique_initializers = []
    for init_func in TOOL_INITIALIZERS:
        if init_func not in unique_initializers:
            unique_initializers.append(init_func)
    
    for initializer in unique_initializers:
        try:
            initializer()
        except Exception as e:
            print(f"Error during tool initialization: {initializer.__name__} failed with {e}")

__all__ = [
    "get_all_tool_definitions",
    "get_tool_executor",
    "initialize_all_tools",
    "TOOL_DEFINITIONS",
    "TOOL_EXECUTORS"
] 