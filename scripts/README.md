# Scripts · Verificar y reproducir el kit (carril B)

Nada de esto es necesario para la sesión. Existe para que **cualquiera pueda auditar el kit**: de dónde salió el corpus, si las citas existen, si los kappa y las pruebas de Fisher del caso se reproducen.

Hay dos maneras de ejecutarlos. Ambas corren el mismo código y dan el mismo resultado:

- **Sin programar**: abre **Cowork** (Claude Desktop), dale acceso a la carpeta del kit y pega el prompt de la tabla. Claude ejecuta el script en su entorno y te explica la salida. No instalas nada.
- **Con terminal**: Python 3.10 o superior. Los scripts de verificación solo usan la biblioteca estándar. Para la API: `pip install -r requirements.txt`.

> **Regla para quien lo pida a Cowork**: pide siempre que te muestre la salida literal del script además de su explicación. Así distingues lo que dice el programa de lo que interpreta Claude.

## 1. Verificaciones (gratis, sin API)

| Qué verificas | Prompt para Cowork | Comando | Lo que debes ver |
|---|---|---|---|
| **Procedencia**: los PDF del kit son idénticos a los que publica la SCJN hoy | *"Ejecuta scripts/verificar_hashes.py --muestra 3 y muéstrame la salida literal. Explícame qué significa que el SHA-256 coincida."* | `python scripts/verificar_hashes.py --muestra 3` | `Coinciden: 6 · No coinciden: 0` (3 resúmenes y 3 sentencias) |
| Lo mismo, sin internet en el entorno | Descarga tú un PDF desde la URL del manifiesto con el navegador y guárdalo en `mi-trabajo/`. *"Ejecuta scripts/verificar_hashes.py --pdf mi-trabajo/<archivo>.pdf y muéstrame la salida."* | `python scripts/verificar_hashes.py --pdf <archivo>.pdf` | `✓ … idéntico al resumen de <ID> registrado en el manifiesto` |
| **Generación del corpus**: el script de descarga funciona y produce el mismo texto | *"Ejecuta scripts/descargar_corpus.py --muestra 3 --destino mi-trabajo/corpus-prueba y muéstrame la salida literal, sobre todo la comparación con el kit. No toques la carpeta corpus/."* | `python scripts/descargar_corpus.py --muestra 3 --destino mi-trabajo/corpus-prueba` | Recorre unas 21 páginas del índice (102 fichas) y al final dice `PDF idénticos (SHA-256): 6 · distintos: 0` y `Textos idénticos: 6`. Tarda menos de un minuto. Si el entorno no tiene `pdftotext` y usa `pypdf`, los textos salen distintos aunque los PDF sean idénticos: el script lo explica (la diferencia viene del extractor, no de la fuente) |
| **Citas** (control 2): cada cita de Opus existe literalmente en su documento | *"Ejecuta scripts/verificar_citas.py con la corrida batch de Opus en caso-completo/04-resultados/corridas/ y muéstrame la salida literal."* | `python scripts/verificar_citas.py caso-completo/04-resultados/corridas/20261106-batch_claude-opus-5-5.jsonl` | `Citas verificadas: 431/431 (100.0%)`. Con Sonnet, 418/421: las 3 fallas están explicadas en la bitácora D10 |
| **Kappa y métricas** del caso contra la referencia SIMULADA | *"Ejecuta scripts/calcular_acuerdo.py con caso-completo/05-validacion/gold-standard-SIMULADO.csv y la corrida batch de Opus, con --desacuerdos --detalle. Muéstrame la tabla y explícame los desacuerdos y la matriz de confusión de proporcionalidad."* | `python scripts/calcular_acuerdo.py caso-completo/05-validacion/gold-standard-SIMULADO.csv caso-completo/04-resultados/corridas/20261106-batch_claude-opus-5-5.jsonl --desacuerdos --detalle` | proporcionalidad κ = 0.40, IC 95% [−0.04, 0.79], α = 0.42, AC1 = 0.40, F1 macro 0.70; resultado κ = 0.75; derecho_principal κ = 0.65 (igual que `05-validacion/confiabilidad-opus.csv`) |
| **Reproducibilidad completa**: de las corridas crudas a todas las tablas, el memo y el sitio | *"Ejecuta scripts/analizar_resultados.py --salida mi-trabajo/reproduccion y muéstrame la salida literal, sobre todo la comparación final con el kit."* | `python scripts/analizar_resultados.py --salida mi-trabajo/reproduccion` | `Archivos idénticos: 108 · distintos: 0` y `✓ El caso se reproduce exactamente.` |

