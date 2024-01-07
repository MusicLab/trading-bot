from PrivateApi import PrivateApi
from envTestFutures import api_key, api_secret


class Orden:
    def __init__(self, interval):
        self.interval = interval



    def procesarOrdenDb(self, df, db):
        ma_corta = df['MA_corta'].iloc[-1]
        ma_corta_pre = df['MA_corta'].iloc[-2]
        ma_media = df['MA_media'].iloc[-1]
        ma_media_pre = df['MA_media'].iloc[-2]
        ma_larga = df['MA_larga'].iloc[-1]
        ma_larga_pre = df['MA_larga'].iloc[-2]

        corte_corta_media = ma_corta_pre < ma_media_pre and ma_corta > ma_media
        corte_media_corta = ma_corta_pre > ma_media_pre and ma_corta < ma_media

        corte_corta_larga = ma_corta_pre < ma_larga_pre and ma_corta > ma_larga
        corte_larga_corta = ma_corta_pre > ma_larga_pre and ma_corta < ma_larga

        corte_media_larga = ma_media_pre < ma_larga_pre and ma_media > ma_larga
        corte_larga_media = ma_media_pre > ma_larga_pre and ma_media < ma_larga

        if (corte_corta_media and ma_corta > ma_larga) or (corte_corta_larga and ma_corta > ma_media):
            print("Abre long")
            db.guardar_orden_db(df.tail(1), "long", "abierto", self.interval)
            request = PrivateApi("BTCUSDT",api_key, api_secret, testnet=True)
            get_position = float(request.get_positions()[0]['positionAmt'])
            if get_position < 0:
                request.abrir_posicion("BUY", 0.2)
            elif get_position == 0:
                request.abrir_posicion("BUY", 0.1)    
            else: 
                pass



        elif (corte_media_corta and ma_corta < ma_larga) or (corte_media_larga and ma_corta < ma_media):
            print("Abre short")
            db.guardar_orden_db(df.tail(1), "short", "abierto", self.interval)
            request = PrivateApi("BTCUSDT",api_key, api_secret, testnet=True)
            get_position = float(request.get_positions()[0]['positionAmt'])
            if get_position > 0:
                request.abrir_posicion("SELL", 0.2)
            elif get_position == 0:
                request.abrir_posicion("SELL", 0.1)    
            else: 
                pass

        

    


        






