#!/bin/bash
# Скрипт для запуска тестов в Docker контейнере

echo "🚀 Запуск тестов DEX API в Docker контейнере..."

# Создание директорий для результатов
mkdir -p allure-results allure-report

# Функция для запуска API тестов
run_api_tests() {
    echo "📊 Запуск API тестов..."
    docker-compose up --build dex-api-tests
    
    if [ $? -eq 0 ]; then
        echo "✅ API тесты успешно выполнены!"
        echo "📈 Отчеты доступны в директории ./allure-report"
    else
        echo "❌ API тесты завершились с ошибками"
        exit 1
    fi
}

# Функция для запуска всех тестов включая UI
run_full_tests() {
    echo "🌐 Запуск всех тестов включая UI..."
    docker-compose --profile full up --build dex-full-tests
    
    if [ $? -eq 0 ]; then
        echo "✅ Все тесты успешно выполнены!"
        echo "📈 Отчеты доступны в директории ./allure-report"
    else
        echo "❌ Тесты завершились с ошибками"
        exit 1
    fi
}

# Функция для запуска сервера отчетов
start_reports_server() {
    echo "🌐 Запуск сервера для просмотра отчетов..."
    echo "📊 Отчеты будут доступны по адресу: http://localhost:8080"
    docker-compose --profile reports up -d reports-server
}

# Функция для интерактивной отладки
debug_mode() {
    echo "🔍 Запуск интерактивного режима отладки..."
    docker-compose --profile debug run --rm debug
}

# Функция для очистки контейнеров и томов
cleanup() {
    echo "🧹 Очистка Docker контейнеров и томов..."
    docker-compose down --volumes
    docker system prune -f
}

# Обработка аргументов командной строки
case "${1:-api}" in
    "api")
        run_api_tests
        ;;
    "full")
        run_full_tests
        ;;
    "reports")
        start_reports_server
        ;;
    "debug")
        debug_mode
        ;;
    "cleanup")
        cleanup
        ;;
    "help")
        echo "Использование: $0 [команда]"
        echo ""
        echo "Доступные команды:"
        echo "  api      - Запуск только API тестов (по умолчанию)"
        echo "  full     - Запуск всех тестов включая UI"
        echo "  reports  - Запуск сервера для просмотра отчетов"
        echo "  debug    - Интерактивный режим отладки"
        echo "  cleanup  - Очистка Docker контейнеров"
        echo "  help     - Показать эту справку"
        ;;
    *)
        echo "❌ Неизвестная команда: $1"
        echo "Используйте '$0 help' для списка доступных команд"
        exit 1
        ;;
esac