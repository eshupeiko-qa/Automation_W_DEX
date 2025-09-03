"""Вспомогательные функции для работы с API"""

import requests
from config.settings import BASE_URL, REQUEST_TIMEOUT

def get_api_url(pair, timeframe=""):
    """Формирует URL для запроса к API"""
    if timeframe:
        return f"{BASE_URL}/api/pair/{pair}/{timeframe}"
    else:
        return f"{BASE_URL}/api/pair/{pair}"

def fetch_data(pair, timeframe=""):
    """Получает данные от API"""
    url = get_api_url(pair, timeframe)
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        return response
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ошибка при запросе к API: {e}") from e

def get_inverse_pair(pair):
    """Возвращает обратную пару"""
    if "-" in pair:
        base, quote = pair.split("-")
        return f"{quote}-{base}"
    return None