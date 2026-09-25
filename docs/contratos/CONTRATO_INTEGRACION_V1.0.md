# REVISIÓN DE PENDIENTES — CONTRATO DE INTEGRACIÓN V1.0

## TechMind / NuevaMente

**Proyecto:** TechMind / NuevaMente  
**Equipo:** G10-LATAM-EQUIPO15  
**Documento relacionado:** `CONTRATO_INTEGRACION_V1.0.md`  
**Estado:** Documento de trabajo para alineación BE + Data + FE  
**Objetivo:** Convertir los puntos pendientes del contrato en propuestas concretas y preguntas de decisión.

---

# 1. Objetivo de esta revisión

El contrato `CONTRATO_INTEGRACION_V1.0.md` ya establece una base común para la integración:

```text
Frontend
   ↓
Backend
   ↓
Data / IA
   ↓
RAG + Knowledge Core + Adaptación
```

Sin embargo, la sección **23. DECISIONES PENDIENTES** contiene varios puntos que deben cerrarse antes de considerar el contrato V1.0 como definitivo.

Esta revisión aplica un criterio común:

```text
Estado actual
      ↓
Propuesta
      ↓
Ejemplo
      ↓
Pregunta concreta
      ↓
Responsable de decisión
      ↓
Actualizar contrato
```

> **Regla:** una propuesta no se considera acordada hasta que BE, Data y/o FE validen el punto que corresponda.

---

# 2. Estado general

## 2.1 Bloqueantes para la integración

Estos puntos deben resolverse antes de que los equipos implementen contra contratos diferentes:

1. JSON Schema.
2. Campos obligatorios y opcionales.
3. Entrada y normalización del documento.
4. Reglas de perfiles.
5. Reglas de formatos.
6. Respuesta Data → Backend.
7. Fuentes y trazabilidad.
8. Estados.
9. Errores.
10. Límites básicos.

## 2.2 Necesarios para cerrar V1

11. Versionamiento.
12. Parámetros y reglas de RAG.
13. Validación IA.
14. Retries.
15. Timeout.
16. Idempotencia.
17. Persistencia OCI.

## 2.3 Pueden quedar para una decisión posterior / MVP según necesidad

18. Streaming.
19. Cancelación.
20. Documentos por referencia.
21. Política avanzada de retención.
22. Compatibilidad entre múltiples versiones.

---

# 3. 23.1 Contrato

## 3.1 JSON Schema formal

**Estado:** 🔴 PENDIENTE

Actualmente existen estructuras JSON conceptuales, pero todavía no un JSON Schema formal.

Ejemplo actual:

```json
{
  "request_id": "req_123",
  "document_id": "doc_456",
  "document": {
    "title": "Título",
    "text": "Texto",
    "source": "origen"
  },
  "profile": "JUNIOR",
  "format": "FLASHCARD"
}
```

### Debe definirse formalmente

- `type`
- `required`
- `enum`
- `nullable`
- `minLength`
- `maxLength`
- cardinalidad de arrays
- estructura de objetos
- restricciones de contenido

### Propuesta

Cerrar primero las decisiones funcionales y después generar:

```text
Decisiones funcionales
        ↓
JSON Schema
        ↓
OpenAPI
        ↓
BE / FE / Data
```

### Pregunta pendiente

> **¿Qué campos y restricciones debemos considerar definitivos antes de generar el JSON Schema?**

**Responsables:** BE + Data + FE.

---

## 3.2 Campos obligatorios / opcionales

**Estado:** 🟡 EN AVANCE

El punto 7 (`sources`) ya tiene una propuesta concreta.

### Propuesta para `sources`

**Obligatorios:**

```text
source_id
document_id
reference
```

**Opcionales:**

```text
page
section
```

**Internos de Data/IA:**

```text
chunk_id
similarity
retrieval_rank
identificadores internos de embeddings/vector store
```

### Pregunta pendiente

> **¿Qué información necesita realmente Frontend para presentar la trazabilidad al usuario?**

Esta pregunta debe resolverse con FE y BE antes de cerrar el esquema definitivo.

**Responsables:** FE + BE, con validación de Data.

---

## 3.3 Tipos y restricciones

