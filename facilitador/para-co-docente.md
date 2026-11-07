# Para la co-docente · Cómo revisar y adaptar el kit (con ayuda de Claude)

> Este documento es tu punto de entrada. En 10 minutos sabes qué hay, qué ya está probado, qué falta decidir y cómo pedirle a Claude que te ayude a revisarlo sin romper nada.

| | |
|---|---|
| **Repositorio** | https://github.com/benjov/kit-ia-cide |
| **Sitio de la sesión** | https://benjov.github.io/kit-ia-cide/ |
| **Descarga completa** | https://github.com/benjov/kit-ia-cide/archive/refs/heads/main.zip |
| **Estado** | Listo para revisión (2026-11-06). Caso completo corrido con datos reales; la referencia humana del caso es **simulada** y así se declara |

## 1. La sesión en un párrafo

Sesión 4 (2.5 h, en vivo, unas 50 personas de ciencias sociales con Claude Pro y créditos de API). Es una **actividad individual**. Primero mostramos un caso terminado: 102 sentencias emblemáticas de la SCJN codificadas con 3 modelos de Claude. Pregunta del caso: ¿argumenta distinto la Corte en control abstracto y en control concreto? Cada código lleva una cita verificable. Después, cada participante elige una variable nueva, la define con Claude (Chat), prueba el prompt (Workbench), lo empaqueta en un skill, codifica 20 documentos con Cowork y **valida a mano 6 documentos a ciegas**. Cierra con una nota de una página. El código es opcional y Claude Code queda para la sesión 5.

## 2. Qué leer, en este orden

