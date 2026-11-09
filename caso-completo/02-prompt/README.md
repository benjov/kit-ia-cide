# Fase 2 · Prototipo del prompt en un Proyecto de prueba

**Objetivo**: convertir el codebook en un prompt que produzca JSON válido y verificable, compararlo entre modelos y estimar el costo **antes** de escalar. Todo en Chat, en claude.ai o en Claude Desktop.

## Paso a paso (unos 15 min en la sesión; los pasos 7 y 8 son para después)

1. Crea un Proyecto nuevo llamado *Prueba del prompt* y **no le subas archivos**: así el modelo solo ve el prompt y el documento.
2. En las **instrucciones del Proyecto**, pega el contenido de [`system-prompt.md`](system-prompt.md). Esas instrucciones hacen el papel del *system prompt*.
3. Sustituye `{{CODEBOOK}}` por el contenido de [`../01-codebook.md`](../01-codebook.md) (o por tu `codebook.md`).
4. Abre un chat en el Proyecto, adjunta `corpus/resumenes/AI-148-2017.txt` y escribe:

   ```
   Codifica el documento adjunto (id AI-148-2017) según el codebook. Responde solo con el JSON del formato de salida.
   ```

5. Elige el modelo en el selector, debajo del cuadro de mensaje. Usa **un chat nuevo por modelo**, para que una respuesta no influya en la otra.
6. Ejecuta con **Haiku 5.5**, luego con **Sonnet 5.5** y luego con **Opus 5.5** (si tu selector no muestra alguno, compara los que tengas). Anota en la hoja de trabajo:
   - ¿Coinciden los códigos?
   - ¿Las citas son literales? Búscalas con Ctrl+F en el documento.
   - ¿El JSON trae los campos `codigo`, `cita` y `confianza` para cada variable?
   - El costo de escalar lo estimas con la [calculadora del sitio](https://benjov.github.io/kit-ia-cide/herramientas/costos.html), que trae los tokens medidos en el caso. El Chat no muestra tokens: decláralo como límite.
7. *Para después de la sesión*: repite el paso 4 con los **3 casos de prueba** de la tabla de abajo, cuyo código correcto ya conocemos, cada vez que cambies el prompt.
8. *Para después*: en el carril B, [`../../scripts/codificar_api.py`](../../scripts/codificar_api.py) usa este mismo prompt, fuerza el JSON con un esquema y registra los tokens de cada documento. Medir y evaluar de forma sistemática es tema de la sesión 5 (evaluaciones, Claude Code y Claude Science).

## Casos de prueba sugeridos

El de `AI-148-2017` lo verificó el equipo docente leyendo la sentencia. Los otros dos vienen de la referencia **SIMULADA** del caso (bitácora D7): sirven para practicar, no como verdad. Úsalos para detectar regresiones cuando cambies el prompt.

| Documento | Variable que pone a prueba | Por qué es difícil |
|---|---|---|
| `AI-148-2017` | `resultado` | Valida un artículo e invalida otros → debe ser `mixto`, no `protege` |
| (ver `../05-validacion/gold-standard-SIMULADO.csv`) | `fuentes_internacionales` | Las partes citan tratados pero la Corte no siempre los cita |
| (ver `../05-validacion/gold-standard-SIMULADO.csv`) | `promovente` | Varios promoventes de distinto tipo |

## Lo que aprendimos al prototipar (bitácora del caso)

Ver [`../../auditoria/bitacora-decisiones.md`](../../auditoria/bitacora-decisiones.md). Ahí se registra cada cambio al prompt, por qué se hizo y qué caso de prueba lo motivó.

## Costo estimado del corpus completo

Haz la estimación en clase: *(tokens por documento) × (103 documentos) × (precio por token)*. El simulador del sitio ([herramientas → costos](../../docs/herramientas/costos.html)) hace la cuenta por ti.
