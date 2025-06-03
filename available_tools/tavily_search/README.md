# Tavily Search Tool 🔍

A powerful web search tool that integrates with the Tavily API to provide real-time search results with relevance scoring and rich metadata. This tool enables AI agents to search the web and retrieve current information from across the internet.

## 🌟 Features

- **Real-time Web Search**: Access current information from across the web
- **Relevance Scoring**: Results ranked by relevance with numerical scores
- **Configurable Search Depth**: Choose between basic and advanced search modes
- **Flexible Result Limits**: Control the number of results (1-20)
- **Rich Metadata**: Includes titles, URLs, content snippets, and raw content
- **Async Execution**: Non-blocking operations for better performance
- **Error Handling**: Comprehensive error reporting and graceful failures

## 📋 Tool Specifications

- **Tool Name**: `tavily_search`
- **Type**: Web Search
- **Protocol**: MCP (Model Context Protocol)
- **API Provider**: Tavily
- **Response Format**: JSON with structured search results

## ⚙️ Configuration

### Prerequisites
- Tavily API account and API key
- Python 3.13+
- Internet connection for API calls

### Environment Setup

1. **Get Tavily API Key**:
   - Sign up at [Tavily](https://tavily.com)
   - Generate an API key from your dashboard

2. **Set Environment Variable**:
   ```bash
   # Add to your .env file
   TAVILY_API_KEY=your_tavily_api_key_here
   
   # Or export directly
   export TAVILY_API_KEY="your_tavily_api_key_here"
   ```

### Dependencies
```bash
pip install tavily-python python-dotenv
```

## 🔧 Usage

### Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | ✅ Yes | - | The search query string |
| `max_results` | integer | ❌ No | 5 | Maximum number of results (1-20) |
| `search_depth` | string | ❌ No | "advanced" | Search depth: "basic" or "advanced" |

### Output Schema

```json
{
  "status": "success|failure",
  "output": {
    "query": "original search query",
    "response_time": 0.5,
    "results": [
      {
        "title": "Page title",
        "url": "https://example.com",
        "content": "Content snippet...",
        "score": 0.92,
        "raw_content": "Full content if available"
      }
    ]
  },
  "error": null
}
```

### MCP JSON-RPC Examples

#### Basic Search
```json
{
  "jsonrpc": "2.0",
  "method": "mcp_call_tool",
  "params": {
    "tool_id": "tavily_search",
    "inputs": {
      "query": "latest AI developments 2024"
    }
  },
  "id": 1
}
```

#### Advanced Search with Custom Parameters
```json
{
  "jsonrpc": "2.0",
  "method": "mcp_call_tool",
  "params": {
    "tool_id": "tavily_search",
    "inputs": {
      "query": "climate change renewable energy solutions",
      "max_results": 10,
      "search_depth": "advanced"
    }
  },
  "id": 2
}
```

#### Response Example
```json
{
  "jsonrpc": "2.0",
  "result": {
    "status": "success",
    "output": {
      "query": "latest AI developments 2024",
      "response_time": 0.7,
      "results": [
        {
          "title": "Major AI Breakthroughs in 2024 - TechCrunch",
          "url": "https://techcrunch.com/2024/ai-breakthroughs",
          "content": "This year has seen unprecedented advances in artificial intelligence, with major developments in large language models, computer vision, and autonomous systems...",
          "score": 0.95,
          "raw_content": null
        },
        {
          "title": "AI Research Trends 2024 | MIT Technology Review",
          "url": "https://technologyreview.com/ai-trends-2024",
          "content": "Researchers are focusing on multimodal AI, improved reasoning capabilities, and more efficient training methods...",
          "score": 0.89,
          "raw_content": null
        }
      ]
    },
    "error": null
  },
  "id": 1
}
```

## 🚀 Programming Interface

### Direct Python Usage

```python
import asyncio
from toolkit.available_tools.tavily_search.tavily_search_tool import (
    initialize_tavily_search_tool,
    execute_tavily_search
)

# Initialize the tool
initialize_tavily_search_tool()

async def search_example():
    # Basic search
    result = await execute_tavily_search({
        "query": "Python async programming best practices"
    })
    print(result)
    
    # Advanced search with parameters
    result = await execute_tavily_search({
        "query": "machine learning model deployment",
        "max_results": 8,
        "search_depth": "advanced"
    })
    print(result)

# Run the example
asyncio.run(search_example())
```

### Integration with Mochi Agent

```python
# In your agent configuration
mcp_tool_servers = [
    {
        "name": "tavily_search_server",
        "endpoint_url": "http://localhost:8001/mcp",
        "timeout_seconds": 30
    }
]

# Tool will be automatically discovered and available as "tavily_search"
```

## 🎯 Use Cases

### Information Research
- **Current Events**: "latest developments in quantum computing"
- **Market Research**: "electric vehicle market trends 2024"
- **Academic Research**: "recent studies on climate change mitigation"

### Fact Checking
- **Verification**: "is the new AI regulation in EU effective"
- **Statistics**: "global renewable energy adoption rates"
- **News Validation**: "recent merger between tech companies"

### Competitive Analysis
- **Product Research**: "best project management tools 2024"
- **Feature Comparison**: "ChatGPT vs Claude capabilities"
- **Market Position**: "top cloud storage providers comparison"

## 🔍 Search Depth Options

### Basic Search
- **Faster results**: Lower latency for quick queries
- **Lighter processing**: Less comprehensive but more efficient
- **Use case**: Simple fact lookups, quick reference checks

### Advanced Search (Recommended)
- **Comprehensive results**: More thorough search across diverse sources
- **Better relevance**: Improved ranking and content quality
- **Use case**: Research tasks, detailed information gathering

## ⚠️ Error Handling

### Common Error Scenarios

#### API Key Not Set
```json
{
  "status": "failure",
  "output": null,
  "error": "Tool error: Tavily client not initialized."
}
```

#### Invalid Query
```json
{
  "status": "failure",
  "output": null,
  "error": "Invalid input: 'query' is missing or not a string."
}
```

#### API Rate Limiting
```json
{
  "status": "failure",
  "output": null,
  "error": "Tool execution error: Rate limit exceeded. Please try again later."
}
```

#### Network Issues
```json
{
  "status": "failure",
  "output": null,
  "error": "Tool execution error: Network connection failed."
}
```

## 🛠️ Troubleshooting

### Setup Issues

**Problem**: "Tavily client not initialized"
- **Solution**: Ensure `TAVILY_API_KEY` is set in environment
- **Check**: Verify API key is valid and active

**Problem**: Import errors
- **Solution**: Install required dependencies:
  ```bash
  pip install tavily-python python-dotenv
  ```

### Runtime Issues

**Problem**: Empty or poor quality results
- **Solution**: 
  - Try different search terms
  - Use "advanced" search depth
  - Increase `max_results`

**Problem**: Slow response times
- **Solution**:
  - Use "basic" search depth for faster results
  - Reduce `max_results` count
  - Check internet connection

**Problem**: Rate limiting errors
- **Solution**:
  - Implement request delays
  - Upgrade Tavily API plan
  - Cache results when possible

## 📊 Performance Considerations

### Response Times
- **Basic Search**: ~0.3-0.8 seconds
- **Advanced Search**: ~0.5-1.5 seconds
- **Factors**: Query complexity, result count, network latency

### Rate Limits
- **Free Tier**: Limited requests per month
- **Paid Plans**: Higher rate limits available
- **Recommendation**: Monitor usage and implement caching

### Best Practices
- **Cache Results**: Store results for repeated queries
- **Batch Processing**: Group related searches when possible
- **Error Handling**: Implement retry logic with exponential backoff
- **Monitoring**: Track API usage and response times

## 🔒 Security & Privacy

### API Key Security
- Never commit API keys to version control
- Use environment variables or secure key management
- Rotate keys periodically

### Query Privacy
- Search queries are sent to Tavily's servers
- Review Tavily's privacy policy for data handling
- Consider query sensitivity in your applications

## 📈 Monitoring & Analytics

### Key Metrics to Track
- **Search Success Rate**: Percentage of successful vs failed searches
- **Response Time**: Average API response times
- **Result Quality**: Relevance scores and user feedback
- **Usage Patterns**: Most common query types and frequencies

### Logging
The tool automatically logs:
- Search executions with query details
- Error conditions and failures
- Performance metrics and timing

## 🔄 Updates & Versioning

### Current Version
- **Tool Version**: 1.0.0
- **Tavily API**: v1
- **Last Updated**: 2024

### Changelog
- **v1.0.0**: Initial implementation with basic and advanced search
- **Future**: Planned support for image search, news-specific search

## 🤝 Contributing

### Reporting Issues
- Use GitHub issues for bug reports
- Include query examples and error messages
- Specify environment details (Python version, OS)

### Feature Requests
- Suggest new search parameters or filters
- Request integration improvements
- Propose performance optimizations

---

**Maintained by**: Mochi Agents Team  
**License**: MIT  
**Support**: [GitHub Issues](../../issues) 