# GAP-06 — Grounding y fidelidad del contenido

**Proyecto:** NuevaMente
**Área:** Data / IA
**Tipo:** GAP de calidad y validación
**Prioridad:** 🔴 Alta
**Estado:** 🟡 Propuesta — pendiente de aprobación

---

# 1. Objetivo

Definir cómo NuevaMente garantizará que el contenido generado por el modelo esté **respaldado por la información recuperada del documento seleccionado**.

El objetivo es reducir:

* información inventada;
* afirmaciones no respaldadas;
* incorporación silenciosa de conocimiento externo;
* distorsión del contenido original;
* pérdida de trazabilidad;
* contradicciones con el documento fuente.

La regla principal es:

> **El contenido generado debe poder justificarse mediante evidencia recuperada del documento.**

---

# 2. Situación actual

El pipeline definido hasta ahora contempla:

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
Context Sufficiency
   ↓
Generación
   ↓
Validación
   ↓
JSON
```

GAP-05 estableció que:

> Si el contexto no es suficiente, el sistema no debe generar.

Sin embargo, todavía falta responder otra pregunta:

> **¿Cómo comprobamos que una respuesta que sí fue generada permanece fiel al contexto utilizado?**

---

# 3. Problema

Que exista contexto suficiente **no garantiza automáticamente** que el LLM genere contenido fiel.

Ejemplo:

```text
Documento:

"Una LAN conecta dispositivos
dentro de un área geográfica limitada."
```

El sistema recupera correctamente el fragmento.

Pero el modelo podría generar:

```text
"Una LAN conecta dispositivos dentro de un área
geográfica limitada y normalmente utiliza Ethernet
con velocidades de hasta X Gbps."
```

La primera parte está respaldada.

La segunda podría no estar presente en el documento.

Por lo tanto:

```text
Contexto correcto
      ≠
Respuesta necesariamente correcta
```

Se necesita una etapa explícita de grounding/fidelidad.

---

# 4. ¿Existe realmente un GAP?

### Sí.

Actualmente necesitamos definir:

1. qué significa fidelidad;
2. qué información debe estar respaldada;
3. cómo se relacionan las afirmaciones con las fuentes;
4. qué validaciones se realizan;
5. qué ocurre cuando una afirmación no está respaldada;
6. qué información debe regresar al Backend;
7. qué parte es automática y qué parte se deja para evolución futura.

---

# 5. Definición propuesta de Grounding

Para NuevaMente:

> **Grounding es la capacidad del sistema para generar contenido cuya información factual esté respaldada por la evidencia recuperada del documento fuente.**

Esto implica que el modelo no debería presentar como parte del contenido:

* hechos externos;
* datos inventados;
* conclusiones que no se desprenden del documento;
* información que no puede relacionarse con una fuente.

---

# 6. Grounding no es lo mismo que Retrieval

Es importante separar responsabilidades.

### Retrieval

Responde:

> ¿Qué información del documento recuperamos?

```text
Query
 ↓
Retriever
 ↓
Chunks
```

### Grounding

Responde:

> ¿Lo que generamos está respaldado por esos chunks?

```text
Chunks
 ↓
Generación
 ↓
Contenido generado
 ↓
¿Está respaldado?
```

Por tanto:

```text
Retrieval
    ↓
selecciona evidencia

Grounding
    ↓
comprueba fidelidad respecto a evidencia
```

---

# 7. Grounding tampoco es lo mismo que contexto suficiente

GAP-05:

> ¿Tenemos suficiente información para generar?

GAP-06:

> ¿Lo que generamos está respaldado por la información utilizada?

Ejemplo:

```text
Contexto
   ↓
Suficiente
   ↓
Generación
   ↓
Afirmación no respaldada
   ↓
Falla de grounding
```

Por eso ambos GAP son necesarios.

---

# 8. Principio fundamental

Se propone adoptar:

> **No basta con recuperar evidencia; el contenido generado debe mantenerse dentro de los límites de esa evidencia.**

Flujo:

```text
                    ┌───────────────┐
                    │    Contexto   │
                    │   recuperado  │
                    └───────┬───────┘
                            ↓
                       Generación
                            ↓
                    ┌───────────────┐
                    │   Grounding   │
                    │   / Fidelity  │
                    └───────┬───────┘
                            ↓
                    ¿Está respaldado?
                       /          \
                     Sí            No
                     ↓              ↓
                 Validación      Ajustar /
                     ↓           rechazar
                  Respuesta
