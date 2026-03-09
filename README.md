# 🤖 Wokflows — AI Agent Workflows & Skills

Este repositorio centraliza los **workflows** y **skills** reutilizables para agentes de IA (Cursor, Antigravity, etc.) que siguen el estándar **Issue-as-Code distribuido v3.0**.

La idea central es que estos archivos actúan como un **sistema operativo de desarrollo** para el agente: le dicen exactamente cómo nombrar tareas, qué pasos seguir, cómo revisar código y cómo hacer commit, de forma consistente en cualquier proyecto que los importe.

> **Modo de uso previsto:** este repo se integra como un **submódulo Git** en la carpeta `.agent/` de cualquier proyecto consumer. Esto permite centralizar la lógica del agente y actualizarla en todos los proyectos simultáneamente.

---

## 📁 Estructura del Repositorio

```
Wokflows/
├── workflows/             # Proxies para comandos de Antigravity
│   ├── task-add-workflow.md
│   ├── req-analysis-workflow.md
│   ├── needs-analysis-workflow.md
│   ├── platform-plan-workflow.md
│   ├── work-plan-workflow.md
│   ├── task-list-workflow.md
│   ├── task-dev-workflow.md
│   ├── bug-add-workflow.md
│   ├── bug-fix-workflow.md
│   ├── commit-workflow.md
│   ├── generate-bdd-workflow.md
│   ├── manage-docs-workflow.md
│   ├── review-code-workflow.md
│   ├── review-fix-workflow.md
│   └── review-test-workflow.md
├── skills/                # Lógica core y habilidades especializadas
│   ├── task-namer/        # Calcula ID y ruta de una tarea
│   ├── doc-generator/     # Genera/actualiza documentación técnica
│   ├── bdd-generator/     # Crea feature files Gherkin en español
│   ├── code-reviewer/     # Audita calidad del código (puntuación 1-10)
│   ├── test-reviewer/     # Audita calidad de la suite de tests
│   ├── bug-fix-reviewer/  # Verifica que un fix resuelve el problema raíz
│   ├── commit-generator/  # Genera mensajes de commit semánticos
│   ├── dev-flow/          # Orquestador del ciclo BDD → TDD → Dev → QA → Doc
│   ├── task-add/          # Añade tarea al backlog (Issue-as-Code)
│   ├── req-analysis/      # Análisis de requisitos funcionales
│   ├── needs-analysis/    # Análisis técnico y NFRs
│   ├── platform-plan/     # Arquitectura y configuración
│   ├── work-plan/         # Plan de desarrollo y creación de tareas
│   ├── task-list/         # Genera backlog técnico en JSON
│   ├── task-dev/          # Lógica completa para desarrollar tarea
│   ├── bug-add/           # Lógica completa para registrar anomalía
│   ├── bug-fix/           # Lógica completa para resolver anomalía
│   ├── commit/            # Lógica completa para generar commit semántico
│   ├── generate-bdd/      # Lógica completa para generar feature BDD
│   ├── manage-docs/       # Gestión inteligente de documentación según docs_config.yaml
│   ├── review-code/       # Lógica completa para revisión de código
│   ├── review-fix/        # Lógica completa para revisión de fix
│   └── review-test/       # Lógica completa para revisión de tests
└── README.md
```

---

## 🔄 Workflows

El nombre del proxy (sin el sufijo `-workflow`) determina el slash command en Antigravity. Por ejemplo, `task-add-workflow.md` se invoca como `/task-add`. En Cursor, las skills son leídas automáticamente de la carpeta `.agents/skills` o `.cursor/rules`.

### `/task-add` — Añadir Tarea al Backlog

Registra una nueva tarea en el backlog del producto siguiendo el estándar **Issue-as-Code distribuido v3.0 (Master/Componente)**.

**Niveles:**
- **Master**: Tarea de negocio/épica. ID: `T-[PRJ]-XXXX`. Urbicación: `docs/plan/tasks/` (calculado con `path` + `folders.tasks`).
- **Componente**: Tarea técnica de componente. ID: `T-[PRJ]-[COMP]-XXXX`. Ubicación: `<comp>/docs/backlog/tasks/` (calculado con `path` + `folders.tasks`).

