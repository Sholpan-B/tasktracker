# Наследуем образ Python
FROM python:3.10-slim-buster

# Копируем файлы проекта
WORKDIR /app
COPY reqs.txt /app/

# Устанавливаем зависимости
RUN pip3 install --upgrade pip && pip3 install -r reqs.txt

# Копируем остальные файлы проекта
COPY . .

WORKDIR /app/code