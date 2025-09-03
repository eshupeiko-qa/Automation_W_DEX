#Тесты валидации объемов в API:

import pytest
from utils.api_helpers import fetch_data
from config.settings import TIMEFRAMES, PAIRS
import time

@pytest.mark.validation
@pytest.mark.parametrize("pair", PAIRS)
@pytest.mark.parametrize("timeframe", TIMEFRAMES)

#Проверка, что объемы положительные:
def test_volume_positive(pair, timeframe):

    response = fetch_data(pair, timeframe)
    assert response.status_code == 200

    data = response.json()

    for i, candle in enumerate(data):
        try:
            volume = float(candle["volumeUSD"])
        except (TypeError, ValueError):
            pytest.fail(f"Ошибка преобразования volumeUSD в свече {i} для {pair}")

        assert volume >= 0, f"Отрицательный объем: {volume} в свече {i} для {pair}"
    time.sleep(1.0)