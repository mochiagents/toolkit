# Google Sheets Tools 📊

A comprehensive suite of tools for interacting with Google Sheets, providing full CRUD (Create, Read, Update, Delete) operations through the Google Sheets API. These tools enable AI agents to seamlessly integrate with Google Sheets for data management, analysis, and reporting.

## 🌟 Features

- **Complete CRUD Operations**: Append, read, and update data in Google Sheets
- **Flexible Range Support**: Work with specific ranges or entire sheets
- **Multiple Value Formats**: Support for raw and formatted data input/output
- **Batch Operations**: Process multiple rows and columns efficiently
- **Error Handling**: Comprehensive error reporting with actionable messages
- **Async Execution**: Non-blocking operations for better performance
- **Authentication Integration**: Seamless Google API authentication

## 📋 Available Tools

| Tool Name | Operation | Description |
|-----------|-----------|-------------|
| `google_sheets_append` | Create | Append new rows to existing data |
| `google_sheets_read` | Read | Read data from specified ranges |
| `google_sheets_update` | Update | Update specific cells or ranges |

## ⚙️ Configuration

### Prerequisites
- Google Cloud Project with Sheets API enabled
- Service Account or OAuth2 credentials
- Python 3.13+
- Internet connection for API calls

### Google Cloud Setup

1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one

