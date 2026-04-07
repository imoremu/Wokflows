---
name: release
description: Gestión de lanzamientos y etiquetado de versiones (Release Management)
---

# Skill: Gestión de Lanzamientos (/release)

Esta skill formaliza el cierre de una versión del proyecto, asegurando que todos los entregables estén listos y etiquetados correctamente en Git.

## Pasos de la Skill

### 1. Validación Pre-Release
- **Validar rama activa**:
  - Si es un bloque funcional: la rama debe seguir el patrón `release/vX.Y`.
  - Si es un hotfix: la rama debe seguir el patrón `hotfix/vX.Y.Z`.
  - Si la rama es `main` o cualquier otra, **abortar** e informar al usuario.
- Verificar coherencia: el número de versión de la rama debe coincidir con la versión en `task_config.yaml`.
- **Validar Completitud del Backlog**:
  - Determinar la versión objetivo a través de `task_config.yaml` o de la rama de trabajo.
  - Ejecutar el script `python .agents/skills/release/scripts/check_release_completeness.py --version [VERSIÓN]`
  - Si el script devuelve un error (exit code 1), abortar la release e informar al usuario de las tareas/bugs expuestos en la salida.
- Verificar que no hay cambios pendientes sin commitear (staged o unstaged).
- Ejecutar `/review-test` y `/review-code` de forma global si es necesario.
- Confirmar que el `CHANGELOG.md` está actualizado (e invocar `/manage-docs` si no lo está).

### 2. Identificación de la Versión
- Leer la versión actual de la configuración del proyecto (`task_config.yaml` -> `project.version`).
- La versión ya está determinada por la rama de trabajo:
  - `release/vX.Y` → release `vX.Y.0`
  - `hotfix/vX.Y.Z` → release `vX.Y.Z`
- Confirmar con el usuario que la versión es correcta.

### 3. Ejecución del Bump
- Verificar que todos los manifiestos ya tienen la versión correcta (deberían estar actualizados desde `/start-version`). Si no, actualizarlos ahora.
- Crear un commit de release: `chore(release): vX.Y.Z`.
- Sincronizar (cerrar) la tarea de release `T-[PRJ]-REL-XXXX` en el backlog.

### 4. Etiquetado (Tagging)
- Crear una etiqueta anotada en Git: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`.
- Indicar al usuario que debe realizar:
  1. Merge de la rama hacia `main`: `git checkout main && git merge release/vX.Y`
  2. Push con tags: `git push --follow-tags`
  3. Eliminar la rama de release: `git branch -d release/vX.Y`

### 4b. Post-Release para Hotfix (Solo si rama `hotfix/*`)
- Tras el merge a `main`, verificar si existe una rama `release/` activa.
- Si existe, hacer merge del hotfix hacia esa rama también:
  `git checkout release/vA.B && git merge hotfix/vX.Y.Z`
- Informar al usuario de los merges realizados.

### 5. Notificación
- Generar un resumen de la release para ser compartido (extraído del CHANGELOG).

