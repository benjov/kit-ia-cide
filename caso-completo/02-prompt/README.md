# Fase 2 · Prototipo del prompt en Console Workbench

**Objetivo**: convertir el codebook en un prompt que produzca JSON válido y verificable, compararlo entre modelos y estimar el costo **antes** de escalar.

## Paso a paso (unos 25 min en la sesión)

1. Entra a **Claude Console → Workbench**.
2. En **System prompt**, pega el contenido de [`system-prompt.md`](system-prompt.md).
3. Sustituye `{{CODEBOOK}}` por el contenido de [`../01-codebook.md`](../01-codebook.md), o déjalo como variable y pégalo en el panel de variables.
4. En el mensaje del usuario, escribe:

   ```
   <documento id="{{ID}}">
   {{DOCUMENTO}}
   </documento>

   Codifica este documento según el codebook. Responde solo con el JSON del formato de salida.
   ```

5. En **Variables**, pega el texto de `corpus/resumenes/AI-148-2017.txt` en `DOCUMENTO` y escribe `AI-148-2017` en `ID`.
6. Ejecuta con **Haiku 5.5**, luego con **Sonnet 5.5** y luego con **Opus 5.5**. Anota en la hoja de trabajo:
   - ¿Coinciden los códigos?
   - ¿Las citas son literales? Búscalas con Ctrl+F en el documento.
   - Tokens de entrada y de salida, y el costo que muestra Workbench.
7. Agrega **3 casos de prueba** (en Workbench, "Evaluate" o "Test cases") con los documentos de la tabla de abajo, cuyo código correcto ya conocemos. Ejecuta la evaluación.
8. Cuando el prompt pase los casos, haz clic en **Get code**. No necesitas usar ese código hoy: es la llave para escalar en la sesión 5.

## Casos de prueba sugeridos (gold standard)

Codificados a mano por el equipo docente. Úsalos para detectar regresiones cuando cambies el prompt.

| Documento | Variable que pone a prueba | Por qué es difícil |
|---|---|---|
| `AI-148-2017` | `resultado` | Valida un artículo e invalida otros → debe ser `mixto`, no `protege` |
| (ver `../05-validacion/gold-standard.csv`) | `fuentes_internacionales` | Las partes citan tratados pero la Corte no siempre los cita |
| (ver `../05-validacion/gold-standard.csv`) | `promovente` | Varios promoventes de distinto tipo |

## Lo que aprendimos al prototipar (bitácora del caso)

Ver [`../../auditoria/bitacora-decisiones.md`](../../auditoria/bitacora-decisiones.md). Ahí se registra cada cambio al prompt, por qué se hizo y qué caso de prueba lo motivó.

## Costo estimado del corpus completo

Haz la estimación en clase: *(tokens por documento) × (103 documentos) × (precio por token)*. El simulador del sitio ([herramientas → costos](../../docs/herramientas/costos.html)) hace la cuenta por ti.
