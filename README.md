# DEX API Test Suite - Docker Setup

Комплексная тестовая среда для DEX API с поддержкой Docker контейнеризации.

## 🚀 Быстрый старт

### Требования
- Docker
- Docker Compose

### Запуск API тестов (рекомендуется)
```bash
# Простой способ
./docker-scripts/run-tests.sh api

# Или через docker-compose
docker-compose up --build dex-api-tests
```

### Запуск всех тестов включая UI
```bash
# С поддержкой Chrome WebDriver
./docker-scripts/run-tests.sh full

# Или через docker-compose
docker-compose --profile full up --build dex-full-tests
```

## 📊 Просмотр отчетов

### Автоматическая генерация
Отчеты автоматически генерируются после каждого запуска тестов в директории `./allure-report`

### Веб-сервер для отчетов
```bash
# Запуск веб-сервера на порту 8080
./docker-scripts/run-tests.sh reports

# Или напрямую
docker-compose --profile reports up -d reports-server
```

Отчеты будут доступны по адресу: http://localhost:8080

## 🔍 Режимы работы

### 1. API тесты (по умолчанию)
- Только тесты API без UI
- Быстро и стабильно
- Не требует Chrome/WebDriver

### 2. Полные тесты
- API + UI тесты
- Требует Chrome WebDriver
- Полное покрытие функциональности

### 3. Интерактивная отладка
```bash
./docker-scripts/run-tests.sh debug
```

## 🏗️ Архитектура Docker

### Многостадийная сборка
- **base**: Базовые системные зависимости
- **deps-builder**: Установка Python зависимостей
- **testing**: Полная среда тестирования с Chrome
- **production**: Оптимизированный образ только для API тестов
- **full-testing**: Полная среда включая UI тесты

### Оптимизации
- Использование виртуальных окружений Python
- Кэширование слоев Docker
- Минимальные production образы
- Непривилегированный пользователь

## 📁 Структура проекта

```
dex-api-tests/
├── docker-scripts/
│   └── run-tests.sh           # Основной скрипт управления
├── config/                    # Конфигурация тестов
├── tests/                     # Тестовые модули
│   ├── basic/                # API тесты доступности
│   ├── validation/           # Тесты валидации данных  
│   ├── UI/                   # Selenium UI тесты
│   └── pages/                # Page Object Models
├── utils/                     # Утилиты
├── allure-results/           # Результаты тестов (авто)
├── allure-report/            # HTML отчеты (авто)
├── Dockerfile                # Многостадийная сборка
├── docker-compose.yml        # Сервисы Docker
├── requirements.txt          # Основные зависимости
└── requirements-dev.txt      # Дев зависимости
```

## ⚙️ Команды

```bash
# Основные команды
./docker-scripts/run-tests.sh api      # API тесты
./docker-scripts/run-tests.sh full     # Все тесты
./docker-scripts/run-tests.sh reports  # Сервер отчетов
./docker-scripts/run-tests.sh debug    # Отладка
./docker-scripts/run-tests.sh cleanup  # Очистка
./docker-scripts/run-tests.sh help     # Справка
```

## 🔧 Конфигурация

### Переменные окружения
- `PYTHONPATH=/app` - путь к проекту
- `CHROME_OPTS="--headless --no-sandbox"` - настройки Chrome

### Тестовые маркеры
- `api` - API тесты
- `ui` - UI тесты (исключены по умолчанию)
- `validation` - тесты валидации
- `consistency` - тесты консистентности

### Запуск конкретных тестов
```bash
# В интерактивном режиме
./docker-scripts/run-tests.sh debug
> pytest tests/basic/ -v                    # Только базовые тесты
> pytest tests/ -v -m "validation"          # По маркерам
> pytest tests/basic/test_availability.py   # Конкретный файл
```

## 📈 Отчеты Allure

### Особенности
- 📊 Детальная статистика прохождения тестов
- 📈 Графики и тренды
- 🔍 Подробная информация по каждому тесту  
- 📝 История выполнения
- 🏷️ Категоризация по типам тестов

### Просмотр локально
1. Запустить тесты: `./docker-scripts/run-tests.sh api`
2. Запустить веб-сервер: `./docker-scripts/run-tests.sh reports`
3. Открыть браузер: http://localhost:8080

## 🛠️ Разработка

### Локальная разработка
```bash
# Интерактивная оболочка для отладки
docker-compose --profile debug run --rm debug

# Монтирование локального кода
docker run -it -v $(pwd):/app dex-api-tests:latest bash
```

### CI/CD Integration
Docker образы готовы для интеграции с:
- GitHub Actions
- GitLab CI
- Jenkins
- Azure DevOps

Пример для GitHub Actions:
```yaml
- name: Run DEX API Tests
  run: docker-compose up --build dex-api-tests
  
- name: Upload Test Results
  uses: actions/upload-artifact@v3
  with:
    name: allure-reports
    path: allure-report/
```

## 🔒 Безопасность

- Непривилегированный пользователь `testuser`
- Минимальные системные зависимости
- Изолированные виртуальные окружения
- Оптимизированные production образы

---

**Готово к использованию!** 🎉