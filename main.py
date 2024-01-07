import sys
import asyncio
from Websocket import Websocket
from PublicApi import ApiCaller
from DatabaseManager import DatabaseManager
from Utilities import *
from Orden import Orden
import requests
import websockets
from loggerConfig import logger







async def main(interval):
    

    db = DatabaseManager("trading-bot.db")
    db.conectar()
    db.crear_tabla_klines()
    db.crear_tabla_ordenes()

    websocket = Websocket()
    await websocket.conectar_socket(interval, testnet=True)
    api_caller = ApiCaller("BTCUSDT", interval, testnet=True)

    # Vinculamos el websocket y la llamada a la API
    websocket.api_caller = api_caller

    while True:
        try:
            mensaje = await websocket.recibir_y_procesar()
            if mensaje is not None:
                db.guardar_kline_en_db(mensaje, interval)
                klines = await api_caller.get_klines()
                if klines is not None:
                    klinesIntegras = integridadKlines(mensaje, klines)
                    Orden("klines" + interval).procesarOrdenDb(klinesIntegras, db)

            if mensaje == "STOP":
                break  # Sale del bucle si el mensaje es "STOP"

        except (requests.exceptions.RequestException, websockets.exceptions.ConnectionClosedError) as e:
            logger.error(f"Error de conexión: {e}")
            logger.info("Intentando reconectar...")
            await websocket.reconectar()

        except Exception as ex:
            logger.error(f"Error inesperado: {ex}")

    await websocket.cerrar_conexion()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <origen>")
        sys.exit(1)
    interval = sys.argv[1]  # Obtenemos el interval desde la línea de comandos

    

    asyncio.run(main(interval))