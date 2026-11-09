# Protocolo de auditoría · ¿Cómo sabemos que podemos confiar en el resultado?

Un análisis asistido por LLM es tan confiable como su **rastro de evidencia**. Este protocolo define cinco controles. Cada uno responde a un riesgo concreto y deja un artefacto que cualquier persona puede revisar.

| # | Control | Riesgo que atiende | Cómo se hace sin código | Cómo se hace con código | Artefacto |
|---|---|---|---|---|---|
| 1 | **Procedencia** | Que el documento no sea el original o haya cambiado | Abrir la URL oficial del manifiesto y comparar | `verificar_hashes.py` | `corpus/manifiesto_emblematicas.csv` |
| 2 | **Citas verificables** | Que el modelo invente o parafrasee la evidencia | Ctrl+F de la cita en el documento (muestra de 10) | `verificar_citas.py` (todas) | `auditoria_citas.csv` |
| 3 | **Validación humana** | Que el modelo aplique mal el codebook de forma sistemática | Codificación humana a ciegas de una submuestra + kappa en Cowork | `calcular_acuerdo.py` | `05-validacion/confiabilidad.csv` |
| 4 | **Versionado** | No poder reproducir o explicar un resultado | Número de versión en codebook, prompt y skill; fecha y modelo en cada corrida | Lo registra `codificar_api.py` en cada línea | `04-resultados/corridas/*.jsonl` |
| 5 | **Bitácora de decisiones** | Decisiones metodológicas invisibles | Escribir qué se cambió, por qué y con qué evidencia | — | `bitacora-decisiones.md` |

## Umbrales de aceptación (los fijamos **antes** de ver resultados)

- **Citas**: al menos 95% verificadas tras la corrección. Toda cita no encontrada se revisa a mano.
- **Kappa humano–Claude**: al menos 0.61 (sustancial) para reportar la variable. Entre 0.41 y 0.60 se reporta con advertencia. Por debajo de 0.41 se revisa el codebook y la variable no se reporta.
- **Confianza baja**: si más del 20% de los documentos de una variable tienen confianza baja, el codebook de esa variable es ambiguo.
- **Métricas complementarias** (se reportan, pero **no deciden**): IC 95% del kappa, α de Krippendorff, AC1 de Gwet y, contra la referencia humana, precisión, exhaustividad y F1 por código (`calcular_acuerdo.py --detalle`). El criterio de decisión es solo el kappa, porque así se fijó. Ejemplo de por qué importa: `proporcionalidad` tiene κ = 0.40 y α = 0.42; si después de ver los datos se aplicara a α el corte de 0.41, entraría con advertencia (con los umbrales propios de α, 0.667, no pasaría). Estas métricas son **referenciales**: se profundizan en la sesión 5 (evaluaciones, Claude Code y Claude Science). Definiciones en [Conceptos](https://benjov.github.io/kit-ia-cide/conceptos.html#metricas).

> **¿Por qué fijarlos antes?** Por la misma razón que se registran las hipótesis antes de ver los datos: para no ajustar el criterio al resultado que nos gusta.

## Validación humana: procedimiento

1. **Muestra**: al menos 20 documentos, estratificados por tipo de control (abstracto o concreto). Es el mínimo didáctico del caso; para un trabajo publicable, 50 o más y un segundo codificador que no haya escrito el codebook (ver `ejercicio/README.md`). En el caso completo: [`../caso-completo/05-validacion/`](../caso-completo/05-validacion/).
2. **A ciegas**: quien codifica no ve los códigos de Claude.
3. **Mismo codebook y misma versión** que usó Claude.
4. **Desacuerdos**: para cada uno se decide si falló Claude, falló el humano o el codebook es ambiguo. Si el codebook es ambiguo, se agrega un caso frontera, sube la versión y se registra en la bitácora.
5. **No se re-codifica la muestra de validación con el codebook nuevo sin validar otra vez**: eso sería sobreajustar.

## Qué **no** garantiza este protocolo

- Que el corpus sea representativo: las sentencias emblemáticas son una **selección** de la SCJN.
- Que el resumen refleje fielmente la sentencia: el resumen es una fuente **secundaria** elaborada por la DGDH. El control 2 verifica contra el resumen y la marca `p.N` permite llegar a la sentencia.
- Que un kappa alto implique validez: dos codificadores pueden coincidir en el error si comparten un codebook mal planteado.
