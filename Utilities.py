from datetime import datetime





def integridadKlines (mensaje, klines):
    minutoMensaje = datetime.fromisoformat(mensaje['kline_close_time']).minute
    minutoRequest = klines['close_time'].iloc[-1].minute
    print(minutoMensaje, "MinutoMensaje", minutoRequest, "MinutoRequest")

    if minutoMensaje == minutoRequest:
        print(mensaje['close_price'], "mensaje Close", klines['close'].iloc[-1], "request close")
        return klines
    elif minutoMensaje != minutoRequest:
        print("adelantado")
        return klines[:-1]

    