import json
#import requests
#import os
import gradio as gr

from collections import deque
from service_stock import get_stock_price   
from service_semantic import semantic_query
from service_third import get_latest_news

print("Chat app starting...")

## Load the secrets file
from dotenv import load_dotenv

# Load the .secrets file
load_dotenv(dotenv_path="./05_src/.secrets")

CONTEXT_SIZE = 15
FORBIDDEN_TOPICS = ["CATS", "DOGS", "HOROSCOPE", "ZODIAC", "TAYLOR SWIFT"]

# memory to keep chat history
chat_memory_list = deque(maxlen=CONTEXT_SIZE)

def chat_with_bot(user_input_text: str, chat_history: list = []):
    """Main chat handler for Gradio ChatInterface."""
    if user_input_text.upper() in FORBIDDEN_TOPICS:
        response = f"Sorry, I cannot help with {user_input_text}"
    else:
        input_text_lowercase = user_input_text.lower()

        # Service 1: Stock price queries
        if "stock" in input_text_lowercase or "price" in input_text_lowercase or "quote" in input_text_lowercase:
            # Extract potential stock symbol from the user input
            words = user_input_text.upper().replace("?", "").split()
            # A ticker symbol is usually 1–5 uppercase letters
            ticker_symbol = [w for w in words if w.isalpha() and len(w) <= 5]

            # Prefer the *last* valid symbol (usually ticker at end)
            stock_symbol = ticker_symbol[-1] if ticker_symbol else None

            if stock_symbol:
                response = get_stock_price(stock_symbol)
            else:
                response = "Please provide a valid stock symbol (e.g., AAPL or MSFT)"
        
        # Service 2: Financial glossary / semantic query
        elif ("financial" in input_text_lowercase 
              or "term" in input_text_lowercase 
              or "define" in input_text_lowercase 
              or "what is" in input_text_lowercase):
    
            print("DEBUG: Using semantic_query for:", user_input_text)
            response = semantic_query(user_input_text)

        # Service 3: Open ended service performing web search
        elif "news" in input_text_lowercase or "headline" in input_text_lowercase:
            response = get_latest_news(user_input_text)

        else:
            response = "I can help with stock prices and financial terms only right now"

    # update memory list
    chat_memory_list.append({"user": user_input_text, "bot": response})

    # return bot’s response
    return response

# define the Gradio app interface
demo = gr.ChatInterface(
    fn = chat_with_bot,
    title = "Stock Prices Bot",
    description = "You can ask for a stock price! Example: *What is the price of AAPL?*",
)

if __name__ == "__main__":
    demo.launch()
