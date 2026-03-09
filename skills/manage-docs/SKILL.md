---
description: Gestión y actualización minimalista de la documentación del proyecto.
---

# Skill: Gestión de Documentación (/manage-docs)

Esta skill orquesta la actualización de los documentos del proyecto definidos en `docs_config.yaml`, asegurando que se mantengan alineados con los cambios técnicos sin añadir ruido innecesario.

## Principios de Actualización
1. **Necesidad**: Solo actualizar si el cambio impacta directamente el propósito del documento.
2. **Minimalismo**: Incluir solo la información mínima útil.
3. **Continuidad**: Mantener el enfoque general y el nivel de profundidad existente. Esto implica solo añadir información o apartados nuevos si es estrictamente necesaria y útil, y siempre manteniendo la coherencia.

## Pasos de la Skill

### 1. Carga de Configuración
- Leer `docs_config.yaml` para identificar los documentos a mantener.
- Cada entrada contiene: `nombre`, `path`, `tipo` (por defecto `md`) y `descripcion`.

### 2. Análisis de Impacto
- Evaluar los cambios realizados en el código o las tareas (`task-dev` o `bug-fix`).
- Identificar cuál de los documentos configurados se ve afectado por estos cambios.

### 3. Actualización de Documentos
Para cada documento afectado:
- Leer el contenido actual.
- Integrar la nueva información siguiendo los principios de minimalismo y utilidad.
- Priorizar diagramas Mermaid si ayudan a simplificar la explicación.
- **Validación**: Asegurar que no se degrada la legibilidad ni se pierde el contexto general.

### 4. Sincronización
- Confirmar que los cambios en la documentación reflejan fielmente la implementación técnica actual.
