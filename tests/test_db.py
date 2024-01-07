import unittest
import sys
import os
import asyncio
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DatabaseManager import DatabaseManager

pd.set_option('display.max_columns', None)

class TestFunciones(unittest.TestCase):
    def test_suma_ordenes(self):
        db = DatabaseManager("trading-bot.db")
        db.conectar()
        ordenes = db.leer_db_ordenes()
        print(type(ordenes['close']))



        self.assertIsNotNone(ordenes)  # Verifica que el DataFrame no esté vacío