"""Тесты доступности API"""

import pytest
from utils.api_helpers import fetch_data
from config.settings import TIMEFRAMES, PAIRS


@pytest.mark.api
@pytest.mark.parametrize("pair", PAIRS)
@pytest.mark.parametrize("timeframe", TIMEFRAMES)
def test_api_availability(pair, timeframe):
    """Проверяет доступность API для всех пар и таймфреймов"""
    response = fetch_data(pair, timeframe)
    assert response.status_code == 200, (
        f"API недоступен для {pair} с таймфреймом {timeframe}. "
        f"Статус код: {response.status_code}, Ответ: {response.text[:200]}"
    )