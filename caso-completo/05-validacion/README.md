# Fase 5 · Validación

> ⚠️ **La referencia humana de este caso es SIMULADA** con fines didácticos. Se generó con [`scripts/simular_codificacion_humana.py`](../../scripts/simular_codificacion_humana.py): parte de los códigos de Opus e introduce desacuerdos plausibles, con más probabilidad donde Claude declaró baja confianza. Ver [bitácora D7](../../auditoria/bitacora-decisiones.md). En tu proyecto y en el ejercicio de la sesión, la referencia debe ser real y a ciegas.

| Archivo | Contenido |
|---|---|
| `gold-standard-SIMULADO.csv` | Referencia simulada: 20 documentos (9 AI + 11 amparos), 6 variables |
| `confiabilidad.csv` | κ y % de acuerdo de cada modelo contra la referencia, por variable |
| `confiabilidad-opus.csv` | Igual, solo Opus (salida directa de `calcular_acuerdo.py`) |

## Cómo se lee

- **Umbrales** (fijados antes de ver los resultados, ver el [protocolo](../../auditoria/protocolo.md)): κ ≥ 0.61 se reporta; de 0.41 a 0.60, con advertencia; < 0.41 no se reporta.
- **Resultado**: `proporcionalidad` (κ = 0.40 con Opus) no se reporta. El análisis de desacuerdos llevó a la regla v1.1 del codebook ([bitácora D8](../../auditoria/bitacora-decisiones.md)).
- **Acuerdo entre modelos ≠ validación**: que Opus y Sonnet coincidan (κ entre 0.83 y 0.95) solo dice que el resultado no depende mucho del modelo, no que sea correcto.

Recalcular: `python scripts/calcular_acuerdo.py caso-completo/05-validacion/gold-standard-SIMULADO.csv caso-completo/04-resultados/corridas/<opus>.jsonl --desacuerdos`
