import sqlite3
from datetime import datetime
import pandas as pd

class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def conectar(self):
        self.conn = sqlite3.connect(self.db_file)

    def cerrar_conexion(self):
        if self.conn:
            self.conn.close()

    def crear_tabla_klines(self):
        cursor = self.conn.cursor()
        cursor.execute('''
    CREATE TABLE IF NOT EXISTS klines(
        origen TEXT,
        event_time TEXT,
        symbol TEXT,
        kline_start_time TEXT,
        kline_close_time TEXT,
        close_price REAL,
        high_price REAL,
        low_price REAL,
        base_asset_volume REAL,
        number_of_trades INTEGER
    )
''')
        self.conn.commit()
        cursor.close()

    def crear_tabla_ordenes(self):

        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ordenes (
                timestamp TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                close_time REAL,
                quote_asset_volume REAL,
                number_of_trades REAL,
                taker_buy_base_asset_volume REAL,
                taker_buy_quote_asset_volume REAL,
                ignore REAL,
                MA_corta REAL,
                MA_media REAL,
                MA_larga REAL,
                estado TEXT,
                tipo TEXT,
                origen TEXT
            )
        ''')
        self.conn.commit()


    def guardar_kline_en_db(self, kline, origen):
        cursor = self.conn.cursor()
        cursor.execute('''
    INSERT INTO klines 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    origen, 
    kline['event_time'], 
    kline['symbol'], 
    kline['kline_start_time'], 
    kline['kline_close_time'], 
    kline['close_price'], 
    kline['high_price'], 
    kline['low_price'], 
    kline['base_asset_volume'], 
    kline['number_of_trades']
))
        self.conn.commit()
        cursor.close()



    def guardar_orden_db(self, registro, tipo, estado, origen):
        registro = registro.iloc[0]     

        cursor = self.conn.cursor()
        cursor.execute('''
    INSERT INTO ordenes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    str(registro['timestamp']), float(registro['open']), float(registro['high']), float(registro['low']),
    float(registro['close']), float(registro['volume']), str(registro['close_time']),
    float(registro['quote_asset_volume']), float(registro['number_of_trades']),
    float(registro['taker_buy_base_asset_volume']), float(registro['taker_buy_quote_asset_volume']),
    float(registro['ignore']), float(registro['MA_corta']), float(registro['MA_media']), float(registro['MA_larga']),
    tipo,
    estado,
    origen
))
        self.conn.commit()


    def leer_db_ordenes(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM ordenes')
        registros = cursor.fetchall()
        return registros
        

    def obtenerUltimas2Websocket(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT subquery.fecha_hora_legible
            FROM (
                SELECT datetime(CAST(tiempo_evento AS INTEGER) / 1000, 'unixepoch', 'localtime') AS fecha_hora_legible
                FROM klines
                ORDER BY id DESC
                LIMIT 2
            ) AS subquery
            ORDER BY subquery.fecha_hora_legible DESC
        ''')
        registros = cursor.fetchall()
        return registros