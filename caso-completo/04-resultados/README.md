# Fase 4 · Resultados de la codificación

| Archivo | Contenido |
|---|---|
| `corridas/*-batch_claude-opus-5-5.jsonl` | Corrida principal: 102 documentos, una línea por documento con código, cita, confianza y nota por variable, más el modelo, la versión, los tokens y el SHA-256 de la fuente |
| `corridas/*-batch_claude-sonnet-5-5.jsonl` · `*-batch_claude-haiku-5-5.jsonl` | Mismo corpus y mismo prompt, otros modelos (para comparar). Haiku: 99 documentos (3 respuestas truncadas, bitácora D11) |
| `corridas/20261106-2039_claude-opus-5-5.jsonl` | Prueba previa con 3 documentos (tarifa normal) |
| `corridas/lotes.json` | IDs de los lotes de la Batch API, fechas y costos |
| `resultados_opus.csv` | Corrida principal en formato plano (abre en Excel), con la marca `p.N` de la sentencia por cita |
| `hallazgos.csv` | Tablas abstracto contra concreto con prueba exacta de Fisher |

**En la sesión** harás esta fase con **Cowork** y el skill, sobre 20 documentos. El resultado es un CSV con las mismas columnas.

Regenerar todo: `python scripts/analizar_resultados.py`
