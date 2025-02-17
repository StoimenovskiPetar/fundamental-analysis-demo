import pandas as pd
import yfinance as yf

def get_stock_info(stock):
    """Extract key stock information."""
    info = stock.info
    return {
        "Company Name": info.get("longName", "N/A"),
        "Sector": info.get("sector", "N/A"),
        "Industry": info.get("industry", "N/A"),
        "Market Cap": f"${info.get('marketCap', 0):,}",
        "P/E Ratio": round(info.get("trailingPE", 0), 2),
        "Forward P/E": round(info.get("forwardPE", 0), 2),
        "PEG Ratio": round(info.get("pegRatio", 0), 2),
        "Price to Book": round(info.get("priceToBook", 0), 2),
        "Dividend Yield": f"{info.get('dividendYield', 0)*100:.2f}%",
        "52 Week High": f"${info.get('fiftyTwoWeekHigh', 0):.2f}",
        "52 Week Low": f"${info.get('fiftyTwoWeekLow', 0):.2f}"
    }

def compare_stocks(ticker1, ticker2):
    """Compare two stocks based on key metrics."""
    stock1 = yf.Ticker(ticker1)
    stock2 = yf.Ticker(ticker2)
    
    metrics = {
        "Market Cap": ["marketCap", lambda x: f"${x:,}"],
        "P/E Ratio": ["trailingPE", lambda x: f"{x:.2f}"],
        "Forward P/E": ["forwardPE", lambda x: f"{x:.2f}"],
        "PEG Ratio": ["pegRatio", lambda x: f"{x:.2f}"],
        "Price to Book": ["priceToBook", lambda x: f"{x:.2f}"],
        "Dividend Yield": ["dividendYield", lambda x: f"{x*100:.2f}%"],
        "Profit Margin": ["profitMargins", lambda x: f"{x*100:.2f}%"],
        "Operating Margin": ["operatingMargins", lambda x: f"{x*100:.2f}%"]
    }
    
    comparison_data = {}
    for metric, (key, formatter) in metrics.items():
        comparison_data[metric] = {
            ticker1: formatter(stock1.info.get(key, 0)),
            ticker2: formatter(stock2.info.get(key, 0))
        }
    
    return pd.DataFrame(comparison_data).T
