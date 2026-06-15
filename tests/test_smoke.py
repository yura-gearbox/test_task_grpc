import subprocess
import time
import signal
import socket
import contextlib
import pytest
import grpc
import monitor_pb2
import monitor_pb2_grpc

from config import GRPC_SERVER_ADDRESS, GRPC_SERVER_PORT, UDP_LISTENER_ADDRESS, UDP_LISTENER_PORT, APP_SERVER_PATH, WORKDIR, SERVER_STARTUP_TIMEOUT, SERVER_TERMINATE_TIMEOUT, STUB_ISREADY_TIMEOUT, RPCERROR_WAIT 

@pytest.mark.smoke
def test_tc_lc_server_init(raw_app_process):
    """ 
    TC-LC-01: Верификация инициализации gRPC-сервера
    """

    start_time = time.time()
    server_ready = False
    while time.time() - start_time < SERVER_STARTUP_TIMEOUT:
        if raw_app_process.poll() is not None:
            break

        channel = grpc.insecure_channel(f'{GRPC_SERVER_ADDRESS}:{GRPC_SERVER_PORT}')
        stub = monitor_pb2_grpc.MonitorServiceStub(channel)
        
        try:
            response = stub.IsReady(monitor_pb2.Empty(), timeout=STUB_ISREADY_TIMEOUT)
            if response.is_ready:
                server_ready = True
                break
        except grpc.RpcError:
            time.sleep(RPCERROR_WAIT)
        finally:
            channel.close()
    
    assert server_ready is True, f'Приложение не перешло в статус IsReady за {SERVER_STARTUP_TIMEOUT} секунд'
        
@pytest.mark.smoke
@pytest.mark.parametrize(
    'terminate_signal, test_id',
    [
        (signal.SIGINT, 'TC-LC-02'),
        (signal.SIGTERM, 'TC-LC-03')
    ],
    ids=['SIGINT', 'SIGTERM']
)
def test_tc_lc_graceful_shutdown(raw_app_process, terminate_signal, test_id):
    """
    Параметризованный тест для верификации корректного завершения работы:
    TC-LC-02 (SIGINT) и TC-LC-03 (SIGTERM).
    """
    raw_app_process.send_signal(terminate_signal)
    
    # waiting for process terminate
    try:
        exit_code = raw_app_process.wait(timeout=SERVER_TERMINATE_TIMEOUT)
    except subprocess.TimeoutExpired:
        pytest.fail(f'[{test_id}] Приложение проигнорировало сигнал {terminate_signal.name} и зависло')
        
    assert exit_code == 0, f'[{test_id}] Приложение завершилось с ошибкой. Exit code: {exit_code}'
    
    # проверка освобождения дескрипторов TCP и UDP
    for port, sock_type in [(GRPC_SERVER_PORT, socket.SOCK_STREAM), (UDP_LISTENER_PORT, socket.SOCK_DGRAM)]:
        with contextlib.closing(socket.socket(socket.AF_INET, sock_type)) as sock:
            try:
                sock.bind(('127.0.0.1', port))
            except OSError:
                pytest.fail(f'[{test_id}] Системный порт {port} не был освобожден после {terminate_signal.name}')

