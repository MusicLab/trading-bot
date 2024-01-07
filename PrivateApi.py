import requests
import time
import hashlib
import hmac
from urllib.parse import urlencode
from envTestFutures import api_key, api_secret
from datetime import datetime

class PrivateApi:
    def __init__(self, symbol, api_key, api_secret, testnet=False):
        self.symbol = symbol
        self.testnet = testnet
        self.api_key = api_key
        self.api_secret = api_secret



    def get_positions(self):
        if self.testnet:
            base_url = 'https://testnet.binancefuture.com'
            endpoint = '/fapi/v2/positionRisk'
        else:
            base_url = 'asd'
            endpoint = 'asd'

        timestamp = int(time.time() * 1000)

        # Crear el query string
        query_string = f'symbol={self.symbol}&timestamp={timestamp}'

        # Firmar la solicitud
        signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

        # Construir el encabezado de la solicitud
        headers = {
            'X-MBX-APIKEY': api_key
        }

        # Realizar la solicitud GET
        url = f"{base_url}{endpoint}?{query_string}&signature={signature}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            positions = response.json()
            return positions
        else:
            print(f"Error al obtener las posiciones de futuros - Código de estado: {response.status_code}")
            print("Mensaje de error:", response.text)




    def abrir_posicion(self, tipo, cantidad):
        if self.testnet:
            base_url = 'https://testnet.binancefuture.com'
            endpoint = '/fapi/v1/order'
        else:
            base_url = "urlReal"
            endpoint= "bla"
        
        params = {
            'symbol': 'BTCUSDT',
            'side': tipo,
            'quantity': cantidad,
            'timestamp': int(time.time() * 1000),
            'type' : 'MARKET'
        }

        sorted_params = dict(sorted(params.items()))
        query_string = urlencode(sorted_params)
        signature = hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

        url = f"{base_url}{endpoint}?{query_string}&signature={signature}"

        response = requests.post(url, headers={'X-MBX-APIKEY': self.api_key})

        if response.status_code == 200:
            order = response.json()
            print(order)
        else:
            print("Error:", response.status_code)
            print("Mensaje de error:", response.text)



