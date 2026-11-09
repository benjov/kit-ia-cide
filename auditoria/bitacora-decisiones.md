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

### D12 · 2026-11-06 · La sesión pasa de mesas a actividad individual

- **Qué**: se elimina el trabajo por mesas. Cada participante elige una de 10 variables (o una propia) y lleva el flujo completo en su equipo. La carpeta `mesas/` se renombra a `ejercicio/`.
- **Validación**: cada persona codifica a mano y a ciegas 6 documentos (`a_mano = si` en `muestra.csv`: los 3 AI y los 3 amparos más cortos) mientras Cowork codifica los 20, antes de ver los resultados de Claude.
- **Límites que se declaran**:
  - con n = 6, el kappa es ilustrativo;
  - quien diseña el codebook es quien valida;
  - los documentos se eligieron por su longitud, no al azar.
- **Comparación**: unas 5 personas eligen la misma variable sin coordinarse, así que en la puesta en común se compara cómo la definió cada una y qué kappa obtuvo.
- **Consecuencia**: el caso completo no cambia. La referencia simulada se regeneró con la nueva ruta y salió idéntica.

### D13 · 2026-11-09 · La ruta del participante se hace solo desde las aplicaciones de Claude

- **Problema**: en la revisión aparecieron pasos que exigían salir de la app. El más grave: los scripts del skill traían las 6 variables del caso escritas en el código. La guía pedía editar `VARIABLES` en `verificar_citas.py` para que la variable del participante contara, y por el atajo (`codificador-scjn` + "agrega mi variable") la verificación de citas y el kappa **ignoraban la variable nueva sin avisar**. Además, la guía no decía dónde se abre cada herramienta (claude.ai, Desktop o Console), ni cómo pasar el codebook del Chat a la carpeta.
- **Cambios**:
  - `verificar_citas.py` y `calcular_acuerdo.py` (en `scripts/` y en los dos skills) detectan solos las variables por los encabezados `<variable>_codigo`. Leen CSV con `;` y BOM (Excel en español), aceptan como ausencia cualquier código que empiece con `no_` o `ningun` (más `--ausencia`), y `calcular_acuerdo.py` acepta `--renombrar variable=<nombre>` y avisa cuando no hay nada que comparar.
  - Los `SKILL.md` indican que **Claude** ejecuta los scripts en su entorno y nunca le pide a la persona que corra comandos. Si no puede ejecutar código, lo declara.
  - Guía: tabla "¿Dónde se hace cada cosa?", sección "Antes de la sesión" y carpeta `mi-trabajo/`. Además, Cowork arma el .zip del skill (fase 3), los pasos de Workbench vienen completos, el codebook se descarga como archivo desde el Chat y el plan B no sale de la app.
- **Verificación**: el caso completo da los mismos números con los scripts nuevos (Opus 431/431; los mismos kappa de `confiabilidad-opus.csv`), y `docs/data/` no cambió. Se probó con una variable nueva (`evidencia`), una cita falsa y una hoja humana con `;`, BOM y encabezado genérico.
- **Criterio que queda**: Workbench (Claude Console, en el navegador) se mantiene en la fase 2 porque no requiere código y los participantes tienen créditos. Si no hay acceso, la fase se hace en Chat.
- **Pendiente**: probar en una cuenta Pro el prompt de la fase 3 (que Cowork genere el .zip) y la instalación del skill.

### D14 · 2026-11-09 · Scripts verificables desde Cowork y página de conceptos

- **Qué**: cualquier participante, programe o no, debe poder comprobar el kit pidiéndole a Claude que ejecute los scripts. La audiencia (docentes con doctorado) necesita además los fundamentos de cada paso.
- **Cambios en los scripts**:
  - `descargar_corpus.py`: modo de prueba con `--muestra N`, `--ids` y `--destino`. No toca el kit, y al final compara el SHA-256 de cada PDF y el texto extraído contra el manifiesto. Las descargas parciales sin `--destino` se rechazan, para no reemplazar el manifiesto del kit por uno incompleto. Corrige también el nombre del manifiesto en el docstring.
  - `verificar_hashes.py`: `--ids` y `--pdf`. Este último verifica un PDF bajado a mano desde el navegador, para entornos sin internet, y reconoce el documento por su huella. Además da mensajes claros si no hay red o aparece una protección anti-bots, y se detiene sin evadirla.
  - `analizar_resultados.py --salida`: reproduce el caso en otra carpeta y compara archivo por archivo con el kit.
  - `codificar_api.py --salida`: prueba por API sin tocar las corridas del caso; avisa si falta la key.
