
#Тесты структуры данных API

import pytest
import json
from utils.api_helpers import fetch_data
from utils.validation import validate_candle_structure
from config.settings import TIMEFRAMES, PAIRS, MIN_DATA_POINTS
import time

@pytest.mark.structure
@pytest.mark.parametrize("pair", PAIRS)
@pytest.mark.parametrize("timeframe", TIMEFRAMES)
#Провека структуры ответа API:

def test_response_structure(pair, timeframe):

    response = fetch_data(pair, timeframe)
    assert response.status_code == 200

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Ответ не является валидным JSON для {pair} с таймфреймом {timeframe}")

    # Проверяем, что ответ - это список свечей
    assert isinstance(data, list), f"Ответ должен быть списком, получен {type(data)}"

    # Если данных достаточно, проверяем структуру
    if len(data) >= MIN_DATA_POINTS:
        for i, candle in enumerate(data[:MIN_DATA_POINTS]):
            is_valid, message = validate_candle_structure(candle)
            assert is_valid, f"Ошибка структуры в свече {i} для {pair}: {message}"
    time.sleep(1)



@pytest.mark.structure
@pytest.mark.parametrize("pair", PAIRS)
@pytest.mark.parametrize("timeframe", TIMEFRAMES)

#Проверяет, что данные не пустые:
def test_non_empty_data(pair, timeframe):

    response = fetch_data(pair, timeframe)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0, f"Нет данных для {pair} с таймфреймом {timeframe}"
    time.sleep(1)