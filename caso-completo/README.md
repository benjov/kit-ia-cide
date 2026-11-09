# Caso completo · ¿Argumenta distinto la SCJN en control abstracto y en control concreto?

El caso resuelto de punta a punta, para ver cómo se ve terminado antes de hacer el propio. **Versión navegable con gráficas**: [sitio → Caso completo](https://benjov.github.io/kit-ia-cide/caso.html).

| Fase | Archivo | Cómo se hizo en el caso | Cómo lo haces tú en la sesión (sin código) |
|---|---|---|---|
| 0 · Pregunta y corpus | este README + [`../corpus/manifiesto_emblematicas.csv`](../corpus/manifiesto_emblematicas.csv) | Script de descarga (`descargar_corpus.py`) | Ya está hecho: usas `ejercicio/muestra-20/`. Si quieres comprobarlo, pídele a Cowork que ejecute el script en modo de prueba ([`scripts/README.md`](../scripts/README.md)) |
| 1 · Codebook | [`01-codebook.md`](01-codebook.md) | Chat con Proyecto | Chat con Proyecto (claude.ai o Desktop) |
| 2 · Prompt | [`02-prompt/`](02-prompt/) | Proyecto de prueba en Chat; tokens medidos después con la API (carril B) | Chat con un Proyecto de prueba y el selector de modelo (claude.ai o Desktop) |
| 3 · Skill | [`../skills/codificador-scjn/`](../skills/codificador-scjn/) | Skills | Cowork arma el .zip; lo subes en Configuración → Capacidades → Skills |
| 4 · Escalar | [`04-resultados/`](04-resultados/) | API Batch: 102 documentos × 3 modelos (carril B) | Cowork con tu skill, 20 documentos (solo Desktop) |
| 5 · Validar | [`05-validacion/`](05-validacion/) | Scripts (carril B) | Cowork: Claude ejecuta los mismos scripts dentro del skill |
| 6 · Comunicar | [`06-memo-metodologico.md`](06-memo-metodologico.md) | Chat | Chat o Cowork |

La Batch API se usó porque el caso compara 3 modelos sobre 102 documentos. Para la escala de la sesión, Cowork basta.

## Fase 0 · Pregunta y corpus

**Pregunta**: cuando la Suprema Corte protege derechos humanos, ¿cambia su forma de argumentar según la vía procesal: control **abstracto** (acción de inconstitucionalidad) o control **concreto** (amparo)?

**Corpus**: las 102 sentencias de la colección *Sentencias emblemáticas* de la Dirección General de Derechos Humanos de la SCJN (9 AI, 86 amparos, 7 de otras vías). **Unidad de análisis**: el resumen oficial de cada sentencia.

**Cómo llegamos a esta pregunta** (y no a la original): ver [bitácora D1](../auditoria/bitacora-decisiones.md).

## Reproducir el caso (carril B, opcional)

Sin terminal: pídele a Cowork *"Ejecuta scripts/analizar_resultados.py --salida mi-trabajo/reproduccion y muéstrame la comparación final con el kit"*. Debe decir `Archivos idénticos: 108 · distintos: 0`. Con terminal, desde cero (gasta créditos de API):

```bash
pip install -r requirements.txt
python scripts/codificar_batch.py enviar --modelos claude-opus-5-5 claude-sonnet-5-5 claude-haiku-5-5
python scripts/codificar_batch.py recoger
python scripts/simular_codificacion_humana.py caso-completo/04-resultados/corridas/<fecha>-batch_claude-opus-5-5.jsonl
python scripts/analizar_resultados.py
```

> ⚠️ La referencia humana de este caso es **simulada** con fines didácticos ([bitácora D7](../auditoria/bitacora-decisiones.md)). En tu proyecto, debe ser real.
