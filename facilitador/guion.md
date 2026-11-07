# Guion del facilitador · Sesión 4 "Del codebook al hallazgo" (150 min)

**Audiencia**: unas 50 personas · **Formato**: en vivo, **actividad individual**. Cada participante replica el flujo en su propio equipo con una variable que elige. · **Requisitos**: Claude Pro (Desktop) + créditos de API.

Facilitan dos docentes: una persona **conduce** (demo y tiempos) y la otra **circula** (resuelve atorones en los equipos y vigila el chat). Conviene alternar los papeles por bloque.

## Checklist previo (48 h antes)

- [ ] Kit publicado y probado: `https://benjov.github.io/kit-ia-cide/` (sitio) y el ZIP del repositorio.
- [ ] Enviar a participantes el enlace con cuatro instrucciones:
  1. descargar y descomprimir el ZIP del kit;
  2. actualizar Claude Desktop;
  3. entrar a Claude Console y confirmar que ven créditos;
  4. **leer las 10 variables de `ejercicio/README.md` y llegar con una elegida** (o con una propia).
- [ ] En Claude Desktop → Configuración → Capacidades: **ejecución de código y creación de archivos** activada (los skills y Cowork la necesitan).
- [ ] Probar Cowork con `ejercicio/muestra-20/` y el skill `codificador-scjn` en una cuenta Pro. Anotar cuánto tarda (referencia para el plan B).
- [ ] Preparar una hoja compartida (Forms o Sheets) con **una fila por persona**: variable, % "sí" abstracto, % "sí" concreto, kappa (n = 6), % citas verificadas, fricción.
- [ ] Tener abiertos: el sitio (caso completo y auditor), Workbench con el prompt cargado y Cowork con la carpeta lista.

## Minuto a minuto

| Tiempo | Fase | Qué pasa | Conduce | Cada participante |
|---|---|---|---|---|
| 0:00–0:12 | **Apertura** | "Así se ve terminado" | Demo del sitio: flujo animado → caso completo → **auditor de citas** (mostrar una cita verificada y explicar la marca p.N) → hallazgos. Pregunta detonadora: *"¿Le creerían a este resultado? ¿Por qué?"* | Abre el sitio en su equipo y sigue la demo |
| 0:12–0:20 | **0 · Corpus** | De dónde salen los datos | Contar la historia del muro anti-bots (bitácora D1). Mostrar el manifiesto con hashes. | Abre `ejercicio/muestra-20/`, confirma su variable y lee su ficha |
| 0:20–0:40 | **1 · Codebook** (Chat) | Mejorar la definición de la variable | Mostrar los prompts sugeridos (abajo). | Crea un Proyecto en Claude, sube el codebook del caso y 3 resúmenes, y refina su variable. **A los 0:38 congela su v1.0** |
| 0:40–0:55 | **2 · Prompt** (Workbench) | Probar antes de escalar | Demo de 3 min: variables, Haiku contra Sonnet, costo por documento, *Get code*. | Prueba el prompt de su variable con 2 documentos (que **no** sean de los 6 `a_mano`) y 2 modelos; anota tokens |
| 0:55–1:05 | *Pausa* | | | |
| 1:05–1:20 | **3 · Skill** | Empaquetar | Mostrar `skills/plantilla-codificador/` y lo que hay que editar (nombre, descripción, codebook, lista de variables). Cómo se sube el ZIP. | Adapta la plantilla, la comprime y la sube. Si se atora, usa `codificador-scjn` tal cual (ver plan B) |
| 1:20–1:45 | **4 · Escalar** (Cowork) + **codificación a ciegas** | Claude codifica 20; tú codificas 6 | Recordar: primero 3 documentos y revisar, luego el resto. **Mientras Cowork trabaja, cada quien codifica a mano sus 6 documentos `a_mano`** sin mirar lo que hace Claude. | Lanza Cowork. Mientras corre, llena `hoja-codificacion-humana.csv` (unos 4 min por documento: síntesis + Ctrl+F) |
| 1:45–2:00 | **5 · Validar** | Kappa y desacuerdos | Abrir el **simulador de kappa** 2 min: la paradoja de la prevalencia, y por qué con n = 6 el kappa salta tanto. | Cowork calcula el kappa contra su hoja. Revisa cada desacuerdo: ¿falló Claude, falló la persona o el codebook es ambiguo? |
| 2:00–2:18 | **6 · Comunicar** | Nota + puesta en común | Proyectar la hoja compartida **agrupada por variable**: ¿quienes eligieron la misma variable la definieron igual? ¿Obtuvieron el mismo kappa? Pedir 4 o 5 voluntarios (1.5 min cada uno). | Pide a Claude su nota de una página y llena su fila |
| 2:18–2:30 | **7 · Puente** | Hacia la sesión 5 | Agrupar las fricciones (copiar y pegar, repetir a mano, no poder re-ejecutar, archivos sueltos, escalar a miles). Cerrar con: *"Todo esto, versionado y re-ejecutable con un comando: eso es Claude Code."* Mostrar 60 s `scripts/` y la carpeta `corridas/` del caso. | — |

