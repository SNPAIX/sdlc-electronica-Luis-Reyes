from abc import ABC, abstractmethod
from typing import Dict, Any

class MessageParser(ABC):
    @abstractmethod
    def parse(self, raw_data: bytes) -> Dict[str, Any]:
        """Contrato abstracto para parsear tramas de datos de sensores."""
        pass

class ModbusParser(MessageParser):
    def parse(self, raw_data: bytes) -> Dict[str, Any]:
        if len(raw_data) < 4:
            raise ValueError("Trama Modbus incompleta")
        device_id = raw_data[0]
        value = (raw_data[2] << 8) | raw_data[3]
        return {"protocol": "Modbus", "device_id": device_id, "value": float(value)}

class NMEAParser(MessageParser):
    def parse(self, raw_data: bytes) -> Dict[str, Any]:
        try:
            decoded = raw_data.decode("ascii")
            if not decoded.startswith("$"):
                raise ValueError("Trama NMEA inválida")
            parts = decoded.split(",")
            return {"protocol": "NMEA", "type": parts[0], "value": float(parts[1])}
        except (UnicodeDecodeError, IndexError, ValueError) as e:
            raise ValueError(f"Error parseando trama NMEA: {e}")