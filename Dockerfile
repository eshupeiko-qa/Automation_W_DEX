# ================================= 
# Stage 1: Base Dependencies
# =================================
FROM python:3.11-slim AS base

# Настройки Python для оптимизации
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    gnupg \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ================================= 
# Stage 2: Dependencies Builder
# =================================
FROM base AS deps-builder

# Создание виртуального окружения
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Копирование и установка основных зависимостей
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ================================= 
# Stage 3: Testing Environment
# =================================
FROM deps-builder AS testing

# Установка Chrome для UI тестов (опционально)
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Установка Allure для отчетов
RUN curl -sL https://github.com/allure-framework/allure2/releases/download/2.24.0/allure-2.24.0.tgz | \
    tar xz -C /opt/ && \
    ln -s /opt/allure-2.24.0/bin/allure /usr/local/bin/allure

# Установка дополнительных зависимостей для тестирования
RUN pip install --no-cache-dir pytest-xdist pytest-html

# Копирование всего проекта
COPY . .

# Создание директорий для результатов
RUN mkdir -p allure-results allure-report

# Установка прав доступа
RUN chmod +x /usr/local/bin/allure

# ================================= 
# Stage 4: API Testing (Production)
# =================================
FROM base AS production

# Создание пользователя без root прав
RUN groupadd -r testuser && useradd -r -g testuser testuser

# Копирование виртуального окружения
COPY --from=deps-builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Копирование Allure CLI
COPY --from=testing /usr/local/bin/allure /usr/local/bin/allure
COPY --from=testing /opt/allure-2.24.0 /opt/allure-2.24.0

# Копирование только необходимых файлов проекта
COPY --chown=testuser:testuser config/ ./config/
COPY --chown=testuser:testuser tests/ ./tests/
COPY --chown=testuser:testuser utils/ ./utils/
COPY --chown=testuser:testuser conftest.py pytest.ini requirements.txt ./

# Создание директорий для результатов
RUN mkdir -p allure-results allure-report && \
    chown -R testuser:testuser allure-results allure-report

USER testuser

# Команда по умолчанию - запуск API тестов с генерацией отчета
CMD ["sh", "-c", "python -m pytest tests/ -v --tb=short -m 'not ui' --alluredir=allure-results && allure generate allure-results --clean -o allure-report"]

# ================================= 
# Stage 5: Full Testing (с UI тестами)
# =================================
FROM testing AS full-testing

# Установка ChromeDriver
RUN CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

# Настройка Chrome для работы в контейнере
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_OPTS="--headless --no-sandbox --disable-dev-shm-usage --disable-gpu"

# Команда для запуска всех тестов включая UI
CMD ["sh", "-c", "python -m pytest tests/ -v --tb=short --alluredir=allure-results && allure generate allure-results --clean -o allure-report"]