```

---

# 9. ¿Qué debe considerarse una afirmación?

Para poder validar fidelidad, primero necesitamos identificar qué partes del resultado requieren respaldo.

Ejemplo:

```text
"Una LAN conecta dispositivos
dentro de un área geográfica limitada."
```

La afirmación factual es:

> Una LAN conecta dispositivos dentro de un área geográfica limitada.

Pero elementos puramente estructurales como:

```text
Pregunta:
Respuesta:
Flashcard:
```

no necesitan validación factual.

Por lo tanto, la validación debe concentrarse principalmente en:

* hechos;
* definiciones;
* características;
* relaciones;
* instrucciones;
* cifras;
* fechas;
* nombres;
* afirmaciones técnicas.

---

# 10. Tipos de contenido que requieren especial atención

## 10.1 Definiciones

```text
"X es..."
```

Debe existir evidencia que respalde esa definición.

---

## 10.2 Datos numéricos

Ejemplo:

```text
"La instancia soporta 64 GB de RAM."
```

Los valores numéricos requieren especial cuidado porque una pequeña alteración puede cambiar completamente el significado.

---

## 10.3 Relaciones

Ejemplo:

```text
"Servicio A depende de Servicio B."
```

La relación debe estar respaldada.

---

## 10.4 Procedimientos

Ejemplo:

```text
1. Crear la instancia.
2. Configurar la red.
3. Asociar el volumen.
```

Los pasos deben poder relacionarse con el contenido fuente.

---

## 10.5 Comparaciones

Ejemplo:

```text
"X es más adecuado que Y."
```

Una comparación puede introducir una interpretación que no está explícitamente en el documento.

Debe tratarse con especial cuidado.

---

# 11. Fidelidad según formato

La validación no necesariamente debe ser idéntica para los cuatro formatos.

## FLASHCARD

Debe verificarse principalmente:

```text
concepto
+
respuesta
```

---

## QUIZ

Debe verificarse:

```text
pregunta
+
respuesta correcta
+
explicación, si existe
+
distractores
```

Los distractores merecen especial atención.

Un distractor puede ser incorrecto, pero no debe introducir información externa presentada como parte del documento.

---

## EXECUTIVE_SUMMARY

Debe verificarse:

```text
ideas principales
+
síntesis
+
no incorporación de hechos externos
```

La síntesis puede reformular el contenido, pero no debe cambiar su significado.

---

## MIND_MAP

Debe verificarse:

```text
tema central
+
conceptos
+
relaciones
```

Las relaciones entre nodos deben estar respaldadas por el contenido.

---

# 12. Tipos de fidelidad

Se propone distinguir al menos tres dimensiones.

## 12.1 Fidelidad factual

La afirmación generada está respaldada por el contenido.

```text
Fuente:
"Una LAN cubre un área geográfica limitada."

Generado:
"Una LAN conecta dispositivos en un área geográfica limitada."

→ Compatible
```

---

## 12.2 Fidelidad semántica

La reformulación mantiene el significado original.

Fuente:

```text
"El sistema requiere autenticación
antes de acceder al recurso."
```

Generado:

```text
"Es necesario autenticarse antes
de acceder al recurso."
```

→ Mantiene el significado.

---

## 12.3 Fidelidad de fuente

Debe poder identificarse de dónde proviene la información.

```text
Contenido generado
       ↓
evidencia
       ↓
chunk
       ↓
sección / página
       ↓
documento
```

---

# 13. Qué NO significa fidelidad

Fidelidad no significa que el texto generado deba ser idéntico al documento.

El sistema puede:

* resumir;
* reformular;
* reorganizar;
* convertir texto en preguntas;
* convertir texto en tarjetas;
* estructurar conceptos;
* adaptar el nivel de explicación.

La condición es:

> **La transformación no debe introducir hechos que no estén respaldados por la fuente.**

---

# 14. Opciones consideradas

## Opción A — Confiar únicamente en el prompt

Ejemplo:

```text
"Responde solamente utilizando el contexto."
```

### Ventajas

* muy simple;
* rápida implementación;
* sin componente adicional.

### Desventajas

* no garantiza cumplimiento;
* el modelo puede generar información no respaldada;
* difícil de medir;
* difícil de detectar automáticamente.

### Decisión

❌ **No suficiente como única estrategia.**

Puede utilizarse como una primera barrera, pero no como mecanismo completo de validación.

---

# 15. Opción B — Validación mediante reglas

Ejemplo:

```text
Generación
   ↓
