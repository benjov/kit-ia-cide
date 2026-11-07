# Memo metodológico · Control abstracto y concreto en sentencias emblemáticas de la SCJN

> **Estatus**: caso didáctico del Kit IA-CIDE (sesión 4). La referencia humana es **simulada**. Los resultados ilustran un procedimiento y **no** constituyen un hallazgo publicable ni análisis jurídico.
> **Fecha**: 2026-11-06 · **Codebook**: v1.0 (corridas) → v1.1 (propuesto) · **Prompt**: v1.0 · **Modelo principal**: Claude Opus 5.5 (`claude-opus-5-5`)

## 1. Pregunta

¿Argumenta distinto la Suprema Corte de Justicia de la Nación cuando protege derechos humanos en **control abstracto** (acción de inconstitucionalidad, AI) y en **control concreto** (amparo)?

- H1: en la vía abstracta, más test de proporcionalidad.
- H2: en la vía concreta, más fuentes internacionales.
- H3: la perspectiva de género aparece igual en ambas vías.

## 2. Datos

| | |
|---|---|
| Fuente | Colección *Sentencias emblemáticas*, Dirección General de Derechos Humanos, SCJN |
| N | 102 sentencias: 9 AI, 86 amparos (51 AR, 26 ADR, 9 AD), 7 otras (CT, CC, DGI) |
| Unidad de análisis | Resumen oficial (carátula, síntesis y extracto), unas 4,600 palabras en promedio |
| Procedencia | `corpus/manifiesto_emblematicas.csv`: URL oficial, fecha de descarga (2026-11-06) y SHA-256 de cada PDF |
| Selección | **No aleatoria**: la SCJN eligió estas sentencias como emblemáticas |

**Restricción de acceso** (bitácora D1): la pregunta original (unas 40 AI) no fue viable porque las fuentes con más AI bloquean la descarga automatizada. La pregunta se reformuló a la comparación abstracto contra concreto.

## 3. Medición

Seis variables codificadas según el [codebook](01-codebook.md): promovente, resultado, derecho principal, fuentes internacionales, proporcionalidad y perspectiva de género. Cada código lleva **cita literal**, **confianza** y **nota**.

**Procedimiento**: prompt de sistema con el codebook en caché, salida JSON restringida por esquema, Batch API. Tres modelos sobre los 102 documentos: Opus 5.5, Sonnet 5.5 y Haiku 5.5.

## 4. Controles de calidad

### 4.1 Citas (control 2)

| Modelo | Citas verificadas | Confianza baja | Costo (Batch) |
|---|---|---|---|
| Opus 5.5 | 431/431 (100%) | 43 códigos | US$4.26 |
| Sonnet 5.5 | 418/421 (99.3%) | 13 códigos | US$1.68 |
| Haiku 5.5 | 420/423 (99.3%) · 99 docs (3 respuestas truncadas) | 17 códigos | US$0.13 |

Las 3 citas fallidas de Sonnet se revisaron a mano (bitácora D10): 2 errores reales (un **embellecimiento**, un cambio de letra) y 1 falso positivo del verificador por un encabezado de página. Haiku tuvo 3 citas no literales y 3 respuestas **truncadas** por exceder `max_tokens` (bitácora D11).

### 4.2 Validación contra la referencia (control 3), n = 20, referencia SIMULADA

| Variable | κ Opus | κ Sonnet | κ Haiku | Decisión (umbral fijado antes: ≥ 0.61) |
|---|---|---|---|---|
| promovente | 1.00 | 1.00 | 1.00 | Se reporta |
| resultado | 0.75 | 0.75 | 0.73 | Se reporta |
| derecho_principal | 0.65 | 0.65 | 0.57 | Se reporta |
| fuentes_internacionales | 0.71 | 0.64 | 0.78 | Se reporta |
| **proporcionalidad** | **0.40** | 0.50 | 0.58 | **No se reporta** (Opus < 0.41); codebook v1.1 pendiente de validar |
| perspectiva_genero | 1.00 | 1.00 | 1.00 | Se reporta, con advertencia: prevalencia baja (12 de 102) |