- **Verificado el 2026-11-09**, contra la SCJN real:
  - `verificar_hashes.py --muestra 3`: 6/6 coinciden;
  - `descargar_corpus.py --muestra 3 --destino …`: 102 fichas en el índice, 6/6 PDF y 6/6 textos idénticos, en unos 40 s;
  - `analizar_resultados.py --salida`: 108/108 archivos idénticos.
  - `codificar_api.py` no se ejecutó, para no gastar créditos; solo se comprobó que compila.
- **Documentación**: `scripts/README.md` (prompt para Cowork, comando y resultado esperado para cada script), sección "Verifica el kit" en `docs/kit.html` y `docs/conceptos.html`, que cubre codebook, codificación humana, confiabilidad contra validez, kappa con ejemplos de n = 6, citas, procedencia, confianza, reproducibilidad con LLM, inferencia y costos, con referencias. La guía tiene un recuadro "¿Por qué?" en cada fase.
- **Pendiente**: confirmar si el entorno de Cowork tiene salida a `scjn.gob.mx` y `api.anthropic.com`. Si no la tiene, la ruta es `verificar_hashes.py --pdf`, y la API queda solo para terminal.

### D15 · 2026-11-09 · Métricas de evaluación más allá del kappa

- **Qué**: la audiencia no viene del NLP, pero la literatura que evalúa LLM como anotadores reporta precisión, exhaustividad (recall), F1 y α de Krippendorff, no solo kappa. Para que alguien pueda leer esa literatura y defender su validación hacía falta calcular esas métricas y explicarlas.
- **Cambios**:
  - `calcular_acuerdo.py` (en `scripts/` y en los dos skills) reporta por variable el IC 95% del kappa (bootstrap de percentiles, 2,000 remuestras, semilla 2026), el α de Krippendorff nominal y el AC1 de Gwet.
  - Con `--detalle`, el script toma A como referencia y agrega la matriz de confusión, la precisión, la exhaustividad y el F1 por código, el F1 macro y el % de acuerdo por nivel de confianza declarado.
  - La función `kappa()` no cambió, y `analizar_resultados.py` sigue dando 108 de 108 archivos idénticos. `confiabilidad-opus.csv` se regeneró con las columnas nuevas; los kappas son los mismos.
  - `docs/conceptos.html` tiene una sección nueva, §8 «Más allá del kappa», con ejemplos de n = 6 y una tabla de qué reportar. Las secciones siguientes se renumeraron de 9 a 14.
  - El simulador de kappa muestra α, AC1, precisión, exhaustividad y F1, y compara las métricas contra la referencia humana y contra la "verdad" simulada.
  - También se actualizaron la guía (fase 5), el guion, el protocolo, los `SKILL.md`, `05-validacion/README.md`, `scripts/README.md` y `docs/kit.html`.
- **Criterio que queda**: el criterio de decisión sigue siendo **solo el kappa**, porque así se fijó antes de ver los datos. Las demás métricas se reportan sin decidir. Si a posteriori se aplicara a α el corte de 0.41 del kappa, `proporcionalidad` (α = 0.42) entraría con advertencia; con los umbrales propios de α (0.667) no pasaría. No se reporta.
- **Alcance (ajuste tras la auditoría previa al commit)**: las métricas complementarias son **referenciales**; se profundizan en la sesión 5 (evaluaciones, Claude Code y Claude Science). En la sesión, la fase 5 se queda con kappa y desacuerdos; el detalle (matriz, precisión, exhaustividad) es opcional y α/AC1 solo se explican si la persona pregunta. El IC se omite («—») cuando uno de los codificadores usa un solo código, porque el bootstrap no puede estimar la variación.
- **Advertencia**: en el caso, el acuerdo es mayor cuando la confianza es alta *por construcción*, porque la referencia simulada (D7) mete más desacuerdos donde la confianza es baja. Así se declara en los textos.
- **También**: las variables 4, 6 y 9 de `ejercicio/README.md` no tenían "trampa", aunque el material del taller de docencia (artifact externo de la sesión 4) dice que las 10 la traen. Se agregó a las tres. También se corrigió en Conceptos el rango de acuerdo entre modelos: 0.79–1.00 es el de los tres pares, no el de Opus–Sonnet (0.83–0.95).
