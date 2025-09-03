"""Общие фикстуры и хуки для pytest"""

import sys
from pathlib import Path
import importlib.util

# Определяем корневой каталог проекта
current_file = Path(__file__).resolve()
project_root = current_file.parent

# Добавляем корневой каталог в sys.path, если его там еще нет
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


# Функция для безопасного импорта модуля
def import_module(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None:
        raise ImportError(f"Не удалось создать спецификацию для модуля {module_name} по пути {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


# Пытаемся импортировать настройки
try:
    from config.settings import PAIRS, TIMEFRAMES
except ImportError:
    # Пытаемся найти и импортировать вручную
    settings_path = project_root / "config" / "settings.py"
    if settings_path.exists():
        try:
            config_module = import_module("config.settings", str(settings_path))
            PAIRS = config_module.PAIRS
            TIMEFRAMES = config_module.TIMEFRAMES
        except Exception as e:
            print(f"Ошибка при ручном импорте config.settings: {e}")
            # Попробуем импортировать напрямую из config
            config_path = project_root / "config"
            if str(config_path) not in sys.path:
                sys.path.insert(0, str(config_path))
            try:
                from settings import PAIRS, TIMEFRAMES
            except ImportError:
                raise ImportError("Не удалось импортировать настройки из config/settings.py") from None
    else:
        raise ImportError("Файл config/settings.py не найден") from None

import pytest


# Параметризованные фикстуры для пар и таймфреймов
@pytest.fixture(params=PAIRS)
def trading_pair(request):
    """Фикстура для тестирования всех торговых пар"""
    return request.param


@pytest.fixture(params=TIMEFRAMES)
def timeframe(request):
    """Фикстура для тестирования всех таймфреймов"""
    return request.param


# Фикстура для получения данных API
@pytest.fixture
def api_data(trading_pair, timeframe):
    """Фикстура для получения данных API для тестов"""
    # Импортируем api_helpers
    try:
        from utils.api_helpers import fetch_data
    except ImportError:
        api_helpers_path = project_root / "utils" / "api_helpers.py"
        if api_helpers_path.exists():
            utils_module = import_module("utils.api_helpers", str(api_helpers_path))
            fetch_data = utils_module.fetch_data
        else:
            # Попробуем импортировать напрямую из utils
            utils_path = project_root / "utils"
            if str(utils_path) not in sys.path:
                sys.path.insert(0, str(utils_path))
            try:
                from api_helpers import fetch_data
            except ImportError:
                raise ImportError("Файл utils/api_helpers.py не найден") from None

    response = fetch_data(trading_pair, timeframe)
    assert response.status_code == 200, f"API недоступен для {trading_pair} с таймфреймом {timeframe}"

    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    return {
        "pair": trading_pair,
        "timeframe": timeframe,
        "data": data
    }
