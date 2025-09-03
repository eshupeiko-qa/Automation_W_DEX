"""Тесты валидации цен в API"""

import pytest

from config.settings import TIMEFRAMES, PAIRS
from utils.api_helpers import fetch_data
from utils.validation import validate_candle_values
import time

@pytest.mark.validation
@pytest.mark.parametrize("pair", PAIRS)
@pytest.mark.parametrize("timeframe", TIMEFRAMES)
def test_price_ranges(pair, timeframe):
    """Проверяет, что цены в разумных пределах"""
    response = fetch_data(pair, timeframe)
    assert response.status_code == 200

    data = response.json()

    for i, candle in enumerate(data):
        is_valid, message = validate_candle_values(candle)
        assert is_valid, f"Ошибка в свече {i} для {pair}: {message}"

        # Дополнительная проверка разумного диапазона цен
        price_usd = float(candle["priceUSD"])
        if "USDT" in pair or "DAI" in pair or "CES" in pair:
            # Для стейблкоинов и токенов ожидаем цены в разумном диапазоне
            assert 0.000001 <= price_usd <= 1000000, (
                f"Цена вне разумного диапазона: {price_usd} для {pair}"
            )
    time.sleep(1.0)

@pytest.mark.validation
@pytest.mark.parametrize("pair", PAIRS)
@pytest.mark.parametrize("timeframe", TIMEFRAMES)
def test_candle_validity(pair, timeframe):
    """Проверяет, что close находится между low и high, а также другие свечные правила"""
    response = fetch_data(pair, timeframe)
    assert response.status_code == 200

    data = response.json()

    for i, candle in enumerate(data):
        is_valid, message = validate_candle_values(candle)
        assert is_valid, f"Нарушение правил свечи {i} для {pair}: {message}"