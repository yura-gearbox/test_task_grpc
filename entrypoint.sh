#!/bin/bash
set -e

if [ ! -d ".venv" ]; then
    echo "[INIT] Виртуальное окружение не найдено. Создаю .venv..."
    python3 -m venv .venv
    source /workspace/.venv/bin/activate
    echo "[INIT] Установка зависимостей из requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "[INIT] Виртуальное окружение .venv уже существует."
    source /workspace/.venv/bin/activate
fi

if [ ! -f "monitor_pb2.py" ] || [ ! -f "monitor_pb2_grpc.py" ]; then
    echo "[INIT] gRPC стабы не найдены. Запускаю генерацию..."
    python3 -m grpc_tools.protoc \
        -I=cpp-application \
        --python_out=. \
        --grpc_python_out=. \
        cpp-application/monitor.proto
    echo "[INIT] gRPC стабы успешно сгенерированы."
else
    echo "[INIT] gRPC стабы уже существуют."
fi

echo "[INFO] Инициализация завершена"

exec "$@"
