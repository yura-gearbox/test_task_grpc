import pytest

import monitor_pb2

from config import GET_UDP_STATISTICS_TIMEOUT, SEND_PACKETS_DELAY


@pytest.mark.overflow
def test_tc_iv_pk_01_packet_counter_max_uint8(grpc_stub, send_udp):
    """
    TC-IV-PK-01: Максимальное заполнение диапазона uint8_t для пакетов.
    """
    send_udp([b'TEST'] * 255, delay_sec = SEND_PACKETS_DELAY)
    response = grpc_stub.GetUdpStatistics(monitor_pb2.Empty(), timeout=GET_UDP_STATISTICS_TIMEOUT)

    assert response.packets == 255, f'Ожидался счетчик пакетов 255, но получено: {response.packets}'

@pytest.mark.overflow
def test_tc_iv_pk_02_packet_counter_overflow(grpc_stub, send_udp):
    """
    TC-IV-PK-02: Триггер переполнения счетчика пакетов (Overflow в 0).
    """
    send_udp([b'TEST'] * 256, delay_sec = SEND_PACKETS_DELAY)
    response = grpc_stub.GetUdpStatistics(monitor_pb2.Empty(), timeout=GET_UDP_STATISTICS_TIMEOUT)

    assert response.packets == 256, f'Ожидался счетчик пакетов 256, но получено: {response.packets}'

@pytest.mark.overflow
def test_tc_iv_by_01_byte_counter_max_uint8(grpc_stub, send_udp):
    """
    TC-IV-BY-01: Максимальное заполнение диапазона uint8_t для байт.
    """
    send_udp([b'A' * 255])
    response = grpc_stub.GetUdpStatistics(monitor_pb2.Empty(), timeout=GET_UDP_STATISTICS_TIMEOUT)

    assert response.aBytes == 255, f'Ожидался счетчик целевых символов 255, но получено: {response.aBytes}'

@pytest.mark.overflow
def test_tc_iv_by_02_byte_counter_overflow(grpc_stub, send_udp):
    """
    TC-IV-BY-02: Триггер переполнения счетчика байт (Overflow в 0).
    """
    send_udp([b'A' * 256])
    response = grpc_stub.GetUdpStatistics(monitor_pb2.Empty(), timeout=GET_UDP_STATISTICS_TIMEOUT)

    assert response.aBytes == 256, f'Ожидался счетчик целевых символов 256, но получено: {response.aBytes}'

