Тесты для DEX API
Тестирование API децентрализованной биржи W-DEX. Включает API тесты и UI тесты интерфейса.

Что нужно для запуска
Docker и Docker Compose
Как запускать
Только API тесты (быстро)
./docker-scripts/run-tests.sh api
Все тесты включая UI
./docker-scripts/run-tests.sh full
Посмотреть отчеты
./docker-scripts/run-tests.sh reports
Потом открыть в браузере http://localhost:8080

Запуск отдельных тестов
Войти в контейнер:

./docker-scripts/run-tests.sh debug
Внутри контейнера запустить:

# Только базовые тесты доступности
pytest tests/basic/ -v
# Только тесты валидации 
pytest tests/validation/ -v
# Тесты консистентности
pytest tests/consistency/ -v
# Конкретный файл
pytest tests/basic/test_availability.py -v
# По маркерам
pytest -m "validation" -v
pytest -m "ui" -v
Без Docker (если нужно)
Установить зависимости:

pip install -r requirements.txt
Запустить тесты:

# Все API тесты
pytest tests/ -v -m "not ui"
# Все UI тесты
python -m pytest tests/ -v -m ui
# С UI тестами (нужен Chrome)
pytest tests/ -v
Сгенерировать отчет:

pytest tests/ --alluredir=allure-results -m "not ui"
allure generate allure-results -o allure-report
allure open allure-report
Что тестируем
API доступность всех эндпоинтов
Структуру данных в ответах
Валидацию цен, дат, объемов
Консистентность обратных торговых пар
UI страниц swap и pools
Структура
tests/basic/ - базовые тесты доступности
tests/validation/ - проверка данных
tests/consistency/ - тесты консистентности
tests/UI/ - Selenium тесты интерфейса
tests/pages/ - объекты страниц для UI тестов
config/ - настройки торговых пар и эндпоинтов
utils/ - вспомогательные функции
Полезные команды
# Помощь
./docker-scripts/run-tests.sh help
# Очистка Docker
./docker-scripts/run-tests.sh cleanup
Отчеты сохраняются в allure-report/ после каждого запуска.