**Pasos:**
1. **Identificación**: Determinar nivel y componente (HMI, CTX, AI, LC).
2. **Asignación**: Calcular ID secuencial y asignar **Weight** (0-10 Crítica, 10-100 Alta, 100-1000 Desarrollo, 1000+ Roadmap).
3. **Creación**: Generar el archivo `.md` con el formato correspondiente y la vinculación obligatoria (parent_id).
4. **Vinculación**: Sincronizar enlaces entre Master y Componente.

**IDs:** `T-[PRJ]-XXXX` (Master) · `T-[PRJ]-[COMP]-XXXX` (Componente)

---

### `/req-analysis` — Análisis de Requisitos Funcionales

Identifica ambigüedades, asunciones y conflictos en los requisitos originales para asegurar que son accionables.

---

### `/needs-analysis` — Análisis de Necesidades Técnicas

Cuantifica requisitos no funcionales (NFRs), riesgos de compliance y viabilidad de APIs en fases inicial y de madurez.

---

### `/platform-plan` — Necesidades de Plataforma

Define la arquitectura, stack tecnológico y plan de configuración detallado para la infraestructura.

---

### `/work-plan` — Plan de Trabajo

Genera la estrategia de desarrollo técnico (Software) basada en BDD/TDD y las tecnologías elegidas.

---

### `/task-dev` — Ciclo de Desarrollo

Orquesta el ciclo completo **BDD → TDD → Dev → QA → Doc → Commit** para una tarea.

**Modos:**
- **Master Mode** (`T-[PRJ]-XXXX`): Ejecuta secuencialmente todas las tareas de componente hijas.
- **Component Mode** (`T-[PRJ]-[COMP]-XXXX`): Foco exclusivo en un componente técnico.

**Comandos relacionados:** `/review-test` · `/review-code` · `/manage-docs` · `/commit`

---

### `/bug-add` — Registrar Anomalía

Crea el archivo de seguimiento de un bug siguiendo el estándar Issue-as-Code distribuido.

**Niveles:**
- `B-[PRJ]-XXXX` → Bug maestro (multi-paquete), en `docs/plan/bugs/`
- `B-[PRJ]-[COMP]-XXXX` → Bug de componente, en `<comp>/docs/backlog/bugs/`

**Pesos:** 0–10 Crítico · 10–100 Prioritario · 100–1000 Desarrollo · 1000+ Mejora futura

---

### `/bug-fix` — Resolver Anomalía

Guía la resolución de un bug: reproducción con tests, implementación del fix, verificación con `/review-fix` y cierre con `/commit`.

---

### `/commit` — Commit Semántico

Analiza todos los cambios (staged, unstaged y untracked), los agrupa funcionalmente y genera commits con el formato:

```
<type>(<scope>): [ID] - <subject>
```

Regla de oro: **ningún archivo queda sin procesar**.

---

### `/generate-bdd` — Generar Feature BDD

Crea un archivo `.feature` en Gherkin siguiendo la regla **Keywords en español + Contenido en español** usando el skill `bdd-generator`.

---

### `/manage-docs` — Gestión de Documentación del Proyecto

Actualiza la documentación del proyecto basándose en los cambios técnicos y la configuración definida en `docs_config.yaml`. Sigue principios de minimalismo y utilidad.

---

### `/review-code` — Revisión de Código

Audita el código con `code-reviewer`, puntuando (1–10): Seguridad, Eficiencia, Testeabilidad, Mantenibilidad, Documentación y Cobertura de Requisitos. **Mínimo 8/10 en Seguridad y Testeabilidad** para pasar a producción.

---

### `/review-fix` — Revisión de Bug Fix

Usa `bug-fix-reviewer` para verificar que el fix resuelve el problema de raíz sin introducir regresiones. Veredicto: ✅ Resuelto · ⚠️ Parcial · ❌ No Resuelto.

---

### `/review-test` — Revisión de Tests

Audita la suite completa con `test-reviewer`: cobertura BDD (features huérfanas), aislamiento en unit tests y flujo real en integración. **Puntuación mínima 8/10**.

---

## 🧠 Skills

Las skills son especialistas que los proxies de Antigravity o el propio IDE invocan para tareas concretas. No se usan directamente como slash commands.

