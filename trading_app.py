import requests
import ccxt
import time
import threading
import ta
from dotenv import load_dotenv
import os
import argparse

load_dotenv()

class TradingBot:
    def __init__(self, api_key, api_secret):
        self.exchange = ccxt.gateio({
            'apiKey': api_key,
            'secret': api_secret,
            'options': {
                'adjustForTimeDifference': True,
            },
        })

    def fetch_balance(self):
        try:
            balance = self.exchange.fetch_balance()
            return balance
        except Exception as e:
            print(f"An error occurred while fetching balance: {e}")
            return None

    def fetch_ohlcv(self, symbol, timeframe='1h', limit=100):
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return ohlcv
        except Exception as e:
            print(f"An error occurred while fetching OHLCV data: {e}")
            return []

    def calculate_sma(self, ohlcv, period=20):
        if len(ohlcv) < period:
            return None
        closes = [x[4] for x in ohlcv]
        sma = ta.trend.SMAIndicator(ta.utils.pd.Series(closes), window=period).sma_indicator()
        return sma.iloc[-1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Trading Bot')
    parser.add_argument('--symbol', type=str, default='BTC/USDT', help='The trading symbol to use')
    parser.add_argument('--timeframe', type=str, default='1h', help='The timeframe to use for OHLCV data')
    parser.add_argument('--limit', type=int, default=100, help='The number of candles to fetch')
    parser.add_argument('--sma_period', type=int, default=20, help='The period for the SMA calculation')
    args = parser.parse_args()

    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    if not api_key or not api_secret:
        print("API_KEY and API_SECRET must be set in the .env file.")
    else:
        bot = TradingBot(api_key, api_secret)
        ohlcv = bot.fetch_ohlcv(args.symbol, args.timeframe, args.limit)
        if ohlcv:
            print(f"Successfully fetched OHLCV data for {args.symbol}.")
            sma = bot.calculate_sma(ohlcv, args.sma_period)
            if sma:
                print(f"Current SMA ({args.sma_period}) for {args.symbol}: {sma}")
