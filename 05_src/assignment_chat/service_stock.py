"""
Service 1: Stock price Service

This service Fetches real-time stock prices from Alpha Vantage API and returns a user-friendly response

"""
import os
import requests
import json

from dotenv import load_dotenv

# Dynamically find the absolute path to the .secrets file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # goes two levels up
secrets_path = os.path.join(BASE_DIR, ".secrets")

## Load the secrets file

print(f"Loading secrets from: {secrets_path}")  # optional debug
load_dotenv(dotenv_path=secrets_path)

def get_stock_price(stock_symbol: str) -> str:
    """
    This function accepts a parameter - Stock symbol, calls Alpha Vantage API and returns a natural-language summary of the stock price
    """
    
    print("------Stock Price Service------")
    alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not alpha_vantage_api_key:
        raise ValueError("Alpha Vantage API key not found. Check your .env or environment variables")
        
    
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={alpha_vantage_api_key}"

    response = requests.get(url)
    stock_quote = response.json()

    print(json.dumps(stock_quote, indent=4))

    # Handle potential errors or missing data
    if "Global Quote" not in stock_quote:
        return f"Sorry, I couldn't retrieve stock information for {stock_symbol}, please try in sometime"

    quote = stock_quote["Global Quote"]
    stock_price = quote.get("05. price", "N/A")
    price_change = quote.get("09. change", "0")
    change_percent = quote.get("10. change percent", "0%")

    try:
        price = float(stock_price)
    except (TypeError, ValueError):
        return f"Stock price not available for {stock_symbol}"

    # Convert the retrived details into natural language
    if float(price_change) > 0:
        direction = "up"
    elif float(price_change) < 0:
        direction = "down"
    else:
        direction = "unchanged"

    return(
        f"\nThe current price of {stock_symbol} is USD ${float(price):.2f}. It is {direction} by {change_percent} today"
    )

# Example usage
if __name__ == "__main__":
    print(get_stock_price("META"))