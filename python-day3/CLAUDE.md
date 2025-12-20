# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit dashboard application that visualizes Japanese economic indicators by fetching real-time data from Japan's official e-Stat API. The dashboard displays:
- **Consumer Price Index (CPI)** - 2020 base year
- **Economic Sentiment Index (CI一致指数)** - 2020 base year

## Running the Application

Start the Streamlit dashboard:
```bash
streamlit run dashboard.py
```

Access the dashboard at http://localhost:8501

**Prerequisite:** Create a `.env` file with your e-Stat API key:
```
ESTAT_API_KEY=your_api_key_here
```

To obtain an API key, register at https://www.e-stat.go.jp/api/

## Development Commands

Install dependencies:
```bash
pip3 install streamlit requests pandas plotly python-dotenv
```

Run API exploration test scripts:
```bash
# Test Consumer Price Index API endpoint
python3 test_estat.py

# Test Economic Sentiment Index API endpoint
python3 test_keiki.py

# Test detailed Economic Sentiment Index data retrieval
python3 test_keiki_detail.py
```

These test scripts help explore available statistics tables and validate API parameters before integrating into the main dashboard.

## Architecture

### Data Fetching Functions

**`get_keiki_data()`** - Retrieves Economic Sentiment Index (景気動向指数)
- Statistics ID: `0003446461` (long-term series)
- Category: CI concordance index (`cdCat01: "100"`)
- Retrieves 1000 records to get full historical data
- **Important:** Sorts by time descending and removes duplicates to get latest data

**`get_cpi_data()`** - Retrieves Consumer Price Index (消費者物価指数)
- Statistics ID: `0003427113` (2020 base year)
- Category: Overall index (`cdCat01: "0001"`)
- Area: All Japan (`cdArea: "13A01"`)
- Retrieves 50 most recent records

### Data Flow

1. Load API key from `.env` using `python-dotenv`
2. Make HTTP GET requests to e-Stat API endpoints
3. Parse JSON responses with comprehensive error handling
4. Transform to pandas DataFrames with Japanese column names
5. Convert time codes (e.g., `2025001111` → `2025年11月`)
6. Visualize with Plotly interactive line charts
7. Display in Streamlit tables (recent 12 months + expandable full data)

### Caching Strategy

Both data functions use `@st.cache_data` decorator to cache API responses and avoid redundant requests during the Streamlit session.

## e-Stat API Integration

Base URL: `https://api.e-stat.go.jp/rest/3.0/app/json/`

Endpoints used:
- `getStatsList` - Search for statistics tables
- `getStatsData` - Retrieve actual data values

Required parameters:
- `appId` - Your API key
- `statsDataId` - Statistics table identifier
- `cdCat01` - Category/classification code
- `limit` - Maximum number of records to retrieve
- `metaGetFlg: "Y"` - Include metadata

### Data Retrieval Considerations

**Economic Sentiment Index:**
- API returns data from oldest to newest
- Use `limit: 1000` to retrieve full historical dataset
- Sort descending by `@time` field after retrieval
- Remove duplicates (some time periods have multiple table versions)
- Extract most recent 12 months from sorted data

**Consumer Price Index:**
- API returns chronological data
- `limit: 50` is sufficient for recent data display
- Data is already in chronological order

## Configuration

**`.env` file** (REQUIRED, not committed to git):
```
ESTAT_API_KEY=<your_api_key>
```

This file is excluded via `.gitignore` to prevent committing sensitive credentials.
