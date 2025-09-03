#Тест для проверки обратных пар

import pytest
from utils.api_helpers import fetch_data, get_inverse_pair
from config.settings import PAIRS


@pytest.mark.consistency
@pytest.mark.parametrize("pair", [p for p in PAIRS if "-" in p and get_inverse_pair(p) in PAIRS])

#Проверка, что обратные пары имеют обратные цены:
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