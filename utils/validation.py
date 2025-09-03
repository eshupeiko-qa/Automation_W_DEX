#Функции валидации данных API:


def validate_candle_structure(candle):
    """Проверяет структуру одной свечи"""
    required_fields = ["id", "date", "volumeUSD", "priceUSD", "close", "high", "low", "open", "token"]
    for field in required_fields:
        if field not in candle:
            return False, f"Отсутствует обязательное поле '{field}'"

    # Проверяем структуру token
    if not isinstance(candle["token"], dict) or "symbol" not in candle["token"]:
        return False, "Некорректная структура поля 'token'"

    return True, "OK"


def validate_candle_values(candle):
    """Проверяет значения в свече на валидность"""
    try:
        open_price = float(candle["open"])
        high = float(candle["high"])
        low = float(candle["low"])
        close = float(candle["close"])
        volume = float(candle["volumeUSD"])
    except (TypeError, ValueError) as e:
        return False, f"Ошибка преобразования цен: {e}"

    # Проверяем основные свечные правила
    if high < low:
        return False, f"high < low: {high} < {low}"

    if not (low <= open_price <= high):
        return False, f"open вне диапазона high-low: {open_price} не в [{low}, {high}]"

    if not (low <= close <= high):
        return False, f"close вне диапазона high-low: {close} не в [{low}, {high}]"

    if volume < 0:
        return False, f"Отрицательный объем: {volume}"

    return True, "OK"


def validate_date_format(date):
    """Проверяет формат и разумный диапазон даты"""
    import datetime

    if not isinstance(date, int):
        return False, "Дата должна быть целым числом"

    current_timestamp = int(datetime.datetime.now().timestamp())
    # Проверяем, что дата в разумном диапазоне (после 2020 и не в будущем)
    if not (1577836800 <= date <= current_timestamp + 86400):
        return False, f"Дата вне разумного диапазона: {date}"

    return True, "OK"