cat > ~/mcp_bakery_app/README.md << 'EOF'
# 🥐 Bakery Location Intelligence Agent

> An AI-powered location intelligence agent built with **Google ADK**, **Gemini 3.1 Pro**, and **MCP servers** (BigQuery + Google Maps) — helping bakery owners make smarter decisions about foot traffic, competitor locations, pricing, and customer demographics.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python) ![Google ADK](https://img.shields.io/badge/Google%20ADK-1.33.0-4285F4?logo=google) ![Gemini](https://img.shields.io/badge/Gemini-3.1%20Pro-purple?logo=google) ![BigQuery](https://img.shields.io/badge/BigQuery-MCP-orange?logo=googlebigquery) ![Maps](https://img.shields.io/badge/Google%20Maps-MCP-green?logo=googlemaps)

---

## 🧠 What It Does

Ask natural language questions and get data-driven answers:

- *"What are the busiest morning hours at bakeries near Connaught Place?"*
- *"Find competitor bakeries within 2km of my location in Bangalore"*
- *"Analyze weekly sales trends and compare with foot traffic patterns"*
- *"What demographics live near high foot-traffic zones in Delhi?"*

The agent autonomously decides which tools to call, queries **BigQuery** for internal business data, and uses **Google Maps** for real-world location intelligence — all in a single conversational interface powered by Gemini.

---

## 🏗️ Architecture

\`\`\`mermaid
flowchart LR
    subgraph INPUT["INPUT"]
        direction TB
        USER(["👤 User"])
        WEBUI["ADK Web UI"]
        USER --> WEBUI
    end

    subgraph CORE["AGENT CORE"]
        AGENT["🤖 Gemini 3.1 Pro\nADK Agent"]
    end

    subgraph MAPS_MCP["Google Maps MCP"]
        direction TB
        MAPS_EP["mapstools.googleapis.com/mcp"]
        SP["search_places"]
        CR["compute_routes"]
        MAPS_EP --> SP
        MAPS_EP --> CR
    end

    subgraph BQ_MCP["BigQuery MCP"]
        direction TB
        BQ_EP["bigquery.googleapis.com/mcp"]
        T1["demographics"]
        T2["bakery_prices"]
        T3["sales_history"]
        T4["foot_traffic"]
        BQ_EP --> T1
        BQ_EP --> T2
        BQ_EP --> T3
        BQ_EP --> T4
    end

    WEBUI -->|"User Query"| AGENT
    AGENT -->|"Intelligence Response"| WEBUI
    AGENT -- "API Key" --> MAPS_EP
    AGENT -- "OAuth Bearer" --> BQ_EP
\`\`\`

### How It Works

1. **User** sends a natural language query via **ADK Web UI** (port 8000)
2. **Gemini 3.1 Pro Agent** orchestrates — understands intent and decides which MCP tool(s) to call
3. For **location queries** → calls \`mapstools.googleapis.com/mcp\` via API Key → runs \`search_places\` / \`compute_routes\`
4. For **data queries** → calls \`bigquery.googleapis.com/mcp\` via OAuth Bearer → queries one of 4 structured tables
5. Agent synthesizes all outputs and returns a natural language **Intelligence Response**

---

## 📁 Project Structure

\`\`\`text
mcp_bakery_app/
├── root_agent/
│   └── mcp_bakery_app/
│       ├── agent.py          # Root agent + MCP toolset configs
│       ├── tools.py          # Custom tool wrappers
│       ├── __init__.py       # Agent module entry point
│       └── .env              # API keys (never committed)
├── .gitignore
├── .env                      # Root-level env fallback
└── README.md
\`\`\`

---

## 🗄️ BigQuery Dataset

**Project:** \`bakery-agent-demo\` | **Dataset:** \`mcp_bakery\`

| Table | Description | Key Fields |
|---|---|---|
| \`foot_traffic\` | Hourly foot traffic by location & day | \`location\`, \`hour\`, \`day_of_week\`, \`traffic_count\` |
| \`demographics\` | Neighborhood demographic profiles | \`area\`, \`age_group\`, \`income_bracket\`, \`population\` |
| \`bakery_prices\` | Competitor pricing by product | \`bakery_name\`, \`item\`, \`price\`, \`location\` |
| \`sales_history_weekly\` | Weekly sales records by product | \`week\`, \`product\`, \`units_sold\`, \`revenue\` |

---

## ⚙️ Tech Stack

| Component | Technology |
|---|---|
| Agent Framework | Google ADK \`1.33.0\` |
| LLM | Gemini 3.1 Pro Preview (Vertex AI) |
| MCP Protocol | MCP \`1.27.1\` · Streamable HTTP |
| Data Source | Google BigQuery (MCP Server) |
| Location Intelligence | Google Maps Platform (MCP Server) |
| Web Server | FastAPI + Uvicorn |
| Auth | Google ADC (BigQuery) + API Key (Maps) |
| Runtime | Python 3.12 · Google Cloud Shell |

---

## 🚀 Setup & Running

### Prerequisites

- Google Cloud Project with billing enabled
- APIs enabled: BigQuery, Maps Platform, Cloud Resource Manager, Vertex AI
- Google Cloud Shell (or local \`gcloud\` setup)

### 1. Clone the Repo

\`\`\`bash
git clone https://github.com/YOUR_USERNAME/mcp-bakery-agent.git
cd mcp-bakery-agent
\`\`\`

### 2. Configure Environment

\`\`\`bash
cat > .env << 'ENVEOF'
MAPS_API_KEY=your_google_maps_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
GOOGLE_API_KEY=your_gemini_api_key
ENVEOF
\`\`\`

> 🔐 \`.env\` is in \`.gitignore\` — keys are never committed to git.

### 3. Install Dependencies

\`\`\`bash
pip install google-adk
\`\`\`

### 4. Authenticate with Google Cloud

\`\`\`bash
gcloud auth application-default login
\`\`\`

### 5. Launch the Agent

\`\`\`bash
# One-command launch (recommended):
start-bakery

# Or manually:
export GOOGLE_API_KEY="your_gemini_key"
export MAPS_API_KEY="your_maps_key"
export GOOGLE_MAPS_API_KEY="your_maps_key"
cd ~/mcp_bakery_app
adk web --allow_origins "regex:https://.*\.cloudshell\.dev"
\`\`\`

### 6. Open the UI

Go to **Web Preview → Port 8000** in Cloud Shell.

---

## 💬 Example Queries

\`\`\`text
"What are the peak foot traffic hours on weekday mornings?"
"Find all bakeries within 3km of MG Road, Bangalore"
"Which neighborhoods have the highest income demographics near Bandra?"
"Compare croissant prices across competitor bakeries in South Delhi"
"Show me weekly sales trends for the last 4 weeks"
\`\`\`

---

## 🛠️ Persistent Shell Alias

Add to \`~/.bashrc\` for one-command startup on every Cloud Shell session:

\`\`\`bash
alias start-bakery='export PATH="$HOME/.local/bin:$PATH" && \
  export GOOGLE_API_KEY="your_key" && \
  export MAPS_API_KEY="your_key" && \
  export GOOGLE_MAPS_API_KEY="your_key" && \
  cd ~/mcp_bakery_app && \
  adk web --allow_origins "regex:https://.*\.cloudshell\.dev"'
\`\`\`

Then every new session is just:

\`\`\`bash
source ~/.bashrc && start-bakery
\`\`\`

---

## 🔐 Security Checklist

- ✅ \`.env\` in \`.gitignore\` — keys never pushed to GitHub
- ✅ \`agent.py\` uses \`os.environ.get()\` — no hardcoded keys in source
- ✅ BigQuery auth via Google ADC — no service account key files
- ✅ Maps API key scoped to Maps Platform only
- ✅ Pre-push check: \`git show HEAD | grep "AIzaSy"\` should return nothing

---

## 📌 Based On

Original sample: [google/mcp](https://github.com/google/mcp) → \`examples/launch-my-bakery\`

---

## 🙋 Author

**Kaustav Kar** · Built on Google Cloud Shell · May 2026
EOF
