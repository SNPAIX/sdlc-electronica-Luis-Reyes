import pytest
import os
import json

from .config import UartConfig
from .parsers import ModbusParser, NMEAParser
from .device import UartDevice
from .recorder import UartDataRecorder

def test_uart_config_invalid_baudrate():
    with pytest.raises(ValueError, match="Baudrate no soportado"):
        UartConfig(port="COM3", baudrate=9601)

def test_modbus_parser_success():
    parser = ModbusParser()
    # Trama ficticia: [ID=1, Fun=3, Val_High=0x00, Val_Low=0xFA (250)]
    raw_bytes = bytes([1, 3, 0, 250])
    result = parser.parse(raw_bytes)
    assert result["protocol"] == "Modbus"
    assert result["value"] == 250.0

def test_nmea_parser_success():
    parser = NMEAParser()
    raw_bytes = b"$GPRMC,23.5,A*3A"
    result = parser.parse(raw_bytes)
    assert result["protocol"] == "NMEA"
    assert result["value"] == 23.5

def test_device_closed_raises_error():
    config = UartConfig(port="COM3", baudrate=115200)
    parser = ModbusParser()
    device = UartDevice(config, parser)
    with pytest.raises(RuntimeError, match="UART está cerrado"):
        device.receive_and_process(bytes([1, 3, 0, 100]))

def test_recorder_saves_json_lines(tmp_path):
    # tmp_path es un fixture de pytest que crea un directorio temporal limpio
    test_file = tmp_path / "telemetry.jsonl"
    recorder = UartDataRecorder(str(test_file))
    
    sample_data = {"protocol": "Modbus", "device_id": 1, "value": 23.5}
    recorder.record(sample_data)
    
    # Verificar que el archivo existe y contiene la estructura correcta
    assert test_file.exists()
    with open(test_file, "r", encoding="utf-8") as f:
        line = f.readline()
        saved_dict = json.loads(line)
        assert saved_dict["protocol"] == "Modbus"
        assert saved_dict["value"] == 23.5