# Codebook v1.1 — ¿Argumenta distinto la Corte en control abstracto y en control concreto?

> **Versión**: 1.1 · **Fecha**: 2026-11-06 · Las corridas del caso completo usaron la **v1.0**; la regla 4 de casos frontera (v1.1) está **pendiente de validar** con una muestra nueva (bitácora D8) · **Unidad de análisis**: resumen oficial (carátula + síntesis + extracto) de una sentencia emblemática de la SCJN en materia de derechos humanos.
> **Diseñado con**: Claude (Chat, Proyecto "Caso SCJN"), revisado por el equipo docente.
> **Cambios respecto de la versión anterior**: ver `auditoria/bitacora-decisiones.md`.

## Pregunta de investigación

Cuando la SCJN protege derechos humanos, **¿cambia su forma de argumentar según la vía procesal?**

- **Control abstracto**: la acción de inconstitucionalidad (AI) revisa una ley "en el papel", promovida por órganos del Estado (CNDH, Fiscalía, minorías legislativas, partidos), sin un caso concreto.
- **Control concreto**: los amparos (AR, ADR, AD) y otras vías parten de un caso con personas afectadas.

**Hipótesis de trabajo** (para discutir, no para confirmar):

- H1. En la vía abstracta la Corte recurre más al **test de proporcionalidad** y a la invalidez de normas.
- H2. En la vía concreta la Corte cita más **fuentes internacionales** (tratados y Corte IDH), porque hay una víctima identificable.
- H3. La **perspectiva de género** aparece con la misma frecuencia en ambas vías.

## Variables

Hay dos tipos de variables:

- **Metadatos (M)**: vienen del manifiesto y no las codifica Claude.
- **Codificadas (C)**: las asigna Claude y las valida un humano. Cada variable C lleva una **cita textual** del resumen que la justifica y un nivel de **confianza** (alta, media o baja).

### M1. `via` — Vía procesal (metadato)

Se toma de la columna `tipo` de `corpus/manifiesto_emblematicas.csv`. Se recodifica en `control`:

| `tipo` | `control` |
|---|---|
| AI (acción de inconstitucionalidad) | abstracto |
| AR, ADR, AD, AI-amparo, CT, DGI, otros | concreto / otro (ver nota) |

Nota: la contradicción de tesis (CT) y la declaratoria general (DGI) no son control concreto en sentido estricto. En el análisis principal se reportan aparte como `otro`.

### C1. `promovente` — ¿Quién llevó el asunto a la Corte?

| Código | Definición | Ejemplo típico |
|---|---|---|
| `persona` | Una o varias personas físicas que reclaman a título propio | "La quejosa promovió amparo…" |
| `colectivo` | Organización de la sociedad civil, comunidad, pueblo indígena, sindicato o grupo | "Integrantes de la comunidad…" |
| `organo_autonomo` | CNDH, comisiones estatales de derechos humanos, INAI u otros órganos constitucionales autónomos | "La CNDH promovió acción de inconstitucionalidad…" |
| `fiscalia` | PGR / FGR | "La Procuraduría General de la República demandó…" |
| `actor_politico` | Partido político o minoría legislativa | "Diputados integrantes de la Legislatura…" |
| `autoridad` | Otra autoridad (municipio, poder estatal, dependencia) | "El municipio de…" |
| `no_identificable` | El resumen no permite saberlo | — |

**Regla de decisión**: si hay varios promoventes, codifica el **primero mencionado** en los ANTECEDENTES.

### C2. `resultado` — ¿La resolución favorece la protección del derecho invocado?

| Código | Definición |
|---|---|
| `protege` | La Corte concede el amparo, invalida la norma impugnada o resuelve a favor de quien alega la violación |
| `no_protege` | La Corte niega el amparo, reconoce la validez de la norma o resuelve en contra de quien alega la violación |
| `mixto` | Invalida unas normas y valida otras, o concede en parte y niega en parte |
| `otro` | Sobresee, desecha, fija criterio sin resolver un caso (p. ej. contradicción de tesis) |

**Caso frontera**: si la Corte "reconoce la validez" de una norma **mediante interpretación conforme** que amplía el derecho, codifica `mixto` y explícalo en la nota.

### C3. `derecho_principal` — Derecho humano central del caso

Elige **uno**, el que organiza la cuestión a resolver:

`igualdad_no_discriminacion` · `derechos_sexuales_reproductivos` · `libertad_expresion_informacion` · `debido_proceso_acceso_justicia` · `libertad_integridad_personal` · `salud` · `pueblos_indigenas` · `medio_ambiente` · `ninez` · `familia` · `trabajo_seguridad_social` · `privacidad_datos` · `otro`

