class Orden:
    def __init__(self, interval):
        self.interval = interval


    def procesarOrdenDb(self, df, db):
        ma_corta = df['MA_corta'].iloc[-1]
        ma_corta_pre = df['MA_corta'].iloc[-2]
        ma_media = df['MA_media'].iloc[-1]
        ma_media_pre = df['MA_media'].iloc[-2]
        ma_larga = df['MA_larga'].iloc[-1]
        
        if ma_corta_pre < ma_media_pre and ma_corta > ma_media and ma_larga < ma_corta and ma_larga < ma_media:            
            #self.abrir_long()
            db.guardar_orden_db(df.tail(1), "long", "abierto", self.interval)
            print("se abre long")

        elif ma_corta_pre > ma_media_pre and ma_corta < ma_media and ma_larga > ma_corta and ma_larga > ma_media:
            #self.abrir_short()
            db.guardar_orden_db(df.tail(1), "short", "abierto", self.interval)
            print("se abre short")

        elif ma_corta_pre > ma_media_pre and ma_corta < ma_media and ma_larga < ma_corta and ma_larga < ma_media:
            #self.cerrar_long()
            db.guardar_orden_db(df.tail(1), "long", "cerrado", self.interval)
            print("se cierra long")
        
        elif ma_corta_pre < ma_media_pre and ma_corta > ma_media and ma_larga > ma_corta and ma_larga > ma_media:
            #self.cerrar_short()
            db.guardar_orden_db(df.tail(1), "short", "cerrado", self.interval)
            print("se cierra short")

        else:
            print("no pasa nada", "desde Orden")