Reglas
   ↓
¿Cumple?
```

Las reglas pueden comprobar:

* campos obligatorios;
* fuentes;
* referencias;
* estructura;
* presencia de evidencia;
* correspondencia básica entre contenido y contexto.

### Ventajas

* determinista;
* rápida;
* económica;
* fácil de probar.

### Desventajas

* limitada para verificar significado;
* difícil detectar todas las formas de paráfrasis incorrecta;
* no resuelve completamente la fidelidad semántica.

### Decisión

🟢 **Adoptar como primera capa del MVP.**

---

# 16. Opción C — Segundo LLM como evaluador

Flujo:

```text
Contexto
   ↓
LLM generador
   ↓
Respuesta
   ↓
LLM evaluador
   ↓
¿Fiel?
```

### Ventajas

* puede evaluar relaciones semánticas;
* mayor capacidad para detectar contradicciones;
* flexible.

### Desventajas

* mayor costo;
* mayor latencia;
* segundo punto de fallo;
* comportamiento probabilístico;
* necesita evaluación propia;
* puede generar falsos positivos/negativos.

### Decisión

🟡 **No obligatorio para MVP.**

Puede evaluarse posteriormente.

---

# 17. Opción D — Sistema híbrido

Combinar:

```text
Reglas
+
Fuentes
+
validación estructural
+
validación semántica posterior
```

Y agregar mecanismos más avanzados únicamente cuando exista evidencia de necesidad.

### Decisión propuesta

✅ **Adoptar como estrategia evolutiva.**

El MVP comienza con mecanismos simples.

---

# 18. Estrategia MVP propuesta

La primera versión debería tener al menos:

```text
1. Prompt orientado a grounding
2. Contexto explícito
3. Sources asociadas
4. Validación estructural
5. Validación de trazabilidad
6. Comprobaciones básicas de contenido
```

Conceptualmente:

```text
Contexto
   ↓
Prompt de grounding
   ↓
LLM
   ↓
Resultado estructurado
   ↓
Validación
   ├── estructura
   ├── fuentes
   ├── campos
   └── grounding básico
   ↓
APPROVED / REQUIRES_ADJUSTMENT / REJECTED
```

---

# 19. Prompt de grounding

El prompt debe establecer explícitamente restricciones como:

```text
Utiliza únicamente la información proporcionada
en el contexto recuperado.

No agregues información externa.

Si la información necesaria no está respaldada
por el contexto, no la inventes.

Mantén el significado del contenido fuente.

Cuando corresponda, asocia el contenido generado
con las fuentes utilizadas.
```

Este mecanismo constituye una **barrera de generación**, pero no sustituye la validación.

---

# 20. Sources

El resultado debe mantener referencias a las fuentes utilizadas.

Ejemplo conceptual:

```json
{
  "sources": [
    {
      "source_id": "src_001",
      "document_id": "doc_001",
      "reference": "redes.pdf",
      "page": 3,
      "section": "Conceptos básicos"
    }
  ]
}
```

Esto permite:

```text
respuesta
   ↓
fuente
   ↓
documento original
```

La estructura definitiva debe respetar el contrato de integración.

---

# 21. No exponer información interna de retrieval

La trazabilidad pública no debe exponer necesariamente:

```text
chunk_id
similarity
retrieval_rank
embedding_id
vector_store_id
```

Estos datos pueden permanecer internos.

El contrato público ya establece una separación entre:

```text
información de trazabilidad
```

y:

```text
detalles internos del pipeline.
```

---

# 22. Ejemplo correcto

### Fuente

```text
"Una LAN conecta dispositivos
dentro de un área geográfica limitada."
```

### Generación

```text
Pregunta:
¿Qué es una LAN?

