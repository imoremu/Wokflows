# 🤖 Wokflows — AI Agent Workflows & Skills

Este repositorio centraliza los **workflows** y **skills** reutilizables para agentes de IA (Cursor, Antigravity, etc.) que siguen el estándar **Issue-as-Code distribuido v3.0**.

La idea central es que estos archivos actúan como un **sistema operativo de desarrollo** para el agente: le dicen exactamente cómo nombrar tareas, qué pasos seguir, cómo revisar código y cómo hacer commit, de forma consistente en cualquier proyecto que los importe.

> **Modo de uso previsto:** este repo está diseñado para integrar sus carpetas `.agent/` y `.cursor/` directamente en la raíz de cualquier proyecto consumer mediante `git checkout` dirigido. Todos los proyectos comparten la misma base de conocimiento y actualizan sus instrucciones con un único comando.

---

## 📁 Estructura del Repositorio

```
Wokflows/
├── .agent/                    # Fuente canónica (leída por Antigravity y similares)
│   ├── workflows/             # Procesos orquestados (slash commands /nombre)
│   │   ├── task-add.md        # /task-add    → Añadir tarea al backlog
│   │   ├── task-dev.md        # /task-dev    → Ciclo completo de desarrollo
│   │   ├── bug-add.md         # /bug-add     → Registrar una anomalía (bug)
│   │   ├── bug-fix.md         # /bug-fix     → Resolver una anomalía
│   │   ├── commit.md          # /commit      → Generar commit semántico
│   │   ├── generate-bdd.md    # /generate-bdd → Generar feature file BDD
│   │   ├── generate-doc.md    # /generate-doc → Generar documentación técnica
│   │   ├── review-code.md     # /review-code  → Revisión de código
│   │   ├── review-fix.md      # /review-fix   → Revisión de un bug fix
│   │   └── review-test.md     # /review-test  → Revisión de la suite de tests
│   └── skills/                # Habilidades especializadas
│       ├── task-namer/        # Calcula ID y ruta de una tarea
│       ├── doc-generator/     # Genera/actualiza documentación técnica
│       ├── bdd-generator/     # Crea feature files Gherkin en español
│       ├── code-reviewer/     # Audita calidad del código (puntuación 1-10)
│       ├── test-reviewer/     # Audita calidad de la suite de tests
│       ├── bug-fix-reviewer/  # Verifica que un fix resuelve el problema raíz
│       ├── commit-generator/  # Genera mensajes de commit semánticos
│       └── dev-flow/          # Orquestador del ciclo BDD → TDD → Dev → QA → Doc
├── .cursor/                   # Leída por Cursor IDE
│   ├── commands/              # ← junction → .agent/workflows/  (mismos archivos)
│   └── skills/                # ← junction → .agent/skills/     (mismas carpetas)
└── README.md
```

> **Fuente única de verdad:** los archivos viven en `.agent/`. Las carpetas bajo `.cursor/` son junctions locales (Windows) o symlinks (Unix) que apuntan a `.agent/`, de modo que ambas herramientas leen exactamente el mismo contenido sin duplicación.

---

## 🔄 Workflows

El nombre del archivo determina el slash command. Por ejemplo, `task-add.md` se invoca como `/task-add`.

### `/task-add` — Añadir Tarea al Backlog

Registra una nueva tarea en el backlog del producto siguiendo el estándar **Issue-as-Code distribuido v3.0 (Master/Package)**.

**Niveles:**
- **Master**: Tarea de negocio/épica. ID: `T-APX-XXXX`. Ubicación: `docs/plan/tasks/`.
- **Package**: Tarea técnica de componente. ID: `T-APX-[PKG]-XXXX`. Ubicación: `<paquete>/docs/backlog/`.

**Pasos:**
1. **Identificación**: Determinar nivel y paquete (HMI, CTX, AI, LC).
2. **Asignación**: Calcular ID secuencial y asignar **Weight** (0-10 Crítica, 10-100 Alta, 100-1000 Desarrollo, 1000+ Roadmap).
3. **Creación**: Generar el archivo `.md` con el formato correspondiente y la vinculación obligatoria (parent_id).
4. **Vinculación**: Sincronizar enlaces entre Master y Package.

**IDs:** `T-APX-XXXX` (Master) · `T-APX-[PKG]-XXXX` (Package)

---

### `/task-dev` — Ciclo de Desarrollo

Orquesta el ciclo completo **BDD → TDD → Dev → QA → Doc → Commit** para una tarea.

