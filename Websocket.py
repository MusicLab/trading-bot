import json
import websockets
from datetime import datetime
import asyncio

class Websocket:
    def __init__(self):
        self.ws = None
        self.origen = None

    async def conectar_socket(self, origen):
        self.origen = origen
        if origen == "1MINUTE":
            self.ws = await websockets.connect("wss://fstream.binance.com/ws/btcusdt@kline_1m")
            print("CONECTE SOCKET 1MINUTE")
        elif origen == "15MINUTE":
            self.ws = await websockets.connect("wss://fstream.binance.com/ws/btcusdt@kline_15m")
            print("CONECTE SOCKET 15MINUTE")
        elif origen == "1HOUR":
            self.ws = await websockets.connect("wss://fstream.binance.com/ws/btcusdt@kline_1h")
            print("CONECTE SOCKET 1HOUR")

    async def recibir_y_procesar(self):
        try:
            async for msg in self.ws:
                res = json.loads(msg)
                if res['k']['x'] == True:
                    resProcesada = await self.procesar_mensaje(res)
                    return resProcesada
        except websockets.exceptions.ConnectionClosedError:
            print("Websocket desconectado. Intentando reconectar...")
            await self.reconectar()

    async def procesar_mensaje(self, res):
        resProcesada = {
            'event_type': res['e'],
            'event_time': datetime.fromtimestamp(res['E'] / 1000).isoformat(),
            'symbol': res['s'],
            'kline_start_time': datetime.fromtimestamp(res['k']['t'] / 1000).isoformat(),
            'kline_close_time': datetime.fromtimestamp(res['k']['T'] / 1000).isoformat(),
            'close_price': float(res['k']['c']),
            'high_price': float(res['k']['h']),
            'low_price': float(res['k']['l']),
            'base_asset_volume': float(res['k']['v']),
            'number_of_trades': int(res['k']['n'])
        }
        return resProcesada

    async def reconectar(self):
        while True:
            try:
                await self.conectar_socket(self.origen)
                print("Reconexión exitosa!")
                return
            except Exception as e:
                print(f"Error al reconectar: {e}")
                await asyncio.sleep(5)

    async def cerrar_conexion(self):
        await self.ws.close()