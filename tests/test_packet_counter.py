import pytest

import monitor_pb2

from config import GET_UDP_STATISTICS_TIMEOUT, SEND_PACKETS_DELAY


@pytest.mark.packet_counter
def test_tc_sv_pk_01_initial_packet_counter(grpc_stub):
    """
    TC-SV-PK-01: Инициализация счетчика пакетов (Нижняя граница 0)
    """
    response = grpc_stub.GetUdpStatistics(monitor_pb2.Empty(), timeout=GET_UDP_STATISTICS_TIMEOUT)
    
    assert response.packets == 0, f'Ожидался начальный счетчик пакетов 0, но получено: {response.packets}'

@pytest.mark.packet_counter
def test_tc_sv_pk_02_single_packet_increment(grpc_stub, send_udp):
    """
    TC-SV-PK-02: Инкремент счетчика при получении одиночной датаграммы (Шаг 1).
    """
    send_udp([b'TEST'])
    response = grpc_stub.GetUdpStatistics(monitor_pb2.Empty(), timeout=GET_UDP_STATISTICS_TIMEOUT)

    assert response.packets == 1, f'Ожидался счетчик пакетов 1, но получено: {response.packets}'

@pytest.mark.packet_counter
def test_tc_sv_pk_03_packet_clumping_accumulation(grpc_stub, send_udp):
    """
    TC-SV-PK-03: Линейное накопление пачки пакетов (Эквивалентный класс 100).
    """
    send_udp([b'TEST'] * 100, delay_sec = SEND_PACKETS_DELAY)
    response = grpc_stub.GetUdpStatistics(monitor_pb2.Empty(), timeout=GET_UDP_STATISTICS_TIMEOUT)

    assert response.packets == 100, f'Ожидался счетчик пакетов 100, но получено: {response.packets}'