Respuesta:
Es una red que conecta dispositivos
dentro de un área geográfica limitada.
```

### Grounding

```text
✓ Concepto respaldado
✓ Significado conservado
✓ Fuente identificable
```

Resultado:

```text
APPROVED
```

---

# 23. Ejemplo con información no respaldada

### Fuente

```text
"Una LAN conecta dispositivos
dentro de un área geográfica limitada."
```

### Generación

```text
Una LAN conecta dispositivos dentro
de un área geográfica limitada y puede
alcanzar velocidades de 10 Gbps.
```

El valor:

```text
10 Gbps
```

no aparece en la fuente.

Resultado:

```text
NO APROBAR
```

La respuesta debería:

* corregirse;
* regenerarse bajo restricciones;
* o rechazarse.

No debe enviarse como resultado aprobado.

---

# 24. Ejemplo de reformulación válida

### Fuente

```text
"El sistema requiere autenticación
antes de acceder al recurso."
```

### Generación

```text
"Es necesario autenticarse antes
de acceder al recurso."
```

Aunque las palabras sean diferentes:

```text
significado
    ↓
se conserva
```

Resultado:

```text
✓ Fiel
```

Por eso una validación basada únicamente en coincidencia de palabras no es suficiente para todos los casos.

---

# 25. Caso especial: Quiz

Los distractores requieren una regla específica.

Ejemplo:

```text
Pregunta:
¿Qué permite una LAN?

A. Conectar dispositivos dentro de un área limitada.
B. ...
C. ...
D. ...
```

La respuesta correcta debe estar respaldada.

Los distractores pueden ser incorrectos, pero el sistema debe evitar introducir afirmaciones externas innecesarias.

Se debe estudiar posteriormente qué estrategia produce distractores consistentes sin aumentar la cantidad de información no respaldada.

---

# 26. Caso especial: Executive Summary

Un resumen necesariamente transforma y comprime información.

Por eso la validación debe centrarse en:

```text
¿La síntesis mantiene las ideas principales?
¿Introduce información nueva?
¿Cambia relaciones o conclusiones?
¿Mantiene el sentido?
```

No se debe exigir coincidencia textual.

---

# 27. Caso especial: Mind Map

El mapa puede introducir relaciones visuales:

```text
Tema
 ├── Concepto A
 │     └── Concepto B
 └── Concepto C
```

La existencia de una relación entre:

```text
A → B
```

debe poder justificarse mediante el documento.

El sistema no debe inventar relaciones únicamente porque sean plausibles.

---

# 28. ¿Debe existir un `quality_score`?

El contrato contempla un campo:

```text
quality_score
```

pero:

> **No se establece en este GAP un umbral fijo de aprobación.**

No se debe adoptar automáticamente:

```text
quality_score >= 0.85
```

porque todavía no se ha demostrado:

* cómo se calcula;
* qué significa;
* qué tan correlacionado está con fidelidad real;
* qué umbral funciona para cada formato.

Primero debe existir una evaluación experimental.

---

# 29. ¿LLM-as-Judge en MVP?

No se propone como requisito obligatorio.

Podría incorporarse posteriormente para evaluar:

```text
contexto
   +
respuesta
   ↓
evaluador
   ↓
fidelidad semántica
```

Pero antes habría que medir:

* precisión;
* costo;
* latencia;
* falsos positivos;
* falsos negativos;
* estabilidad.

---

# 30. Implementación MVP

Se propone una arquitectura de validación por capas.

```text
                    ┌───────────────┐
                    │    Contexto   │
                    └───────┬───────┘
                            ↓
                       Generación
                            ↓
                  ┌───────────────────┐
                  │ Validación básica │
                  └─────────┬─────────┘
                            ↓
                ┌───────────────────────┐
                │ 1. Schema             │
                │ 2. Sources            │
                │ 3. Trazabilidad       │
                │ 4. Grounding básico   │
                └───────────┬───────────┘
                            ↓
                     Decisión final