**Estado:** 🔴 PENDIENTE

Algunos enums ya están definidos:

```text
profile:
  JUNIOR
  SENIOR
  EJECUTIVO

format:
  FLASHCARD
  QUIZ
  EXECUTIVE_SUMMARY
  MIND_MAP
```

Faltan restricciones como:

```text
title.maxLength
document.text.maxLength
sources.maxItems
content.maxItems
```

### Pregunta pendiente

> **¿Qué límites de tamaño y cardinalidad puede soportar el MVP sin afectar la integración?**

**Responsables:** BE + Data.

---

## 3.4 `contract_version`

**Estado:** 🟡 PARCIALMENTE DEFINIDO

Ya existe:

```json
{
  "contract_version": "1.0"
}
```

### Propuesta

Utilizar:

```text
MAJOR.MINOR
```

Ejemplo:

```text
1.0
1.1
1.2
2.0
```

### Pregunta pendiente

> **¿Qué tipo de cambio incrementará MINOR y qué tipo de cambio obligará a una nueva versión MAJOR?**

**Responsable:** BE + Data.

---

## 3.5 Compatibilidad entre versiones

**Estado:** 🔴 PENDIENTE

Debe definirse qué ocurre si dos componentes utilizan versiones distintas.

Ejemplo:

```text
BE → contrato 1.0
Data → contrato 1.1
```

### Pregunta pendiente

> **¿El MVP necesita soportar simultáneamente más de una versión del contrato o podemos trabajar con una única versión coordinada?**

**Responsable:** BE + Data.

---

# 4. 23.2 Documento de entrada

## 4.1 Extracción de PDF / Markdown / etc.

**Estado:** 🔴 PENDIENTE

El contrato actual deja pendiente quién realiza la extracción.

### Propuesta de flujo

```text
FE
 ↓
BE
 ↓
Extracción / normalización
 ↓
Data
```

La propuesta parte de que Backend recibe y controla la entrada pública, mientras Data recibe texto normalizado.

### Pregunta pendiente

> **¿BE será responsable de extraer y normalizar los documentos antes de enviarlos a Data, o Data recibirá también archivos y será responsable de la extracción?**

**Responsables:** BE + Data.

---

## 4.2 Formato de texto normalizado

**Estado:** 🔴 PENDIENTE

La idea es que Data reciba una representación textual estable:

```json
{
  "title": "Título del documento",
  "text": "Texto limpio y normalizado",
  "source": "origen"
}
```

### Pregunta pendiente

> **¿Qué reglas mínimas de normalización necesita Data para garantizar que el texto recibido sea procesable?**

**Responsables:** Data + BE.

---

## 4.3 Tamaño máximo del documento

**Estado:** 🔴 PENDIENTE

Todavía no se define un valor concreto.

### Debe considerar

- extracción;
- contexto;
- RAG;
- tiempo de procesamiento;
- recursos;
- límites de la infraestructura.

### Pregunta pendiente

> **¿Cuál será el tamaño máximo de documento aceptado por el MVP y dónde se validará ese límite?**

**Responsable:** BE + Data.

---

## 4.4 Documentos por referencia

**Estado:** 🔴 PENDIENTE

Alternativa a enviar todo el texto:

```json
{
  "document_id": "doc_456"
}
```

en lugar de:

```json
{
  "document": {
    "text": "..."
  }
}
```

### Propuesta MVP

Inicialmente podría utilizarse:

```text
document.title
document.text
```

y dejar la referencia a documentos almacenados para una evolución posterior, si no es necesaria para el MVP.

### Pregunta pendiente

> **¿El MVP necesita recibir documentos por referencia o basta con recibir el texto normalizado directamente?**

**Responsables:** BE + Data.

---

# 5. 23.3 Perfiles

Los perfiles del MVP ya están acordados:

```text
JUNIOR
SENIOR
EJECUTIVO
```

Lo pendiente son las reglas de adaptación.

## 5.1 Propuesta de matriz

