# Fase 5 · Validación

> ⚠️ **La referencia humana de este caso es SIMULADA** con fines didácticos. Se generó con [`scripts/simular_codificacion_humana.py`](../../scripts/simular_codificacion_humana.py): parte de los códigos de Opus e introduce desacuerdos plausibles, con más probabilidad donde Claude declaró baja confianza. Ver [bitácora D7](../../auditoria/bitacora-decisiones.md). En tu proyecto y en el ejercicio de la sesión, la referencia debe ser real y a ciegas.

| Archivo | Contenido |
|---|---|
| `gold-standard-SIMULADO.csv` | Referencia simulada: 20 documentos (9 AI + 11 amparos), 6 variables |
| `confiabilidad.csv` | κ y % de acuerdo de cada modelo contra la referencia, por variable |
| `confiabilidad-opus.csv` | Solo Opus, salida directa de `calcular_acuerdo.py`: % de acuerdo, κ con IC 95%, α de Krippendorff, AC1 de Gwet y F1 macro |

## Cómo se lee

- **Umbrales** (fijados antes de ver los resultados, ver el [protocolo](../../auditoria/protocolo.md)): κ ≥ 0.61 se reporta; de 0.41 a 0.60, con advertencia; < 0.41 no se reporta.
- **Resultado**: `proporcionalidad` (κ = 0.40 con Opus) no se reporta. El análisis de desacuerdos llevó a la regla v1.1 del codebook ([bitácora D8](../../auditoria/bitacora-decisiones.md)).
- **Métricas complementarias** (Opus contra la referencia SIMULADA; no deciden, ver el protocolo):

  | Variable | κ | IC 95% (bootstrap) | α | AC1 | F1 macro |
  |---|---|---|---|---|---|
  | promovente | 1.00 | [1.00, 1.00] | 1.00 | 1.00 | 1.00 |
  | resultado | 0.75 | [0.49, 1.00] | 0.75 | 0.79 | 0.77 |
  | derecho_principal | 0.65 | [0.40, 0.85] | 0.65 | 0.67 | 0.61 |
  | fuentes_internacionales | 0.71 | [0.38, 0.93] | 0.72 | 0.74 | 0.87 |
  | proporcionalidad | 0.40 | [−0.04, 0.79] | 0.42 | 0.40 | 0.70 |
  | perspectiva_genero | 1.00 | [1.00, 1.00] | 1.00 | 1.00 | 1.00 |

  Con N = 20 los intervalos son anchos: el de `proporcionalidad` es compatible con acuerdo nulo y con acuerdo sustancial. La matriz de confusión de `derecho_principal` muestra una confusión concreta: dos sentencias que la referencia codifica como `igualdad_no_discriminacion` van a `otro`. El acuerdo por nivel de confianza en `derecho_principal` (90% en "alta", 0% en "baja") existe aquí **por construcción**, porque la simulación metió más desacuerdos donde Claude declaró confianza baja. Se reproduce con `calcular_acuerdo.py … --detalle`.
- **Acuerdo entre modelos ≠ validación**: que Opus y Sonnet coincidan (κ entre 0.83 y 0.95) solo dice que el resultado no depende mucho del modelo, no que sea correcto.

**En la sesión**, el kappa lo calcula Claude en Cowork con el script del skill; tú no ejecutas nada. Carril B (opcional), recalcular el caso: `python scripts/calcular_acuerdo.py caso-completo/05-validacion/gold-standard-SIMULADO.csv caso-completo/04-resultados/corridas/<opus>.jsonl --desacuerdos --detalle`
