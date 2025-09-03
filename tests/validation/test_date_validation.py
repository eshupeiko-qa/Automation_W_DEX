"""Тесты валидации дат в API"""

import pytest
from utils.api_helpers import fetch_data
from utils.validation import validate_date_format
from config.settings import TIMEFRAMES, PAIRS


@pytest.mark.validation
@pytest.mark.parametrize("pair", PAIRS)
@pytest.mark.parametrize("timeframe", TIMEFRAMES)
def test_dates_ordered(pair, timeframe):
    """Проверяет, что даты упорядочены по времени (от новых к старым)"""
    response = fetch_data(pair, timeframe)
    assert response.status_code == 200

    data = response.json()

    # Проверяем, что даты упорядочены по убыванию (новые данные в начале)
    for i in range(len(data) - 1):
        assert data[i]["date"] >= data[i + 1]["date"], (
            f"Даты не упорядочены: {data[i]['date']} < {data[i + 1]['date']} "
            f"в свечах {i} и {i + 1} для {pair} с таймфреймом {timeframe}"
        )


@pytest.mark.validation
@pytest.mark.parametrize("pair", PAIRS)
@pytest.mark.parametrize("timeframe", TIMEFRAMES)
def test_no_duplicate_dates(pair, timeframe):
    """Проверяет, что нет дублирующихся дат в данных"""
    response = fetch_data(pair, timeframe)
    assert response.status_code == 200

    data = response.json()
    dates = [candle["date"] for candle in data]

    # Проверяем, что все даты уникальны
    assert len(dates) == len(set(dates)), (
        f"Есть дублирующиеся даты для {pair} с таймфреймом {timeframe}. "
        f"Количество записей: {len(dates)}, уникальных дат: {len(set(dates))}"
    )


@pytest.mark.validation
@pytest.mark.parametrize("pair", PAIRS)
@pytest.mark.parametrize("timeframe", TIMEFRAMES)
def test_date_format_and_range(pair, timeframe):
    """Проверяет формат и разумный диапазон дат"""
    response = fetch_data(pair, timeframe)
    assert response.status_code == 200

    data = response.json()

    for i, candle in enumerate(data):
        date = candle["date"]
        is_valid, message = validate_date_format(date)
        assert is_valid, f"Ошибка в дате свечи {i} для {pair}: {message}"