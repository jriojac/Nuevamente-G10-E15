# GAP-04 — Metadata pedagógica mínima

**Proyecto:** NuevaMente
**Área:** Data / IA
**Tipo:** GAP de arquitectura y diseño
**Prioridad:** Alta
**Estado:** 🟡 Propuesta — pendiente de aprobación

---

## 1. Objetivo

Definir qué **metadata mínima** necesita el pipeline de IA para permitir:

* mejorar el chunking;
* facilitar el retrieval;
* orientar el Query Builder;
* adaptar el contenido al perfil del usuario;
* generar los formatos del MVP;
* mantener trazabilidad hacia el documento original.

El objetivo **no** es enriquecer cada fragmento con la mayor cantidad posible de información.

La decisión debe buscar el equilibrio entre:

> **utilidad para el pipeline + calidad + complejidad + tiempo de implementación + mantenibilidad.**

---

# 2. Situación actual

El pipeline definido para NuevaMente contempla:

```text
Documento
   ↓
Extracción / Normalización
   ↓
Chunking
   ↓
Metadata
   ↓
Embeddings
   ↓
Knowledge Core
   ↓
Query Builder
   ↓
Retrieval
   ↓
Context Builder
   ↓
Generación
   ↓
Validación
```

La metadata se encuentra entre **chunking y retrieval**, pero también puede ser utilizada posteriormente por otros componentes.

Por lo tanto, no debe diseñarse únicamente pensando en el almacenamiento.

Debe responder a una pregunta:

> ¿Qué información adicional sobre cada fragmento realmente ayuda al sistema a encontrar, seleccionar, contextualizar o generar contenido?

---

# 3. Problema

El pipeline necesita información estructurada sobre los fragmentos del documento, pero actualmente no está completamente definido:

* qué campos son obligatorios;
* qué campos son opcionales;
* quién los genera;
* qué componentes los consumen;
* cuáles son necesarios para el MVP;
* cuáles pueden agregarse posteriormente.

Existe además el riesgo de crear una metadata excesivamente rica desde el inicio.

Por ejemplo, podríamos generar:

* resumen;
* conceptos;
* preguntas hipotéticas;
* prerequisitos;
* dificultad;
* tipo de contenido;
* relaciones;
* sector;
* tiempo estimado de estudio;
* score de anclaje;
* etc.

Pero cada campo adicional implica:

```text
más procesamiento
       ↓
más lógica
       ↓
más almacenamiento
       ↓
más validaciones
       ↓
más posibilidades de inconsistencia
       ↓
más mantenimiento
```

Por eso necesitamos definir una **metadata mínima viable**.

---

# 4. ¿Existe realmente un GAP?

### Sí.

El pipeline necesita metadata para trabajar de manera consistente, pero todavía no existe una definición cerrada de:

1. campos mínimos;
2. obligatoriedad;
3. origen de cada campo;
4. consumidores;
5. reglas de generación;
6. evolución futura.

Por tanto:

> **GAP-04 requiere una decisión arquitectónica antes de cerrar la implementación de IA-03 e IA-04.**

---

# 5. Principio de diseño

La metadata debe cumplir una regla:

> **Cada campo debe existir porque un componente del sistema lo necesita.**

No se debe agregar metadata únicamente porque:

* puede ser útil algún día;
* mejora visualmente el dataset;
* es técnicamente interesante;
* otro sistema la utiliza;
* una propuesta externa la recomienda.

Primero debemos identificar:

```text
Campo
  ↓
¿Quién lo consume?
  ↓
¿Para qué?
  ↓
¿Mejora una decisión del pipeline?
  ↓
¿Es necesario para el MVP?
```

Si la respuesta es no, puede quedar fuera del MVP.

---

# 6. Metadata candidata

A partir del pipeline definido y de las propuestas analizadas, podemos agrupar la metadata en diferentes categorías.

## 6.1 Identificación y trazabilidad