**Quien circula**: en las fases 1–4 recorre los equipos; las dudas más comunes son el ZIP del skill, los permisos de carpeta en Cowork y el encabezado del CSV humano. Junta en una nota las fricciones que oiga para la fase 7.

## Prompts sugeridos para la fase 1 (Chat)

1. *"Adjunto el codebook de un proyecto y 3 resúmenes de sentencias. Voy a agregar la variable [VARIABLE] con esta definición inicial: [PEGAR]. Lee los 3 resúmenes y dime, con citas, en cuáles sería difícil aplicar mi definición y por qué."*
2. *"Ponte en el papel de un codificador escéptico. Encuentra 3 ambigüedades en mi definición y propón una regla de decisión para cada una."*
3. *"Reescribe la variable en el formato del codebook adjunto (tabla de códigos, regla de decisión, caso frontera). Mantén máximo 5 códigos."*

## Prompt sugerido para Cowork (fase 4)

> *"Usa el skill [nombre] para codificar los archivos .txt de la carpeta ejercicio/muestra-20. Empieza con 3 documentos que no estén marcados a_mano = si en muestra.csv y muéstrame el resultado antes de seguir. Después codifica el resto sin mostrarme los resultados de los 6 documentos a_mano. Al terminar, verifica las citas, corrige las que no se encuentren y dame la distribución por tipo de control."*

Después de llenar la hoja:

> *"Esta es mi codificación a ciegas de 6 documentos (hoja-codificacion-humana.csv). Calcula el kappa contra tu codificación con el script del skill y explícame los desacuerdos uno por uno."*

## Plan B

| Problema | Alternativa |
|---|---|
| Cowork no disponible o lento | Chat con un Proyecto: subir 5 resúmenes y pedir la codificación en una tabla; luego verificar 5 citas a mano con Ctrl+F |
| El skill no se activa | Pegar el contenido de `SKILL.md` como primer mensaje y pedir que lo siga |
| Límite de uso de Pro | Reducir a 10 documentos (incluidos los 6 `a_mano`) |
| Sin créditos en Workbench | Hacer la fase 2 en Chat comparando 2 versiones del prompt (sin medir tokens) |
| Alguien va muy atrasado | Saltar la fase 3 y usar `codificador-scjn` con la instrucción "agrega mi variable" |
| No le alcanza el tiempo para los 6 documentos a mano | Codificar 3 y declararlo; terminar los otros 3 después de la sesión |

## Mensajes clave (si sólo recuerdan tres cosas)

1. **Una cita verificable vale más que un código.** Sin evidencia rastreable, no hay resultado.
2. **Valida antes de escalar.** Las reglas se fijan antes de ver los datos, y codificas a mano *antes* de ver a Claude.
3. **El acceso a los datos y el codebook son decisiones metodológicas**, no trámites. Escríbelas.
