import json
from pathlib import Path
from typing import Dict, Any

class UartDataRecorder:
    def __init__(self, output_path: str) -> None:
        self.output_path = Path(output_path)

    def record(self, data: Dict[str, Any]) -> None:
        """Guarda la lectura procesada del sensor en formato JSON-lines."""
        # Se abre en modo append 'a' para no sobreescribir las lecturas anteriores
        with open(self.output_path, mode="a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")