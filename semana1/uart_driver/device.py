from typing import Dict, Any
from .config import UartConfig
from .parsers import MessageParser

class UartDevice:
    def __init__(self, config: UartConfig, parser: MessageParser) -> None:
        self.config = config
        self.parser = parser
        self.is_open: bool = False

    def open_connection(self) -> None:
        self.is_open = True

    def close_connection(self) -> None:
        self.is_open = False

    def receive_and_process(self, raw_buffer: bytes) -> Dict[str, Any]:
        if not self.is_open:
            raise RuntimeError("El puerto UART está cerrado")
        return self.parser.parse(raw_buffer)