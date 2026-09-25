# CONTRATO_INTEGRACION_V1.0.md

## TechMind / NuevaMente --- Contrato de Integración FE ↔ BE ↔ Data/DS

**Proyecto:** TechMind / NuevaMente\
**Equipo:** G10-LATAM-EQUIPO15\
**Versión:** 1.0\
**Fecha:** 2026-09-25\
**Estado:** Propuesta consolidada para alineación del equipo\
**Documento:** Contrato de integración

------------------------------------------------------------------------

## 1. Objetivo

Este documento define los contratos de integración entre:

-   **Frontend (FE) ↔ Backend (BE)**
-   **Backend (BE) ↔ Data Science / IA (DS)**

El objetivo es que FE, BE y Data puedan desarrollar de forma
desacoplada, utilizando estructuras, responsabilidades, entradas,
salidas, errores y reglas claramente identificadas.

> **Regla principal:** lo que aparece como **ACORDADO** forma parte del
> contrato. Lo que aparece como **PENDIENTE DE DEFINICIÓN** no debe ser
> asumido por ningún equipo.

------------------------------------------------------------------------

# 2. Alcance funcional del MVP

## 2.1 Perfiles

El MVP contempla tres perfiles:

-   `JUNIOR`
-   `SENIOR`
-   `EJECUTIVO`

El perfil será un parámetro de adaptación. No implica crear un agente
independiente por perfil.

## 2.2 Formatos

El MVP contempla cuatro formatos:

-   `FLASHCARD`
-   `QUIZ`
-   `EXECUTIVE_SUMMARY`
-   `MIND_MAP`

### Fuera del MVP

`STEP_BY_STEP` / `GUIA_PASO_A_PASO` queda como funcionalidad futura y no
debe considerarse obligatoria para la primera versión.

------------------------------------------------------------------------

# 3. Principio de arquitectura

``` mermaid
flowchart LR
    FE[Frontend]
    BE[Backend]
    DS[Data Science / IA]
    RAG[RAG + Knowledge Core]
    OCI[OCI Storage]

    FE -->|API pública| BE
    BE -->|Contrato interno| DS
    DS --> RAG
    RAG --> DS
    DS -->|Resultado estructurado| BE
    BE --> OCI
    BE -->|Respuesta estable| FE
```

## 3.1 Responsabilidad de cada capa

  -----------------------------------------------------------------------
  Capa                                Responsabilidad
  ----------------------------------- -----------------------------------
  FE                                  Interfaz, captura de parámetros,
                                      presentación de resultados y
                                      estados

  BE                                  API pública, validación, seguridad,
                                      IDs, orquestación, persistencia y
                                      exposición del contrato a FE

  Data/DS                             RAG, Knowledge Core, adaptación por
                                      perfil/formato, fuentes y
                                      validación IA

  OCI                                 Persistencia gestionada por
                                      Backend/infraestructura
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 4. CONTRATO BE ↔ DATA SCIENCE

## 4.1 Propósito

El contrato BE ↔ DS define cómo Backend solicita a Data una adaptación
educativa y cómo Data devuelve el resultado estructurado, validado y
trazable.

Data no debe exponer a Backend la implementación interna de:

-   embeddings;
-   vector store;
-   estrategia RAG;
-   prompts;
-   modelo utilizado;
-   framework de orquestación;
-   configuración interna del pipeline.

Backend debe consumir el contrato, no depender de la implementación.

------------------------------------------------------------------------

## 4.2 Flujo

``` mermaid
sequenceDiagram
    participant BE as Backend
    participant DS as Data / IA

    BE->>DS: Solicitud de adaptación
    DS->>DS: Retrieval / RAG
    DS->>DS: Knowledge Core
    DS->>DS: Adaptación por perfil y formato
    DS->>DS: Validación IA
    DS-->>BE: Resultado estructurado
    BE->>BE: Validación del contrato
```

------------------------------------------------------------------------

## 4.3 Solicitud BE → DS

La solicitud interna deberá contener, como mínimo, la información
necesaria para identificar el documento y ejecutar la adaptación.

### Estructura conceptual

``` json
{
  "request_id": "req_123",
  "document_id": "doc_456",
  "document": {
    "title": "Título del documento",
    "text": "Texto normalizado del documento",
    "source": "origen"
  },
  "profile": "JUNIOR",
  "format": "FLASHCARD"
}
```

