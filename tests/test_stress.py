import pytest

import monitor_pb2

from config import GET_UDP_STATISTICS_TIMEOUT


@pytest.mark.stress
def test_tc_nf_01_udp_listener_burst_rate_stress(grpc_stub, send_udp):
    """
    TC-NF-01: Стресс-тест UDP-приемника импульсной нагрузкой (Burst Rate).
    """
    send_udp([b'A'] * 255, delay_sec=0.0)
    response = grpc_stub.GetUdpStatistics(monitor_pb2.Empty(), timeout=GET_UDP_STATISTICS_TIMEOUT)

    assert response.packets == 255, f'Ожидался счетчик пакетов 255, но получено: {response.packets}'
    assert response.aBytes == 255, f'Ожидался счетчик целевых символов 255, но получено: {response.aBytes}'