| Campo         | Propósito                          |
| ------------- | ---------------------------------- |
| `document_id` | Identificar el documento de origen |
| `chunk_id`    | Identificar el fragmento           |
| `section`     | Identificar la sección de origen   |
| `source`      | Mantener referencia al origen      |

Estos campos tienen una función principalmente estructural y de trazabilidad.

---

## 6.2 Información semántica

| Campo          | Propósito                        |
| -------------- | -------------------------------- |
| `concept`      | Concepto principal del fragmento |
| `content_type` | Tipo de contenido                |
| `difficulty`   | Nivel de dificultad              |

Estos campos pueden ayudar a:

* filtrar;
* recuperar;
* adaptar;
* seleccionar contexto;
* orientar la generación.

---

## 6.3 Metadata pedagógica enriquecida

Se pueden considerar:

| Campo                    | Propósito                                     |
| ------------------------ | --------------------------------------------- |
| `summary`                | Resumen del fragmento                         |
| `prerequisites`          | Conceptos previos necesarios                  |
| `hypothetical_questions` | Preguntas que podrían derivarse del contenido |
| `relationships`          | Relación con otros conceptos                  |
| `main_concept`           | Concepto central                              |

Estos campos pueden aportar valor, pero requieren mayor procesamiento y reglas de generación.

---

# 7. Propuesta de metadata mínima para el MVP

Se propone inicialmente:

```text
document_id
chunk_id
section
content_type
concept
difficulty
source
```

Representado conceptualmente:

```json
{
  "document_id": "doc_001",
  "chunk_id": "chunk_001",
  "section": "Introducción",
  "content_type": "CONCEPT",
  "concept": "Redes de computadores",
  "difficulty": "JUNIOR",
  "source": {
    "reference": "document.pdf",
    "page": 3
  }
}
```

> Este JSON es conceptual. El esquema técnico definitivo debe definirse durante la implementación de IA-03/IA-04.

---

# 8. ¿Por qué estos campos?

## `document_id`

Permite relacionar cada chunk con el documento original.

Es necesario para:

* trazabilidad;
* recuperación;
* agrupación;
* respuesta;
* validación de fuentes.

### Decisión propuesta

**MVP: obligatorio.**

---

## `chunk_id`

Identifica un fragmento individual.

Permite:

* distinguir chunks;
* depurar retrieval;
* analizar resultados;
* rastrear evidencia.

### Decisión propuesta

**MVP: obligatorio.**

---

## `section`

Permite conservar el contexto estructural del documento.

Ejemplo:

```text
Documento
 ├── Introducción
 ├── Conceptos básicos
 │    ├── Redes LAN
 │    └── Redes WAN
 └── Conclusiones
```

Un chunk que pertenece a:

```text
Conceptos básicos > Redes LAN
```

puede conservar una referencia estructural que el contenido textual por sí solo podría perder.

### Decisión propuesta

**MVP: obligatorio cuando la estructura del documento lo permita.**

Si un documento no tiene secciones claras, no se debe inventar una estructura.

---

# 9. `content_type`

Permite diferenciar la naturaleza del contenido.

Ejemplos:

```text
CONCEPT
DEFINITION
EXAMPLE
PROCEDURE
LIST
TABLE
CODE
WARNING
INTRODUCTION
CONCLUSION
```

La lista definitiva de valores todavía debe ser definida.

### Importante

No debemos crear una taxonomía excesivamente grande.

La clasificación debe ser:

* útil;
* estable;
* fácil de validar;
* utilizada realmente por el pipeline.

### Decisión propuesta

**MVP: sí, con catálogo reducido y cerrado.**

---

# 10. `concept`

Representa el concepto principal asociado al chunk.

Ejemplo:

```text
Chunk:
"Una red LAN conecta dispositivos dentro de un área geográfica limitada..."

concept:
"Red LAN"
```

Puede utilizarse para:

