---
description: Ciclo de desarrollo completo para una tarea del backlog (BDD -> TDD -> Dev -> QA -> Doc)
---

# Workflow: Desarrollo de Tarea (/task-dev)

Este workflow orquesta el ciclo completo de desarrollo de una tarea, soportando la jerarquía **Master/Package v3.0**.

## Modos de Ejecución

1.  **Modo Maestro (Master Mode)**:
    - Entrada: `T-APX-XXXX`
    - Comportamiento: El AI analiza el plan, identifica todas las tareas de paquete vinculadas y las ejecuta secuencialmente.
    - Ideal para: Implementación completa de funcionalidades que cruzan capas.
2.  **Modo Paquete (Package Mode)**:
    - Entrada: `T-APX-[PKG]-XXXX`
    - Comportamiento: El AI se enfoca exclusivamente en el alcance del paquete técnico.
    - Ideal para: Trabajo especializado o colaborativo.

## Workflow Completo

### 1. Inicialización y Contexto

**Acciones:**
- Cargar metadatos de la tarea (ID, Weight, Version, Effort).
- Si es **Package Mode**, identificar `parent_id` para actualizar métricas globales.
- Si es **Master Mode**, cargar lista de tareas hijas pendientes.

### 2. Gestión de Esfuerzo (Inicio)

- Confirmar `estimated_effort`.
- Establecer `remaining_effort` inicial igual al estimado si es nueva.
- **Actualizar Estado**: Cambiar `status` a `in_progress` (en curso).

### 3. Ciclo de Desarrollo Técnico (Por cada Paquete)

Para cada paquete afectado (secuencialmente en Master Mode, o el único en Package Mode):

#### 3.1 Fase BDD (Behavior-Driven Development)
- Definir escenarios en `<paquete>/tests/bdd/features/`.
- Actualizar estado en el archivo `.md`.
- *Regla*: En la medida de lo posible, integrar el escenario en un `.feature` de sistema existente, salvo que sea necesario crear una nueva funcionalidad no existente para resolver la tarea. No crear archivos `.feature` nominales al bug o ID de tarea: los feature son de sistema, no de proceso.

#### 3.2 Fase TDD y Desarrollo
- Crear tests unitarios en `<paquete>/tests/unit/`.
- Implementar código siguiendo estándares (Docstrings obligatorios, no comentarios inline).
- Refactorizar hasta pasar tests.

#### 3.3 Calidad y Revisión
- Ejecutar `/review-test` y `/review-code`.
- Puntuación mínima: 8/10.

#### 3.4 Documentación
- Generar/actualizar `docs/architecture/design_*.md` usando `/generate-doc`.

### 4. Actualización de Métricas y Esfuerzo

**Al completar una sesión o el total de un paquete:**
- Calcular `actual_effort` invertido en la sesión.
- Actualizar `remaining_effort` en el archivo de la tarea (estimación de lo que falta).
- Si el paquete está terminado, marcar `status: completed` (finalizado).

### 5. Finalización y Commit

- Generar commit message con `/commit`.
- Si es **Master Mode**, verificar si todos los paquetes hijos están `completed`.
- Si todo está cerrado, marcar la Tarea Maestra como `completed`.

## Comandos Relacionados

- `/task-add` - Crear nueva tarea
- `/task-dev [ID]` - Iniciar este flujo
- `/commit` - Confirmar cambios