| Skill | Responsabilidad |
|---|---|
| `req-analysis` | Análisis de ambigüedades y asunciones funcionales |
| `needs-analysis` | Cuantificación de NFRs, rendimiento y compliance |
| `platform-plan` | Definición de arquitectura, stack y plan de infra |
| `work-plan` | Desarrollo de estrategia y registro automático de tareas |
| `task-add` | Calcula IDs dinámicos y añade tareas al backlog |
| `task-list` | Generación de backlog técnico en formato JSON |
| `task-dev` | Orquesta el ciclo de desarrollo BDD → TDD → Dev → QA → Doc |
| `bug-add` | Registra anomalías usando la jerarquía de proyecto y componente |
| `bug-fix` | Verificia logs, corrige bugs y llama a un reviewer riguroso |
| `commit` | Genera mensajes semánticos de commit con trazabilidad |
| `generate-bdd` | Produce feature files Gherkin estandarizados en español |
| `manage-docs` | Gestión inteligente y minimalista de documentación |
| `review-code` | Auditoría de código multicriteroia (Seguridad, Mantenibilidad, etc) |
| `review-fix` | Auditoría específica para evitar regresiones tras un bug fix |
| `review-test` | Detecta features huérfanas, calidad de mocks y aislamiento unitario |

---

## 🏗 Estándares

### Issue-as-Code Distribuido v3.0

Cada componente (servicio, app, paquete) es dueño de su propio backlog. Las tareas maestras en `docs/plan/` dan visibilidad global; las de componente viven junto al código. Ambas separan tareas (`tasks/`) y anomalías (`bugs/`) según la configuración.

### Estructura de IDs

```
T-[PRJ]-XXXX             # Tarea Maestra
T-[PRJ]-[COMP]-XXXX       # Tarea de Componente
B-[PRJ]-XXXX             # Bug Maestro
B-[PRJ]-[COMP]-XXXX       # Bug de Componente
```

`[PRJ]` y `[COMP]` se configuran en `task_config.yaml` de cada proyecto.

### BDD — Regla de Idioma

```gherkin
# language: es
Característica: Título en español
  Escenario: Descripción en español
    Dado que ...
    Cuando ...
    Entonces ...
```

Keywords y contenido **siempre en español**.

### Flujo de Desarrollo Estándar (dev-flow)

```
🔴 Red Phase   → BDD + TDD (tests que fallan)
              ↓  /review-test (mínimo 8/10)
🟢 Green Phase → Implementación
              ↓
🔵 QA Phase    → /review-code (mínimo 8/10)
              ↓
📄 Sync Phase  → /manage-docs (según docs_config.yaml)
              ↓
✅ Final Phase → /commit
```

---

## 🔗 Integración en proyectos consumer

Este repositorio está diseñado para vivir dentro de otros proyectos como un **submódulo Git** en la carpeta `.agent/`.

### 1. Añadir el submódulo

```bash
# Desde la raíz del proyecto consumer:
git submodule add https://github.com/<org>/Wokflows.git .agent
```

### 2. Estructura resultante en el proyecto consumer

```
mi-proyecto/
├── .agents/                    ← submódulo (este repo)
│   ├── workflows/             ← slash commands (leído por Antigravity)
│   └── skills/                ← habilidades
├── task_config.yaml           ← configuración específica del proyecto
├── src/
└── docs/
```

### 3. Configuración para Cursor IDE

Cursor detecta de forma nativa las reglas y skills ubicadas en la carpeta `.agents/`. Solo asegúrate de que el submódulo esté correctamente inicializado como se describe en el paso 1.

### 4. Actualizar a la última versión

Para actualizar los workflows en un proyecto consumer:

```bash
git submodule update --remote .agents
git add .agents
git commit -m "chore(agent): update workflows to latest"
```

### 5. Configurar `task_config.yaml` en el proyecto

Crea este archivo en la raíz del proyecto consumer para que los workflows calculen IDs y rutas correctamente:

```yaml
project:
  prefix: PRJ           # Prefijo global del proyecto (ej: APX)
  name: Mi Proyecto

levels:
  master:
    id_prefix: ""
    path: docs/plan/
    folders:
      tasks: tasks/
      bugs: bugs/
  components:
    - type: service
      id_prefix: SRV
      path: services/{name}/docs/backlog/
      folders:
        tasks: tasks/
        bugs: bugs/
    - type: app
      id_prefix: HMI
      path: app/{name}/docs/backlog/
      folders:
        tasks: tasks/
        bugs: bugs/
    - type: package
      id_prefix: PKG
      path: packages/{name}/docs/backlog/
      folders:
        tasks: tasks/
        bugs: bugs/
```

> **Nota:** `task_config.yaml` es propio de cada proyecto y no forma parte de este repositorio.
