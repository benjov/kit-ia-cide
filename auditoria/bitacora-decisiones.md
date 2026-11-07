# Bitácora de decisiones · Caso completo

Registro cronológico de las decisiones metodológicas. Formato: **qué** se decidió, **por qué**, **evidencia** y **consecuencia**.

---

### D1 · 2026-11-06 · Fuente del corpus: sentencias emblemáticas de la DGDH-SCJN

- **Qué**: el corpus base son las 102 sentencias de la colección "Sentencias emblemáticas" de la Dirección General de Derechos Humanos de la SCJN.
- **Por qué**: la pregunta original era sobre acciones de inconstitucionalidad. El Buscador Jurídico, @lex, el Semanario Judicial y el DOF tienen protección anti-bots (Imperva/Incapsula) que bloquea la descarga automatizada. Decidimos **no** evadirla. La colección de emblemáticas está en archivos estáticos descargables y trae un resumen oficial por sentencia.
- **Evidencia**: pruebas de acceso del 2026-11-06 (respuesta `_Incapsula_Resource` en bj.scjn.gob.mx, sjf2.scjn.gob.mx, dof.gob.mx, www2.scjn.gob.mx).
- **Consecuencia**: solo hay 9 acciones de inconstitucionalidad. La pregunta se reformula como una comparación entre control abstracto y concreto. Queda pendiente la ampliación con unas 30 AI descargadas a mano desde el Buscador Jurídico (D5).
- **Lección para la sesión**: *conseguir los datos es parte del método*. El acceso define la pregunta más de lo que solemos admitir.

### D2 · 2026-11-06 · Unidad de análisis: el resumen oficial, no la sentencia completa

- **Qué**: Claude codifica el resumen (carátula, síntesis y extracto, de 1,500 a 6,500 palabras). La sentencia completa queda como fuente de verificación.
- **Por qué**: las sentencias completas tienen entre 50 y 200 páginas. Con 50 personas en plan Pro, codificarlas en vivo agotaría los límites de uso. El extracto conserva las marcas `p.N` de los párrafos de la sentencia, lo que permite rastrear cada cita hasta la fuente primaria.
- **Riesgo aceptado**: el resumen es una selección editorial de la DGDH. Ciertas variables (p. ej. citas a precedentes) pueden estar subrepresentadas. Lo explora la variable 10 del ejercicio.

### D3 · 2026-11-06 · Codebook v1.0

- **Qué**: 6 variables codificadas (promovente, resultado, derecho principal, fuentes internacionales, proporcionalidad, perspectiva de género) y 1 metadato (vía procesal → control).
- **Por qué**: cubren las tres hipótesis (H1–H3) con variables observables en el texto. Se descartaron variables más interpretativas (p. ej. "activismo judicial") por su baja confiabilidad esperada. La variable 9 del ejercicio explora una así a propósito.
- **Casos frontera iniciales**: 3, registrados en el codebook.

### D4 · 2026-11-06 · Prueba del verificador de citas

- **Qué**: se probó `verificar_citas.py` con 4 citas reales y 1 parafraseada de la AI 148/2017.
- **Resultado**: detectó la cita parafraseada ("la Corte aplicó un test de proporcionalidad estricto"), que no está en el texto.
- **Consecuencia**: el verificador es el control principal contra la evidencia inventada.

### D5 · PENDIENTE · Ampliación con acciones de inconstitucionalidad descargadas a mano

- Descargar unas 30 AI desde el Buscador Jurídico ("Consultar documento de origen") de forma manual, registrar la URL y el SHA-256, y marcarlas en el manifiesto con `metodo_obtencion = manual`.

### D6 · 2026-11-06 · Codificación con Batch API y tres modelos

- **Qué**: los 102 documentos se codificaron con Opus 5.5, Sonnet 5.5 y Haiku 5.5 mediante la Batch API (50% de descuento). La prueba previa con 3 documentos en tarifa normal costó US$0.34.
- **Por qué**: la estimación inicial (unos US$4) subestimó el tamaño de los resúmenes. Con datos reales (unos 19,000 tokens de entrada por documento), los tres modelos en tarifa normal costaban unos US$17. Batch bajó el costo a la mitad sin cambiar el resultado.
- **Lección**: mide en el Workbench antes de estimar. Nuestra primera estimación se equivocó por un factor de 4.

### D7 · 2026-11-06 · Referencia humana SIMULADA

