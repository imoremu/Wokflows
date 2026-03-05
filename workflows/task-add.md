---
description: Añade una nueva tarea al backlog del producto siguiendo estándares de Issue-as-Code v3.1
---

# Workflow: Añadir Tarea al Backlog (/task-add)

Este flujo permite registrar tareas pendientes en el backlog del producto, siguiendo el estándar **Issue-as-Code distribuido v3.1 (Global/Local)**.

## Estructura del Backlog

El backlog se organiza de forma descentralizada según la naturaleza del componente y la configuración en `task_config.yaml`:

- **Tareas Maestras (Globales)**: `docs/plan/tasks/`
- **Servicios (Backend)**: `services/[nombre]/docs/backlog/`
- **App (HMI)**: `app/[nombre]/docs/backlog/`
- **Paquetes (Soporte)**: `packages/[nombre]/docs/backlog/`

En el archivo `task_config.yaml` se definen el prefijo del proyecto (`[PRJ]`), el prefijo de cada componente (`[COMP]`) y las rutas de destino correspondientes (tanto globales como de componente).

## Pasos

1.  **Clasificación e Identificación de Destino** (Skill: `@task-namer`):
    *   Determinar si la tarea es de nivel **Master** o de **Componente**. Toda tarea de componente debe tener un `parent_id` apuntando a su Tarea Maestra. Si no existe la maestra, se debe crear una.
    *   Cargar `task_config.yaml` para resolver el prefijo del proyecto y la ruta de destino.
    *   Calcular el ID secuencial basándose en los archivos existentes en la ruta resuelta.
    *   **Resultado**: ID de tarea (ej: `T-[PRJ]-[COMP]-XXXX`) y ruta de archivo.

2.  **Asignación de Metadatos** (Skill: `@task-generator`):
    *   Cargar el template correspondiente al nivel de la tarea.
    *   Asignar **Peso (Weight)** según prioridad (0-10 Crítica, 10-100 Alta, 100-1000 Estándar, 1000+ Mejora Futura).
    *   Establecer versión objetivo, fechas de creación y estado inicial (`backlog`).

3.  **Generación del Documento** (Skill: `@task-generator`):
    *   Crear el archivo `.md` en la ruta calculada.
    *   **Importante**: La tarea de componente debe incluir obligatoriamente el `parent_id` apuntando a su Tarea Maestra.
    *   Incluir secciones de **Objetivo Técnico**, **Criterios de Aceptación (BDD)** y **Plan de Implementación (TDD)**.

4.  **Vinculación y Trazabilidad** (Skill: `@doc-generator`):
    *   Localizar la Tarea Maestra vinculada en `docs/plan/tasks/`.
    *   Añadir el enlace a la nueva tarea de componente en la sección `## 🛠 Tareas de Componente`.
    *   Validar que todos los enlaces relativos funcionen correctamente entre los directorios.

## Estados del Workflow

## Verificación de la Tarea

### Checklist de Calidad
- [ ] **ID Correcto**: El ID sigue el patrón `T-[PRJ]-[COMP]-[NNNN]` y es el siguiente de la secuencia.
- [ ] **Ubicación**: El archivo se ha creado en la ruta definida por `task_config.yaml`.
- [ ] **Metadatos**: El frontmatter tiene `type`, `weight`, `status` y `parent_id` (para tareas de componente).
- [ ] **Trazabilidad**:
    - [ ] La Tarea Maestra tiene un enlace a esta nueva tarea en `## 🛠 Tareas de Componente`.
    - [ ] El `parent_id` de la tarea de componente es válido.
- [ ] **Estructura**: El cuerpo del markdown contiene las secciones de **Objetivo**, **BDD** (Escenarios) y **TDD** (Plan de Tests).
- [ ] **Enlaces**: Todos los enlaces relativos (`../`) funcionan correctamente (verificados).
- [ ] **Standard**: El lenguaje de BDD sigue la regla "English Keywords + Spanish Content".

