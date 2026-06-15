import subprocess
import time
import signal
import pytest
import grpc
import monitor_pb2
import monitor_pb2_grpc

from config import GRPC_SERVER_ADDRESS, GRPC_SERVER_PORT, UDP_LISTENER_ADDRESS, UDP_LISTENER_PORT, APP_SERVER_PATH, WORKDIR, SERVER_STARTUP_TIMEOUT, SERVER_TERMINATE_TIMEOUT, STUB_ISREADY_TIMEOUT, RPCERROR_WAIT 

@pytest.fixture
def raw_app_process(scope='session'):
    process = subprocess.Popen(
        [f'{WORKDIR}{APP_SERVER_PATH}'],
        text=True
    )
    
    yield process

    if process.poll() is None:
        process.send_signal(signal.SIGTERM)
        try:
            process.wait(timeout=SERVER_TERMINATE_TIMEOUT)
        except subprocess.TimeoutExpired:
            process.kill()

@pytest.fixture
def grpc_server(raw_app_process):
    start_time = time.time()
    server_ready = False
    while time.time() - start_time < SERVER_STARTUP_TIMEOUT:
        if raw_app_process.poll() is not None:
            pytest.fail(f"Приложение упало при старте с кодом {raw_app_process.returncode}")

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
    
    if not server_ready:
        raw_app_process.kill()
        pytest.fail(f'Приложение не перешло в статус IsReady за {SERVER_STARTUP_TIMEOUT} секунд')
        
    return raw_app_process


@pytest.fixture
def grpc_stub(grpc_server):
    channel = grpc.insecure_channel(f'{GRPC_SERVER_ADDRESS}:{GRPC_SERVER_PORT}')
    stub = monitor_pb2_grpc.MonitorServiceStub(channel)

    yield stub

    channel.close()