| Característica | JUNIOR | SENIOR | EJECUTIVO |
|---|---|---|---|
| Profundidad | Pendiente | Pendiente | Pendiente |
| Lenguaje | Pendiente | Pendiente | Pendiente |
| Ejemplos | Pendiente | Pendiente | Pendiente |
| Longitud | Pendiente | Pendiente | Pendiente |
| Conocimiento previo | Pendiente | Pendiente | Pendiente |

### Pregunta pendiente

> **¿Qué reglas concretas diferencian a JUNIOR, SENIOR y EJECUTIVO para que Data pueda aplicarlas de forma consistente?**

**Responsable principal:** Data.

---

# 6. 23.4 Formatos

Los formatos MVP ya están acordados:

```text
FLASHCARD
QUIZ
EXECUTIVE_SUMMARY
MIND_MAP
```

## 6.1 FLASHCARD

Debe definirse:

```text
cantidad
pregunta
respuesta
explicación
ejemplo
fuente
```

### Ejemplo conceptual

```json
{
  "question": "¿Qué es X?",
  "answer": "...",
  "explanation": "...",
  "source_ids": ["src_001"]
}
```

### Pregunta pendiente

> **¿Cuál es la estructura mínima y los límites de una Flashcard para el MVP?**

**Responsable:** Data, validación de FE.

---

## 6.2 QUIZ

Debe definirse:

```text
cantidad de preguntas
cantidad de opciones
single/multiple choice
respuesta correcta
explicación
fuente
```

### Pregunta pendiente

> **¿Qué estructura y límites debe tener un Quiz MVP?**

**Responsable:** Data, validación de FE.

---

## 6.3 EXECUTIVE_SUMMARY

Debe definirse:

```text
longitud
puntos clave
conclusiones
conceptos técnicos
fuentes
```

### Pregunta pendiente

> **¿Qué estructura mínima debe tener un Resumen Ejecutivo y qué límite de extensión tendrá?**

**Responsable:** Data, validación de FE.

---

## 6.4 MIND_MAP

Debe definirse:

```text
nodo raíz
profundidad máxima
cantidad máxima de nodos
relación padre/hijo
fuentes
```

El Mapa Mental forma parte del MVP al mismo nivel que los otros tres formatos.

### Pregunta pendiente

> **¿Cuál será la estructura mínima y los límites del Mapa Mental para que FE pueda representarlo de forma estable?**

**Responsables:** Data + FE.

---

# 7. 23.5 Parámetros adicionales

Los documentos anteriores contemplaban:

```text
nicho_sector
nivel_detalle
```

**Estado:** 🔴 PENDIENTE.

### Propuesta

No agregarlos automáticamente al contrato MVP.

Primero debe demostrarse que son necesarios para los cuatro formatos y tres perfiles.

### Pregunta pendiente

> **¿`nicho_sector` y `nivel_detalle` aportan valor necesario para el MVP o deben quedar fuera de V1?**

**Responsables:** Data + BE + FE.

---

# 8. 23.6 RAG / Data

## 8.1 `top_k`

**Estado:** 🔴 PENDIENTE

Debe probarse experimentalmente.

Ejemplo de evaluación:

```text
top_k = 3
top_k = 5
top_k = 8
```

Evaluar:

```text
fidelidad
contexto
ruido
tokens
tiempo
```

### Pregunta pendiente

> **¿Qué valor de `top_k` ofrece el mejor equilibrio para el MVP según las pruebas de Data?**

**Responsable:** Data.

---

## 8.2 Similarity threshold

**Estado:** 🔴 PENDIENTE

No debe asumirse todavía un valor como:

```text
0.85
```

El valor debe validarse experimentalmente.

### Pregunta pendiente

> **¿Data necesita un similarity threshold explícito y qué valor se obtiene de las pruebas?**

**Responsable:** Data.

---

## 8.3 Contexto insuficiente

**Estado:** 🟡 REQUIERE DEFINICIÓN

Si RAG no encuentra suficiente evidencia, no se debe inventar contenido.

### Propuesta

Introducir un estado/error específico, por ejemplo:

```text
INSUFFICIENT_CONTEXT
```

### Pregunta pendiente

> **¿Qué condición determina que el contexto sea insuficiente y qué respuesta debe devolver Data en ese caso?**

**Responsable:** Data.

---

## 8.4 Límite de contexto

