# Наследуем образ Python
FROM python:3.10-slim-buster

# Устанавливаем poetry
RUN pip3 install --upgrade pip && pip3 install poetry

# Копируем файлы проекта
WORKDIR /app
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости с помощью poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем остальные файлы проекта
COPY . .