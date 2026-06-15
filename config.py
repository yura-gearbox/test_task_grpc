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
# gRPC server application relative path
APP_SERVER_PATH = os.getenv("APP_SERVER_PATH", "/build/grpc_udp_monitor")
# Work directory path
BASEDIR = os.path.dirname(os.path.abspath(__file__))
WORKDIR = os.getenv("WORKDIR", BASEDIR)

# Server startup timeout
SERVER_STARTUP_TIMEOUT = float(os.getenv("SERVER_STARTUP_TIMEOUT", "5.0"))
# Server terminate timeout
SERVER_TERMINATE_TIMEOUT = float(os.getenv("SERVER_TERMINATE_TIMEOUT", "3.0"))
# Stub.IsReady() timeout
STUB_ISREADY_TIMEOUT = float(os.getenv("STUB_ISREADY_TIMEOUT", "0.5"))
# Wait if RpcError
RPCERROR_WAIT = float(os.getenv("RPCERROR_WAIT", "0.2"))
# Get UDP Statistics timeout
GET_UDP_STATISTICS_TIMEOUT = float(os.getenv("GET_UDP_STATISTICS_TIMEOUT", "0.5"))


# GRPC_SERVER_ADDRESS, GRPC_SERVER_PORT, UDP_LISTENER_ADDRESS, UDP_LISTENER_PORT, SERVER_STARTUP_TIMEOUT, APP_SERVER_PATH, WORKDIR 