**Estado:** 🔴 PENDIENTE

Debe definirse según:

```text
modelo
tokens
costos
RAG
documento
```

### Pregunta pendiente

> **¿Cuál será el límite máximo de contexto utilizado por Data en el MVP?**

**Responsable:** Data.

---

## 8.5 Límite de salida

**Estado:** 🔴 PENDIENTE

Debe definirse por formato.

```text
Flashcard → cantidad máxima
Quiz → cantidad máxima
Summary → extensión máxima
Mind Map → nodos máximos
```

### Pregunta pendiente

> **¿Cuáles serán los límites máximos de salida por formato?**

**Responsable:** Data + FE.

---

## 8.6 Retries internos

**Estado:** 🔴 PENDIENTE

Debe distinguirse:

```text
retryable
non-retryable
```

### Pregunta pendiente

> **¿Qué errores puede reintentar Data internamente y cuántos intentos máximos tendrá?**

**Responsable:** Data.

---

# 9. 23.7 Validación

## 9.1 `APPROVED`

Debe cumplir las reglas acordadas.

Propuesta de criterios:

```text
estructura correcta
formato correcto
perfil correcto
fuentes válidas
contenido basado en contexto
```

**Estado:** 🟡 Propuesta pendiente de validación.

---

## 9.2 `REQUIRES_ADJUSTMENT`

Debe utilizarse cuando el resultado tiene posibilidad de ser corregido mediante regeneración o ajuste.

### Pregunta pendiente

> **¿Qué condiciones provocan un ajuste/reintento en lugar de rechazo definitivo?**

**Responsable:** Data.

---

## 9.3 `REJECTED`

Debe significar que el resultado no puede entregarse como válido.

### Pregunta pendiente

> **¿Qué condiciones obligan a rechazar definitivamente una generación?**

**Responsable:** Data.

---

## 9.4 Score de calidad

**Estado:** 🔴 PENDIENTE

El valor:

```text
anclaje_fuente_score >= 0.85
```

se mantiene como hipótesis, no como regla definitiva.

### Pregunta pendiente

> **¿Data utilizará un score de calidad en V1 y cómo se calculará de forma reproducible?**

**Responsable:** Data.

---

# 10. 23.8 Errores

## 10.1 Catálogo de errores

**Estado:** 🔴 PENDIENTE

Propuesta inicial:

```text
INVALID_PROFILE
INVALID_FORMAT
EMPTY_DOCUMENT
DOCUMENT_TOO_LARGE
INSUFFICIENT_CONTEXT
DS_TIMEOUT
DS_ERROR
VALIDATION_REJECTED
```

Estos códigos son propuestas de trabajo y deben validarse.

### Pregunta pendiente

> **¿Cuál será el catálogo definitivo de errores y qué equipo es responsable de cada uno?**

**Responsables:** BE + Data.

---

## 10.2 HTTP status

**Estado:** 🔴 PENDIENTE

BE debe definir los códigos HTTP correspondientes.

### Pregunta pendiente

> **¿Qué HTTP status utilizará BE para cada categoría de error?**

**Responsable:** BE.

---

## 10.3 Retryable

Cada error debe indicar:

```json
{
  "retryable": true
}
```

o:

```json
{
  "retryable": false
}
```

### Pregunta pendiente

> **¿Qué errores son reintentables y cuáles deben finalizar inmediatamente?**

**Responsables:** BE + Data.

---

## 10.4 Mensaje público

El mensaje para FE debe ser distinto de los detalles técnicos internos.

### Regla

No exponer:

```text
stack trace
prompts
credenciales
detalles internos del modelo
```

### Pregunta pendiente

> **¿Qué información mínima debe recibir FE para mostrar un error útil sin exponer detalles internos?**

**Responsables:** BE + FE.

---

# 11. 23.9 Proceso

## 11.1 Estados

Propuesta actual:

```text
RECEIVED
PROCESSING
RETRIEVING
GENERATING
VALIDATING
COMPLETED
```

Errores:

```text
FAILED
TIMEOUT
CANCELLED
```

**Estado:** 🟡 Propuesta.

### Pregunta pendiente

