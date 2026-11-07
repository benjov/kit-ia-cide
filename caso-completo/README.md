# Caso completo · ¿Argumenta distinto la SCJN en control abstracto y en control concreto?

El caso resuelto de punta a punta, para ver cómo se ve terminado antes de hacer el propio. **Versión navegable con gráficas**: [sitio → Caso completo](https://benjov.github.io/kit-ia-cide/caso.html).

| Fase | Archivo | Herramienta |
|---|---|---|
| 0 · Pregunta y corpus | este README + [`../corpus/manifiesto_emblematicas.csv`](../corpus/manifiesto_emblematicas.csv) | — |
| 1 · Codebook | [`01-codebook.md`](01-codebook.md) | Chat (Proyecto) |
| 2 · Prompt | [`02-prompt/`](02-prompt/) | Console Workbench |
| 3 · Skill | [`../skills/codificador-scjn/`](../skills/codificador-scjn/) | Skills |
| 4 · Escalar | [`04-resultados/`](04-resultados/) | API Batch (en la sesión: Cowork) |
| 5 · Validar | [`05-validacion/`](05-validacion/) | Scripts / Cowork |
| 6 · Comunicar | [`06-memo-metodologico.md`](06-memo-metodologico.md) | Chat |

## Fase 0 · Pregunta y corpus

**Pregunta**: cuando la Suprema Corte protege derechos humanos, ¿cambia su forma de argumentar según la vía procesal: control **abstracto** (acción de inconstitucionalidad) o control **concreto** (amparo)?

**Corpus**: las 102 sentencias de la colección *Sentencias emblemáticas* de la Dirección General de Derechos Humanos de la SCJN (9 AI, 86 amparos, 7 de otras vías). **Unidad de análisis**: el resumen oficial de cada sentencia.

**Cómo llegamos a esta pregunta** (y no a la original): ver [bitácora D1](../auditoria/bitacora-decisiones.md).

## Reproducir el caso (carril B, opcional)

```bash
pip install -r requirements.txt
python scripts/codificar_batch.py enviar --modelos claude-opus-5-5 claude-sonnet-5-5 claude-haiku-5-5
python scripts/codificar_batch.py recoger
python scripts/simular_codificacion_humana.py caso-completo/04-resultados/corridas/<fecha>-batch_claude-opus-5-5.jsonl
python scripts/analizar_resultados.py
```

> ⚠️ La referencia humana de este caso es **simulada** con fines didácticos ([bitácora D7](../auditoria/bitacora-decisiones.md)). En tu proyecto, debe ser real.