⚠️ La referencia se derivó de los códigos de Opus (bitácora D7), así que los κ están distorsionados por construcción. Por ejemplo, Haiku "supera" a Opus en proporcionalidad (0.58 contra 0.40) porque la simulación puso los desacuerdos justo donde Opus dudaba. Esta tabla sirve para mostrar el procedimiento, no para comparar la calidad de los modelos.

### 4.3 Robustez entre modelos (102 documentos)

Los tres modelos coinciden entre sí con κ entre 0.79 y 1.00. Las variables más sensibles al modelo son `resultado`, `proporcionalidad` y `derecho_principal`, con los κ más bajos en los pares que incluyen a Haiku. Ver la tabla completa en [`05-validacion/`](05-validacion/) y en el sitio.

## 5. Resultados (Opus 5.5; prueba exacta de Fisher bilateral)

| Hipótesis | Variable | Abstracto (AI) | Concreto (amparos) | p | Lectura |
|---|---|---|---|---|---|
| H1 | Test de proporcionalidad | 7/9 (78%) | 28/86 (33%) | 0.011 | **No evaluable**: la variable no pasó la validación |
| H2 | Cita a la Corte IDH | 5/9 (56%) | 30/86 (35%) | 0.282 | Dirección **contraria** a H2, sin evidencia suficiente |
| H3 | Perspectiva de género | 3/9 (33%) | 8/86 (9%) | 0.067 | Diferencia no significativa al 5%; potencia muy baja |
| — | Resultado: protege | 3/9 (33%) | 54/86 (63%) | 0.149 | En las AI predominan los resultados **mixtos** (5/9) |

## 6. Interpretación

1. **El hallazgo más llamativo es justo el que no podemos sostener.** La diferencia en proporcionalidad (p = 0.011) confirmaría H1, pero la variable no pasó el umbral de confiabilidad. Las notas de Claude mostraron la ambigüedad: la Corte a menudo *enuncia* estándares de necesidad y proporcionalidad sin *aplicar* un test por etapas. Reportarlo sería sobreinterpretar una medición defectuosa.
2. **H2 apunta en dirección contraria**: las AI emblemáticas citan más a la Corte IDH. Una explicación posible (por explorar) es que los promoventes de las AI (CNDH y otros órganos autónomos en 5 de 9) litigan con estándares interamericanos.
3. **Con 9 AI no hay potencia estadística.** Cada AI mueve la proporción 11 puntos. Ampliar el corpus (bitácora D5) es la prioridad.

## 7. Límites

- Corpus **seleccionado** por la SCJN (no aleatorio): los resultados describen las sentencias emblemáticas, no la jurisprudencia en general.
- Unidad de análisis **secundaria** (resúmenes de la DGDH). La marca `p.N` permite verificar en la sentencia, pero ciertas variables pueden estar subrepresentadas.
- Referencia humana **simulada**.
- Las fuentes oficiales tienen errores en sus carátulas (bitácora D9).

## 8. Reproducibilidad

| Artefacto | Ubicación |
|---|---|
| Corpus y procedencia | `corpus/` + `scripts/descargar_corpus.py` + `scripts/verificar_hashes.py` |
| Codebook y prompt versionados | `caso-completo/01-codebook.md`, `caso-completo/02-prompt/` |
| Corridas (modelo, versión, tokens y fecha por documento) | `caso-completo/04-resultados/corridas/*.jsonl` |
| Auditoría de citas | `scripts/verificar_citas.py` |
| Validación | `caso-completo/05-validacion/` |
| Decisiones | `auditoria/bitacora-decisiones.md` |
| Análisis | `scripts/analizar_resultados.py` |

**Declaración de uso de IA** (sugerida para la sección de métodos): *"La codificación se realizó con Claude Opus 5.5 (Anthropic) mediante la API, con un codebook versionado (v1.0) incluido en el prompt de sistema y salida estructurada. Cada código se acompañó de una cita textual, verificada automáticamente contra el documento fuente (100% verificadas). La confiabilidad se evaluó contra una codificación humana a ciegas de 20 documentos estratificados (κ por variable en la Tabla X). Las variables con κ < 0.41 se excluyeron del análisis. Prompt, codebook, salidas y scripts están disponibles en [repositorio]."*
