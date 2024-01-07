import aiohttp
import pandas as pd
import asyncio
import logging

class ApiCaller:
    def __init__(self, symbol, interval, testnet=False):
        self.interval = interval
        self.symbol = symbol
        self.max_retries = 3  # Máximo número de reintentos
        self.retry_interval = 5  # Intervalo de tiempo para reintentar en segundos
        self.testnet = testnet

    async def get_klines(self):

        
        if self.testnet:
            endpoint = f"https://testnet.binancefuture.com/fapi/v1/klines?symbol={self.symbol}&interval={self.interval}"
        else:
            endpoint = f"https://api.binance.com/api/v3/klines?symbol={self.symbol}&interval={self.interval}"
            
        retries = 0
        while retries < self.max_retries:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint) as response:
                        if response.status == 200:
                            data = await response.json()

                            # Proceso de respuesta...
                            keys = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                    'quote_asset_volume', 'number_of_trades',
                                    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
                            klines_dict = [dict(zip(keys, kline)) for kline in data]
                            df = pd.DataFrame(klines_dict)
                            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                            df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
                            
                            # df['MA_corta'] = df['close'].rolling(window=9).mean()
                            # df['MA_media'] = df['close'].rolling(window=27).mean()
                            # df['MA_larga'] = df['close'].rolling(window=200).mean()
                            df['MA_corta'] = df['close'].ewm(span=8, min_periods=0, adjust=False).mean()
                            df['MA_media'] = df['close'].ewm(span=21, min_periods=0, adjust=False).mean()
                            df['MA_larga'] = df['close'].ewm(span=50, min_periods=0, adjust=False).mean()
                            return df  # DataFrame resultante

                        else:
                            logging.warning(f"La solicitud falló con el código de estado {response.status}")
                            await asyncio.sleep(self.retry_interval)  # Espera antes de reintentar
                            retries += 1

            except aiohttp.ClientError as e:
                logging.error(f"Error de solicitud: {e}")
                logging.info("Reintentando...")
                await asyncio.sleep(self.retry_interval)
                retries += 1

        logging.error("Se alcanzó el máximo de reintentos")
        return None  # Retorna None si se alcanza el máximo de reintentos

# Configurar el registro de errores
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')