### Campos actualmente acordados

  ---------------------------------------------------------------------------
  Campo               Tipo              Estado            Descripción
  ------------------- ----------------- ----------------- -------------------
  `request_id`        string            ACORDADO          Identificador de la
                                                          solicitud

  `document_id`       string            ACORDADO          Identificador del
                                                          documento

  `document.title`    string            ACORDADO          Título

  `document.text`     string            ACORDADO          Texto normalizado

  `document.source`   string            ACORDADO          Origen o referencia

  `profile`           enum              ACORDADO          JUNIOR / SENIOR /
                                                          EJECUTIVO

  `format`            enum              ACORDADO          FLASHCARD / QUIZ /
                                                          EXECUTIVE_SUMMARY /
                                                          MIND_MAP
  ---------------------------------------------------------------------------

------------------------------------------------------------------------

## 4.4 Parámetros propuestos pero pendientes

Las propuestas anteriores contemplan parámetros adicionales:

``` text
nicho_sector
nivel_detalle
```

Estos campos **no deben considerarse obligatorios todavía**.

### Decisión pendiente

Definir si:

-   forman parte del MVP;
-   son opcionales;
-   se eliminan del contrato V1;
-   o se incorporan en una versión posterior.

------------------------------------------------------------------------

# 5. Respuesta DS → BE

Data debe devolver un resultado estructurado y trazable.

### Estructura conceptual

``` json
{
  "contract_version": "1.0",
  "request_id": "req_123",
  "document_id": "doc_456",
  "profile": "JUNIOR",
  "format": "FLASHCARD",
  "status": "APPROVED",
  "metadata": {},
  "content": {},
  "sources": [],
  "validation": {},
  "pipeline_version": "..."
}
```

------------------------------------------------------------------------

## 5.1 Campos

  Campo                Estado      Descripción
  -------------------- ----------- ---------------------------------
  `contract_version`   ACORDADO    Versión del contrato
  `request_id`         ACORDADO    Correlación de la solicitud
  `document_id`        ACORDADO    Documento procesado
  `profile`            ACORDADO    Perfil utilizado
  `format`             ACORDADO    Formato generado
  `status`             ACORDADO    Resultado de validación/proceso
  `metadata`           ACORDADO    Metadatos funcionales
  `content`            ACORDADO    Contenido generado
  `sources`            ACORDADO    Trazabilidad de fuentes
  `validation`         ACORDADO    Resultado de validación
  `pipeline_version`   PROPUESTO   Versión interna del pipeline

------------------------------------------------------------------------

# 6. Estados de validación Data/IA

Los estados definidos actualmente son:

``` text
APPROVED
REQUIRES_ADJUSTMENT
REJECTED
```

### Interpretación

  Estado                  Significado
  ----------------------- -------------------------------------------------------
  `APPROVED`              El resultado cumple las reglas de validación
  `REQUIRES_ADJUSTMENT`   El resultado requiere ajuste/reintento
  `REJECTED`              El resultado no debe entregarse como resultado válido

> Un resultado rechazado no debe ser presentado por Backend como una
> generación exitosa.

------------------------------------------------------------------------

# 7. Fuentes y trazabilidad

El resultado debe permitir identificar de dónde proviene la información
utilizada para generar el contenido.

La trazabilidad debe ser suficiente para que Backend y Frontend puedan
identificar y, cuando corresponda, mostrar al usuario la fuente de origen,
sin exponer detalles internos de la implementación de Data/IA.

## 7.1 Esquema propuesto de `sources`

Se propone inicialmente la siguiente estructura:

```json
{
  "source_id": "src_001",
  "document_id": "doc_456",
  "reference": "manual.pdf - Introducción - página 12",
  "page": 12,
  "section": "Introducción"
}
```

### 7.1.1 Clasificación inicial de campos

| Campo | Estado propuesto | Descripción |
|---|---|---|
| `source_id` | **OBLIGATORIO** | Identificador de la fuente dentro de la respuesta |
| `document_id` | **OBLIGATORIO** | Identificador del documento de origen |
| `reference` | **OBLIGATORIO** | Referencia legible que permita identificar el origen de la información |
| `page` | **OPCIONAL** | Número de página, cuando el tipo de documento disponga de esta información |
| `section` | **OPCIONAL** | Sección o apartado de origen, cuando pueda identificarse |

### 7.1.2 Ejemplo con información completa

Para un documento con páginas y secciones:

```json
{
  "source_id": "src_001",
  "document_id": "doc_456",
  "reference": "manual.pdf - Introducción - página 12",
  "page": 12,
  "section": "Introducción"
}
```

### 7.1.3 Ejemplo sin número de página

Para un documento que no maneje páginas, por ejemplo Markdown:

```json
{
  "source_id": "src_002",
  "document_id": "doc_789",
  "reference": "README.md - Instalación",
  "section": "Instalación"
}
```

En este caso `page` no debe ser obligatorio ni debe generarse
artificialmente para cumplir el contrato.

### 7.1.4 Información interna de Data/IA

Data puede utilizar información adicional para la trazabilidad interna
del proceso RAG, por ejemplo:

```json
{
  "source_id": "src_001",
  "document_id": "doc_456",
  "chunk_id": "chunk_045",
  "page": 12,
  "section": "Introducción",
  "similarity": 0.91,
  "retrieval_rank": 1
}
```

Los siguientes campos se consideran inicialmente **internos de Data/IA**
y no forman parte del contrato público con Frontend:

- `chunk_id`
- `similarity`
- `retrieval_rank`
- identificadores internos de embeddings;
- identificadores del vector store;
- cualquier otro dato técnico utilizado por el proceso de retrieval.

Esto permite que Data pueda modificar su implementación interna sin
romper el contrato con Backend o Frontend.

## 7.2 Propuesta de exposición hacia Frontend

Frontend debería recibir únicamente la información necesaria para
presentar la trazabilidad al usuario.

Como propuesta inicial:

```json
{
  "sources": [
    {
      "source_id": "src_001",
      "document_id": "doc_456",
      "reference": "manual.pdf - Introducción - página 12",
      "page": 12,
      "section": "Introducción"
    }
  ]
}
```

La información técnica utilizada internamente por Data para el retrieval
no debe ser una dependencia de Frontend.

## 7.3 PREGUNTA PENDIENTE PARA BE + FE

> **¿Qué información necesita realmente Frontend para presentar la
> trazabilidad al usuario?**

Esta decisión debe validarse antes de cerrar el esquema definitivo de
`sources`.

En particular, BE + FE deben confirmar:

- si `source_id` debe ser visible para Frontend;
- si `document_id` debe ser visible para Frontend;
- qué formato debe tener `reference`;
- si `page` debe mostrarse al usuario cuando exista;
- si `section` debe mostrarse al usuario cuando exista;
- si Frontend necesita algún dato adicional para permitir al usuario
  identificar o consultar la fuente.

### Propuesta inicial para revisión

**Obligatorios:**

- `source_id`
- `document_id`
- `reference`

**Opcionales:**

- `page`
- `section`

**Internos de Data/IA y no expuestos a FE:**

- `chunk_id`
- `similarity`
- `retrieval_rank`
- identificadores internos de embeddings/vector store

> **Estado: PROPUESTA — PENDIENTE DE VALIDACIÓN CON BE + FE.**

------------------------------------------------------------------------

# 8. Knowledge Core

Data utilizará una representación intermedia común para evitar ejecutar
un RAG independiente por cada formato.

### Concepto

``` mermaid
flowchart LR
    DOC[Documento]
    RAG[RAG / Retrieval]
    KC[Knowledge Core]
    F1[Flashcard]
    F2[Quiz]
    F3[Resumen]
    F4[Mapa Mental]

    DOC --> RAG
    RAG --> KC
    KC --> F1
    KC --> F2
    KC --> F3
    KC --> F4
```

## 8.1 Estructura conceptual

``` json
{
  "topic": "...",
  "concepts": [],
  "definitions": [],
  "key_points": [],
  "relationships": [],
  "examples": [],
  "procedures": [],
  "comparisons": [],
  "questions_candidates": [],
  "sources": []
}
```

### Estado

**Arquitectura acordada conceptualmente.**

### Pendiente

Definir formalmente:

-   campos obligatorios;
-   campos opcionales;
-   tipos;
-   cardinalidad;
-   comportamiento cuando un campo no exista en la fuente;
-   relación entre Knowledge Core y `sources`.

------------------------------------------------------------------------

# 9. Reglas de los formatos MVP

La existencia de los cuatro formatos está acordada, pero sus
restricciones exactas todavía deben cerrarse.

## 9.1 Flashcard

Debe definirse:

-   número de tarjetas;
-   estructura pregunta/respuesta;
-   longitud máxima;
-   nivel de dificultad;
-   uso de ejemplos;
-   inclusión de explicación;
-   referencias a fuentes.

## 9.2 Quiz

Debe definirse:

-   número de preguntas;
-   número de opciones;
-   selección única o múltiple;
-   respuesta correcta;
-   explicación;
-   dificultad;
-   referencias a fuentes.

## 9.3 Resumen Ejecutivo

Debe definirse:

-   longitud máxima;
-   cantidad de puntos clave;
-   estructura;
-   tratamiento de conceptos técnicos;
-   inclusión de conclusiones;
-   fuentes.

## 9.4 Mapa Mental

Debe definirse:

-   nodo raíz;
-   profundidad máxima;
-   número máximo de nodos;
-   relación padre/hijo;
-   contenido de cada nodo;
-   posibilidad de incluir relaciones cruzadas;
-   fuentes.

> Estas reglas son necesarias antes de considerar cerrado el contrato de
> contenido.

------------------------------------------------------------------------

# 10. CONTRATO BE ↔ FE

## 10.1 Propósito

Backend expone a Frontend una API estable. Frontend no debe depender de
la implementación interna de Data.

``` mermaid
flowchart LR
    FE[Frontend]
    API[BE API v1]
    ORQ[Orquestación Backend]
    DS[Data / IA]
    STORAGE[OCI]

    FE --> API
    API --> ORQ
    ORQ --> DS
    DS --> ORQ
    ORQ --> STORAGE
    ORQ --> API
    API --> FE
```

------------------------------------------------------------------------

# 11. Endpoint principal

## POST

``` text
POST /api/v1/adaptacion/generar
```

### Objetivo

Solicitar la generación de contenido adaptado.

### Solicitud conceptual

``` json
{
  "document": {
    "title": "Título",
    "text": "Texto del documento"
  },
  "profile": "JUNIOR",
  "format": "FLASHCARD"
}
```

### Importante

La propuesta original contempla también escenarios de archivo/binario o
referencia a documentos almacenados, pero su incorporación al mínimo
contractual todavía debe definirse.

------------------------------------------------------------------------

# 12. Respuesta BE → FE

La respuesta pública deberá ocultar los detalles internos de IA.

### Estructura propuesta

``` json
{
  "status": "COMPLETED",
  "request_id": "req_123",
  "document_id": "doc_456",
  "contract_version": "1.0",
  "metadata": {},
  "content": {},
  "sources": [],
  "validation": {},
  "storage": {}
}
```

------------------------------------------------------------------------

# 13. Qué puede consumir FE

FE puede depender de:

-   `status`;
-   `request_id`;
-   `document_id`;
-   `contract_version`;
-   `profile`;
-   `format`;
-   `metadata`;
-   `content`;
-   `sources`;
-   información pública de validación;
-   información pública de almacenamiento, si corresponde.

## FE NO debe depender de:

-   prompts;
-   embeddings;
-   chunks internos;
-   similarity interna;
-   nombres de modelos;
-   tokens;
-   configuración de LangChain/LangGraph;
-   Chroma u otro vector store;
-   stack traces;
-   secretos;
-   configuración interna de OCI.

------------------------------------------------------------------------

# 14. Ciclo de vida de una solicitud

Se propone utilizar estados de proceso independientes del resultado de
validación.

