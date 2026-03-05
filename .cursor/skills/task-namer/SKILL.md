---
name: task-namer
description: Skill de nombrado y ubicación de tareas técnica y maestras basada en configuración de proyecto.
---

# Task Namer Skill

Esta skill se encarga de calcular el ID, el nombre de archivo y la ruta de destino de una tarea siguiendo el estándar de nombrado dinámico configurado en `task_config.yaml`.

## Workflow de Nombrado

1. **Leer Configuración**:
   - Localizar `task_config.yaml` en la raíz del proyecto.
   - Extraer `project.prefix`.

2. **Determinar el Escenario**:
   - Si la tarea es **Master**:
     - Usar `levels.master.id_prefix`.
     - Ruta: `levels.master.path`.
   - Si la tarea es de **Componente**:
     - Identificar el tipo (app, service, package).
     - Usar el `id_prefix` correspondiente del nivel `levels.components`.
     - Si la ruta contiene `{name}`, preguntar al usuario por el nombre específico del servicio/paquete.

3. **Cálculo de ID Secuencial**:
   - Listar los archivos en el directorio de destino.
   - Buscar el ID más alto existente (`T-PRE-COMP-XXXX`).
   - Incrementar el número para el nuevo ID.

4. **Formato de Salida**:
   - **ID**: `T-{prefix}-{comp_prefix}-{number}` (si no hay prefijo de componente, omitir el guion central).
   - **Archivo**: `[ID]-descripcion-corta.md`.
   - **Ruta Completa**: [Path Definido en Config].

## Ejemplo de Resolución (Aprexx)
- **Config**: `prefix: APX`.
- **Tarea**: Master (Global).
- **Resultado**: `T-APX-0245` -> `docs/plan/tasks/T-APX-0245-mi-tarea.md`.

- **Config**: `prefix: APX`, `comp_prefix: SRV` (services).
- **Tarea**: Servicio "orchestrator".
- **Resultado**: `T-APX-SRV-0012` -> `services/orchestrator/docs/backlog/T-APX-SRV-0012-fix-bug.md`.