2. **Enable Google Sheets API**:
   ```bash
   # Using gcloud CLI
   gcloud services enable sheets.googleapis.com
   ```
   
   Or enable via [API Library](https://console.cloud.google.com/apis/library/sheets.googleapis.com)

3. **Set Up Authentication** (Choose one method):

#### Option A: Service Account (Recommended for Production)
```bash
# Create service account
gcloud iam service-accounts create sheets-tool-account \
    --display-name="Google Sheets Tool Service Account"

# Create and download key
gcloud iam service-accounts keys create credentials.json \
    --iam-account=sheets-tool-account@your-project.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
```

#### Option B: User Account (For Development)
```bash
# Install and initialize gcloud
gcloud auth application-default login
```

### Dependencies
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Share Sheets with Service Account
If using a service account, share your Google Sheets with the service account email:
```
sheets-tool-account@your-project.iam.gserviceaccount.com
```

## 🔧 Tool Usage

---

## 📝 Google Sheets Append

Appends new rows to the end of existing data in a Google Sheet.

### Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `spreadsheet_id` | string | ✅ Yes | - | The ID of the Google Sheet |
| `range` | string | ✅ Yes | - | A1 notation range (e.g., 'Sheet1!A:C') |
| `values` | array | ✅ Yes | - | 2D array of values to append |
| `value_input_option` | string | ❌ No | "USER_ENTERED" | How to interpret input data |
| `insert_data_option` | string | ❌ No | - | How to insert data ("OVERWRITE", "INSERT_ROWS") |

### Usage Examples

#### Basic Append
```json
{
  "jsonrpc": "2.0",
  "method": "mcp_call_tool",
  "params": {
    "tool_id": "google_sheets_append",
    "inputs": {
      "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
      "range": "Sheet1!A:C",
      "values": [
        ["John Doe", "john@example.com", "Manager"],
        ["Jane Smith", "jane@example.com", "Developer"]
      ]
    }
  },
  "id": 1
}
```

#### Append with Raw Values
```json
{
  "jsonrpc": "2.0",
  "method": "mcp_call_tool",
  "params": {
    "tool_id": "google_sheets_append",
    "inputs": {
      "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
      "range": "Data!A:D",
      "values": [
        ["2024-01-15", "=SUM(C:C)", "100", "Revenue"]
      ],
      "value_input_option": "RAW"
    }
  },
  "id": 2
}
```

---

## 📖 Google Sheets Read

Reads data from specified ranges in a Google Sheet.

### Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `spreadsheet_id` | string | ✅ Yes | - | The ID of the Google Sheet |
| `range` | string | ✅ Yes | - | A1 notation range to read |
| `major_dimension` | string | ❌ No | "ROWS" | "ROWS" or "COLUMNS" |
| `value_render_option` | string | ❌ No | "FORMATTED_VALUE" | How to render values |
| `date_time_render_option` | string | ❌ No | "SERIAL_NUMBER" | How to render dates |

### Usage Examples

#### Basic Read
```json
{
  "jsonrpc": "2.0",
  "method": "mcp_call_tool",
  "params": {
    "tool_id": "google_sheets_read",
    "inputs": {
      "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
      "range": "Sheet1!A1:C10"
    }
  },
  "id": 3
}
```

#### Read with Custom Options
```json
{
  "jsonrpc": "2.0",
  "method": "mcp_call_tool",
  "params": {
    "tool_id": "google_sheets_read",
    "inputs": {
      "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
      "range": "Data!A:Z",
      "major_dimension": "COLUMNS",
      "value_render_option": "UNFORMATTED_VALUE"
    }
  },
  "id": 4
}
```

### Response Example
```json
{
  "jsonrpc": "2.0",
  "result": {
    "status": "success",
    "output": {
      "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
      "range": "Sheet1!A1:C3",
      "major_dimension": "ROWS",
      "values": [
        ["Name", "Email", "Role"],
        ["John Doe", "john@example.com", "Manager"],
        ["Jane Smith", "jane@example.com", "Developer"]
      ]
    },
    "error": null
  },
  "id": 3
}
```

---

## ✏️ Google Sheets Update

Updates specific cells or ranges in a Google Sheet.

### Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `spreadsheet_id` | string | ✅ Yes | - | The ID of the Google Sheet |
| `range` | string | ✅ Yes | - | A1 notation range to update |
| `values` | array | ✅ Yes | - | 2D array of values to write |
| `value_input_option` | string | ❌ No | "USER_ENTERED" | How to interpret input data |

### Usage Examples

#### Update Specific Cells
```json
{
  "jsonrpc": "2.0",
  "method": "mcp_call_tool",
  "params": {
    "tool_id": "google_sheets_update",
    "inputs": {
      "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
      "range": "Sheet1!A1:B2",
      "values": [
        ["Updated Name", "updated@example.com"],
        ["Another Update", "another@example.com"]
      ]
    }
  },
  "id": 5
}
```

#### Update with Formulas
```json
{
  "jsonrpc": "2.0",
  "method": "mcp_call_tool",
  "params": {
    "tool_id": "google_sheets_update",
    "inputs": {
      "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
      "range": "Summary!A1:B1",
      "values": [
        ["Total", "=SUM(Data!C:C)"]
      ],
      "value_input_option": "USER_ENTERED"
    }
  },
  "id": 6
}
```

---

## 🚀 Programming Interface

### Direct Python Usage

```python
import asyncio
from toolkit.available_tools.google_sheets.google_sheets_tool import (
    initialize_google_sheets_tool,
    execute_google_sheets_append,
    execute_google_sheets_read,
    execute_google_sheets_update
)

# Initialize the tool
initialize_google_sheets_tool()

async def sheets_example():
    spreadsheet_id = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
    
    # Read current data
    read_result = await execute_google_sheets_read({
        "spreadsheet_id": spreadsheet_id,
        "range": "Sheet1!A:C"
    })
    print("Current data:", read_result)
    
    # Append new data
    append_result = await execute_google_sheets_append({
        "spreadsheet_id": spreadsheet_id,
        "range": "Sheet1!A:C",
        "values": [["New User", "new@example.com", "Analyst"]]
    })
    print("Append result:", append_result)
    
    # Update specific cell
    update_result = await execute_google_sheets_update({
        "spreadsheet_id": spreadsheet_id,
        "range": "Sheet1!C1",
        "values": [["Updated Role"]]
    })
    print("Update result:", update_result)

# Run the example
asyncio.run(sheets_example())
```

### Integration with Mochi Agent

```python
# In your agent configuration
mcp_tool_servers = [
    {
        "name": "google_sheets_server",
        "endpoint_url": "http://localhost:8001/mcp",
        "timeout_seconds": 30
    }
]

# Tools will be automatically discovered:
# - google_sheets_append
# - google_sheets_read
# - google_sheets_update
```

## 🎯 Common Use Cases

### Data Collection & Analysis
```python
# Read survey responses
read_surveys = {
    "spreadsheet_id": "survey_sheet_id",
    "range": "Responses!A:Z"
}

# Append new response
new_response = {
    "spreadsheet_id": "survey_sheet_id",
    "range": "Responses!A:F",
    "values": [["2024-01-15", "John", "5", "Great product", "Yes", "john@example.com"]]
}
```

### Inventory Management
```python
# Read current inventory
inventory_data = {
    "spreadsheet_id": "inventory_sheet_id",
    "range": "Stock!A:E"
}

# Update stock levels
update_stock = {
    "spreadsheet_id": "inventory_sheet_id",
    "range": "Stock!D2:D10",
    "values": [["50"], ["25"], ["100"], ["0"], ["75"], ["200"], ["150"], ["30"], ["80"]]
}
```

### Report Generation
```python
# Append daily metrics
daily_report = {
    "spreadsheet_id": "metrics_sheet_id",
    "range": "Daily!A:D",
    "values": [["2024-01-15", "1250", "98.5%", "42"]]
}

# Update summary formulas
summary_update = {
    "spreadsheet_id": "metrics_sheet_id",
    "range": "Summary!B1:B4",
    "values": [
        ["=AVERAGE(Daily!B:B)"],
        ["=MAX(Daily!C:C)"],
        ["=SUM(Daily!D:D)"],
        ["=COUNT(Daily!A:A)"]
    ]
}
```

## 📊 Understanding Google Sheets Ranges

### A1 Notation Examples
```bash
# Specific cells
"Sheet1!A1"           # Single cell
"Sheet1!A1:C3"        # Rectangle range
"Sheet1!A:A"          # Entire column A
"Sheet1!1:1"          # Entire row 1

# Named sheets
"Data!A1:Z100"        # Range in 'Data' sheet
"'My Sheet'!A1:C10"   # Sheet with spaces (use quotes)

# Open ranges
"Sheet1!A:C"          # Columns A through C (all rows)
"Sheet1!1:5"          # Rows 1 through 5 (all columns)
"Sheet1!A1:C"         # From A1 to end of column C
```

### Range Best Practices
- **Use open ranges** for append operations: `"Sheet1!A:C"`
- **Specify exact ranges** for reads: `"Sheet1!A1:C100"`
- **Include sheet names** to avoid ambiguity: `"Data!A1:C10"`
- **Use quotes for sheet names** with spaces: `"'Q1 Results'!A1:Z50"`

## ⚠️ Error Handling

### Common Error Scenarios

#### Authentication Issues
```json
{
  "status": "failure",
  "output": null,
  "error": "Tool error: Google Sheets client not initialized."
}
```

#### Invalid Spreadsheet ID
```json
{
  "status": "failure",
  "output": null,
  "error": "API error (read): 404 - Requested entity was not found."
}
```

#### Permission Denied
```json
{
  "status": "failure",
  "output": null,
  "error": "API error (append): 403 - The caller does not have permission."
}
```

#### Invalid Range Format
```json
{
  "status": "failure",
  "output": null,
  "error": "API error (update): 400 - Unable to parse range: InvalidRange"
}
```

#### Empty Data Range
```json
{
  "status": "failure",
  "output": null,
  "error": "No meaningful data found in spreadsheet range. Check: 1. Range includes sheet name (e.g., 'Sheet1!A1:Z100') 2. Cells contain non-empty values 3. Range contains actual data"
}
```

## 🛠️ Troubleshooting

### Setup Issues

**Problem**: "Google Sheets client not initialized"
- **Solution**: Check authentication setup
- **Verify**: `GOOGLE_APPLICATION_CREDENTIALS` environment variable
- **Test**: `gcloud auth application-default print-access-token`

**Problem**: Import errors
- **Solution**: Install required dependencies:
  ```bash
  pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
  ```

### Permission Issues

**Problem**: "403 - The caller does not have permission"
- **Solution**: Share the spreadsheet with your service account email
- **Check**: Service account has appropriate roles (Editor or Viewer)
- **Verify**: Spreadsheet is accessible with current credentials

**Problem**: "404 - Requested entity was not found"
- **Solution**: Verify spreadsheet ID is correct
- **Check**: Spreadsheet exists and is shared properly
- **Extract ID**: From URL `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`

### Data Issues

**Problem**: Empty results when reading
- **Solution**:
  - Verify range contains data
  - Check sheet name spelling
  - Use correct A1 notation
  - Ensure cells aren't just whitespace

**Problem**: Formulas not working
- **Solution**:
  - Use `value_input_option: "USER_ENTERED"` for formulas
  - Use `value_input_option: "RAW"` for literal values
  - Verify formula syntax is correct

## 📊 Value Input Options

### USER_ENTERED (Default)
- Parses input as if typed in the Sheets UI
- Formulas are parsed and calculated
- Dates and numbers are formatted automatically
- **Use for**: Interactive data entry, formulas

### RAW
- Input is stored exactly as provided
- No parsing or formatting
- Formulas stored as text strings
- **Use for**: Literal text, preserving exact formatting

## 🔒 Security & Privacy

### Authentication Security
- Store credentials securely (avoid hardcoding)
- Use service accounts for production
- Rotate credentials periodically
- Limit service account permissions

### Data Privacy
- Only request minimum necessary permissions
- Audit spreadsheet access regularly
- Consider data sensitivity when sharing
- Use private sheets for sensitive data

### Permission Management
```bash
# Grant minimum required access
# For read-only operations:
# - Sheets API read access
# - Viewer role on specific spreadsheets

# For write operations:
# - Sheets API write access  
# - Editor role on specific spreadsheets
```

## 📈 Performance Optimization

### Batch Operations
```python
# Instead of multiple single-cell updates
# Use range updates for better performance

# ❌ Inefficient
for i, value in enumerate(values):
    update_single_cell(f"A{i+1}", value)

# ✅ Efficient
update_range("A1:A100", values)
```

### Rate Limiting
- Google Sheets API: 100 requests per 100 seconds per user
- Implement retry logic with exponential backoff
- Cache read results when possible
- Batch multiple operations when feasible

### Response Times
- **Single cell read**: ~0.2-0.5 seconds
- **Range read (100 cells)**: ~0.3-0.8 seconds
- **Append operation**: ~0.4-1.0 seconds
- **Update operation**: ~0.3-0.7 seconds

## 📊 Monitoring & Analytics

### Key Metrics to Track
- **Operation Success Rate**: Percentage of successful vs failed operations
- **Response Time**: Average API response times per operation type
- **Error Patterns**: Common error types and frequencies
- **Usage Patterns**: Most accessed spreadsheets and ranges

### Logging
The tools automatically log:
- All API operations with parameters
- Authentication events and failures
- Error conditions with detailed context
- Performance metrics and timing

## 🔄 Updates & Versioning

### Current Version
- **Tool Version**: 1.0.0
- **Google Sheets API**: v4
- **Last Updated**: 2024

### Changelog
- **v1.0.0**: Initial implementation with append, read, and update operations
- **Future**: Planned support for batch operations, advanced formatting, chart creation

## 🤝 Contributing

### Reporting Issues
- Use GitHub issues for bug reports
- Include spreadsheet IDs (if sharable) and error messages
- Specify authentication method and environment details

### Feature Requests
- Request new operations (delete, format, charts)
- Suggest performance improvements
- Propose additional value input/output options

---

**Maintained by**: Mochi Agents Team  
**License**: MIT  
**Support**: [GitHub Issues](../../issues) 