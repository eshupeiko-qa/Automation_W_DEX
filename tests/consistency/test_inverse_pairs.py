#Тест для проверки обратных пар

import pytest
from utils.api_helpers import fetch_data, get_inverse_pair
from config.settings import PAIRS, TIMEFRAMES
import time

'''@pytest.mark.consistency
@pytest.mark.parametrize("pair", [p for p in PAIRS if "-" in p and get_inverse_pair(p) in PAIRS])

#Проверка, что обратные пары имеют обратные цены (только для 1d):
def test_inverse_pairs(pair):

    inverse_pair = get_inverse_pair(pair)

    # Получаем данные для обеих пар с таймфреймом 1d
    response1 = fetch_data(pair, "")
    response2 = fetch_data(inverse_pair, "")

    if response1.status_code == 200 and response2.status_code == 200:
        data1 = response1.json()
        data2 = response2.json()

        if isinstance(data1, list) and isinstance(data2, list) and data1 and data2:
            # Находим общие временные точки
            dates1 = {candle["date"]: candle for candle in data1}
            dates2 = {candle["date"]: candle for candle in data2}
            common_dates = set(dates1.keys()) & set(dates2.keys())

            # Проверяем, что цены обратны друг другу
            for date in common_dates:
                try:
                    price1 = float(dates1[date]["priceUSD"])
                    price2 = float(dates2[date]["priceUSD"])
                except (TypeError, ValueError):
                    continue  # Пропускаем проблемные записи

                # Проверяем, что price1 * price2 примерно равно 1
                # Допускаем небольшую погрешность из-за спреда и округления
                product = price1 * price2
                assert 0.95 <= product <= 1.05, (
                    f"Цены для обратных пар не обратны: {price1} * {price2} = {product} "
                    f"для {pair} и {inverse_pair} на дату {date}"
                )


# Вспомогательная функция для создания списка пар для тестирования
def _get_inverse_test_pairs():
    test_pairs = []
    for tf in TIMEFRAMES:
        for p in PAIRS:
            if "-" in p:
                inverse_p = get_inverse_pair(p)
                if inverse_p and inverse_p in PAIRS and p < inverse_p:
                    test_pairs.append((tf, p))
    return test_pairs'''


#Проверка обратной пары на всех таймфреймах

@pytest.mark.consistency
@pytest.mark.parametrize("timeframe,pair", _get_inverse_test_pairs())

#Проверка обратных пар для всех таймфреймов:
def test_inverse_pairs_all_timeframes(timeframe, pair):

    from config.settings import MIN_DATA_POINTS
    
    inverse_pair = get_inverse_pair(pair)

    # Получаем данные для обеих пар с указанным таймфреймом
    response1 = fetch_data(pair, timeframe)
    response2 = fetch_data(inverse_pair, timeframe)

    # Проверяем успешность запросов
    assert response1.status_code == 200, (
        f"Не удалось получить данные для пары {pair} "
        f"на таймфрейме {timeframe if timeframe else '1d'}: код {response1.status_code}"
    )
    
    assert response2.status_code == 200, (
        f"Не удалось получить данные для пары {inverse_pair} "
        f"на таймфрейме {timeframe if timeframe else '1d'}: код {response2.status_code}"
    )

    data1 = response1.json()
    data2 = response2.json()

    # Проверяем, что данные не пустые
    assert isinstance(data1, list) and data1, (
        f"Пустые или неверные данные для пары {pair} "
        f"на таймфрейме {timeframe if timeframe else '1d'}"
    )
    
    assert isinstance(data2, list) and data2, (
        f"Пустые или неверные данные для пары {inverse_pair} "
        f"на таймфрейме {timeframe if timeframe else '1d'}"
    )

    # Находим общие временные точки
    dates1 = {candle["date"]: candle for candle in data1}
    dates2 = {candle["date"]: candle for candle in data2}
    common_dates = set(dates1.keys()) & set(dates2.keys())

    # Должны быть общие временные точки
    assert common_dates, (
        f"Нет общих временных точек для обратных пар {pair} и {inverse_pair} "
        f"на таймфрейме {timeframe if timeframe else '1d'}"
    )
    
    # Проверяем минимальное количество точек данных
    assert len(common_dates) >= MIN_DATA_POINTS, (
        f"Недостаточно общих временных точек ({len(common_dates)}) "
        f"для надежной проверки пар {pair} и {inverse_pair} "
        f"на таймфрейме {timeframe if timeframe else '1d'}. "
        f"Минимум требуется: {MIN_DATA_POINTS}"
    )

    valid_comparisons = 0
    
    # Проверяем, что цены обратны друг другу
    for date in common_dates:
        try:
            price1 = float(dates1[date]["priceUSD"])
            price2 = float(dates2[date]["priceUSD"])
        except (TypeError, ValueError, KeyError):
            continue  # Пропускаем проблемные записи

        # Пропускаем нулевые цены
        if price1 <= 0 or price2 <= 0:
            continue

        valid_comparisons += 1
        
        # Проверяем, что price1 * price2 примерно равно 1
        # Допускаем погрешность 5% из-за спреда и округления
        product = price1 * price2
        assert 0.95 <= product <= 1.05, (
            f"Цены для обратных пар не обратны на таймфрейме {timeframe if timeframe else '1d'}: "
            f"{price1} * {price2} = {product} "
            f"для пар {pair} и {inverse_pair} на дату {date}"
        )
    
    # Проверяем, что были валидные сравнения
    assert valid_comparisons > 0, (
        f"Не найдено валидных цен для сравнения пар {pair} и {inverse_pair} "
        f"на таймфрейме {timeframe if timeframe else '1d'}"
    )
    time.sleep(3)