* búsqueda semántica;
* filtros;
* Query Builder;
* organización del contexto;
* evaluación.

### Riesgo

La identificación automática del concepto puede ser imperfecta.

Por eso debemos evitar asumir que:

> `concept` = verdad absoluta.

Debe considerarse metadata auxiliar.

### Decisión propuesta

**MVP: sí, si puede generarse de manera consistente.**

---

# 11. `difficulty`

Permite asociar el contenido con un nivel pedagógico.

Los perfiles del MVP son:

```text
JUNIOR
SENIOR
EJECUTIVO
```

Sin embargo, es importante distinguir:

```text
profile ≠ difficulty
```

El perfil representa al usuario.

La dificultad representa una característica del contenido.

Por ejemplo:

```text
Perfil: JUNIOR
Chunk difficulty: INTERMEDIATE
```

No necesariamente significa que el sistema deba descartar ese chunk.

Puede servir como señal para selección y adaptación.

### Decisión propuesta

**MVP: sí, pero su uso exacto en retrieval/generación debe validarse.**

---

# 12. `source`

La metadata debe mantener la referencia al origen del contenido.

Ejemplo:

```json
{
  "reference": "manual_oci.pdf",
  "page": 15,
  "section": "Compute"
}
```

Esto es importante para:

* trazabilidad;
* validación;
* grounding;
* construcción de `sources` en la respuesta.

### Importante

La metadata interna puede contener más información que el contrato público.

Por ejemplo:

```text
metadata interna
    ↓
chunk_id
similarity
retrieval_rank
embedding_id
...
```

Pero no todo debe exponerse al Backend o Frontend.

### Decisión propuesta

**MVP: obligatorio para mantener trazabilidad.**

---

# 13. Metadata enriquecida: ¿MVP o futuro?

Se analizarán los siguientes campos:

```text
summary
prerequisites
hypothetical_questions
relationships
main_concept
nicho_sector
tiempo_estimado_estudio_minutos
anclaje_fuente_score
```

La propuesta es **no convertirlos automáticamente en requisitos del MVP**.

---

# 14. Opción A — Metadata mínima

```text
document_id
chunk_id
section
content_type
concept
difficulty
source
```

### Ventajas

* menor complejidad;
* menor tiempo de implementación;
* menor costo computacional;
* menor riesgo de inconsistencias;
* fácil de probar;
* suficiente para iniciar retrieval + generación.

### Desventajas

* menor riqueza pedagógica;
* algunas estrategias avanzadas podrían necesitar información adicional.

---

# 15. Opción B — Metadata enriquecida desde el inicio

Incluir además:

```text
summary
prerequisites
hypothetical_questions
relationships
main_concept
...
```

### Ventajas

* mayor información disponible;
* potencialmente mejores señales para retrieval;
* mayor capacidad de adaptación pedagógica.

### Desventajas

* mayor complejidad;
* mayor procesamiento;
* más tiempo;
* mayor superficie de errores;
* más campos que validar;
* difícil determinar qué campo realmente aporta valor.

---

# 16. Opción C — Metadata evolutiva basada en evidencia

Esta opción combina ambas estrategias.

### Fase inicial

Implementar metadata mínima:

```text
document_id
chunk_id
section
content_type
concept
difficulty
source
```

### Evaluación

Medir:

* calidad del retrieval;
* suficiencia del contexto;
* calidad de generación;
* adaptación al perfil;
* trazabilidad.

### Si aparece un problema

Identificar qué información falta.

Ejemplo:

```text
Problema:
Quiz recupera contenido demasiado general.

        ↓

Análisis

        ↓

¿El problema es chunking?
¿embeddings?
¿retrieval?
¿Query Builder?
¿metadata?

        ↓

Si metadata es la causa

        ↓

Agregar campo específico
```

Esta estrategia evita enriquecer el sistema sin evidencia.

---

# 17. Propuesta

