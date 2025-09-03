"""Тесты согласованности данных между разными таймфреймами"""

import pytest
from utils.api_helpers import fetch_data, get_api_url
from config.settings import TIMEFRAMES, PAIRS


@pytest.mark.consistency
@pytest.mark.parametrize("pair", PAIRS)
def test_timeframe_consistency(pair):
    """Проверяет, что данные для более длинных таймфреймов содержат меньше записей за тот же период"""
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


@pytest.mark.consistency
@pytest.mark.parametrize("pair", PAIRS)
def test_timeframe_data_length_consistency(pair):
    """Проверяет соотношение количества данных для разных таймфреймов"""
    # Получаем данные для всех таймфреймов
    data_lengths = {}
    for timeframe in TIMEFRAMES:
        response = fetch_data(pair, timeframe)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                data_lengths[timeframe] = len(data)

    # Проверяем соотношения только если есть данные для основных таймфреймов
    if "" in data_lengths and "15m" in data_lengths:
        ratio_1d_to_15m = data_lengths[""] / data_lengths["15m"]
        # 1 день = 24 часа = 96 интервалов по 15 минут
        assert 0.8 <= ratio_1d_to_15m * 96 <= 1.2, (
            f"Неправильное соотношение данных для 1d и 15m: {ratio_1d_to_15m}. "
            f"Ожидалось ~0.0104 (1/96), получено {ratio_1d_to_15m}"
        )

    if "1h" in data_lengths and "15m" in data_lengths:
        ratio_1h_to_15m = data_lengths["1h"] / data_lengths["15m"]
        # 1 час = 4 интервала по 15 минут
        assert 0.8 <= ratio_1h_to_15m * 4 <= 1.2, (
            f"Неправильное соотношение данных для 1h и 15m: {ratio_1h_to_15m}. "
            f"Ожидалось ~0.25 (1/4), получено {ratio_1h_to_15m}"
        )

    if "4h" in data_lengths and "1h" in data_lengths:
        ratio_4h_to_1h = data_lengths["4h"] / data_lengths["1h"]
        # 4 часа = 4 интервала по 1 часу
        assert 0.8 <= ratio_4h_to_1h * 4 <= 1.2, (
            f"Неправильное соотношение данных для 4h и 1h: {ratio_4h_to_1h}. "
            f"Ожидалось ~0.25 (1/4), получено {ratio_4h_to_1h}"
        )

    if "1w" in data_lengths and "" in data_lengths:
        ratio_1w_to_1d = data_lengths["1w"] / data_lengths[""]
        # 1 неделя = 7 дней
        assert 0.8 <= ratio_1w_to_1d * 7 <= 1.2, (
            f"Неправильное соотношение данных для 1w и 1d: {ratio_1w_to_1d}. "
            f"Ожидалось ~0.142 (1/7), получено {ratio_1w_to_1d}"
        )