# Mochi Toolkit 🛠️

A collection of tools and utilities designed to extend the capabilities of the Mochi Worker Agent through the Model Context Protocol (MCP). This toolkit provides a standardized way to add new tools and serve them via MCP for integration with AI agents.

## 🌟 Features

- **MCP Server Integration**: Built-in MCP JSON-RPC server for seamless tool discovery and execution
- **Modular Tool Architecture**: Easy-to-extend framework for adding new tools
- **Standardized Tool Definitions**: Consistent schema and interface across all tools
- **Async Tool Execution**: Non-blocking tool operations for better performance

## 📋 Currently Available Tools

| Tool Name | Description | Documentation |
|-----------|-------------|---------------|
| `tavily_search` | Real-time web search using Tavily API | [📖 Docs](available_tools/tavily_search/README.md) |
| `google_sheets_append` | Append data to Google Sheets | [📖 Docs](available_tools/google_sheets/README.md) |
| `google_sheets_read` | Read data from Google Sheets ranges | [📖 Docs](available_tools/google_sheets/README.md) |
| `google_sheets_update` | Update specific ranges in Google Sheets | [📖 Docs](available_tools/google_sheets/README.md) |

> 📝 **Note**: Detailed documentation, examples, and configuration for each tool can be found in their respective directories.

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Required API keys (see Configuration section)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd toolkit

# Install dependencies
pip install -r requirements.txt  # If available
```

### Running the MCP Server
```bash
# Start the MCP server
python -m toolkit.mcp_server.main

# Server will be available at http://localhost:8001
```

### Server Endpoints
- **MCP JSON-RPC**: `POST /mcp` - Main MCP protocol endpoint
- **Schema Discovery**: `GET /schema` - Get server and tool schemas

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the toolkit root directory:

For example:
```bash
# Tavily Search API
TAVILY_API_KEY=your_tavily_api_key_here
```

### Google Authentication
The Google tools use Google's Application Default Credentials. Set up authentication using one of these methods:

1. **Service Account** (Recommended for production):
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
   ```

2. **User Account** (For local development):
   ```bash
   gcloud auth application-default login
   ```

## 🔧 Usage Examples

### MCP JSON-RPC Requests

#### List Available Tools
```json
{
  "jsonrpc": "2.0",
  "method": "mcp_list_tools",
  "id": 1
}
```

#### Execute a Tool
```json
{
  "jsonrpc": "2.0",
  "method": "mcp_call_tool",
  "params": {
    "tool_id": "tavily_search",
    "inputs": {
      "query": "latest AI developments 2024",
      "max_results": 3
    }
  },
  "id": 2
}
```

### Integration with Mochi Worker Agent

Add the toolkit server to your `worker_config.yaml`:

```yaml
mcp_tool_servers:
  - name: "mochi_toolkit"
    endpoint_url: "http://localhost:8001/mcp"
    timeout_seconds: 30
    retry_attempts: 3
```

## 🏗️ Architecture

### Directory Structure
```
toolkit/
├── available_tools/           # Tool implementations
│   ├── __init__.py           # Tool registry and management
│   ├── tool_1/               # A tool + README
│   └── tool_2/               # Another tool + README
├── mcp_server/               # MCP server implementation
│   ├── main.py              # FastAPI server and routing
│   ├── tool_registry.py     # Tool discovery and execution
│   └── models.py            # Pydantic models for MCP protocol
└── README.md                # This file
```

### Tool Registration System
Tools are automatically discovered and registered through the `available_tools/__init__.py` registry. Each tool provides:
- **Definition**: Schema describing inputs, outputs, and behavior
- **Executor**: Async function implementing the tool logic
- **Initializer**: Setup function for API clients and configuration

## 🔨 Development

### Adding New Tools

1. **Create Tool Directory**:
   ```bash
   mkdir toolkit/available_tools/your_tool_name/
   ```

2. **Implement Tool Interface**:
   ```python
   # your_tool_name/your_tool.py
   from toolkit.mcp_server.models import ToolDefinition
   
   def get_your_tool_definition() -> ToolDefinition:
       return ToolDefinition(
           tool_name="your_tool_name",
           description="Description of what your tool does",
           inputs=[...],
           output=...
       )
   
   async def execute_your_tool(inputs: Dict[str, Any]) -> Dict[str, Any]:
       # Implement tool logic
       return {"status": "success", "output": result, "error": None}
   
   def initialize_your_tool():
       # Setup API clients, load config, etc.
       pass
   ```

3. **Register Tool**:
   ```python
   # In available_tools/__init__.py
   from .your_tool_name.your_tool import (
       get_your_tool_definition,
       execute_your_tool,
       initialize_your_tool
   )
   
   register_tool(
       tool_name="your_tool_name",
       definition_getter=get_your_tool_definition,
       executor=execute_your_tool,
       initializer=initialize_your_tool
   )
   ```

4. **Create Tool Documentation**:
   ```bash
   # Create detailed README for your tool
   touch toolkit/available_tools/your_tool_name/README.md
   ```

### Testing Tools
```bash
# Test individual tool functionality
python -m toolkit.available_tools.your_tool_name.your_tool

# Test MCP server integration
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"mcp_list_tools","id":1}'
```

## 🚧 Roadmap & Upcoming Tools

**More tools are actively being developed to expand the toolkit's capabilities:**

### 🔜 Planned Tools
- **Database Connectors**: PostgreSQL, MySQL, SQLite integration
- **File Operations**: Advanced file manipulation and processing
- **API Integrations**: Popular REST API connectors (GitHub, Slack, etc.)
- **Data Processing**: CSV/JSON manipulation and transformation tools
- **Cloud Services**: AWS S3, Azure Blob Storage integrations
- **Communication Tools**: Email sending, SMS notifications
- **Image Processing**: Basic image manipulation and analysis
- **Document Processing**: PDF reading, text extraction
- **Time & Scheduling**: Calendar integrations, cron-like scheduling
- **Monitoring Tools**: System metrics, health checks

### 🎯 Development Priorities
1. **Core Infrastructure**: Enhanced error handling, logging, and monitoring
2. **Documentation**: Comprehensive tool documentation and examples
3. **Testing Framework**: Unit and integration tests for all tools
4. **Security**: Authentication, authorization, and input validation
5. **Performance**: Caching, connection pooling, and optimization

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest new tools.

### Development Guidelines
- Follow the established tool interface patterns
- Include comprehensive error handling
- Add proper logging and documentation
- Create a detailed README for each tool in its directory
- Test tools both standalone and via MCP server
- Update the main README's tool table when adding new tools

## 🔗 Related Projects

- [Mochi Worker Agent](../worker/) - The main agent framework that uses these tools
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) - The protocol specification

---

**Status**: 🚧 Active development - New tools are being added regularly to expand the toolkit's capabilities.