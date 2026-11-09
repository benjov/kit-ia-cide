# Ejercicio individual · Elige una variable y llévala de la definición al hallazgo

Cada participante trabaja **solo/a, en su propio equipo**. Eliges **una variable nueva** (de las 10 de abajo o una tuya) y la llevas por todo el flujo: codebook → prompt → skill → Cowork → validación → hallazgo.

**Todo se hace desde las aplicaciones de Claude**: Chat con Proyecto (claude.ai o Desktop; también para probar el prompt y comparar modelos), Skills (Configuración → Capacidades) y Cowork (solo Claude Desktop). No necesitas terminal ni Python: los scripts de auditoría los ejecuta Claude dentro de Cowork. El paso a paso, con dónde se abre cada herramienta, está en la [guía de la sesión](https://benjov.github.io/kit-ia-cide/guia.html). Si usas Claude Desktop en modo desarrollador con tu API key, todo se hace en Cowork: ver [Si usas tu API key](https://benjov.github.io/kit-ia-cide/guia.html#modo-api).

**Tu corpus**: [`muestra-20/`](muestra-20/), con 20 resúmenes: las 9 acciones de inconstitucionalidad (control abstracto) y 11 amparos elegidos al azar con semilla 2026 (control concreto). La lista está en [`muestra-20/muestra.csv`](muestra-20/muestra.csv).

## Tú haces los dos papeles: diseñas y validas

Sin equipo, la validación humana la haces tú, con una regla: **codificas a mano antes de ver lo que hizo Claude**.

| Documentos | Quién los codifica | Cuándo |
|---|---|---|
| Los **6 marcados `a_mano = si`** en `muestra.csv` (3 AI y 3 amparos, los más cortos) | **Tú, a ciegas**, en [`hoja-codificacion-humana.csv`](hoja-codificacion-humana.csv), y también Claude | Mientras Cowork trabaja (fase 4). No mires sus resultados de esos 6 hasta terminar tu hoja |
| Los otros 14 | Solo Claude | Fase 4 |

**Cómo codificar rápido (unos 4 minutos por documento)**: abre la hoja con Excel, Numbers o Google Sheets. Cambia `variable` por el nombre de tu variable en los encabezados (p. ej. `evidencia_codigo` y `evidencia_cita`). Abre cada `.txt` con TextEdit o el Bloc de notas, lee la carátula y la síntesis (la primera página), busca con Ctrl+F las palabras clave de tu variable y copia la frase que justifica tu código en la columna de cita. Guarda la hoja en `mi-trabajo/` como CSV o como .xlsx; Cowork lee ambos formatos, también el CSV con `;` que guarda Excel en español.

**Por qué así** (detalles y referencias en [Conceptos](https://benjov.github.io/kit-ia-cide/conceptos.html#humana)): tu codificación es la *referencia* contra la que se mide a Claude. Tiene que ser a ciegas porque, si ves sus códigos antes, tiendes a confirmarlos y el acuerdo sale inflado. El kappa de Cohen mide ese acuerdo descontando el que ocurriría por azar.

**Límites que debes declarar**:

- Con n = 6, el kappa es una **ilustración del procedimiento**, no una medida de confiabilidad. Un error mueve mucho el resultado.
- Quien diseñó el codebook también es quien valida, así que no es una validación independiente.
- Los 6 documentos se eligieron por ser cortos, no al azar.

Para un trabajo publicable necesitas una muestra de 50 o más documentos y un segundo codificador que no haya escrito el codebook.

## Las 10 variables para elegir

Cada ficha trae una **definición inicial** a propósito imperfecta: parte del ejercicio es mejorarla con Claude en la fase 1. Como unas 5 personas elegirán la misma variable sin coordinarse, al final comparamos cómo cada quien la definió y qué kappa obtuvo.

### 1 · Grupos en situación de vulnerabilidad
**Pregunta**: ¿A qué grupo protege explícitamente la sentencia?
**Códigos iniciales**: `mujeres` · `ninez` · `pueblos_indigenas` · `discapacidad` · `diversidad_sexual` · `personas_migrantes` · `personas_privadas_libertad` · `periodistas` · `ninguno_explicito`
**Trampa**: ¿cuenta si el grupo aparece solo en los alegatos?

### 2 · Interpretación conforme
**Pregunta**: ¿La Corte salva la norma interpretándola de forma compatible con la Constitución en vez de invalidarla?
**Códigos iniciales**: `si` · `no`
**Trampa**: distinguir la interpretación conforme de la simple validez.

### 3 · Principio pro persona
**Pregunta**: ¿La Corte invoca el principio pro persona (art. 1º constitucional) para elegir entre interpretaciones?
**Códigos iniciales**: `invocado_decisivo` · `invocado_accesorio` · `no_invocado`
**Trampa**: ¿cómo distinguir "decisivo" de "accesorio" solo con el resumen?

### 4 · Uso de evidencia empírica
**Pregunta**: ¿El razonamiento de la Corte usa datos, estadísticas, estudios o peritajes?
**Códigos iniciales**: `datos_estadisticos` · `estudios_academicos` · `peritajes` · `ninguna`
**Por qué importa**: es la pregunta más "de ciencias sociales" de todas. ¿La Corte usa nuestro trabajo?
**Trampa**: ¿cuenta un dato que solo aparece en los alegatos o en la síntesis del caso, y no en el razonamiento de la Corte?

### 5 · Órdenes al legislador
**Pregunta**: ¿La sentencia ordena o exhorta a un poder legislativo a legislar o modificar una ley?
**Códigos iniciales**: `ordena` · `exhorta` · `no`
**Trampa**: las omisiones legislativas y el plazo.

### 6 · Orden de gobierno de la norma o acto impugnado
**Pregunta**: ¿De qué orden de gobierno es la norma o el acto que se revisa?
**Códigos iniciales**: `federal` · `estatal` · `municipal` · `mixto` · `no_aplica`
**Por qué importa**: federalismo judicial. ¿La Corte es más estricta con los estados?
**Trampa**: en los amparos el acto puede ser de una autoridad local que aplica una ley federal. ¿Se codifica la norma o el acto?

### 7 · Categoría sospechosa
**Pregunta**: ¿La Corte identifica una categoría sospechosa (art. 1º, último párrafo) y aplica escrutinio estricto por ello?
**Códigos iniciales**: `genero` · `orientacion_sexual` · `origen_etnico` · `discapacidad` · `edad` · `otra` · `ninguna`
**Trampa**: se cruza con C5 (proporcionalidad) del caso completo. ¿Coinciden?

### 8 · Generación de derechos
**Pregunta**: ¿El derecho central es civil y político o económico, social, cultural y ambiental (DESCA)?
**Códigos iniciales**: `civil_politico` · `desca` · `ambos`
**Trampa**: la salud reproductiva y la libertad de expresión de periodistas, ¿dónde caen?

### 9 · Tono hacia la autoridad
**Pregunta**: ¿Cómo caracteriza la Corte la actuación de la autoridad o del legislador?
**Códigos iniciales**: `critico_explicito` · `neutral_tecnico` · `deferente`
**Por qué importa**: es una variable **interpretativa**. Esperamos un kappa más bajo. ¿Qué nos dice eso del uso de LLM en variables latentes?
**Trampa**: el lenguaje judicial es formal casi siempre. ¿Qué frase concreta distingue "crítico" de "neutral", y la puedes citar?

### 10 · Diálogo jurisprudencial interno
**Pregunta**: ¿La Corte se apoya en sus propios precedentes (tesis o jurisprudencia de la SCJN)?
**Códigos iniciales**: `cita_jurisprudencia_obligatoria` · `cita_precedentes_aislados` · `no_cita`
**Trampa**: en el resumen los precedentes pueden haber sido editados u omitidos. ¿La unidad de análisis basta?

### O trae la tuya
Una variable propia, siempre que se pueda observar en el texto de los resúmenes. Escríbela con el mismo formato: pregunta, códigos y una trampa que anticipes.

## Tu entregable (fase 6)

Una **nota de una página** (Claude te ayuda a redactarla) y **una fila** en la hoja compartida del grupo:

1. Variable y codebook final (versión 1.x): ¿qué cambiaste respecto de la definición inicial y por qué?
2. Distribución por tipo de control (abstracto o concreto), con N.
3. % de citas verificadas y kappa tuyo contra Claude (n = 6).
4. Un desacuerdo interesante: ¿quién tenía razón, tú o Claude?
5. **Una fricción** del proceso. Las recogemos para la sesión 5.
