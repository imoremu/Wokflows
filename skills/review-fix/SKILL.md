---
name: review-fix
description: Revisión específica de correcciones de bugs
---

# Skill: Review Fix (/review-fix)

Este flujo (ahora skill) está especializado en revisar y validar que la corrección aplicada a un Bug (Anomalía) es válida, completa y segura.

## Pasos de la Skill

### 1. Analizar el Fix
Identificar exactamente qué issue (bug) o qué comentarios de una revisión anterior se están intentando resolver con los cambios actuales.

### 2. Verificación de Corrección y Regresiones (Bug Fix Reviewer)
Verificar rigurosamente técnica y funcionalmente:
* ¿Se ha resuelto el problema de raíz (Root Cause) o es solo un parche?
* ¿Se han añadido tests de integración/unitarios que cubran el escenario específico que fallaba?
* ¿Se han introducido nuevos problemas (regresiones) colaterales?

### 3. Veredicto Final
Emitir un veredicto claro y tajante determinando si la corrección es suficiente:
* ✅ **RESUELTO**: Corrección completa, de alta calidad y testeada.
* ⚠️ **PARCIAL**: Falta algún detalle menor o test.
* ❌ **NO RESUELTO**: El problema original persiste o se ha roto algo grave.

### 4. Generar Reporte de Validación
Guardar en `docs/review/code_reviews/code_review_report - [Fase] - Re-Review [Bug ID].md` con la siguiente estructura simplificada:

#### Estructura del Reporte:
1. **Veredicto**: [RESUELTO / PARCIAL / NO RESUELTO]
2. **Análisis de Validación**: Por cada punto (Root Cause, Tests, Regresiones):
   - **Explicación**: Breve razonamiento del cumplimiento.
   - **Puntos Fuertes/Debilidades** (si aplica).
3. **Plan de Acción (si no está resuelto)**: Listado de mejoras por criticidad (🔴 CRÍTICO, 🟠 ALTA).

