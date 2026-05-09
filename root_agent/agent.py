import os
import google.auth
import google.auth.transport.requests
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

MAPS_API_KEY = os.environ.get("MAPS_API_KEY", "AIzaSyAsyEultV_xe-aCbIxGzT7-9TKIZ1C6lAg")

maps_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://mapstools.googleapis.com/mcp",
        headers={"X-Goog-Api-Key": MAPS_API_KEY},
        timeout=120,
    )
)

credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
credentials.refresh(google.auth.transport.requests.Request())

bigquery_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://bigquery.googleapis.com/mcp",
        headers={"Authorization": "Bearer " + credentials.token},
        timeout=120,
    )
)

root_agent = LlmAgent(
    model="gemini-2.5-pro",
    name="root_agent",
    instruction="""You are an expert Location Intelligence assistant for bakery business decisions.
For foot traffic queries, use BigQuery — billing project is bakery-agent-demo. Use list_table_ids first to discover available tables, then query them. Write SQL yourself.
Use search_places to find competitors and validate locations.
Always include a Google Maps link in your final response.
You can also answer general knowledge questions.""",
    tools=[maps_toolset, bigquery_toolset],
)
