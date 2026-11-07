# Kit IA-CIDE · Sesión 4: "Del codebook al hallazgo"

**Análisis de contenido asistido por IA, de punta a punta y verificable**, con 102 sentencias de la Suprema Corte de Justicia de la Nación.

🌐 **Sitio de la sesión**: https://benjov.github.io/kit-ia-cide/ (caso completo, auditor de citas, simulador de kappa, calculadora de costos)

## ¿Por dónde empiezo?

| Si eres… | Empieza en |
|---|---|
| Participante de la sesión | [`docs/guia.html`](https://benjov.github.io/kit-ia-cide/guia.html) y las variables de [`ejercicio/README.md`](ejercicio/README.md) |
| Quieres ver el caso terminado | [`caso-completo/`](caso-completo/) o [en el sitio](https://benjov.github.io/kit-ia-cide/caso.html) |
| Quieres usarlo con tu corpus | [`plantilla-tu-corpus/README.md`](plantilla-tu-corpus/README.md) |
| Facilitas la sesión | [`facilitador/guion.md`](facilitador/guion.md) |
| Co-docente que va a revisar o adaptar el kit | [`facilitador/para-co-docente.md`](facilitador/para-co-docente.md) |

## La pregunta del caso

Cuando la SCJN protege derechos humanos, **¿argumenta distinto en control abstracto (acción de inconstitucionalidad) que en control concreto (amparo)?** Seis variables, tres modelos de Claude, validación contra una codificación de referencia y cada código respaldado por una cita verificable.

## El flujo

```
Pregunta y corpus → Codebook (Chat) → Prompt (Workbench) → Skill → Escalar (Cowork / API Batch) → Validar (kappa) → Memo
```

## Contenido

| Carpeta | Qué hay |
|---|---|
| `corpus/` | 102 resúmenes y sentencias en texto + `manifiesto_emblematicas.csv` (URL oficial, fecha, SHA-256) |
| `ejercicio/` | Actividad individual: 10 variables para elegir, muestra de 20 documentos y hoja para codificar 6 a mano |
| `skills/` | `codificador-scjn` (listo para instalar) y `plantilla-codificador` (para adaptar) |
| `caso-completo/` | El caso resuelto, fase por fase: codebook, prompt, resultados de 3 modelos, validación, memo |
| `auditoria/` | Protocolo de 5 controles y bitácora de decisiones |
| `scripts/` | **Opcional** (Python): descarga, verificación de hashes y citas, kappa, codificación por API y Batch |
| `docs/` | Sitio web (GitHub Pages) |
| `facilitador/` | Guion minuto a minuto, checklist, plan B y guía para la co-docente |

## Fuente y licencia del corpus

Los documentos son públicos y provienen de la colección **Sentencias emblemáticas** de la Dirección General de Derechos Humanos de la SCJN (https://www.scjn.gob.mx/derechos-humanos/). Se redistribuyen en texto plano con fines docentes, con su URL de origen y su huella SHA-256 para verificar integridad. Los PDF originales no se incluyen: `scripts/descargar_corpus.py` los vuelve a descargar.

Los resultados de codificación son **ilustrativos** (material docente) y no constituyen análisis jurídico.
