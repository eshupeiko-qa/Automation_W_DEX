
# Вспомогательные функции для работы с API

import requests
from config.settings import BASE_URL, REQUEST_TIMEOUT

#Формирование URL для запроса к API
def get_api_url(pair, timeframe=""):

    if timeframe:
        return f"{BASE_URL}/api/pair/{pair}/{timeframe}"
    else:
        return f"{BASE_URL}/api/pair/{pair}"

#Получение данных от API
def fetch_data(pair, timeframe=""):

    url = get_api_url(pair, timeframe)
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        return response
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ошибка при запросе к API: {e}") from e

#Инверсия пары
def get_inverse_pair(pair):

    if "-" in pair:
        base, quote = pair.split("-")
        return f"{quote}-{base}"
    return None