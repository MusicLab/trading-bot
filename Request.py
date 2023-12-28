import requests
import pandas as pd
import asyncio

class ApiCaller:
    def __init__(self, symbol, interval):
        self.interval = interval
        self.symbol = symbol




    async def get_klines(self):
        
        if self.interval == "1MINUTE":
            self.interval = "1m"
        elif self.interval == "15MINUTE":
            self.interval = "15m"
        elif self.interval == "1HOUR":
            self.interval = "1h"

        endpoint = f"https://api.binance.com/api/v3/klines?symbol={self.symbol}&interval={self.interval}"
        
        while True:
            try:
                response = requests.get(endpoint)
                response.raise_for_status()  # Lanza una excepción si la solicitud falla (no 200 OK)

                

                if response.status_code == 200:
                    data = response.json()

                    # proceso de respuesta
                    keys = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                            'quote_asset_volume', 'number_of_trades',
                            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
                    klines_dict = [dict(zip(keys, kline)) for kline in data]
                    df = pd.DataFrame(klines_dict)
                    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
                    df['MA_corta'] = df['close'].rolling(window=9).mean()
                    df['MA_media'] = df['close'].rolling(window=27).mean()
                    df['MA_larga'] = df['close'].rolling(window=200).mean()
                    return df
        

            except requests.exceptions.RequestException as e:
                print(f"Error de solicitud: {e}")
                print("Reintentando...")
                await asyncio.sleep(2)  # Espera antes de reintentar
