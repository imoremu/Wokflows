---
name: bug-add
description: Registro de una nueva anomalía (bug) siguiendo el estándar Issue-as-Code (Distribuido)
---

# Skill: Registro de Anomalía (/bug-add)

Este flujo implementa el estándar de **Issue-as-Code distribuido v3.0**, donde cada componente es responsable de su propio historial de calidad, integrándose con la visión global.

## Estructura de Anomalías
El backlog de anomalías se organiza de forma descentralizada. Así, para un proyecto dado habrá bugs maestros (críticos/negocio), que a su vez pueden relacionarse con bugs de cada uno de los componentes. Los componentes, a su vez, estarán divididos en:

- **Servicios (Backend)**: Servicios de backend
- **Apps (HMI)**: aplicaciones / interfaces de usuario
- **Paquetes (Soporte)**: paquetes de soporte al resto de elementos

En el archivo `task_config.yaml` se definen el prefijo del proyecto (`[PRJ]`), el prefijo de cada componente (`[COMP]`), las rutas base (`path`) y las subcarpetas de destino (`folders.tasks` y `folders.bugs`).

## Pasos de la Skill

### 1. Clasificación e Identificación de Destino (Namer)

- Determinar si el bug es de nivel **Master** o de **Componente**. Existirá bug maestro si el bug afecta a producción (no en fase de desarrollo) o si el el bug afecta a más de un componente. En caso contrario, será exclusivamente un bug de componente.

Nota: En caso de ser un bug de producción, el id informado a clientes y usuarios será el id del bug maestro.

- Cargar `task_config.yaml` de la raíz del proyecto para resolver el prefijo del proyecto, la ruta base y la subcarpeta `folders.bugs`.
- Calcular el ID secuencial basándose en los archivos existentes en la ruta final resuelta (`path` + `folders.bugs`).
- **Resultado**: Nuevo ID de bug (ej: `B-[PRJ]-XXXX` o `B-[PRJ]-[COMP]-XXXX`) y ruta de archivo final.

### 2. Asignación de Metadatos

Al crear el bug, se aplican las siguientes reglas:
- **Estado y Versión por Defecto**:
    - `status: backlog`
    - `version: ""` (vacío)
- **Excepción (Asignación Explícita)**:
    - Si el usuario indica explícitamente una versión, establecer `status: planned` y `version: [versión proporcionada]`.
- **Asignación automática desde rama**:
    - Si la rama activa sigue el patrón `release/vX.Y`, proponer `version: "vX.Y.0"` y `status: planned`.
    - Si la rama activa sigue el patrón `hotfix/vX.Y.Z`, proponer `version: "vX.Y.Z"` y `status: planned`.
    - El usuario puede rechazar la asignación automática.
- Establecer fechas de creación (`created_at`) y actualización (`updated_at`).

### 3. Creación del Archivo

**Nombre del archivo:** `[ID]-descripcion-corta.md`

**Metadatos (YAML Frontmatter):**

```markdown
---
id: B-[PRJ]-[COMP]-XXXX
title: "Título descriptivo"
type: bug
weight: [integer]
version: ""
status: backlog
effort_unit: h
estimated_effort: 0
remaining_effort: 0
actual_effort: 0
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
references: [RF-XXX, T-[PRJ]-YYYY]
parent_id: [Master ID if Componente bug]
assets: [./assets/[ID]-evidencia.png]
---
```

### 3. Gestión de Assets

- Guardar evidencias en la carpeta `assets/` local al componente o en la subcarpeta `assets/` dentro de la ruta de bugs de maestros.
- Referenciar relativamente en el markdown.

### 4. Ciclo de Vida y Pesos

- Los bugs críticos (urgentes) deben tener un **Weight** entre 0 y 10.
- Los bugs prioritarios deben tener un **Weight** entre 10 y 100.
- Los bugs de desarrollo deben tener un **Weight** entre 100 y 1000.
- Los bugs no necesarios deben tener un **Weight** mayor que 1000.

- El Hub permitirá reordenar y editar estos pesos para priorizar el "Fix" sobre el "Feature".

### 5. Cierre

- Al cerrar un bug de componente, se debe actualizar el `remaining_effort` a 0.
- Si es el último bug de componente vinculado a un Master, se debe cerrar también el Master.

## Estados del Workflow

Los estados permitidos para el campo `status` son:

- **backlog**: Anomalía registrada y pendiente de priorizar (estado inicial por defecto).
- **planned**: Anomalía asignada a una versión específica para su futura resolución.
- **open**: Anomalía registrada y pendiente de análisis (opcional, si se prefiere sobre backlog).
- **in_progress**: Anomalía en proceso de corrección ("En curso").
- **completed**: Corrección implementada y verificada (reemplaza a 'closed' o 'resolved').
- **superseded**: Anomalía corregida debida a un cambio previo por otra tarea o anomalía. Implica que no hay cambio trazado con ella.
- **blocked**: Anomalía bloqueada por dependencias externas o impedimentos.
- **rejected**: Anomalía descartada (no reproducible, duplicada, etc.).

