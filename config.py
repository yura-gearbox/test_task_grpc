"""
Файл конфигурации тестового окружения 
Файл импортируется в тесте
Функция os.getenv считывает переменнную окружения (первый параметр), если она не найдена, берется дефолтное значение (второй параметр)
"""
import os

# gRPC server address
GRPC_SERVER_ADDRESS = os.getenv("GRPC_SERVER_ADDRESS", "127.0.0.1")
# gRPC server port
GRPC_SERVER_PORT = int(os.getenv("GRPC_SERVER_PORT", "2031"))
# UDP listener address
UDP_LISTENER_ADDRESS = os.getenv("UDP_LISTENER_ADDRESS", "127.0.0.1")
# UDP listener port
UDP_LISTENER_PORT = int(os.getenv("UDP_LISTENER_PORT", "2032"))
# Server startup timeout
SERVER_STARTUP_TIMEOUT = float(os.getenv("SERVER_STARTUP_TIMEOUT", "5.0"))
# gRPC server application relative path
APP_SERVER_PATH = os.getenv("APP_SERVER_PATH", "/build/grpc_udp_monitor")
# Work directory path
BASEDIR = os.path.dirname(os.path.abspath(__file__))
WORKDIR = os.getenv("WORKDIR", BASEDIR)

# GRPC_SERVER_ADDRESS, GRPC_SERVER_PORT, UDP_LISTENER_ADDRESS, UDP_LISTENER_PORT, SERVER_STARTUP_TIMEOUT, APP_SERVER_PATH, WORKDIR 

