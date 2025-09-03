#Тесты согласованности данных между разными таймфреймами:

import pytest
from utils.api_helpers import fetch_data, get_api_url
from config.settings import TIMEFRAMES, PAIRS
import time


@pytest.mark.consistency
@pytest.mark.parametrize("pair", PAIRS)
#Проверяет, что данные для более длинных тайм фреймов содержат меньше записей за тот же период:
def test_timeframe_consistency(pair):
    # Получаем данные для всех таймфреймов
    data_by_timeframe = {}
    for timeframe in TIMEFRAMES:
        response = fetch_data(pair, timeframe)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                data_by_timeframe[timeframe] = data

    # Если есть данные для нескольких таймфреймов, проверяем их согласованность
    if len(data_by_timeframe) > 1:
        # Находим общий временной диапазон
        all_dates = []
        for data in data_by_timeframe.values():
            all_dates.extend([candle["date"] for candle in data])

        if all_dates:
            min_date = max(min([candle["date"] for candle in data]) for data in data_by_timeframe.values())
            max_date = min(max([candle["date"] for candle in data]) for data in data_by_timeframe.values())

            # Считаем количество записей в общем диапазоне для каждого таймфрейма
            counts = {}
            for timeframe, data in data_by_timeframe.items():
                filtered_data = [candle for candle in data if min_date <= candle["date"] <= max_date]
                counts[timeframe] = len(filtered_data)

            # Проверяем, что для более длинных таймфреймов данных меньше
            # Порядок таймфреймов от самых коротких к самым длинным
            ordered_timeframes = ["15m", "1h", "4h", "", "1w"]

            # Удаляем таймфреймы, для которых нет данных в общем диапазоне
            available_timeframes = [tf for tf in ordered_timeframes if tf in counts and counts[tf] > 0]

            for i in range(len(available_timeframes) - 1):
                current_tf = available_timeframes[i]
                next_tf = available_timeframes[i + 1]

                # Допускаем небольшую погрешность из-за особенностей агрегации
                assert counts[current_tf] >= counts[next_tf], (
                    f"Нарушена последовательность таймфреймов: {current_tf} имеет {counts[current_tf]} записей, "
                    f"{next_tf} имеет {counts[next_tf]} записей для {pair}"
                )
    time.sleep(0.5)


@pytest.mark.consistency
@pytest.mark.parametrize("pair", PAIRS)
#Проверяет согласованность данных на разных таймфреймах за двухнедельный период:
def test_timeframe_consistency_2_weeks(pair):
    # Получаем данные для всех таймфреймов
    data_by_timeframe = {}

    for timeframe in TIMEFRAMES:
        response = fetch_data(pair, timeframe)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                data_by_timeframe[timeframe] = data

    # Проверяем, что есть данные для недельного таймфрейма
    if "1w" not in data_by_timeframe:
        pytest.skip(f"Нет данных для таймфрейма 1w для пары {pair}")

    # Берем последнюю недельную свечу как отправную точку
    weekly_data = data_by_timeframe["1w"]
    if len(weekly_data) < 2:
        pytest.skip(f"Недостаточно недельных данных для пары {pair}")

    # Определяем двухнедельный период на основе последних двух недельных свечей
    last_week_candle = weekly_data[0]
    prev_week_candle = weekly_data[1]

    period_start = prev_week_candle["date"]  # Начало двухнедельного периода
    period_end = last_week_candle["date"] + 7 * 24 * 3600  # Конец двухнедельного периода

    # Проверяем согласованность для каждого таймфрейма
    expected_ratios = {
        "15m": 672,  # 2 недели * 7 дней * 24 часа * 4 интервала по 15 минут
        "1h": 336,  # 2 недели * 7 дней * 24 часа
        "4h": 84,  # 2 недели * 7 дней * 6 интервалов по 4 часа
        "": 14,  # 2 недели * 7 дней
        "1w": 2  # 2 недели
    }

    for timeframe in TIMEFRAMES:
        if timeframe not in data_by_timeframe:
            continue
