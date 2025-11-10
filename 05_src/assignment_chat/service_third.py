"""
Service 3: Open ended Services performing Web Search

This service allows to fetch live information from the web. Example: Latest stock news headlines or financial tips.
"""

import requests
import os
import requests
import json

print("------Open ended Service performing Web search------")

from dotenv import load_dotenv

# Dynamically find the absolute path to the .secrets file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # goes two levels up
secrets_path = os.path.join(BASE_DIR, ".secrets")

## Load the secrets file
print(f"Loading secrets from: {secrets_path}")  # optional debug
load_dotenv(dotenv_path=secrets_path)

BASE_URL = "https://newsapi.org/v2/top-headlines"
COUNTRY_NAME = "us"
FALLBACK_URL = "https://newsapi.org/v2/everything"

news_api_key = os.getenv("NEWS_API_KEY")
if not news_api_key:
    raise ValueError("News API key not found. Check your .env or environment variables")
        

def get_latest_news(user_input: str, max_results: int = 5) -> str:
    """
    Fetch latest news, if no headlines found, fetch using 'everything' search
    """
    category = "business" if "business" in user_input.lower() else "general"
    
    print(f"User Input:{user_input}, category: {category}")

    # Prepare NewsAPI parameters
    params = {
        "category": category,
        "country": COUNTRY_NAME,         
        "apiKey": news_api_key,
        "pageSize": max_results
    }

    print("Fetch the latest news from NewsAPI")
    response = requests.get(BASE_URL, params=params)
    latest_news = response.json()

    print("API responded:\n", json.dumps(latest_news, indent=2))

    # Extract articles
    articles = latest_news.get("articles", [])
    if not articles:
        print("Sorry, No top headlines found — falling back to keyword search")
        query = "business OR finance OR stock OR economy OR market"
        params = {
            "q": query,
            "sortBy": "publishedAt",
            "language": "en",
            "apiKey": news_api_key,
            "pageSize": max_results
        }
        response = requests.get(FALLBACK_URL, params=params)
        general_news = response.json()
        articles = general_news.get("articles", [])
    
        if not articles:
            return "Sorry, no recent news headlines found."
        
    # Format top articles
    news_lines = []
    for a in articles[:max_results]:
        title = a.get("title", "")
        source = a.get("source", {}).get("name", "")
        news_lines.append(f"{title} ({source})")
    
    # Combine into one readable string
    all_news_lines = "\n".join(news_lines)
    print("Final formatted news:\n", all_news_lines)

    return all_news_lines

