---
description: Añade una nueva tarea al backlog del producto siguiendo estándares de Issue-as-Code v3.0
---

# Workflow: Añadir Tarea al Backlog (/task-add)

Este flujo permite registrar tareas pendientes en el backlog del producto, siguiendo el estándar **Issue-as-Code distribuido v3.0 (Master/Componente)**.

## Estructura del Backlog
El backlog se organiza de forma descentralizada. Así, para un proyecto dado habrá tareas de proyecto (épicas), que a su vez pueden dividirse en tareas de cada uno de los componentes. Los componentes, a su vez, estarán divididos en

- **Servicios (Backend)**: Servicios de backend
- **Apps (HMI)**: aplicaciones / interfaces de usuario
- **Paquetes (Soporte)**: paquetes de soporte al resto de elementos

En el archivo `task_config.yaml` se definen el prefijo del proyecto (`[PRJ]`), el prefijo de cada componente (`[COMP]`) y las rutas de destino correspondientes (tanto globales como de componente).

## Pasos

### 1.  **Clasificación e Identificación de Destino** (Skill: `@task-namer`):
    *   Determinar si la tarea es de nivel **Master** o de **Componente**. Toda tarea de componente debe tener un `parent_id` apuntando a su Tarea Maestra. Si no existe la maestra, se debe crear una.
    *   Cargar `task_config.yaml` para resolver el prefijo del proyecto y la ruta de destino.
    *   Calcular el ID secuencial basándose en los archivos existentes en la ruta resuelta.
    *   **Resultado**: ID de tarea (ej: `T-[PRJ]-[COMP]-XXXX`) y ruta de archivo.

### 2.  **Asignación de Metadatos**:
    *   Cargar el template correspondiente al nivel de la tarea.
    *   Asignar **Peso (Weight)** según prioridad (0-10 Crítica, 10-100 Alta, 100-1000 Estándar, 1000+ Mejora Futura).
    *   Establecer versión objetivo, fechas de creación y estado inicial (`backlog`).

### 3. Creación del Archivo

**Nombre:** `[ID]-descripcion-corta.md`

**Formato para Tarea Maestra (Master):**

```markdown
---
id: T-[PRJ]-XXXX
title: "Título descriptivo"
type: funcional | despliegue | diseño | tools | infra
weight: [integer]
version: "v0.2.X"
status: backlog | planned | in_progress | completed | blocked
estimated_effort: 0
remaining_effort: 0
actual_effort: 0
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
original_ref: [Legacy ID if any]
---

# [ID]: [Título]

## 🎯 Objetivo de Negocio
[Descripción del valor de negocio y el "qué" se quiere conseguir]

## 📋 Criterios de Aceptación (Nivel Máster)
- [ ] **CA-M-1:** [Criterio de alto nivel]

## 🛠 Tareas de Componente
- [T-[PRJ]-[COMP]-XXXX: Título]
```

**Formato para Tarea de Componente:**

```markdown
---
id: T-[PRJ]-[COMP]-XXXX
title: "Título técnico"
type: feature | enhancement | refactor | technical-debt
parent_id: T-[PRJ]-XXXX
weight: [integer]
version: "v0.2.X"
status: backlog | planned | in_progress | completed | blocked
estimated_effort: 0
remaining_effort: 0
actual_effort: 0
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
---

# [ID]: [Título]

## 🔗 Tarea Maestra
- [T-[PRJ]-XXXX: Título Maestros](../../../docs/plan/tasks/T-[PRJ]-XXXX.md)

## 🎯 Objetivo Técnico
[Descripción técnica del cambio]

## 📋 Criterios de Aceptación (BDD)
- [ ] **CA-1:** Escenario: [Descripción]

## 🧪 Plan de Implementación (TDD)
- [ ] **Test 1:** [Descripción del test unitario]

## 🏗️ Implementación Técnica
[Detalles técnicos, módulos afectados, etc.]
```

### 4. Vinculación Master/Componente (Obligatoria)

- **Componente-> Master**: Es obligatorio incluir el `parent_id` en el frontmatter y un enlace en la sección `## 🔗 Tarea Maestra`.
- **Master -> Componente**: Es obligatorio listar las tareas técnicas en la sección `## 🛠 Tareas de Componente`.
- **Automatización**: Se puede usar `python tools/scripts/link_tasks.py` para sincronizar estos enlaces automáticamente.


## Estados del Workflow

Los estados permitidos para el campo `status` son:

- **backlog**: Tarea registrada pero no planificada ni iniciada.
- **planned**: Tarea asignada a un plan de ejecución (sprint/fase).
- **in_progress**: Tarea en curso (desarrollo activo).
- **completed**: Tarea finalizada y verificada (reemplaza a 'closed' o 'resolved').
- **blocked**: Tarea bloqueada por dependencias externas o impedimentos.

## Verificación de la Tarea

### Checklist de Calidad
- [ ] **ID Correcto**: El ID sigue el patrón `T-[PRJ]-[XXXX]` o `T-[PRJ]-[COMP]-XXXX` y es el siguiente de la secuencia.
- [ ] **Ubicación**: El archivo se ha creado en la ruta correcta según su nivel.
- [ ] **Metadatos**: El frontmatter tiene `type`, `weight`, `status` y `parent_id` (para tareas de componente).
- [ ] **Trazabilidad (Bidireccional)**:
    - [ ] La Tarea Maestra tiene un enlace a esta nueva tarea en `## 🛠 Tareas de Componente`.
    - [ ] El `parent_id` y el enlace en `## 🔗 Tarea Maestra` son válidos para tareas de componente.
- [ ] **Estructura**: El cuerpo del markdown contiene las secciones obligatorias (**Objetivo**, **Escenarios BDD**, **Plan TDD**).
- [ ] **Enlaces**: Todos los enlaces relativos (`../`) funcionan correctamente y apuntan a los archivos `.md`.
- [ ] **Standard**: El lenguaje de BDD sigue la regla "English Keywords + Spanish Content".