# Guion del facilitador · Sesión 4 "Del codebook al hallazgo" (150 min)

**Audiencia**: unas 50 personas · **Formato**: en vivo, **actividad individual**. Cada participante replica el flujo en su propio equipo con una variable que elige. · **Requisitos**: Claude Pro (Desktop). Los créditos de API solo hacen falta para el carril B opcional.

**Regla de la sesión: todo se hace desde las aplicaciones de Claude** (claude.ai o Claude Desktop; Cowork solo en Desktop). Nadie abre una terminal ni edita código: los scripts de auditoría los ejecuta Claude dentro de Cowork como parte del skill. La tabla "¿Dónde se hace cada cosa?" de la [guía](https://benjov.github.io/kit-ia-cide/guia.html) es la referencia para resolver dudas.

| Fase | Aplicación | ¿claude.ai o Desktop? |
|---|---|---|
| 1 · Codebook | Chat con Proyecto | Cualquiera |
| 2 · Prompt | Chat con un Proyecto de prueba (instrucciones = system prompt) y el selector de modelo | Cualquiera |
| 3 · Skill | Cowork arma el .zip; se instala en Configuración → Capacidades → Skills | Cowork: solo Desktop |
| 4 · Escalar | Cowork + hoja de cálculo (Excel, Numbers o Sheets) | Solo Desktop |
| 5 · Validar | Cowork (Claude ejecuta los scripts del skill) | Solo Desktop |
| 6 · Comunicar | Cowork o Chat | Cualquiera |

Facilitan dos docentes: una persona **conduce** (demo y tiempos) y la otra **circula** (resuelve atorones en los equipos y vigila el chat). Conviene alternar los papeles por bloque.

## Checklist previo (48 h antes)

- [ ] Kit publicado y probado: `https://benjov.github.io/kit-ia-cide/` (sitio) y el ZIP del repositorio.
- [ ] Enviar a participantes el enlace con cinco instrucciones:
  1. descargar y descomprimir el ZIP del kit, y crear dentro la carpeta `mi-trabajo/`;
  2. actualizar Claude Desktop y confirmar que ven la pestaña **Cowork**;
  3. activar en Configuración → Capacidades la **ejecución de código y creación de archivos**;
  4. si usan Claude Desktop en modo desarrollador con su API key: configurar y hacer la prueba de la sección [Si usas tu API key](https://benjov.github.io/kit-ia-cide/guia.html#modo-api) de la guía;
  5. **leer las 10 variables de `ejercicio/README.md` y llegar con una elegida** (o con una propia).

  Todo esto está en la sección "Antes de la sesión" de la guía.
- [ ] En Claude Desktop → Configuración → Capacidades: **ejecución de código y creación de archivos** activada (los skills y Cowork la necesitan).
- [ ] Probar Cowork con `ejercicio/muestra-20/` y el skill `codificador-scjn` en una cuenta Pro. Anotar cuánto tarda (referencia para el plan B).
- [ ] Probar en una cuenta Pro **la ruta completa sin código** de la guía: el prompt de la fase 3 (Cowork arma el .zip del skill), la instalación del .zip, y la fase 5 con una hoja humana guardada desde Excel en español (separador `;`).
- [ ] Ejecutar en Cowork, con una cuenta Pro, las verificaciones de `scripts/README.md` (hashes, descarga en modo de prueba, citas, `analizar_resultados.py --salida`). Anotar si el entorno de Cowork tiene salida a `scjn.gob.mx`: si no la tiene, la alternativa es `verificar_hashes.py --pdf`.
- [ ] Probar la ruta completa también en Claude Desktop en **modo desarrollador con una API key** (inferencia de terceros): configurar *Model list* con los tres modelos, hacer la prueba de Python de la guía y las fases 1 a 5 en Cowork, con el skill leído desde la carpeta. Anotar el costo real de la fase 4 y corregir la estimación de la guía (US$2–5 con Sonnet). Desde el 2026-11-10 la app usa la vista unificada: revisar que los nombres de menú de la guía sigan coincidiendo.
- [ ] Preparar una hoja compartida (Forms o Sheets) con **una fila por persona**: variable, % "sí" abstracto, % "sí" concreto, kappa (n = 6), % citas verificadas, fricción.
- [ ] Tener abiertos: el sitio (caso completo y auditor), un Proyecto de prueba con el system prompt del caso en sus instrucciones, y Cowork con la carpeta lista.

## Minuto a minuto

| Tiempo | Fase | Qué pasa | Conduce | Cada participante |
|---|---|---|---|---|
| 0:00–0:12 | **Apertura** | "Así se ve terminado" | Demo del sitio: flujo animado → caso completo → **auditor de citas** (mostrar una cita verificada y explicar la marca p.N) → hallazgos. Pregunta detonadora: *"¿Le creerían a este resultado? ¿Por qué?"* | Abre el sitio en su equipo y sigue la demo |
| 0:12–0:20 | **0 · Corpus** | De dónde salen los datos | Contar la historia del muro anti-bots (bitácora D1). Mostrar el manifiesto con hashes. | Abre `ejercicio/muestra-20/`, confirma su variable y lee su ficha |
| 0:20–0:40 | **1 · Codebook** (Chat) | Mejorar la definición de la variable | Mostrar los prompts sugeridos (abajo). | Crea un Proyecto en Claude, sube el codebook del caso y 3 resúmenes, y refina su variable. **A los 0:38 congela su v1.0** |
| 0:40–0:55 | **2 · Prompt** (Chat, Proyecto de prueba) | Probar antes de escalar | Demo de 3 min: Proyecto sin archivos con el system prompt en sus instrucciones, un chat nuevo por modelo (Haiku contra Sonnet) y costo de escalar con la calculadora del sitio. | Prueba el prompt de su variable con 2 documentos (que **no** sean de los 6 `a_mano`) y 2 modelos; anota si coinciden y si las citas son literales |
| 0:55–1:05 | *Pausa* | | | |
| 1:05–1:20 | **3 · Skill** (Cowork + Configuración) | Empaquetar | Mostrar `skills/plantilla-codificador/`: qué cambia (nombre, descripción, codebook) y qué **no** se toca (los scripts detectan solos la variable). Demo: el prompt de la guía para que Cowork arme el .zip, y cómo se sube en Configuración → Capacidades → Skills. | Pide a Cowork que adapte la plantilla y genere el .zip; lo sube y abre una tarea nueva de Cowork. Si se atora, usa `codificador-scjn` tal cual (ver plan B) |
| 1:20–1:45 | **4 · Escalar** (Cowork) + **codificación a ciegas** | Claude codifica 20; tú codificas 6 | Recordar: primero 3 documentos y revisar, luego el resto. **Mientras Cowork trabaja, cada quien codifica a mano sus 6 documentos `a_mano`** sin mirar lo que hace Claude. | Lanza Cowork. Mientras corre, llena `hoja-codificacion-humana.csv` (unos 4 min por documento: síntesis + Ctrl+F) |
| 1:45–2:00 | **5 · Validar** | Kappa y desacuerdos | Abrir el **simulador de kappa** 2 min: la paradoja de la prevalencia, y por qué con n = 6 el kappa salta tanto. | Cowork calcula el kappa contra su hoja. Revisa cada desacuerdo: ¿falló Claude, falló la persona o el codebook es ambiguo? |
| 2:00–2:18 | **6 · Comunicar** | Nota + puesta en común | Proyectar la hoja compartida **agrupada por variable**: ¿quienes eligieron la misma variable la definieron igual? ¿Obtuvieron el mismo kappa? Pedir 4 o 5 voluntarios (1.5 min cada uno). | Pide a Claude su nota de una página y llena su fila |
| 2:18–2:30 | **7 · Puente** | Hacia la sesión 5 | Agrupar las fricciones (copiar y pegar, repetir a mano, no poder re-ejecutar, archivos sueltos, escalar a miles). Cerrar con: *"Todo esto, versionado y re-ejecutable con un comando: eso es Claude Code."* Anunciar que la sesión 5 también cubre **evaluaciones** (la validación de hoy fue la versión mínima) y **Claude Science**. Mostrar 60 s `scripts/` y la carpeta `corridas/` del caso: es la ruta con código que usamos para las 102 sentencias y los 3 modelos. | — |

**Quien circula**: en las fases 1–4 recorre los equipos; las dudas más comunes son dónde se sube el ZIP del skill, los permisos de carpeta en Cowork, que Cowork no vea el skill (hay que abrir una tarea nueva) y el encabezado de la hoja humana. Si alguien pregunta "¿tengo que instalar Python?": no, Claude ejecuta los scripts dentro de Cowork. Junta en una nota las fricciones que oiga para la fase 7.

## Prompts sugeridos para la fase 1 (Chat)

1. *"Adjunto el codebook de un proyecto y 3 resúmenes de sentencias. Voy a agregar la variable [VARIABLE] con esta definición inicial: [PEGAR]. Lee los 3 resúmenes y dime, con citas, en cuáles sería difícil aplicar mi definición y por qué."*
2. *"Ponte en el papel de un codificador escéptico. Encuentra 3 ambigüedades en mi definición y propón una regla de decisión para cada una."*
3. *"Escribe mi codebook v1.0 con el formato del codebook adjunto, pero solo con mi variable: tabla de códigos (máximo 5), regla de decisión, casos frontera, reglas generales y un formato de salida JSON con los campos codigo, cita y confianza. Entrégamelo como un archivo descargable llamado codebook.md."* (Se descarga y se guarda en `mi-trabajo/`.)

## Prompt sugerido para la fase 3 (Cowork arma el skill)

> *"Copia la carpeta skills/plantilla-codificador a mi-trabajo/codificador-[mi-variable]. En la copia: (1) reemplaza referencias/codebook.md por mi-trabajo/codebook.md; (2) en SKILL.md cambia name a codificador-[mi-variable] y escribe una description específica para mi variable; (3) ajusta la sección Salida con el nombre de mi variable; (4) borra el recuadro "Cómo usar esta plantilla". No edites los scripts. Después comprime la carpeta en mi-trabajo/codificador-[mi-variable].zip y muéstrame el SKILL.md final."*

## Prompt sugerido para Cowork (fase 4)

> *"Usa el skill [nombre] para codificar los archivos .txt de la carpeta ejercicio/muestra-20. Empieza con 3 documentos que no estén marcados a_mano = si en muestra.csv y muéstrame el resultado antes de seguir. Después codifica el resto sin mostrarme los resultados de los 6 documentos a_mano. Guarda resultados_codificacion.csv en mi-trabajo/. Al terminar, verifica las citas con el script del skill, corrige las que no se encuentren y dame la distribución de mi variable por tipo de control."*

Después de llenar la hoja:

> *"Esta es mi codificación a ciegas de 6 documentos (mi-trabajo/hoja-codificacion-humana). Calcula el kappa contra tu codificación con el script del skill, sin cambiar ninguno de mis códigos, y explícame los desacuerdos uno por uno."* (Opcional, para quien termine antes: pedir el detalle con matriz de confusión, precisión y exhaustividad.)

## Plan B

| Problema | Alternativa |
|---|---|
| Cowork no disponible o lento | Chat con un Proyecto y el skill activado: adjuntar 6 a 10 resúmenes (incluidos los 6 `a_mano`) y el mismo prompt. Con la ejecución de código activada, Claude corre los mismos scripts. Si no puede ejecutar código, verificar 5 citas a mano con Ctrl+F |
| Claude dice que no puede ejecutar código | Configuración → Capacidades → activar la ejecución de código y creación de archivos; abrir una tarea o chat nuevo |
| El skill no se activa | Pegar el contenido de `SKILL.md` como primer mensaje y pedir que lo siga |
| Límite de uso de Pro | Reducir a 10 documentos (incluidos los 6 `a_mano`) |
| Modo desarrollador (API key): no ve el Chat, los Proyectos o dónde subir el skill | Todo en Cowork, según la tabla de la guía: el codebook se lee desde la carpeta y el skill no se instala (*"sigue las instrucciones de mi-trabajo/codificador-[mi-variable]/SKILL.md"*) |
| Modo desarrollador: Cowork no abre la carpeta, no ejecuta Python o no tiene internet | Revisar *Allowed workspace folders*; sin Python, verificar citas buscándolas en el texto y declararlo; la red solo hace falta para las verificaciones opcionales (*Allowed egress hosts*) |
| El selector no muestra Haiku | Comparar Sonnet con Opus; lo que importa es que sean dos modelos distintos |
| "¿Por qué kappa y no F1 o accuracy, como en los papers de NLP?" | Responden a preguntas distintas: kappa/α miden si dos codificadores coinciden más allá del azar (confiabilidad); precisión, exhaustividad y F1 miden si Claude acierta contra una referencia que se toma como verdad. El script da las dos familias; el protocolo decide con kappa porque así se fijó antes. Hoy son de referencia: se profundizan en la sesión 5 (evaluaciones, Claude Code y Claude Science). Ver [Conceptos §8](https://benjov.github.io/kit-ia-cide/conceptos.html#metricas) |
| Alguien va muy atrasado | Saltar la fase 3 y usar `codificador-scjn` con la instrucción "agrega mi variable". La verificación de citas y el kappa incluyen la variable nueva sin editar nada |
| No le alcanza el tiempo para los 6 documentos a mano | Codificar 3 y declararlo; terminar los otros 3 después de la sesión |

## Para quien pregunte "¿y cómo sé que esto es cierto?"

La audiencia es exigente, y está bien. Hay dos respuestas ya preparadas:

- **Fundamentos**: [Conceptos](https://benjov.github.io/kit-ia-cide/conceptos.html) cubre codebook, codificación humana, confiabilidad contra validez, kappa (con el ejemplo de n = 6 y la paradoja de la prevalencia), otras métricas de evaluación (matriz de confusión, precisión, exhaustividad, F1, α, AC1, IC por bootstrap), citas verificables, procedencia, reproducibilidad con LLM e inferencia, con referencias.
- **Comprobación**: cualquiera puede pedirle a Cowork que ejecute los scripts y obtener los mismos números (sitio → *Descargar kit → Verifica el kit*).

## Mensajes clave (si sólo recuerdan tres cosas)

1. **Una cita verificable vale más que un código.** Sin evidencia rastreable, no hay resultado.
2. **Valida antes de escalar.** Las reglas se fijan antes de ver los datos, y codificas a mano *antes* de ver a Claude.
3. **El acceso a los datos y el codebook son decisiones metodológicas**, no trámites. Escríbelas.