``` text
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

Estados de fallo:

``` text
FAILED
TIMEOUT
CANCELLED
```

### Estado

**PENDIENTE DE DEFINICIÓN FORMAL.**

Debe decidirse:

-   catálogo definitivo;
-   transición permitida entre estados;
-   qué estados verá FE;
-   qué estados serán internos de BE;
-   qué estados serán reportados por Data.

------------------------------------------------------------------------

# 15. Errores

Los errores deben ser estructurados y diferenciables.

### Ejemplo

``` json
{
  "status": "FAILED",
  "error": {
    "code": "UNSUPPORTED_FORMAT",
    "message": "El formato solicitado no está disponible.",
    "retryable": false
  },
  "request_id": "req_123"
}
```

## Debe existir una matriz de errores

  Código             HTTP Retryable   Responsable   Público
  ----------- ----------- ----------- ------------- ---------
  Pendiente     Pendiente Pendiente   BE/DS         Sí
  Pendiente     Pendiente Pendiente   BE/DS         Sí
  Pendiente     Pendiente Pendiente   BE/DS         Sí

### Debe definirse

-   códigos;
-   HTTP status;
-   mensaje público;
-   `retryable`;
-   responsable;
-   comportamiento FE.

------------------------------------------------------------------------

# 16. Timeout y reintentos

Debe establecerse explícitamente:

-   timeout BE → DS;
-   timeout total de solicitud;
-   timeout del stream, si existe;
-   cantidad máxima de retries;
-   qué errores permiten retry;
-   cuándo detener el proceso.

**Estado: PENDIENTE DE DEFINICIÓN.**

------------------------------------------------------------------------

# 17. Idempotencia

Debe definirse qué ocurre si FE envía dos veces la misma solicitud.

Se debe decidir si el MVP utilizará:

``` text
idempotency_key
```

o una estrategia equivalente.

Objetivo:

-   evitar llamadas duplicadas a IA;
-   evitar duplicar procesamiento;
-   evitar duplicar objetos en OCI.

**Estado: PENDIENTE DE DEFINICIÓN.**

------------------------------------------------------------------------

# 18. Persistencia OCI

OCI pertenece a la responsabilidad de Backend/infraestructura.

Flujo conceptual:

``` text
FE
 ↓
BE
 ├──→ DS
 │     └── resultado
 │
 └──→ OCI
       ├── documento original
       └── resultado
```

Data no debe depender directamente de OCI para cumplir el contrato BE ↔
DS.

### Pendiente

Definir:

-   qué objetos se almacenan;
-   naming convention;
-   estructura de carpetas/objetos;
-   cuándo se considera exitosa la persistencia;
-   qué ocurre si IA termina correctamente pero OCI falla;
-   si ese caso devuelve `COMPLETED`, `PARTIAL` o `FAILED`.

------------------------------------------------------------------------

# 19. Progreso / Streaming

La propuesta original contempla un endpoint de progreso:

``` text
GET /api/v1/adaptacion/stream
```

y propone SSE/WebSocket.

Sin embargo, para V1 todavía debe definirse:

-   si el streaming forma parte del MVP;
-   transporte definitivo;
-   endpoint definitivo;
-   correlación con `request_id`;
-   eventos;
-   comportamiento ante desconexión;
-   si FE realmente necesita progreso en tiempo real.

### Si se mantiene

La correlación recomendada conceptualmente sería:

``` text
POST /api/v1/adaptacion/generar
        ↓
request_id = req_123

GET /api/v1/adaptacion/stream/{request_id}
        ↓