- **Qué**: la muestra de validación (20 documentos) se codificó con un procedimiento simulado, no con personas (`scripts/simular_codificacion_humana.py`).
- **Por qué**: es un caso didáctico. El objetivo es enseñar el procedimiento de validación, no producir un hallazgo publicable.
- **Consecuencia**: el kappa Opus–referencia está inflado por construcción. En la sesión, cada participante hace una validación humana real a ciegas (6 documentos).

### D8 · 2026-11-06 · `proporcionalidad` no pasa el umbral (κ = 0.40)

- **Qué**: según el protocolo (κ < 0.41), la variable no se reporta y H1 queda sin evaluar.
- **Evidencia**: en sus notas, Opus marcó confianza baja o media justo donde la Corte **enuncia** estándares de necesidad y proporcionalidad sin **aplicar** un test por etapas (AI 25/2016, AI 87/2015, AI 54/2018).
- **Decisión**: el codebook v1.1 agrega una regla. Enunciar el estándar sin aplicarlo por etapas = `no`; aplicar al menos dos etapas (finalidad, idoneidad, necesidad, proporcionalidad estricta) a la norma o acto = `si`. Hay que **validar v1.1 con una muestra nueva** antes de reportar H1; no se re-codifica la muestra vieja para "arreglar" el kappa.
- **Tentación evitada**: la diferencia abstracto–concreto en proporcionalidad da p = 0.011. Es exactamente el resultado que confirmaría H1, y por eso mismo no lo reportamos con una medición no validada.

### D9 · 2026-11-06 · Errores en la fuente oficial detectados durante la codificación

- **Qué**: Opus advirtió en sus notas que la carátula del resumen de la AI 35/2014 cita "Acción de Inconstitucionalidad 22/2016… 2 de octubre de 2019", que es otro caso. Verificado en el texto. También, la carátula de la AI 148/2017 fecha la sentencia en "7 de septiembre de 2017", pero la sentencia es del 7 de septiembre de 2021 (así lo dicen la misma carátula, en el campo FECHA, y el extracto).
- **Consecuencia**: no afecta las variables codificadas, pero sí las referencias. En el memo citamos el caso por su número y la fecha del extracto.

### D10 · 2026-11-06 · Auditoría de citas: tres tipos de falla (Sonnet 5.5)

El verificador encontró 3 citas no literales de 421 en la corrida de Sonnet (Opus: 0 de 431). Las revisamos a mano:

| Documento | Claude escribió | El texto dice | Diagnóstico |
|---|---|---|---|
| AD 35/2014 | "…en representación de **su hijo** DBG, demandó…" | "…en representación de DBG, demandó…" | **Embellecimiento**: agregó palabras. Error real. |
| ADR 5490/2016 | "**el** derecho a una justa indemnización…" | "**al** derecho a una justa indemnización…" | **Alteración mínima**. Error real, pero sin consecuencia sustantiva. |
| ADR 2944/2017 | "…la prueba idónea para acreditar el vínculo filial…" | La frase está partida por el encabezado de página "DIRECCIÓN GENERAL DE ESTUDIOS…" | **Falso positivo del verificador**: la cita es fiel, el PDF la interrumpe. |

Además, en el AR 166/2019 Sonnet asignó un código sustantivo de `derecho_principal` **sin cita**.

- **Lección**: el verificador es necesario pero no suficiente. Toda alarma se revisa a mano (aquí, 1 de 3 era falsa alarma). Y la cita literal es la mejor defensa contra el embellecimiento, que es el error más peligroso porque **suena verdadero**.
- **Mejora pendiente**: quitar los encabezados de página repetidos al extraer el texto del PDF.

### D11 · 2026-11-06 · Haiku 5.5: barato y bueno, pero con respuestas truncadas

- **Qué**: Haiku codificó 99 de 102 documentos por US$0.13, 33 veces menos que Opus. En 3 documentos (AD 9/2018, AR 659/2017, AI 35/2014), la respuesta superó `max_tokens = 4000` y quedó truncada, sin un JSON válido.
- **Diagnóstico**: sus notas fueron más largas de lo necesario en documentos complejos.
- **Consecuencia**: esos 3 documentos quedan fuera de la corrida de Haiku. Para reprocesarlos: subir `max_tokens` o pedir notas de 2 o 3 oraciones como máximo.
- **Lección**: además de las citas, revisa siempre el `stop_reason`. Una respuesta truncada no es un error de la API: es una salida incompleta que hay que detectar.
