import yfinance as yf
from llama_index.core.tools import FunctionTool

def calculate_ratio(numerator: float, denominator: float) -> float:
    """
    Calculates the ratio of two numbers (numerator / denominator).
    Use this tool for financial calculations like debt-to-equity, current ratio, etc.
    """
    if denominator == 0:
        return float('inf')
    return numerator / denominator

def get_stock_price(ticker: str) -> str:
    """
    Gets the latest stock price for a given ticker symbol.
    Use this tool to find the current market price of a company's stock.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        if hist.empty:
            return f"Could not find stock data for ticker: {ticker}"
        current_price = hist['Close'].iloc[-1]
        return f"The latest stock price for {ticker} is ${current_price:.2f}"
    except Exception as e:
        return f"An error occurred: {e}"

# --- Create Tool Objects ---
ratio_tool = FunctionTool.from_defaults(fn=calculate_ratio, name="financial_ratio_calculator", description="Use this tool for financial calculations like debt-to-equity, current ratio, etc.")
stock_price_tool = FunctionTool.from_defaults(fn=get_stock_price, name="stock_price_checker", description="Use this tool to find the current market price of a company's stock.")