1. **El sitio**, sobre todo [Guía](https://benjov.github.io/kit-ia-cide/guia.html) y [Caso completo](https://benjov.github.io/kit-ia-cide/caso.html). Es lo que verán los participantes.
2. [`facilitador/guion.md`](guion.md): minuto a minuto, checklist previo y plan B. Ahí está el reparto **conduce / circula** entre las dos.
3. [`ejercicio/README.md`](../ejercicio/README.md): las 10 variables para elegir y cómo se hace la validación individual.
4. [`caso-completo/06-memo-metodologico.md`](../caso-completo/06-memo-metodologico.md): el caso resuelto en dos páginas.
5. [`auditoria/bitacora-decisiones.md`](../auditoria/bitacora-decisiones.md) (D1–D11): por qué el kit es como es.
6. [`CLAUDE.md`](../CLAUDE.md): el contexto del proyecto para Claude (y para ti). Contiene las reglas que no hay que romper.

## 3. Qué es real, qué es simulado y qué ya se verificó

| Elemento | Estatus |
|---|---|
| Corpus (102 resúmenes y sentencias) | **Real**. Descargado de la SCJN (colección DGDH) con URL y SHA-256 por archivo. `scripts/verificar_hashes.py` confirmó 10/10 contra la fuente |
| Codificación de Claude (Opus, Sonnet, Haiku 5.5) | **Real**. Batch API; las salidas crudas están en `caso-completo/04-resultados/corridas/` |
| Citas | **Verificadas automáticamente**: Opus 431/431, Sonnet 418/421, Haiku 420/423. Las fallas se revisaron a mano (bitácora D10 y D11) |
| Referencia "humana" del caso (20 documentos) | **SIMULADA** a partir de Opus (`scripts/simular_codificacion_humana.py`, bitácora D7). Por eso los kappa del caso están inflados por construcción. Se dice en el sitio, el memo y la bitácora |
| Costo real | US$6.07 por las tres corridas, más US$0.34 de la prueba previa |
| Sitio | Probado en navegador (tema claro y oscuro, móvil a 390 px). El auditor de citas del navegador coincide con el de Python (431/431) |
| Guion en vivo | **Sin probar con personas.** Los tiempos son una estimación |

## 4. Decisiones ya tomadas (y su porqué)

- **Actividad individual**, no por mesas. Cada quien codifica a mano 6 documentos (los más cortos: 3 AI y 3 amparos) **mientras Cowork trabaja**, para no ver los resultados de Claude antes. Con n = 6, el kappa es ilustrativo; se declara así.
- **Corpus de emblemáticas**: los buscadores de la SCJN y el DOF bloquean la descarga automatizada y decidimos **no evadir** esa protección (D1). Por eso hay solo 9 AI y la pregunta pasó a ser abstracto contra concreto.
- **Se codifica el resumen oficial, no la sentencia completa** (D2). La razón es el tamaño de las sentencias y los límites de uso de Pro.
- **La variable `proporcionalidad` no se reporta** (κ = 0.40 < 0.41), aunque daba el resultado "bonito" (p = 0.011). Es el mensaje didáctico central (D8).

## 5. Lo que más me ayudaría que revisaras

En orden de prioridad:

1. **Tiempos del guion.** ¿Caben las fases 1–4 en 85 minutos para alguien que no programa? ¿Son realistas **4 minutos por documento** a mano (síntesis + Ctrl+F)?
2. **Las 10 variables** de `ejercicio/README.md`. ¿Son observables en los resúmenes? ¿Alguna es jurídicamente imprecisa? ¿Cambiarías alguna por una más cercana a sus disciplinas?
3. **El codebook del caso** (`caso-completo/01-codebook.md`), sobre todo C3 (derecho principal) y C5 (proporcionalidad, regla v1.1).
4. **Prueba en vivo de Cowork** con tu cuenta Pro: instala el skill `codificador-scjn` y córrelo sobre `ejercicio/muestra-20/`. Anota cuánto tarda; es la referencia del plan B.
5. **Tono y claridad** de la guía del participante (sitio → Guía).

## 6. Cómo trabajar el kit con Claude

### Opción A · Cowork (recomendada: Claude lee la carpeta completa)

1. Descarga y descomprime el ZIP (o clona el repositorio).
2. En Claude Desktop, abre **Cowork** y dale acceso a la carpeta `kit-ia-cide`.
3. Primer mensaje:

> *"Lee CLAUDE.md y facilitador/para-co-docente.md. Soy la co-docente de esta sesión. Antes de cambiar cualquier archivo, dime qué entendiste del proyecto y qué reglas no debes romper."*

### Opción B · Proyecto en Chat

Crea un Proyecto y sube como conocimiento: `CLAUDE.md`, este archivo, `facilitador/guion.md`, `ejercicio/README.md`, `caso-completo/01-codebook.md` y `caso-completo/06-memo-metodologico.md`.

### Prompts útiles

- **Revisión crítica del guion**: *"Actúa como una docente con experiencia en talleres para académicos que no programan. Revisa facilitador/guion.md y docs/guia.html. Señala los 5 puntos donde es más probable que la gente se atore o se atrase, y propón un ajuste concreto para cada uno, sin pasar de 150 minutos."*
- **Revisión de variables**: *"Lee ejercicio/README.md y 3 resúmenes de ejercicio/muestra-20. Para cada una de las 10 variables, dime si es observable en estos textos, qué tan difícil sería codificarla a mano en 4 minutos y si la definición inicial tiene un error conceptual."*
- **Consistencia**: *"Revisa que los números del memo (caso-completo/06-memo-metodologico.md), del sitio (docs/caso.html) y de la bitácora coincidan con docs/data/resumen.json. Lista cualquier discrepancia; no corrijas nada todavía."*
- **Adaptar una variable**: *"Quiero reemplazar la variable 6 por [nueva variable]. Escríbela con el mismo formato que las demás (pregunta, códigos iniciales, trampa) y dime qué otros archivos habría que tocar."*

### Reglas para adaptar sin romper (dáselas a Claude si no leyó `CLAUDE.md`)

1. **No editar a mano `docs/data/`**: se genera con `scripts/analizar_resultados.py`.
2. **No cambiar números** en el memo, el sitio o los README sin regenerarlos y copiarlos de `docs/data/resumen.json`.
3. La referencia humana del caso se llama **SIMULADA** en todas partes. No quitar la etiqueta.
4. **No evadir la protección anti-bots** de la SCJN. Las AI nuevas se descargan a mano (bitácora D5).
5. **Cada cambio de codebook sube de versión** (1.1 → 1.2) y deja una entrada en la bitácora (D12, D13…).
6. Todo en español de México, segunda persona ("tú") y sin hype.

## 7. Pendientes y preguntas abiertas

- [ ] **Validar el guion** en un ensayo de 30 minutos con 2 o 3 colegas.
- [ ] ¿Pedimos que elijan la variable **antes** de la sesión (está en el checklist) o la asignamos en vivo para balancear las 10?
- [ ] ¿Dónde vive la **hoja compartida** (una fila por persona): Forms, Sheets u otra?
- [ ] D5: ampliar con unas 30 AI descargadas a mano (opcional, para una versión 2 del caso).
- [ ] Reprocesar los 3 documentos que Haiku dejó truncados (D11) y quitar los encabezados de página al extraer el texto (D10). Ambas cosas son opcionales.

## 8. Cómo proponer cambios

- **Si tienes cuenta de GitHub y acceso de colaboradora**: edita directamente en el repositorio. Desde el navegador, el lápiz en cualquier archivo `.md` permite hacer *commit*. Para cambios grandes, mejor abre un *pull request*.
- **Si no**: abre un *issue* en el repositorio, o mándame tus comentarios o el archivo modificado y yo lo integro.
- Cada cambio se refleja en el sitio en 1 o 2 minutos (GitHub Pages se actualiza solo).
