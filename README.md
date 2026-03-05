# 🤖 Wokflows — AI Agent Workflows & Skills

Este repositorio centraliza los **workflows** y **skills** reutilizables para agentes de IA (Cursor, Antigravity, etc.) que siguen el estándar **Issue-as-Code distribuido v3.0**.

La idea central es que estos archivos actúan como un **sistema operativo de desarrollo** para el agente: le dicen exactamente cómo nombrar tareas, qué pasos seguir, cómo revisar código y cómo hacer commit, de forma consistente en cualquier proyecto que los importe.

> **Modo de uso previsto:** este repo se integra como un **submódulo Git** en la carpeta `.agent/` de cualquier proyecto consumer. Esto permite centralizar la lógica del agente y actualizarla en todos los proyectos simultáneamente.

---

## 📁 Estructura del Repositorio

```
Wokflows/
├── workflows/             # Procesos orquestados (slash commands /nombre)
│   ├── task-add.md        # /task-add    → Añadir tarea al backlog
│   ├── task-dev.md        # /task-dev    → Ciclo completo de desarrollo
│   ├── bug-add.md         # /bug-add     → Registrar una anomalía (bug)
│   ├── bug-fix.md         # /bug-fix     → Resolver una anomalía
│   ├── commit.md          # /commit      → Generar commit semántico
│   ├── generate-bdd.md    # /generate-bdd → Generar feature file BDD
│   ├── generate-doc.md    # /generate-doc → Generar documentación técnica
│   ├── review-code.md     # /review-code  → Revisión de código
│   ├── review-fix.md      # /review-fix   → Revisión de un bug fix
│   └── review-test.md     # /review-test  → Revisión de la suite de tests
├── skills/                # Habilidades especializadas
│   ├── task-namer/        # Calcula ID y ruta de una tarea
│   ├── doc-generator/     # Genera/actualiza documentación técnica
│   ├── bdd-generator/     # Crea feature files Gherkin en español
│   ├── code-reviewer/     # Audita calidad del código (puntuación 1-10)
│   ├── test-reviewer/     # Audita calidad de la suite de tests
│   ├── bug-fix-reviewer/  # Verifica que un fix resuelve el problema raíz
│   ├── commit-generator/  # Genera mensajes de commit semánticos
│   └── dev-flow/          # Orquestador del ciclo BDD → TDD → Dev → QA → Doc
└── README.md
```

---

## 🔄 Workflows

El nombre del archivo determina el slash command. Por ejemplo, `task-add.md` se invoca como `/task-add`.

### `/task-add` — Añadir Tarea al Backlog

Registra una nueva tarea en el backlog del producto siguiendo el estándar **Issue-as-Code distribuido v3.0 (Master/Componente)**.

**Niveles:**
- **Master**: Tarea de negocio/épica. ID: `T-[PRJ]-XXXX`. Ubicación: `docs/plan/tasks/`.
- **Componente**: Tarea técnica de componente. ID: `T-[PRJ]-[COMP]-XXXX`. Ubicación: `<componente>/docs/backlog/`.

**Pasos:**
1. **Identificación**: Determinar nivel y componente (HMI, CTX, AI, LC).
2. **Asignación**: Calcular ID secuencial y asignar **Weight** (0-10 Crítica, 10-100 Alta, 100-1000 Desarrollo, 1000+ Roadmap).
3. **Creación**: Generar el archivo `.md` con el formato correspondiente y la vinculación obligatoria (parent_id).
4. **Vinculación**: Sincronizar enlaces entre Master y Componente.

**IDs:** `T-[PRJ]-XXXX` (Master) · `T-[PRJ]-[COMP]-XXXX` (Componente)

---

### `/task-dev` — Ciclo de Desarrollo

Orquesta el ciclo completo **BDD → TDD → Dev → QA → Doc → Commit** para una tarea.

**Modos:**
- **Master Mode** (`T-[PRJ]-XXXX`): Ejecuta secuencialmente todas las tareas de componente hijas.
- **Component Mode** (`T-[PRJ]-[COMP]-XXXX`): Foco exclusivo en un componente técnico.

**Comandos relacionados:** `/review-test` · `/review-code` · `/generate-doc` · `/commit`

---

### `/bug-add` — Registrar Anomalía

Crea el archivo de seguimiento de un bug siguiendo el estándar Issue-as-Code distribuido.

**Niveles:**
- `B-[PRJ]-XXXX` → Bug maestro (multi-paquete), en `docs/plan/tasks/`
- `B-[PRJ]-[COMP]-XXXX` → Bug de componente, en `<componente>/docs/backlog/`

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

### `/generate-doc` — Generar Documentación Técnica

Actualiza o crea documentación de arquitectura en `docs/architecture/` usando `doc-generator`. Incluye diagramas Mermaid y compliance de seguridad.

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

Las skills son especialistas que los workflows invocan para tareas concretas. No se usan directamente como slash commands.

| Skill | Responsabilidad |
|---|---|
| `task-namer` | Calcula ID secuencial y ruta desde `task_config.yaml` |
| `doc-generator` | Crea/actualiza `docs/architecture/design_*.md` con diagramas Mermaid |
| `bdd-generator` | Produce feature files Gherkin en español con tags y trazabilidad RF |
| `code-reviewer` | Auditoría de código multi-categoría con puntuación 1–10 |
| `test-reviewer` | Auditoría de BDD, unit e integration tests con detección de orfandad |
| `bug-fix-reviewer` | Valida que un fix es completo y sin regresiones |
| `commit-generator` | Genera mensajes semánticos con prefijo `type(scope): ID - subject` |
| `dev-flow` | Orquestador Red → Green → QA → Doc → Commit |

---

## 🏗 Estándares

### Issue-as-Code Distribuido v3.0

Cada componente (servicio, app, paquete) es dueño de su propio backlog. Las tareas maestras en `docs/plan/tasks/` dan visibilidad global; las de componente viven junto al código.

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
📄 Sync Phase  → /generate-doc (si hay cambios de diseño)
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
├── .agent/                    ← submódulo (este repo)
│   ├── workflows/             ← slash commands (leído por Antigravity)
│   └── skills/                ← habilidades
├── task_config.yaml           ← configuración específica del proyecto
├── src/
└── docs/
```

### 3. Configuración para Cursor IDE (Opcional)

Si usas Cursor IDE, este busca los comandos en `.cursor/commands/`. Puedes crear un enlace para que use los mismos workflows del agente:

```bash
# Windows (PowerShell):
New-Item -ItemType Junction -Path ".cursor\commands" -Target ".agent\workflows"

# Unix / Mac:
ln -s ../.agent/workflows .cursor/commands
```

### 4. Actualizar a la última versión

Para actualizar los workflows en un proyecto consumer:

```bash
git submodule update --remote .agent
git add .agent
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
    path: docs/plan/tasks/
  components:
    - type: service
      id_prefix: SRV
      path: services/{name}/docs/backlog/
    - type: app
      id_prefix: HMI
      path: app/{name}/docs/backlog/
    - type: package
      id_prefix: PKG
      path: packages/{name}/docs/backlog/
```

> **Nota:** `task_config.yaml` es propio de cada proyecto y no forma parte de este repositorio.
