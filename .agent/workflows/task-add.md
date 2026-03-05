---
description: Añade una nueva tarea al backlog del producto siguiendo estándares de Issue-as-Code v3.0
---

# Workflow: Añadir Tarea al Backlog (/task-add)

Este flujo permite registrar tareas pendientes en el backlog del producto, siguiendo el estándar **Issue-as-Code distribuido v3.0 (Master/Package)**.

## Estructura del Backlog

El backlog se organiza de forma descentralizada:

- **Tareas Maestras (Globales)**: `docs/plan/tasks/` (Definen el "Qué" / Épicas)
- **HMI**: `packages/hmi/docs/backlog/`
- **Contexto**: `packages/context/docs/backlog/`
- **IA/Orquestador**: `packages/orchestrator/docs/backlog/`
- **Licencia**: `packages/license/docs/backlog/`

## Workflow

### 1. Identificación del Nivel y Paquete

Determinar si es una tarea de negocio (Master) o técnica (Package):
- **Master**: Afecta a la visión global o a múltiples paquetes. ID: `T-APX-XXXX`. Ubicación: `docs/plan/tasks/`.
- **Package**: Tarea técnica específica de un componente. ID: `T-APX-[PKG]-XXXX`. Ubicación: `<paquete>/docs/backlog/`.
  - `[PKG]` puede ser: `HMI`, `CTX`, `AI`, `LC`.

### 2. Asignación de ID y Peso

- **ID**: Secuencial por nivel/paquete. Verificar el último ID en el directorio correspondiente.
- **Peso (Weight)**: Valor entero (0 - ∞). 
  - **Prioridad Crítica**: 0-10 (Urgencias).
  - **Prioridad Alta**: 10-100 (ASAP).
  - **Desarrollo**: 100-1000.
  - **Roadmap**: 1000+.
  - *Nota*: Tareas de versiones futuras deben tener pesos mayores que las actuales.

### 3. Creación del Archivo

**Nombre:** `[ID]-descripcion-corta.md`

**Formato para Tarea Maestra (Master):**

```markdown
---
id: T-APX-XXXX
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
- [T-APX-PKG-XXXX: Título](../../packages/pkg/docs/backlog/T-APX-PKG-XXXX.md)
```

**Formato para Tarea de Paquete (Package):**

```markdown
---
id: T-APX-[PKG]-XXXX
title: "Título técnico"
type: feature | enhancement | refactor | technical-debt
parent_id: T-APX-XXXX
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
- [T-APX-XXXX: Título Maestros](../../../docs/plan/tasks/T-APX-XXXX.md)

## 🎯 Objetivo Técnico
[Descripción técnica del cambio]

## 📋 Criterios de Aceptación (BDD)
- [ ] **CA-1:** Escenario: [Descripción]

## 🧪 Plan de Implementación (TDD)
- [ ] **Test 1:** [Descripción del test unitario]

## 🏗️ Implementación Técnica
[Detalles técnicos, módulos afectados, etc.]
```

### 4. Vinculación Master/Package (Obligatoria)

- **Package -> Master**: Es obligatorio incluir el `parent_id` en el frontmatter y un enlace en la sección `## 🔗 Tarea Maestra`.
- **Master -> Package**: Es obligatorio listar las tareas técnicas en la sección `## 🛠 Tareas de Componente`.
- **Automatización**: Se puede usar `python tools/scripts/link_tasks.py` para sincronizar estos enlaces automáticamente.

### 5. Registro en el Hub

No es necesario registrar manualmente en tablas globales. El Hub escaneará los directorios automáticamente y ordenará por `version` y luego por `weight`.

## Estados del Workflow

Los estados permitidos para el campo `status` son:

- **backlog**: Tarea registrada pero no planificada ni iniciada.
- **planned**: Tarea asignada a un plan de ejecución (sprint/fase).
- **in_progress**: Tarea en curso (desarrollo activo).
- **completed**: Tarea finalizada y verificada (reemplaza a 'closed' o 'resolved').
- **blocked**: Tarea bloqueada por dependencias externas o impedimentos.

## Verificación de la Tarea

### Checklist de Calidad
- [ ] **ID Correcto**: El ID sigue el patrón `T-APX-[XXXX]` o `T-APX-[PKG]-XXXX` y es el siguiente de la secuencia.
- [ ] **Ubicación**: El archivo se ha creado en la ruta correcta según su nivel.
- [ ] **Metadatos**: El frontmatter tiene `type`, `weight`, `status` y `parent_id` (para tareas de componente).
- [ ] **Trazabilidad (Bidireccional)**:
    - [ ] La Tarea Maestra tiene un enlace a esta nueva tarea en `## 🛠 Tareas de Componente`.
    - [ ] El `parent_id` y el enlace en `## 🔗 Tarea Maestra` son válidos para tareas de componente.
- [ ] **Estructura**: El cuerpo del markdown contiene las secciones obligatorias (**Objetivo**, **Escenarios BDD**, **Plan TDD**).
- [ ] **Enlaces**: Todos los enlaces relativos (`../`) funcionan correctamente y apuntan a los archivos `.md`.
- [ ] **Standard**: El lenguaje de BDD sigue la regla "English Keywords + Spanish Content".