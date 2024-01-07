from datetime import datetime
from DatabaseManager import DatabaseManager





def integridadKlines (mensaje, klines):
    minutoMensaje = datetime.fromisoformat(mensaje['kline_close_time']).minute
    minutoRequest = klines['close_time'].iloc[-1].minute


    if minutoMensaje == minutoRequest:

        return klines
    elif minutoMensaje != minutoRequest:

        return klines[:-1]
    

def obtenerSuma():
    db = DatabaseManager("trading-bot.db")
    db.conectar()
    ordenes = db.leer_db_ordenes()
    print(ordenes)


    