Si Cowork responde que no tiene acceso a internet para `scjn.gob.mx`, es una restricción de su entorno, no un error del kit: usa la fila "sin internet". En Claude Desktop con inferencia de terceros (modo desarrollador con tu API key), la máquina virtual de Cowork no tiene red salvo los hosts que pongas en *Allowed egress hosts* (`www.scjn.gob.mx`; para la sección 2, `api.anthropic.com`), y cada verificación consume tokens de tu cuenta ([guía → Si usas tu API key](https://benjov.github.io/kit-ia-cide/guia.html#modo-api)). Las verificaciones de citas, kappa y reproducibilidad no necesitan red.

## 2. Volver a codificar con la API (gasta créditos)

Necesitas una API key de Claude Console (`platform.claude.com` → API keys). Copia `.env.ejemplo` como `.env` en la raíz del kit y pon ahí tu key **tú mismo**, con TextEdit o el Bloc de notas. Nunca la pegues en un chat. Conviene crear una key solo para esto, con límite de gasto, y borrarla al terminar.

| Qué haces | Prompt para Cowork | Comando | Costo aproximado |
|---|---|---|---|
| Codificar 1 documento con Haiku, sin tocar las corridas del caso | *"Ejecuta scripts/codificar_api.py --modelo claude-haiku-5-5 --limite 1 --salida mi-trabajo/api. No muestres el contenido de .env. Después verifica las citas del archivo generado con scripts/verificar_citas.py."* | `python scripts/codificar_api.py --modelo claude-haiku-5-5 --limite 1 --salida mi-trabajo/api` | Menos de US$0.01 (unos 19,000 tokens de entrada y 1,750 de salida) |
| Lo mismo con Opus | igual, con `--modelo claude-opus-5-5` | | Unos US$0.11 por documento |
| El corpus completo con la Batch API (50% menos) | Mejor en terminal: es asíncrono y se recoge después | `python scripts/codificar_batch.py enviar --modelos claude-haiku-5-5` y luego `python scripts/codificar_batch.py recoger` | Ver la [calculadora de costos](https://benjov.github.io/kit-ia-cide/herramientas/costos.html) y `corridas/lotes.json` (el caso costó US$6.07 con 3 modelos) |

Los precios están en `codificar_api.py`; verifícalos en la página oficial antes de citarlos. Si Cowork no tiene salida a `api.anthropic.com`, esta sección solo funciona desde una terminal.

**Por qué tu corrida no será idéntica a la del caso**: un LLM no es determinista y los modelos se actualizan. Lo reproducible no es la salida exacta sino el **procedimiento** (codebook, prompt y modelo versionados) más las **salidas archivadas** (`corridas/*.jsonl`), que son las que se auditan. Ver [Conceptos → reproducibilidad](https://benjov.github.io/kit-ia-cide/conceptos.html#reproducibilidad).

## 3. Referencia de cada script

| Script | Hace | Opciones útiles | Dependencias |
|---|---|---|---|
| `descargar_corpus.py` | Recorre el índice público de sentencias emblemáticas, baja los PDF, extrae el texto y escribe el manifiesto | `--muestra N`, `--ids`, `--destino`, `--sin-sentencias`, `--solo-ai` | stdlib + `pdftotext` o `pypdf` |
| `verificar_hashes.py` | Compara el SHA-256 de cada PDF con el manifiesto | `--muestra N`, `--ids`, `--pdf archivo`, `--local` | stdlib |
| `codificar_api.py` | Codifica vía API, un documento a la vez; registra modelo, versiones, tokens y SHA-256 de la fuente | `--modelo`, `--limite`, `--ids`, `--salida` | `anthropic` |
| `codificar_batch.py` | Igual, con la Batch API (asíncrona, −50%) | `enviar --modelos …`, `recoger` | `anthropic` |
| `verificar_citas.py` | Control 2: ¿cada cita existe literalmente? Detecta solo las variables | `--corpus`, `--csv`, `--ausencia` | stdlib |
| `calcular_acuerdo.py` | Por variable: % de acuerdo, kappa de Cohen con IC 95% (bootstrap), α de Krippendorff, AC1 de Gwet y desacuerdos; con `--detalle`, matriz de confusión, precisión, exhaustividad y F1 por código y acuerdo por nivel de confianza. Detecta solo las variables | `--desacuerdos`, `--detalle`, `--csv`, `--renombrar` | stdlib |
| `simular_codificacion_humana.py` | Genera la referencia "humana" **SIMULADA** del caso (didáctica, bitácora D7) | — | stdlib |
| `analizar_resultados.py` | Tablas, Fisher, acuerdo entre modelos y datos del sitio | `--salida` (no toca el kit y compara) | stdlib |

Todos tienen `--help` con su explicación en español.

**Límite ético** (bitácora D1): los scripts solo usan la colección pública de sentencias emblemáticas, esperan 1 s entre solicitudes y se identifican. Si un sitio responde con protección anti-bots, se detienen. No se intenta evadirla, tampoco "desde el navegador".