```

---

# 31. Responsabilidades

| Componente          | Responsabilidad                            |
| ------------------- | ------------------------------------------ |
| Query Builder       | Definir señales para encontrar evidencia   |
| Retriever           | Recuperar evidencia                        |
| Context Builder     | Construir contexto                         |
| Generator           | Generar limitado al contexto               |
| Grounding Validator | Comprobar fidelidad                        |
| Validation          | Validar estructura y reglas                |
| Backend             | Recibir estado y resultado                 |
| Frontend            | Presentar contenido/fuentes según contrato |

---

# 32. Estados

GAP-05 definió:

```text
APPROVED
REQUIRES_ADJUSTMENT
REJECTED
```

GAP-06 propone utilizarlos así:

### `APPROVED`

El resultado cumple:

* estructura;
* formato;
* perfil;
* evidencia;
* trazabilidad;
* reglas de grounding.

---

### `REQUIRES_ADJUSTMENT`

Existe un resultado potencialmente recuperable.

Ejemplo:

```text
contenido parcialmente respaldado
```

Puede requerir:

* regeneración;
* ajuste;
* revisión;
* recuperación adicional en una futura implementación.

---

### `REJECTED`

El resultado no puede aprobarse de forma confiable.

Ejemplo:

```text
afirmaciones relevantes no respaldadas
```

---

# 33. Flujo completo

Integrando GAP-03, GAP-05 y GAP-06:

```text
Documento
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
Retriever
    ↓
Context Builder
    ↓
¿Contexto suficiente?
    │
    ├── NO
    │    ↓
    │  GAP-05
    │  REQUIRES_ADJUSTMENT /
    │  REJECTED
    │
    └── SÍ
         ↓
      Generación
         ↓
    GAP-06 Grounding
         ↓
    ¿Contenido respaldado?
       │
       ├── NO
       │    ↓
       │  Ajustar / Rechazar
       │
       └── SÍ
            ↓
       Validación
            ↓
        APPROVED
            ↓
           JSON
            ↓
         Backend
```

---

# 34. Pruebas mínimas

Data/IA debería probar al menos:

| Caso                                | Resultado esperado |
| ----------------------------------- | ------------------ |
| Generación completamente respaldada | `APPROVED`         |
| Paráfrasis fiel                     | `APPROVED`         |
| Información externa agregada        | No aprobar         |
| Número no respaldado                | No aprobar         |
| Fuente incorrecta                   | No aprobar         |
| Relación inventada                  | No aprobar         |
| Resumen fiel                        | `APPROVED`         |
| Quiz con respuesta respaldada       | `APPROVED`         |
| Quiz con afirmaciones externas      | No aprobar         |
| Mind Map con relación no sustentada | No aprobar         |
| Resultado estructuralmente inválido | Validación fallida |

---

# 35. Métricas

Para evaluar la solución:

## Grounding

* porcentaje de resultados respaldados;
* porcentaje de afirmaciones no respaldadas;
* tasa de falsos positivos;
* tasa de falsos negativos.

## Calidad

* fidelidad semántica;
* preservación del significado;
* cobertura de evidencia;
* trazabilidad.

## Operación

* latencia;
* costo;
* cantidad de regeneraciones;
* porcentaje de rechazos.

---

# 36. Riesgos

| Riesgo                                | Impacto  | Mitigación                          |
| ------------------------------------- | -------- | ----------------------------------- |
| El LLM agrega información externa     | Muy alto | Prompt + validación                 |
| Validación demasiado estricta         | Alto     | Evaluar falsos negativos            |
| Validación demasiado permisiva        | Muy alto | Casos de prueba                     |
| LLM-as-Judge introduce nuevos errores | Medio    | No hacerlo obligatorio inicialmente |
| Costo elevado                         | Medio    | Reglas simples primero              |
| Latencia                              | Medio    | Validación por capas                |
| Score arbitrario                      | Alto     | No fijar umbral sin evidencia       |
| Fuentes incorrectas                   | Alto     | Validar trazabilidad                |
| Paráfrasis considerada incorrecta     | Medio    | Evaluar semántica, no solo texto    |

---

# 37. Relación con otros GAP

```text
GAP-03
Query Builder
     ↓
Retrieval
     ↓
GAP-05
Contexto suficiente
     ↓
Generación
     ↓
GAP-06
Grounding / Fidelidad
     ↓
GAP-07
Estados de validación
     ↓
