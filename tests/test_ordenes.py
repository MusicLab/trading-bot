import unittest
import sys
import os
import asyncio
import pandas as pd
from envTestFutures import api_key, api_secret

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from envTestFutures import api_key, api_secret
from PrivateApi import PrivateApi

pd.set_option('display.max_columns', None)

class TestFunciones(unittest.TestCase):
    
    def setUp(self):
        self.privateApi = PrivateApi("BTCUSDT", api_key, api_secret, testnet=True)
    
    def test_get_positions(self):
        request = self.privateApi.get_positions()
        print(request)

    def test_abrir_long(self): 

        get_position = float(self.privateApi.get_positions()[0]['positionAmt'])
        if get_position < 0:
            self.privateApi.abrir_posicion("BUY", 0.2)
        elif get_position == 0:
            self.privateApi.abrir_posicion("BUY", 0.1)    
        else: 
            pass

    def test_abrir_short(self): 

        get_position = float(self.privateApi.get_positions()[0]['positionAmt'])
        if get_position > 0:
            self.privateApi.abrir_posicion("SELL", 0.2)
        elif get_position == 0:
            self.privateApi.abrir_posicion("SELL", 0.1)    
        else: 
            pass

