import os
import logging
from typing import Optional, Dict, Any, List
import asyncio

from tavily import TavilyClient
from dotenv import load_dotenv

# Assuming general MCP models are in toolkit.mcp_server.models
# Adjust import path if necessary based on final structure
from toolkit.mcp_server.models import ToolDefinition, ToolInputSchema, ToolOutputSchemaDefinition

# Load environment variables from .env file (if used, ensure .env is in the correct path relative to execution)
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

logger = logging.getLogger(__name__)

# Global Tavily client instance for this tool
tavily_client: Optional[TavilyClient] = None

def initialize_tavily_search_tool():
    """Initializes the Tavily client for the search tool."""
    global tavily_client
    if tavily_client:
        logger.info("Tavily search tool client already initialized.")
        return

    api_key = TAVILY_API_KEY # Use the module-level loaded key
    if api_key:
        tavily_client = TavilyClient(api_key=api_key)
        logger.info("Tavily client initialized successfully for tavily_search_tool.")
    else:
        logger.warning("TAVILY_API_KEY not set. Tavily search tool will be non-functional.")

def get_tavily_search_tool_definition() -> ToolDefinition:
    return ToolDefinition(
        tool_name="tavily_search",
        description="Performs a web search using the Tavily API and returns a list of relevant results including snippets and URLs.",
        inputs=[
            ToolInputSchema(name="query", description="The search query string.", type="string", required=True, example="latest news on AI model advancements"),
            ToolInputSchema(name="max_results", description="The maximum number of search results to return. Default is 5 (Min:1, Max:20).", type="integer", required=False, example=3),
            # Consider adding other Tavily parameters like search_depth if they should be exposed
        ],
        output=ToolOutputSchemaDefinition(
            type="object",
            description="An object containing the status of the search and a list of search results from Tavily.",
            # This schema should describe the raw output from tavily_client.search
            # For simplicity, we'll use a generic object type here, but a more detailed schema is better.
            # Example: properties might include 'query', 'results' (list of objects), etc.
            # The Tavily client's `search` method returns a dictionary. We should ideally define its structure.
            # For now, let's keep it somewhat aligned with the original example, but acknowledge it wraps Tavily's raw output.
            properties={
                "query": {"type": "string", "description": "The original query used for the search."},
                "response_time": {"type": "number", "description": "Time taken for the search."},
                "results": {
                    "type": "array",
                    "description": "A list of search result items from Tavily.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Title of the search result."},
                            "url": {"type": "string", "description": "URL of the search result."},
                            "content": {"type": "string", "description": "Snippet or summary of the content."},
                            "score": {"type": "number", "description": "Relevance score from Tavily."},
                            "raw_content": {"type": "string", "description": "Raw content (if available from Tavily).", "nullable": True}
                        }
                    }
                },
                # Add other fields that Tavily client returns if they are consistently present and useful, e.g.:
                # "company_name_and_role": {"type": "string", "description": "Company name and role context if applicable."}
            },
            example={
                "query": "example query",
                "response_time": 0.5,
                "results": [
                    {
                        "title": "Example Tavily Result",
                        "url": "https://example.com/tavily-result",
                        "content": "Snippet of the Tavily search result...",
                        "score": 0.92,
                        "raw_content": None
                    }
                ]
            }
        )
    )

async def execute_tavily_search(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes the Tavily search with the given inputs.
    Returns a dictionary structured for the MCP tool_execution_payload:
    { "status": "success" | "failure", "output": <tavily_response_dict> | None, "error": <error_message> | None }
    """
    global tavily_client
    if not tavily_client:
        logger.error("Tavily client not initialized for execute_tavily_search.")
        return {"status": "failure", "output": None, "error": "Tool error: Tavily client not initialized."}

    query = inputs.get("query")
    if not query or not isinstance(query, str):
        return {"status": "failure", "output": None, "error": "Invalid input: 'query' is missing or not a string."}

    try:
        logger.info(f"Executing tavily_search with query: '{query}'") # Corrected logging quote
        search_depth = inputs.get("search_depth", "advanced") # Default to advanced as in original main.py
        max_results = inputs.get("max_results", 5) # Default to 5 as in original

        if not isinstance(search_depth, str) or search_depth not in ["basic", "advanced"]:
            search_depth = "advanced"
        if not isinstance(max_results, int) or not (0 < max_results <= 20):
            max_results = 5

        # Run the blocking Tavily SDK call in a separate thread
        raw_tavily_search_output = await asyncio.to_thread(
            tavily_client.search, # The blocking function
            query=query,          # Arguments to the function
            search_depth=search_depth,
            max_results=max_results
            # include_answer=False, # Can be a configurable input if added to schema
        )
        
        # The output schema defined earlier should match the structure of raw_tavily_search_output.
        # Tavily client itself returns a dict. We assume this dict is the desired output.
        return {"status": "success", "output": raw_tavily_search_output, "error": None}

    except Exception as e:
        logger.error(f"Error during Tavily search execution: {e}", exc_info=True)
        return {"status": "failure", "output": None, "error": f"Tool execution error: {str(e)}"}

# Example of how to initialize (e.g., called from server startup)
# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     initialize_tavily_search_tool()
#     if tavily_client:
#         print("Tavily client initialized for standalone test.")
#         # Example execution (requires asyncio for async def)
#         async def test_run():
#             result = await execute_tavily_search({"query": "hello world"})
#             print(json.dumps(result, indent=2))
#         asyncio.run(test_run())
#     else:
#         print("Failed to initialize Tavily client for standalone test.") 