eventos de req_123
```

**Estado: PENDIENTE DE DEFINICIÓN.**

------------------------------------------------------------------------

# 20. Seguridad y límites

## Backend

Debe controlar:

-   autenticación/autorización;
-   validación de entrada;
-   tamaño máximo del documento;
-   límites de concurrencia;
-   rate limiting;
-   seguridad;
-   prompt injection;
-   datos sensibles;
-   secretos;
-   logs.

## Data

Debe controlar:

-   límites de `top_k`;
-   tamaño del contexto;
-   límites de salida;
-   retries internos;
-   validación de contenido;
-   comportamiento ante contexto insuficiente.

### Pendiente

Definir valores concretos para cada límite.

------------------------------------------------------------------------

# 21. Lo que NO forma parte del contrato público

No deben exponerse a FE:

``` text
Modelo LLM
Prompt
Embedding
Vector store
Chunk interno
Similarity score interno
Tokens
Temperatura
Chain/Graph interno
Stack trace
Credenciales
Secretos
Configuración OCI
```

Esto permite evolucionar Data y Backend sin romper Frontend.

------------------------------------------------------------------------

# 22. Matriz de responsabilidades

  Actividad                    FE        BE            Data/DS      OCI
  --------------------------- ---- --------------- --------------- -----
  Captura de parámetros        ✓                                   
  Validación básica UI         ✓                                   
  API pública                             ✓                        
  IDs                                     ✓                        
  Seguridad API                           ✓                        
  Extracción de documento           **PENDIENTE**   **PENDIENTE**  
  Normalización de texto                                  ✓        
  Chunking                                                ✓        
  Embeddings                                              ✓        
  RAG                                                     ✓        
  Knowledge Core                                          ✓        
  Adaptación por perfil                                   ✓        
  Adaptación por formato                                  ✓        
  Validación IA                                           ✓        
  Contrato BE ↔ DS                        ✓               ✓        
  Contrato BE ↔ FE             ✓          ✓                        
  Persistencia OCI                        ✓                          ✓
  Presentación resultado       ✓                                   
  Manejo público de errores               ✓                        
  Trazabilidad                            ✓               ✓        

------------------------------------------------------------------------

# 23. DECISIONES PENDIENTES

Esta sección es obligatoria antes de considerar el contrato
completamente cerrado.

## 23.1 Contrato

-   [ ] Definir JSON Schema formal.
-   [ ] Definir campos obligatorios/opcionales.
-   [ ] Definir tipos y restricciones.
-   [ ] Definir `contract_version`.
-   [ ] Definir compatibilidad entre versiones.

## 23.2 Documento de entrada

-   [ ] Definir quién realiza la extracción de PDF/Markdown/etc.
-   [ ] Definir formato de texto normalizado.
-   [ ] Definir tamaño máximo.
-   [ ] Definir si se aceptan documentos por referencia.

## 23.3 Perfil

-   [ ] Definir reglas concretas de JUNIOR.
-   [ ] Definir reglas concretas de SENIOR.
-   [ ] Definir reglas concretas de EJECUTIVO.

## 23.4 Formatos

-   [ ] Definir restricciones de FLASHCARD.
-   [ ] Definir restricciones de QUIZ.
-   [ ] Definir restricciones de EXECUTIVE_SUMMARY.
-   [ ] Definir restricciones de MIND_MAP.

## 23.5 Parámetros adicionales

-   [ ] Decidir `nicho_sector`.
-   [ ] Decidir `nivel_detalle`.

## 23.6 RAG / Data

-   [ ] Definir `top_k`.
-   [ ] Definir similarity threshold, si corresponde.
-   [ ] Definir estrategia ante contexto insuficiente.
-   [ ] Definir límite de contexto.
-   [ ] Definir límite de salida.
-   [ ] Definir retries.

> Los valores como `anclaje_fuente_score >= 0.85` no deben considerarse
> definitivos hasta que Data los valide experimentalmente.

## 23.7 Validación

-   [ ] Definir criterios de `APPROVED`.
-   [ ] Definir criterios de `REQUIRES_ADJUSTMENT`.
-   [ ] Definir criterios de `REJECTED`.
-   [ ] Definir si existe score de calidad.
-   [ ] Definir cómo se calcula y reproduce.

## 23.8 Errores

-   [ ] Catálogo de códigos.
-   [ ] HTTP status.
-   [ ] Retryable / non-retryable.
-   [ ] Mensaje público.
-   [ ] Responsable del error.

## 23.9 Proceso

-   [ ] Estados definitivos.
-   [ ] Transiciones.
-   [ ] Timeout.
-   [ ] Retries.
-   [ ] Cancelación.
-   [ ] Idempotencia.

## 23.10 Streaming

-   [ ] Decidir si entra al MVP.
-   [ ] SSE/WebSocket.
-   [ ] Endpoint.
-   [ ] Eventos.
-   [ ] Correlación mediante `request_id`.

## 23.11 OCI

-   [ ] Objetos que se almacenan.
-   [ ] Naming convention.
-   [ ] Estructura.
-   [ ] Retención.
-   [ ] Error de persistencia.
-   [ ] Política de éxito parcial.

## 23.12 Seguridad

-   [ ] Autenticación.
-   [ ] Autorización.
-   [ ] Rate limit.
-   [ ] Límites de documento.
-   [ ] Límites de concurrencia.
-   [ ] Política de logs.

------------------------------------------------------------------------

# 24. Matriz de pruebas de integración

Antes de cerrar V1, BE + Data deben probar como mínimo:

  Caso                             Resultado esperado
  -------------------------------- -------------------------------------
  Perfil válido + formato válido   Éxito
  Perfil inválido                  Error estructurado
  Formato inválido                 Error estructurado
  Documento vacío                  Error estructurado
  Documento demasiado grande       Error estructurado
  Contexto insuficiente            Estado definido por Data
  Validación IA aprobada           Resultado entregable
  Validación IA requiere ajuste    Reintento/estado definido
  Validación IA rechazada          No reportar éxito
  Error DS                         Error traducible por BE
  Timeout DS                       Error controlado
  Error OCI                        Comportamiento definido
  Solicitud duplicada              Comportamiento idempotente definido
  Sources válidas                  Trazabilidad verificable

------------------------------------------------------------------------

# 25. Definition of Done --- Data/IA

Data/IA podrá considerarse integrado cuando:

-   [ ] Recibe el request definido por el contrato.
-   [ ] Procesa los perfiles acordados.
-   [ ] Procesa los cuatro formatos MVP.
-   [ ] Ejecuta RAG.
-   [ ] Construye Knowledge Core.
-   [ ] Genera contenido estructurado.
-   [ ] Devuelve fuentes.
-   [ ] Devuelve estado de validación.
-   [ ] Maneja errores estructurados.
-   [ ] Respeta límites acordados.
-   [ ] Tiene pruebas de los casos principales.
-   [ ] No depende directamente de OCI.
-   [ ] No obliga a BE a conocer su implementación interna.

------------------------------------------------------------------------

# 26. Definition of Done --- Backend

BE podrá considerarse integrado cuando:

-   [ ] Expone la API pública versionada.
-   [ ] Valida requests.
-   [ ] Genera/gestiona IDs.
-   [ ] Invoca Data mediante el contrato interno.
-   [ ] Valida la respuesta de Data.
-   [ ] Traduce errores.
-   [ ] Gestiona timeout/retry.
-   [ ] Gestiona persistencia OCI según definición.
-   [ ] Expone una respuesta estable a FE.
-   [ ] No expone detalles internos de IA.
-   [ ] Tiene pruebas de integración.

------------------------------------------------------------------------

# 27. Definition of Done --- Frontend

FE podrá considerarse integrado cuando:

-   [ ] Envía únicamente los campos definidos.
-   [ ] Utiliza los enums acordados.
-   [ ] Interpreta los estados definidos.
-   [ ] Presenta errores públicos.
-   [ ] Presenta contenido según el formato recibido.
-   [ ] Presenta fuentes cuando corresponda.
-   [ ] No depende de detalles internos de IA.
-   [ ] Maneja loading/processing.
-   [ ] Maneja timeout/error.
-   [ ] Maneja respuesta exitosa.

------------------------------------------------------------------------

# 28. Regla de cambios

Cualquier cambio en:

-   campos;
-   enums;
-   estructura JSON;
-   endpoints;
-   estados;
-   códigos de error;
-   comportamiento;

debe actualizar este contrato antes de que los equipos implementen el
cambio.

### Regla

``` text
Cambio de contrato
       ↓
