import pytest

import monitor_pb2

from config import GET_UDP_STATISTICS_TIMEOUT, SEND_PACKETS_DELAY

@pytest.mark.byte_counter
def test_tc_sv_by_01_initial_byte_counter(grpc_stub):
    """
    TC-SV-BY-01: Инициализация счетчика целевых символов (Нижняя граница 0).
    """
    response = grpc_stub.GetUdpStatistics(monitor_pb2.Empty(), timeout=GET_UDP_STATISTICS_TIMEOUT)
   
    assert response.aBytes == 0, f'Ожидался начальный счетчик целевых символов 0, но получено: {response.aBytes}'

@pytest.mark.byte_counter
def test_tc_sv_by_02_noise_filtering(grpc_stub, send_udp):
    """
    TC-SV-BY-02: Игнорирование шумовых символов (Фильтрация мусора).
    """
    send_udp([b'XYZ123'])
    response = grpc_stub.GetUdpStatistics(monitor_pb2.Empty(), timeout=GET_UDP_STATISTICS_TIMEOUT)
   
    assert response.aBytes == 0, f'Ожидался счетчик целевых символов 0, но получено: {response.aBytes}'

@pytest.mark.byte_counter
def test_tc_sv_by_03_single_target_byte(grpc_stub, send_udp):
    """
    TC-SV-BY-03: Фиксация одиночного целевого символа (Шаг 1).
    """
    send_udp([b'A'])
    response = grpc_stub.GetUdpStatistics(monitor_pb2.Empty(), timeout=GET_UDP_STATISTICS_TIMEOUT)
   
    assert response.aBytes == 1, f'Ожидался счетчик целевых символов 1, но получено: {response.aBytes}'

@pytest.mark.byte_counter
def test_tc_sv_by_04_multiple_target_bytes_in_single_packet(grpc_stub, send_udp):
    """
    TC-SV-BY-04: Побайтовый разбор нескольких целевых символов в одном пакете.
    """
    send_udp([b'BACAADA'])
    response = grpc_stub.GetUdpStatistics(monitor_pb2.Empty(), timeout=GET_UDP_STATISTICS_TIMEOUT)
   
    assert response.aBytes == 4, f'Ожидался счетчик целевых символов 4, но получено: {response.aBytes}'

@pytest.mark.byte_counter
def test_tc_sv_by_05_byte_accumulation_across_packets(grpc_stub, send_udp):
    """
    TC-SV-BY-05: Накопление целевых байтов из множества пакетов (Эквивалентный класс 100).
    """
    send_udp([b'A'] * 100, SEND_PACKETS_DELAY)
    response = grpc_stub.GetUdpStatistics(monitor_pb2.Empty(), timeout=GET_UDP_STATISTICS_TIMEOUT)
   
    assert response.aBytes == 100, f'Ожидался счетчик целевых символов 100, но получено: {response.aBytes}'

