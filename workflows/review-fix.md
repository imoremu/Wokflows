// turbo-all
---
description: Proxy para el workflow /review-fix
---

> [!IMPORTANT]
> Este workflow es **TURBO**. Todos los pasos serán auto-ejecutados EXCEPTO:
> - Cambios fuera del entorno (workspace)
> - Comandos git peligrosos (ej. `git push`, `git reset --hard`)
> - **Control de Bucles:** Si una secuencia de comandos se repite más de 3 veces sin progreso, detened el modo turbo y pedid permiso manual.

# /review-fix

Has sido invocado para revisar un fix. Tu **único objetivo** es leer y ejecutar estrictamente los pasos definidos en la skill correspondiente:
👉 Usa la herramienta `view_file` en `../skills/review-fix/SKILL.md` (o la ruta correspondiente si estás en un proyecto consumidor) y sigue sus instrucciones.

