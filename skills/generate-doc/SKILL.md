---
description: Generación o actualización de documentación técnica y compliance
---

# Skill: Documentation (/generate-doc)

Este flujo (ahora skill) guía la generación o actualización de documentación técnica y de arquitectura.

## Pasos de la Skill

### 1. Analizar Cambios
Identificar el impacto en la arquitectura o diseño del sistema provenientes de los cambios recientes.

### 2. Generar/Actualizar Documentación (Doc Generator)
- Crear o modificar `docs/architecture/design_[modulo].md`.
- **Diagramas**: Es obligatorio incluir diagramas `sequenceDiagram` o `classDiagram` (Mermaid) priorizándolos sobre texto denso.
- Explicar entradas, salidas y trazabilidad con requisitos.
- Mantener actualizada la sección de Decisiones Técnicas (ADR).

### 3. Control de Compliance de Seguridad (CRÍTICO)
Si hay cambios que afecten a la **seguridad, credenciales, autenticación o cifrado**, es **obligatorio** asegurar que la documentación en `docs/architecture/security/` sea revisada y actualizada consecuentemente.

### 4. Confirmar
Verificar que la documentación generada es fiel a la implementación actual del código.
