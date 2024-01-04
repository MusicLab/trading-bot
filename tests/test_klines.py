import unittest
import sys
import os
import asyncio
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from RequestApi import *
from Request import ApiCaller
from envTestFutures import api_key, api_secret

pd.set_option('display.max_columns', None)

class TestFunciones(unittest.TestCase):
    def test_klines(self):
        async def get_klines():
            api_caller = ApiCaller("BTCUSDT", "1MINUTE")
            return await api_caller.get_klines()
        

        klines = asyncio.run(get_klines())

        print(klines.tail(1))

        # Verificar si klines es un DataFrame
        self.assertIsInstance(klines, pd.DataFrame)
        # Ejemplo de aserciones adicionales
        self.assertIsNotNone(klines)  # Verifica que el DataFrame no esté vacío

    def test_ordenes(self):
        pass


