import subprocess
import time
import signal
import pytest
import grpc
import monitor_pb2
import monitor_pb2_grpc

from config import GRPC_SERVER_ADDRESS, GRPC_SERVER_PORT, UDP_LISTENER_ADDRESS, UDP_LISTENER_PORT, SERVER_STARTUP_TIMEOUT, APP_SERVER_PATH, WORKDIR 

@pytest.fixture
def grpc_server():
    process = subprocess.Popen(
        [f'{WORKDIR}{APP_SERVER_PATH}'],
        text=True
    )
    
    start_time = time.time()
    server_ready = False
    while time.time() - start_time < SERVER_STARTUP_TIMEOUT:
        if process.poll() is not None:
            pytest.fail(f"Приложение упало при старте с кодом {process.returncode}")

        channel = grpc.insecure_channel(f'{GRPC_SERVER_ADDRESS}:{GRPC_SERVER_PORT}')
        stub = monitor_pb2_grpc.MonitorServiceStub(channel)
        
        try:
            response = stub.IsReady(monitor_pb2.Empty(), timeout=0.5)
            if response.is_ready:
                server_ready = True
                break
        except grpc.RpcError:
            time.sleep(0.2)           
        finally:
            channel.close()
    
    if not server_ready:
        process.kill()
        pytest.fail(f'Приложение не перешло в статус IsReady за {SERVER_STARTUP_TIMEOUT} секунд')
        
    yield process

    if process.poll() is None:
        process.send_signal(signal.SIGTERM)
        try:
            process.wait(timeout=3.0)
        except subprocess.TimeoutExpired:
            process.kill()

@pytest.fixture
def grpc_stub(grpc_server):
    channel = grpc.insecure_channel(f'{GRPC_SERVER_ADDRESS}:{GRPC_SERVER_PORT}')
    stub = monitor_pb2_grpc.MonitorServiceStub(channel)

    yield stub

    channel.close()

