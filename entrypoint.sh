#!/bin/bash
set -e

# Если папки .venv нет, создаем её и ставим зависимости
if [ ! -d ".venv" ]; then
    echo "[INIT] Виртуальное окружение не найдено. Создаю .venv..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "[INIT] Установка зависимостей из requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "[INIT] Виртуальное окружение .venv уже существует."
fi

# Передаем управление основной команде контейнера (sleep infinity)
exec "$@"