Actualizar documento
       ↓
Alinear BE + Data + FE
       ↓
Actualizar código
       ↓
Actualizar pruebas
```

------------------------------------------------------------------------

# 29. Estado del documento

## ACORDADO

-   Arquitectura desacoplada FE → BE → Data.
-   Perfiles MVP.
-   Formatos MVP.
-   Data es responsable del RAG y adaptación.
-   BE es responsable de API pública, orquestación y persistencia.
-   FE consume una interfaz estable.
-   Fuentes y trazabilidad son parte del resultado.
-   El contrato debe estar versionado.
-   Los errores deben ser estructurados.
-   La implementación interna de Data no forma parte del contrato
    público.

## PENDIENTE

Los puntos de la sección **23. DECISIONES PENDIENTES** deben resolverse
antes de marcar este contrato como **V1.0 DEFINITIVO**.

------------------------------------------------------------------------

# 30. Próximo paso recomendado

La secuencia de trabajo debe ser:

``` mermaid
flowchart TD
    A[Contrato V1.0 propuesta] --> B[Reunión BE + Data]
    B --> C[Resolver contrato BE ↔ DS]
    C --> D[Resolver reglas de formatos]
    D --> E[Resolver errores / estados / límites]
    E --> F[Resolver BE ↔ FE]
    F --> G[JSON Schema / OpenAPI]
    G --> H[Pruebas de contrato]
    H --> I[Implementación]
```

### Prioridad

**Primero cerrar BE ↔ Data.**

Una vez establecida esa frontera, Backend puede construir la API pública
y Frontend puede trabajar contra el contrato sin depender de la
evolución interna de Data.

------------------------------------------------------------------------

## Referencias de trabajo

Este documento consolida las propuestas:

-   `Propuesta_Marco_CONTRATOS_BACKEND_API.md`
-   `Propuesta_Jacqueline_Contrato_Data_Science_BE.md`

Ambas propuestas deben considerarse documentos de trabajo previos. Este
archivo pasa a ser la referencia común para la alineación del equipo una
vez aprobado.