**Regla de decisión**: si el resumen enumera varios TEMAS, el derecho principal es el que aparece en **CUESTIÓN A RESOLVER**, no el primero de la lista de temas.

### C4. `fuentes_internacionales` — ¿La Corte apoya su razonamiento en fuentes internacionales?

| Código | Definición |
|---|---|
| `ninguna` | No cita tratados ni jurisprudencia internacional |
| `tratados` | Cita tratados o instrumentos internacionales (CADH, PIDCP, CEDAW, Convención sobre los Derechos del Niño, etc.) pero no jurisprudencia |
| `corte_idh` | Cita sentencias u opiniones consultivas de la Corte Interamericana (con o sin tratados) |
| `otra_jurisprudencia` | Cita jurisprudencia de otros tribunales u órganos (TEDH, comités de la ONU) pero no de la Corte IDH |

**Regla de decisión**: cuenta solo lo que la **Corte** dice en el EXTRACTO, no lo que alegan las partes.

### C5. `proporcionalidad` — ¿Aplica un test de proporcionalidad o de escrutinio?

| Código | Definición |
|---|---|
| `si` | Analiza de forma explícita la finalidad, la idoneidad, la necesidad o la proporcionalidad en sentido estricto, o aplica un escrutinio estricto u ordinario |
| `no` | No hay análisis por etapas de la medida |

**Regla de decisión (v1.1)**: enunciar un estándar ("la restricción debe ser necesaria y proporcional") **sin aplicarlo por etapas** a la norma o acto = `no`. Aplicar al menos dos etapas (finalidad, idoneidad, necesidad, proporcionalidad en sentido estricto) o un escrutinio explícito = `si`.

**Señales**: "finalidad constitucionalmente imperiosa", "idónea", "necesaria", "proporcional en sentido estricto", "escrutinio estricto", "test".

### C6. `perspectiva_genero` — ¿La Corte declara juzgar con perspectiva de género?

| Código | Definición |
|---|---|
| `si` | La Corte invoca de forma **explícita** la perspectiva de género como método |
| `no` | No la invoca, aunque el caso trate sobre mujeres |

## Formato de salida (por documento)

```json
{
  "id": "AI-148-2017",
  "codebook_version": "1.1",
  "promovente":            {"codigo": "fiscalia",  "cita": "La Procuraduría General de la República (PGR) demandó la invalidez", "confianza": "alta"},
  "resultado":             {"codigo": "mixto",     "cita": "Se reconoció la validez del artículo 195; se invalidó el artículo 196", "confianza": "alta"},
  "derecho_principal":     {"codigo": "derechos_sexuales_reproductivos", "cita": "…", "confianza": "alta"},
  "fuentes_internacionales": {"codigo": "…", "cita": "…", "confianza": "…"},
  "proporcionalidad":      {"codigo": "si", "cita": "no puede tener su origen en ninguna finalidad imperiosa desde el punto de vista constitucional", "confianza": "media"},
  "perspectiva_genero":    {"codigo": "si", "cita": "esta Corte guía su análisis y decisión desde la obligación de apreciar el caso con perspectiva de género", "confianza": "alta"},
  "nota": "Casos frontera o dudas del codificador."
}
```

## Reglas generales

1. **Cita literal obligatoria.** Cópiala tal como aparece en el resumen, sin parafrasear, con 5 a 40 palabras. Si el código es `ninguna`, `no` o `no_identificable`, la cita es `""` y la nota explica qué se buscó.
2. **Solo el texto.** No uses conocimiento externo sobre el caso, aunque sea famoso.
3. **Ante la duda, confianza baja.** Es preferible marcar la duda a forzar un código.
4. **No inventes categorías.** Si nada encaja, usa `otro` y explícalo en la nota.

## Libro de casos frontera (se actualiza tras la validación)

| # | Situación | Decisión | Versión |
|---|---|---|---|
| 1 | Interpretación conforme que salva la norma ampliando el derecho | `resultado = mixto` | 1.0 |
| 2 | Varios promoventes de distinto tipo | Se codifica el primero mencionado | 1.0 |
| 3 | Las partes citan la CADH pero la Corte no | `fuentes_internacionales = ninguna` | 1.0 |
| 4 | La Corte enuncia necesidad y proporcionalidad como estándar, pero no los aplica por etapas (p. ej. AI 25/2016, AI 87/2015) | `proporcionalidad = no` | 1.1 (pendiente de validar) |