GAP-08
Schema de validación
```

Los GAP están relacionados, pero tienen responsabilidades distintas:

| GAP    | Pregunta                             |
| ------ | ------------------------------------ |
| GAP-03 | ¿Qué debemos buscar?                 |
| GAP-05 | ¿Tenemos suficiente evidencia?       |
| GAP-06 | ¿Lo generado está respaldado?        |
| GAP-07 | ¿Qué estado debe tener el resultado? |
| GAP-08 | ¿La respuesta cumple el schema?      |

---

# 38. Qué NO forma parte del MVP

No se establece como requisito:

* LLM-as-Judge;
* NLI;
* score fijo `>= 0.85`;
* evaluación mediante múltiples LLM;
* GraphRAG;
* Knowledge Graph;
* validación avanzada de cada afirmación mediante un modelo independiente;
* sistema autónomo de regeneración ilimitada;
* múltiples validadores especializados por formato.

Estas capacidades podrán evaluarse posteriormente.

---

# 39. Evaluación de propuestas externas

Toda propuesta relacionada con grounding debe evaluarse considerando:

| Criterio      | Pregunta                                   |
| ------------- | ------------------------------------------ |
| Problema      | ¿Qué falla actualmente?                    |
| Evidencia     | ¿Tenemos casos que demuestren el problema? |
| Cobertura     | ¿Qué tipo de errores detecta?              |
| Precisión     | ¿Qué tan confiable es?                     |
| Complejidad   | ¿Cuánto agrega?                            |
| Latencia      | ¿Cuánto aumenta el tiempo?                 |
| Costo         | ¿Cuánto aumenta el consumo?                |
| Mantenimiento | ¿Quién mantiene la solución?               |
| Integración   | ¿Afecta el contrato?                       |
| Medición      | ¿Cómo demostramos mejora?                  |
| Alternativa   | ¿Existe una solución más sencilla?         |
| Futuro        | ¿Puede incorporarse posteriormente?        |

---

# 40. Decisión propuesta

### 🟡 Propuesta para aprobación

Adoptar un enfoque de **Grounding por capas**.

### MVP

```text
Prompt de grounding
        +
Contexto explícito
        +
Sources
        +
Validación estructural
        +
Validación básica de fidelidad
```

Con las siguientes reglas:

1. El contenido generado debe estar respaldado por la evidencia recuperada.
2. Retrieval y grounding son responsabilidades diferentes.
3. Contexto suficiente y fidelidad son evaluaciones diferentes.
4. No se debe confiar únicamente en el prompt.
5. No se establece `quality_score >= 0.85`.
6. LLM-as-Judge no es obligatorio para el MVP.
7. Las fuentes deben conservar trazabilidad.
8. El conocimiento externo del modelo no debe presentarse como información del documento.
9. La validación debe considerar las características de cada formato.
10. Las técnicas avanzadas se incorporarán únicamente si las pruebas demuestran necesidad.

---

# 41. Criterios para cerrar GAP-06

El GAP podrá considerarse cerrado cuando Data/IA y Backend acuerden:

* [ ] Definición operativa de grounding.
* [ ] Diferencia entre grounding y contexto suficiente.
* [ ] Reglas mínimas de fidelidad.
* [ ] Estrategia de sources.
* [ ] Validación básica de contenido.
* [ ] Tratamiento de información no respaldada.
* [ ] Tratamiento de paráfrasis.
* [ ] Reglas específicas para los cuatro formatos.
* [ ] Comportamiento ante fallo de grounding.
* [ ] Integración con `APPROVED`.
* [ ] Integración con `REQUIRES_ADJUSTMENT`.
* [ ] Integración con `REJECTED`.
* [ ] Casos de prueba.
* [ ] Métricas iniciales.
* [ ] Decisión sobre si `quality_score` se utiliza y cómo.
* [ ] Definición de qué queda para futuras versiones.

---

# 42. Estado final

**GAP-06 — Grounding y fidelidad del contenido**

**Estado:** 🟡 Propuesta

**Decisión propuesta:**

> NuevaMente debe validar que el contenido generado esté respaldado por la evidencia recuperada. El MVP utilizará una estrategia por capas basada en contexto explícito, instrucciones de grounding, trazabilidad mediante fuentes y validaciones básicas, sin introducir inicialmente un segundo LLM evaluador ni umbrales arbitrarios.

**Principio rector:**

> **Recuperar evidencia no es suficiente: el contenido generado debe mantenerse dentro de los límites de esa evidencia.**
