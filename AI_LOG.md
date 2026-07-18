# AI Log - Semana 1
**Estudiante:** Luis Khaled Reyes Casanova

## Entrada 1: Abstracción de Configuración UART
- **Prompt usado:** "Crea una configuración para un driver UART en Python que reemplace los structs típicos de C, usando buenas prácticas de tipado estricto."
- **Qué produjo la IA:** Sugirió usar una clase común con métodos de validación manuales.
- **Mi decisión y porqué:** Modifiqué la sugerencia para utilizar una `dataclass(frozen=True)`. La configuración de hardware de un periférico UART debe ser inmutable una vez inicializada; usar estructuras mutables expondría el código a colisiones o cambios de baudrate accidentales en tiempo de ejecución.

## Entrada 2: Diseño de la FSM de Semáforo
- **Prompt usado:** "Cómo mapear una máquina de estados (FSM) típica de microcontroladores en C a un diseño elegante orientado a objetos en Python."
- **Qué produjo la IA:** Un script con variables globales y un ciclo `while` simulando el Superloop de C.
- **Mi decisión y porqué:** Rechacé el uso de globales. Implementé una arquitectura OO usando `Enum` y encapsulando el estado dentro de una clase `TrafficLightFSM`. Esto elimina el acoplamiento rígido de C y permite instanciar múltiples FSM de forma aislada y testeable de acuerdo a los estándares del curso.

## Entrada 3: Resolución de Colisión de Librerías en Principio DIP
- **Prompt usado:** "Implementa el principio de Inversión de Dependencias (DIP) usando typing_extensions para un lector ADC."
- **Qué produjo la IA:** Un bloque utilizando `from typing import typing_extensions` y `typing_extensions.Protocol`.
- **Mi decisión y porqué:** Durante la fase de pruebas con Python 3.14.4, el intérprete arrojó un `ImportError` debido a cambios en la estructura interna de la librería estándar. Decidí refactorizar el código de inmediato para importar `Protocol` de manera directa desde `typing`, resolviendo la colisión y manteniendo el código idiomático y compatible con las versiones más modernas del entorno.
