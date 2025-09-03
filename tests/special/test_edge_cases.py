"""Тесты крайних случаев и специальных ситуаций"""

import pytest
from utils.api_helpers import fetch_data
from config.settings import PAIRS, TIMEFRAMES


@pytest.mark.special
@pytest.mark.parametrize("pair", PAIRS)
@pytest.mark.parametrize("timeframe", TIMEFRAMES)
def test_zero_volume_cases(pair, timeframe):
    """Проверяет случаи с нулевым объемом"""
    response = fetch_data(pair, timeframe)
    assert response.status_code == 200

    data = response.json()

    for i, candle in enumerate(data):
        volume = float(candle["volumeUSD"])
        # Если объем нулевой, проверяем, что цены одинаковые (без движения)
        if volume == 0:
            open_price = float(candle["open"])
            high = float(candle["high"])
            low = float(candle["low"])
            close = float(candle["close"])

            # В случае нулевого объема все цены должны быть одинаковыми
            assert open_price == high == low == close, (
                f"Несоответствие цен при нулевом объеме в свече {i} для {pair}: "
                f"open={open_price}, high={high}, low={low}, close={close}"
            )


@pytest.mark.special
def test_latest_data_timestamp():
    """Проверяет, что самые свежие данные не слишком устарели"""
    import time

    response = fetch_data("POL-USDT", "")
    assert response.status_code == 200

    data = response.json()
    if data:
        latest_timestamp = data[0]["date"]
        current_time = int(time.time())

        # Проверяем, что самые свежие данные не старше 24 часов
        assert current_time - latest_timestamp <= 86400, (
            f"Самые свежие данные слишком устарели: {current_time - latest_timestamp} секунд"
        )