> **¿Qué estados debe conocer FE y cuáles deben permanecer internos de BE/Data?**

**Responsables:** BE + FE + Data.

---

## 11.2 Transiciones

Propuesta:

```text
RECEIVED
   ↓
PROCESSING
   ↓
RETRIEVING
   ↓
GENERATING
   ↓
VALIDATING
   ↓
COMPLETED
```

### Pregunta pendiente

> **¿Qué transiciones son válidas y qué ocurre cuando falla cada etapa?**

**Responsables:** BE + Data.

---

## 11.3 Timeout

Debe definirse:

```text
BE → DS
solicitud total
stream, si existe
```

### Pregunta pendiente

> **¿Cuál será el timeout máximo de la llamada BE → Data y de la solicitud completa?**

**Responsables:** BE + Data.

---

## 11.4 Cancelación

**Estado:** 🔴 Pendiente / posiblemente fuera del MVP.

### Pregunta

> **¿FE necesita cancelar una generación en curso para el MVP?**

**Responsables:** FE + BE.

---

## 11.5 Idempotencia

Propuesta:

```text
idempotency_key
```

Objetivo:

```text
evitar procesamiento duplicado
evitar llamadas duplicadas a IA
evitar duplicación en OCI
```

### Pregunta pendiente

> **¿La idempotencia es necesaria para el MVP o puede quedar fuera de V1?**

**Responsables:** BE + Data.

---

# 12. 23.10 Streaming

**Estado:** 🔴 PENDIENTE

La propuesta original contemplaba:

```text
GET /api/v1/adaptacion/stream
```

con SSE/WebSocket.

### Primera decisión

> **¿FE realmente necesita mostrar progreso en tiempo real para el MVP?**

Si no:

```text
POST
 ↓
procesamiento
 ↓
respuesta
```

Si sí:

```text
POST → request_id
       ↓
SSE/WebSocket
       ↓
eventos
```

### Si se mantiene

Definir:

- transporte;
- endpoint;
- eventos;
- correlación;
- desconexión;
- estados visibles.

**Responsables:** FE + BE.

---

# 13. 23.11 OCI

## 13.1 Objetos

Debe decidirse qué almacenar:

```text
documento original
resultado generado
metadata
```

### Pregunta

> **¿Qué objetos son obligatorios para el MVP y cuáles no necesitan persistencia?**

**Responsable:** BE + OCI.

---

## 13.2 Naming

Propuesta conceptual:

```text
documents/{document_id}/original
documents/{document_id}/results/{request_id}
```

**Estado:** Propuesta.

### Pregunta

> **¿Esta convención es adecuada para el almacenamiento del MVP?**

**Responsable:** BE + OCI.

---

## 13.3 Retención

### Pregunta

> **¿Cuánto tiempo deben conservarse documentos y resultados en OCI durante el MVP?**

**Responsable:** BE + OCI.

---

## 13.4 Error de persistencia

Caso:

```text
IA → OK
OCI → ERROR
```

### Pregunta

> **¿Qué estado debe recibir FE cuando la generación es correcta pero falla la persistencia?**

**Responsables:** BE + FE + OCI.

---

## 13.5 Éxito parcial

Debe decidirse si existe:

```text
PARTIAL
```

o si el caso anterior se representa mediante:

```text
FAILED
```

### Pregunta

> **¿El MVP necesita un estado PARTIAL o basta con COMPLETED/FAILED?**

**Responsables:** BE + FE.

---

# 14. 23.12 Seguridad

## 14.1 Autenticación

**Estado:** 🔴 Pendiente.

### Pregunta

> **¿Qué mecanismo de autenticación necesita el MVP y será obligatorio para la demo?**

**Responsable:** BE.

---

## 14.2 Autorización

### Pregunta

> **¿Qué usuarios/roles pueden generar, consultar y acceder a documentos?**

**Responsable:** BE + FE.

---

## 14.3 Rate limit

### Pregunta

> **¿Qué límite de solicitudes debe aplicar BE para proteger el MVP?**

**Responsable:** BE.

---

## 14.4 Límite de documento

Debe estar alineado con la sección 4.3.

> **No definir este límite dos veces en el contrato.**

---

## 14.5 Concurrencia