**Modos:**
- **Master Mode** (`T-[PRJ]-XXXX`): Ejecuta secuencialmente todas las tareas de componente hijas.
- **Package Mode** (`T-[PRJ]-[COMP]-XXXX`): Foco exclusivo en un componente técnico.

**Comandos relacionados:** `/review-test` · `/review-code` · `/generate-doc` · `/commit`

---

### `/bug-add` — Registrar Anomalía

Crea el archivo de seguimiento de un bug siguiendo el estándar Issue-as-Code distribuido.

**Niveles:**
- `B-[PRJ]-XXXX` → Bug maestro (multi-paquete), en `docs/plan/tasks/`
- `B-[PRJ]-[PKG]-XXXX` → Bug de componente, en `<paquete>/docs/backlog/`

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
T-APX-XXXX             # Tarea Maestra
T-APX-[PKG]-XXXX       # Tarea de Paquete
B-APX-XXXX             # Bug Maestro
B-APX-[PKG]-XXXX       # Bug de Paquete
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

Este repositorio está diseñado para que sus carpetas `.agent/` y `.cursor/` aterricen **directamente en la raíz de cualquier proyecto** que quiera usar los workflows y skills. La integración se hace mediante `git checkout` dirigido, que copia solo las carpetas que importan sin crear dependencias de submódulo complejas.

### 1. Setup inicial en un proyecto nuevo

```bash
# Registrar este repo como remote (sólo una vez):
git remote add wokflows https://github.com/<org>/Wokflows.git
git fetch wokflows

# Traer las carpetas .agent/ y .cursor/ a la raíz del proyecto:
git checkout wokflows/main -- .agent .cursor

# Commitear en el proyecto consumer:
git add .agent .cursor
git commit -m "chore(agent): init AI agent configuration from Wokflows"
```

### 2. Actualizar a la última versión

```bash
git fetch wokflows
git checkout wokflows/main -- .agent .cursor
git add .agent .cursor
git commit -m "chore(agent): update AI agent configuration to latest"
```

### 3. Estructura resultante en el proyecto consumer

```
mi-proyecto/
├── .agent/                    ← workflows y skills (leído por Antigravity)
│   ├── workflows/
│   │   ├── task-add.md
│   │   ├── task-dev.md
│   │   └── ...
│   └── skills/
│       ├── task-namer/
│       └── ...
├── .cursor/                   ← mismo contenido (leído por Cursor IDE)
│   ├── commands/              # mismos *.md que .agent/workflows/
│   └── skills/                # mismas carpetas que .agent/skills/
├── task_config.yaml           ← configuración específica del proyecto
├── src/
└── docs/
```

> **Sin duplicación:** en el consumer los archivos `.cursor/` son copias reales (Git no preserva junctions entre repos), pero provienen del mismo commit de Wokflows. Al actualizar, `git checkout wokflows/main -- .agent .cursor` regenera ambas carpetas en una sola operación.

### 4. Configurar `task_config.yaml` en el proyecto

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

> **Nota:** `task_config.yaml` es propio de cada proyecto y no forma parte de Wokflows.

---

## 🛠 Mantenimiento de este repo

Las carpetas `.cursor/commands/` y `.cursor/skills/` son **junctions** (Windows) que apuntan a `.agent/workflows/` y `.agent/skills/` respectivamente. Git los trackea como archivos independientes, por lo que:

- Al editar un workflow en `.agent/workflows/`, el cambio se refleja automáticamente en `.cursor/commands/` (misma carpeta física).
- Al hacer commit, hay que incluir **ambas rutas**: `git add .agent .cursor` para que Git registre el cambio en los dos árboles.

```bash
# Flujo de edición en este repo:
# 1. Edita el archivo en .agent/workflows/ o .agent/skills/
# 2. Commitea incluyendo ambas carpetas:
git add .agent .cursor
git commit -m "..."
git push
```

Si por alguna razón las junctions se rompen (p.ej. clonar en Unix), recréalas:

```bash
# Unix / Mac:
rm -rf .cursor/commands .cursor/skills
ln -s ../.agent/workflows .cursor/commands
ln -s ../.agent/skills    .cursor/skills

# Windows (PowerShell, sin admin necesario):
Remove-Item .cursor\commands, .cursor\skills -Recurse -Force
New-Item -ItemType Junction -Path ".cursor\commands" -Target ".agent\workflows"
New-Item -ItemType Junction -Path ".cursor\skills"   -Target ".agent\skills"
```