## Adoptar la Opción C

> **Metadata mínima inicialmente + evolución basada en evidencia.**

No se propone construir desde el inicio una metadata pedagógica altamente enriquecida.

El sistema debe permitir agregar nuevos campos posteriormente sin romper el pipeline.

---

# 18. Relación con el Query Builder

La metadata puede convertirse en una señal utilizada por el Query Builder.

Ejemplo:

```text
Documento
+
Perfil = JUNIOR
+
Formato = QUIZ
+
Metadata
       ↓
Query Builder
       ↓
Señales de búsqueda
       ↓
Retriever
```

Pero esto no significa que todos los campos deban utilizarse directamente.

El Query Builder debe consumir únicamente la metadata que realmente ayude a definir la estrategia de retrieval.

Esto mantiene la separación:

```text
Metadata
   ↓
información sobre el contenido

Query Builder
   ↓
define señales de búsqueda

Retriever
   ↓
ejecuta la búsqueda
```

---

# 19. Relación con Chunking

La metadata no debe utilizarse para compensar un chunking deficiente.

Ejemplo:

```text
Chunking incorrecto
       ↓
metadata muy rica
       ↓
retrieval
```

No necesariamente resolverá el problema.

Por eso el orden lógico sigue siendo:

```text
Documento
   ↓
Normalización
   ↓
Chunking correcto
   ↓
Metadata
   ↓
Embeddings
   ↓
Retrieval
```

La metadata complementa al chunking; no lo sustituye.

---

# 20. Relación con Embeddings

Los embeddings representan principalmente el contenido semántico.

La metadata aporta señales adicionales.

Conceptualmente:

```text
                 ┌──────────────┐
                 │   Contenido  │
                 └──────┬───────┘
                        │
                    Embedding
                        │
                        ▼
                  Búsqueda semántica
                        
Metadata ───────────────┐
                        │
                        ▼
                Filtros / señales
```

Esto permite que retrieval combine:

* similitud semántica;
* información estructural;
* información pedagógica.

La estrategia exacta de combinación queda abierta para IA-04/IA-05.

---

# 21. Relación con los perfiles

Los perfiles:

```text
JUNIOR
SENIOR
EJECUTIVO
```

no deben convertirse automáticamente en tres conjuntos diferentes de metadata.

La metadata describe el contenido.

El perfil describe al usuario.

```text
                 ┌──────────────┐
                 │   Metadata   │
                 │ del contenido│
                 └──────┬───────┘
                        │
                        ▼
                  Query / Context
                        ▲
                        │
                 ┌──────┴───────┐
                 │    Perfil    │
                 │ del usuario  │
                 └──────────────┘
```

Esto mantiene desacoplados:

* contenido;
* usuario;
* formato.

---

# 22. Relación con los formatos MVP

La misma metadata debe poder alimentar los cuatro formatos:

```text
                  Knowledge Core
                       │
             ┌─────────┴─────────┐
             │                   │
         Metadata             Context
             │                   │
             └─────────┬─────────┘
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
      FLASHCARD       QUIZ      EXECUTIVE
                                      SUMMARY
                       │
                       ↓
                   MIND MAP
```

No se propone crear una metadata independiente por formato.

Eso generaría:

```text
metadata_flashcard
metadata_quiz
metadata_summary
metadata_mindmap
```

y aumentaría innecesariamente la complejidad.

---

# 23. Implementación MVP

## 23.1 Componente responsable

La generación y asociación de metadata estará dentro del flujo de Data/IA.

Conceptualmente:

```text
Documento normalizado
        ↓
Chunking
        ↓
Metadata Enricher
        ↓
Chunk + Metadata
        ↓
Embeddings
        ↓
Knowledge Core
```

---

## 23.2 Estructura conceptual

Una estructura inicial podría ser:

```text
Chunk
 ├── chunk_id
 ├── document_id
 ├── text
 └── metadata
      ├── section
      ├── content_type
      ├── concept
      ├── difficulty
      └── source
```

No se establece todavía una implementación concreta.

La estructura final dependerá de la tecnología seleccionada para el Knowledge Core / Vector Store.

---

# 24. Reglas MVP

### Regla 1

`document_id` y `chunk_id` deben permitir trazabilidad inequívoca.

### Regla 2

No inventar `section` cuando el documento no proporciona una estructura identificable.

### Regla 3

Los valores categóricos deben tener un catálogo controlado.

### Regla 4

La metadata no debe reemplazar el contenido original del chunk.

### Regla 5

Los campos deben poder ser utilizados por algún componente del pipeline.

### Regla 6

Los campos opcionales no deben bloquear el procesamiento cuando no puedan determinarse de forma confiable.

### Regla 7

Agregar metadata nueva requiere identificar el problema que resuelve.

---

# 25. Ejemplo de flujo MVP

Documento:

```text
"Una red LAN permite conectar dispositivos
dentro de un área geográfica limitada..."
```

### Después del chunking

```text
chunk_id: chunk_001
```

### Enriquecimiento

```json
{
  "document_id": "doc_001",
  "chunk_id": "chunk_001",
  "section": "Conceptos básicos",
  "content_type": "DEFINITION",
  "concept": "Red LAN",
  "difficulty": "JUNIOR",
  "source": {
    "reference": "redes.pdf",
    "page": 3
  }
}
```

### Embedding

```text
chunk + metadata
       ↓
embedding
       ↓
Knowledge Core
```

### Retrieval

```text
Perfil: JUNIOR
Formato: FLASHCARD
       ↓
Query Builder
       ↓
Retriever
       ↓
chunk_001
```

### Generación

El LLM recibe el contexto recuperado y genera el formato solicitado.

---

# 26. ¿Qué queda fuera del MVP?

No se consideran obligatorios inicialmente:

```text
summary
prerequisites
hypothetical_questions
relationships
nicho_sector
tiempo_estimado_estudio_minutos
anclaje_fuente_score
```

Tampoco se establece como requisito:

* Knowledge Graph;
* GraphRAG;
* clasificación pedagógica avanzada;
* metadata generada por múltiples modelos;
* enriquecimiento multimodal;
* taxonomías complejas.

Estas capacidades pueden evaluarse posteriormente.

---

# 27. ¿Cuándo agregar metadata adicional?

Se propone este ciclo:

```text
Problema observado
       ↓
Medición
       ↓
Hipótesis
       ↓
¿La metadata puede resolverlo?
       ↓
Prueba
       ↓
Comparación
       ↓
¿Existe mejora medible?
       │
     Sí ─────────→ incorporar
       │
      No
       ↓
mantener fuera
```

Esto conecta GAP-04 directamente con el enfoque definido en GAP-03:

> **Primero demostrar el problema; después introducir complejidad.**

---

# 28. Riesgos

| Riesgo                                          | Impacto | Mitigación                    |
| ----------------------------------------------- | ------- | ----------------------------- |
| Metadata excesiva                               | Alto    | Limitar MVP                   |
| Campos inconsistentes                           | Alto    | Catálogos controlados         |
| Metadata incorrecta                             | Alto    | Validación y evaluación       |
| Metadata no utilizada                           | Medio   | Exigir consumidor             |
| Costo de enriquecimiento                        | Medio   | Generar solo lo necesario     |
| Dependencia excesiva del LLM                    | Medio   | Mantener reglas simples       |
| Metadata utilizada como sustituto del contenido | Alto    | Mantener chunk original       |
| Dificultad para evolucionar esquema             | Medio   | Diseñar estructura extensible |

---

# 29. Criterios para cerrar GAP-04

El GAP podrá considerarse cerrado cuando exista acuerdo sobre:

* [ ] Metadata mínima del MVP.
* [ ] Campos obligatorios.
* [ ] Campos opcionales.
* [ ] Catálogo inicial de `content_type`.
* [ ] Valores permitidos para `difficulty`.
* [ ] Estructura de `source`.
* [ ] Responsable de generación.
* [ ] Uso de metadata en retrieval.
* [ ] Reglas para campos no disponibles.
* [ ] Estrategia para agregar metadata posteriormente.
* [ ] Integración con IA-03.
* [ ] Integración con IA-04.
* [ ] Pruebas mínimas.

---

# 30. Relación con Issues

| Issue     | Relación                                               |
| --------- | ------------------------------------------------------ |
| **IA-01** | Define dónde participa metadata dentro del pipeline    |
| **IA-02** | Proporciona información estructural del documento      |
| **IA-03** | Responsable principal del chunking + metadata          |
| **IA-04** | Utiliza metadata junto con embeddings / Knowledge Core |
| **IA-05** | Puede utilizar metadata como filtros/señales           |
| **IA-06** | Utiliza contexto enriquecido para generación           |
| **IA-07** | Puede validar trazabilidad y consistencia              |
| **IA-08** | No expone necesariamente toda la metadata interna      |

---

# 31. Evaluación de propuestas externas

Cualquier propuesta adicional de metadata debe evaluarse con:

| Criterio      | Pregunta                                  |
| ------------- | ----------------------------------------- |
| Problema      | ¿Qué problema real resuelve?              |
| Consumidor    | ¿Qué componente la utiliza?               |
| Necesidad MVP | ¿Es realmente necesaria ahora?            |
| Calidad       | ¿Mejora el resultado?                     |
| Complejidad   | ¿Cuánto agrega?                           |
| Tiempo        | ¿Cuánto demora implementarla?             |
| Costo         | ¿Aumenta consumo de recursos/API?         |
| Mantenimiento | ¿Quién mantiene el campo?                 |
| Consistencia  | ¿Puede generarse de forma confiable?      |
| Medición      | ¿Podemos demostrar que mejora?            |
| Alternativa   | ¿Existe una solución más sencilla?        |
| Futuro        | ¿Puede quedar para una siguiente versión? |

Clasificación:

```text
ADOPTAR
   ↓
ADAPTAR
   ↓
FUTURO
   ↓
NO ADOPTAR
```

No se debe incorporar una propuesta automáticamente por provenir de una investigación técnica.

---

# 32. Decisión propuesta

### 🟡 Propuesta para aprobación

Adoptar una estrategia de:

> **Metadata mínima + evolución basada en evidencia.**

Metadata inicial:

```text
document_id
chunk_id
section
content_type
concept
difficulty
source
```

Con las siguientes reglas:

1. No enriquecer el MVP innecesariamente.
2. Mantener trazabilidad.
3. Utilizar catálogos controlados.
4. Mantener la metadata desacoplada del perfil y formato.
5. Permitir evolución futura.
6. Agregar nuevos campos únicamente cuando exista una necesidad demostrable.
7. Medir antes de aumentar la complejidad.

---

# 33. Decisión pendiente del equipo

Antes de cerrar IA-03/IA-04, Data/IA debe validar:

```text
¿Aceptamos esta metadata mínima?
             │
        ┌────┴────┐
       Sí          No
       │            │
       ↓            ↓
Implementar     Revisar campos
       │            │
       └─────┬──────┘
             ↓
        IA-03 / IA-04
```

---

# 34. Estado

**GAP-04:** 🟡 Propuesta

**Decisión propuesta:**

> Metadata mínima para MVP, con evolución basada en evidencia.

**No se consideran requisitos MVP:** metadata pedagógica avanzada, Knowledge Graph, GraphRAG ni enriquecimiento excesivo.

**Próximo paso:**

Validar la propuesta con Data/IA y cerrar los campos mínimos antes de implementar completamente IA-03 e IA-04.
