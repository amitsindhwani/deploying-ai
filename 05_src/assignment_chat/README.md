# StockBot — AI Conversational Finance Assistant

## Overview
**StockBot** is an AI-powered chat system that combines real-time data, semantic understanding, and live web search to deliver conversational financial insights. It integrates **three distinct services** and provides a conversational interface that allows users to interact with financial data and semantic knowledge.  

It integrates **three modular services**:
1. **Service 1 — Stock Price Service (API-based)**  
2. **Service 2 — Financial Glossary Semantic Search (ChromaDB)**  
3. **Service 3 — Live News Headlines (News API)**  

The app runs as a conversational **Gradio** interface (`chat_app.py`) and supports lightweight memory and topic filtering.

----------

## Features

- **Real-time stock prices** using Alpha Vantage API  
- **Semantic search** for financial terms via ChromaDB embeddings  
- **Live business headlines** using NewsAPI (with fallback for general news)  
- **Contextual chat memory** (last 15 exchanges)  
- **Forbidden topics:** Cats, Dogs, Horoscope, Zodiac, Taylor Swift  

----------

## How Each Service Works

### **Service 1 — Stock Price Service**

**File:** `service_stock.py`  
Fetches **real-time stock quotes** using the **Alpha Vantage API** and presents the results in a user-friendly format.

**Workflow:**
1. Loads `ALPHA_VANTAGE_API_KEY` from `.secrets` file.  
2. Calls Alpha Vantage `GLOBAL_QUOTE` endpoint.  
3. Extracts stock price, percent change, and formats a summary.  
4. Handles missing or invalid stock symbols.

**Example Output:**
```
The current price of AAPL is USD $175.43. It is up by 0.65% today.
```

----------

### **Service 2 — Financial Glossary Semantic Search**

**File:** `service_semantic.py`  
Handles *“What is…”* or *“Define…”* style questions using semantic similarity search on a **ChromaDB** vector store.

**Workflow:**
1. Embeddings generated using `sentence-transformers/all-MiniLM-L6-v2`.  
2. Searches the ChromaDB vector database for top-matching financial definitions.  
3. Returns the best-matched terms with contextual answers.  

Note: I am using Financial terms glossary from the SIFMA Foundation SMG Glossary pdf (Copyright 2023 SIFMA Foundation), I copied page by page and created a csv file out of the terms listed in the pdf. The credit for the glossary goes to them.

**Example:**
```
User: What is a derivative?
Bot: Derivative — A financial instrument whose value depends on another asset such as a stock or bond.
```

----------

### **Service 3 — Live News Headlines**

**File:** `service_third.py`  
Fetches **latest news headlines** from the **NewsAPI**.  
If the input includes finance-related terms, it lists *business headlines*. Otherwise, it retrieves general top news.

**Workflow:**
1. Loads `NEWS_API_KEY` from `.secrets`.  
2. Uses `https://newsapi.org/v2/top-headlines` endpoint.  
3. Accepts optional finance-related query keywords: `finance`, `stock`, `market`, `economy`, `business`.  
4. Returns up to 3 formatted news headlines.  

**Example:**
```
Fetch the latest news from NewsAPI...
Today's Top Headlines:
- Federal Reserve signals no change in interest rates.
- Major tech stocks rally after strong earnings.
- Oil prices stabilize amid global supply concerns.
```

----------

## **Main Chat Application**

**File:** `chat_app.py`  
Manages all service interactions and chat interface.

**Core Functions:**
- Detects user intent and routes queries to one of the three services.  
- Maintains chat memory for last 15 exchanges (`deque`).  
- Blocks unrelated topics.  
- Uses **Gradio** ChatInterface for conversational flow.

----------

## **Project Structure**
```
05_src/
├── chat_app.py
├── service_stock.py
├── service_semantic.py
├── service_third.py
└── .secrets

It also includes couple of additional folders for data (.csvfile) and Output_screenshots (has screenshots of chat interfact)
```

----------

## 🧪 **Example Queries**

| Type | Example User Query | Service Used |
|------|--------------------|---------------|
| Stock | "What’s the price of MSFT?" | Stock Price API |
| Definition | "Define Asset" | Semantic Glossary |
| News | "Give me the latest headlines" | NewsAPI |

----------


## Author
**Amit Kumar Sindhwani**  
