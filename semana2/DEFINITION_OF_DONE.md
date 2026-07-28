# Definition of Done (DoD) - Proyecto SDLC Electrónica

Para que una User Story o tarea se considere **DONE**, debe cumplir estrictamente con los siguientes criterios:

1. **TDD Estricto:**
   - La historia fue iniciada escribiendo primero la prueba unitaria (*Red*).
   - Existe un commit previo explícito que contiene únicamente el test fallando antes del commit de la solución (*Green*).
2. **Cobertura de Código (Code Coverage):**
   - El código implementado cuenta con una cobertura de pruebas de al menos **80%** (medido mediante `pytest-cov`).
3. **Calidad y Estilo de Código:**
   - Cero errores reportados por el linter `ruff check`.
   - Verificación de tipos estáticos exitosa mediante `mypy` sin errores.
4. **Revisión de Código y Git:**
   - Cada User Story fue desarrollada en una rama independiente (`feature/US-XX`).
   - Se realizó un Pull Request (PR) cerrado e integrado a la rama `main`.
5. **Criterios de Aceptación:**
   - Todos los escenarios especificados en sintaxis **Gherkin** (Given / When / Then) han sido cubiertos y pasan en verde.