### Pregunta

> **¿Cuántas generaciones simultáneas soportará el MVP según los recursos disponibles?**

**Responsables:** BE + Data + OCI.

---

## 14.6 Logs

### Puede registrarse

```text
request_id
document_id
profile
format
status
duración
error_code
```

### No debe registrarse

```text
secretos
credenciales
tokens
información sensible innecesaria
```

### Pregunta

> **¿Qué campos de logging son necesarios para trazabilidad y diagnóstico sin registrar información sensible?**

**Responsables:** BE + Data.

---

# 15. Priorización para la próxima reunión

## Prioridad 1 — Cerrar para poder integrar

```text
1. Entrada del documento
2. Campos obligatorios/opcionales
3. Sources
4. Perfiles
5. Formatos
6. Respuesta DS → BE
7. Estados
8. Errores
9. Límites básicos
```

## Prioridad 2 — Cerrar antes de V1 definitiva

```text
10. JSON Schema
11. Versionamiento
12. RAG
13. Validación
14. Retries
15. Timeout
16. Idempotencia
17. OCI
```

## Prioridad 3 — Decidir si realmente entra al MVP

```text
18. Streaming
19. Cancelación
20. Documentos por referencia
21. Retención avanzada
22. Compatibilidad multi-versión
```

---

# 16. Método de decisión

Cada pendiente debería terminar en uno de estos estados:

```text
ACORDADO
PROPUESTO
PENDIENTE DE DECISIÓN
PENDIENTE DE PRUEBA
FUERA DEL MVP
```

### Ejemplo: `sources`

```text
Estado actual:
PENDIENTE

        ↓

Propuesta:
source_id       obligatorio
document_id     obligatorio
reference       obligatorio
page            opcional
section         opcional

        ↓

Pregunta:
¿Qué necesita realmente FE?

        ↓

Responsables:
BE + FE + Data

        ↓

Resultado:
ACORDADO / MODIFICAR PROPUESTA
```

---

# 17. Regla para no sobrecargar el MVP

No todos los puntos deben convertirse en funcionalidades.

Antes de agregar un campo, parámetro o mecanismo debe preguntarse:

> **¿Es necesario para que el MVP funcione, se integre o pueda demostrarse?**

Si la respuesta es no, puede quedar:

```text
FUERA DEL MVP
```

o:

```text
V1.1 / FUTURO
```

Esto aplica especialmente a:

- `nicho_sector`
- `nivel_detalle`
- streaming
- cancelación
- documentos por referencia
- compatibilidad multi-versión
- métricas avanzadas
- persistencia avanzada

---

# 18. Resultado esperado

La meta de esta revisión no es eliminar todos los pendientes inmediatamente.

La meta es transformar:

```text
LISTA DE PENDIENTES
```

en:

```text
DECISIONES CLARAS
       +
PROPUESTAS CONCRETAS
       +
PREGUNTAS DIRIGIDAS
       +
RESPONSABLES
       +
CRITERIOS DE VALIDACIÓN
```

Una vez resueltos los puntos bloqueantes:

```text
Contrato funcional
      ↓
JSON Schema
      ↓
OpenAPI
      ↓
Pruebas de contrato
      ↓
Implementación BE + Data + FE
```

---

# 19. Relación con `CONTRATO_INTEGRACION_V1.0.md`

Este documento es **complementario** al contrato.

```text
CONTRATO_INTEGRACION_V1.0.md
        │
        ├── Define el contrato
        │
        └── Se actualiza cuando una decisión queda acordada
                 ↑
                 │
REVISION_PENDIENTES_CONTRATO_V1.0.md
        │
        ├── Analiza pendientes
        ├── Presenta propuestas
        ├── Formula preguntas
        └── Prepara decisiones del equipo
```

> **Este documento no reemplaza el contrato.**
> Sirve como documento de trabajo para cerrarlo.

---

## Estado

**Versión:** 0.1  
**Estado:** Propuesta para revisión BE + Data + FE  
**Próximo paso:** Resolver primero los puntos de Prioridad 1 y actualizar `CONTRATO_INTEGRACION_V1.0.md` únicamente cuando las decisiones sean aprobadas.
