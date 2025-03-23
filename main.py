
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd

app = FastAPI()

# Allow requests from GPT
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stock/{symbol}")
def get_stock_data(symbol: str, period: str = "3mo", interval: str = "1d"):
    ticker = f"{symbol.upper()}.NS"
    data = yf.Ticker(ticker).history(period=period, interval=interval)

    if data.empty:
        return {"error": "No data found"}

    data.reset_index(inplace=True)
    data['Date'] = data['Date'].astype(str)

    return {
        "symbol": symbol.upper(),
        "data": data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].to_dict(orient='records')
    }

