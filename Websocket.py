import json
import websockets
from datetime import datetime
import asyncio
from loggerConfig import logger


class Websocket:
    def __init__(self):
        self.ws = None
        self.interval = None
        self.intentos_reconexion = 0
        self.max_intentos_reconexion = 15


    async def conectar_socket(self, interval, testnet = False):
        self.interval = interval

        if testnet:
            url = f"wss://stream.binancefuture.com/ws/btcusdt@kline_{self.interval}"
        else:
            url = f"wss://fstream.binance.com/ws/btcusdt@kline_{self.interval}"
        
        try:
            self.ws = await websockets.connect(url)
            mensaje = "Testnet" if testnet else "Real"
            logger.info(f"CONECTE SOCKET {interval} {mensaje}")  # Registro de información con logger
            self.intentos_reconexion = 0  # Restablecer el contador de intentos de reconexión en caso de conexión exitosa
        except Exception as e:
            logger.error(f"Error al conectar: {e}")  # Registro de error con logger
            await self.reconectar()

    async def recibir_y_procesar(self):
        try:
            async for msg in self.ws:
                res = json.loads(msg)
                if res.get('k', {}).get('x') == True:
                    resProcesada = await self.procesar_mensaje(res)
                    print(resProcesada)
                    return resProcesada
        except websockets.exceptions.ConnectionClosedError:
            logger.warning("Websocket desconectado. Intentando reconectar...")  # Registro de advertencia con logger
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
        if self.intentos_reconexion < self.max_intentos_reconexion:
            self.intentos_reconexion += 1
            await asyncio.sleep(3)  # Espera antes de intentar reconectar
            await self.conectar_socket(self.interval)
        else:
            logger.error("Se alcanzó el máximo de intentos de reconexión")  # Registro de error con logger

    async def cerrar_conexion(self):
        if self.ws:
            await self.ws.close()