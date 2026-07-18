from dataclasses import dataclass

VALID_BAUDRATES = {9600, 115200, 921600}

@dataclass(frozen=True)
class UartConfig:
    port: str
    baudrate: int
    data_bits: int = 8
    stop_bits: int = 1

    def __post_init__(self) -> None:
        if self.baudrate not in VALID_BAUDRATES:
            raise ValueError(f"Baudrate no soportado por el hardware: {self.baudrate}")
        if self.data_bits not in {7, 8}:
            raise ValueError("Data bits debe ser 7 u 8")