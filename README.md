# Kit IA-CIDE · Sesión 4: "Del codebook al hallazgo"

**Análisis de contenido asistido por IA, de punta a punta y verificable**, con 102 sentencias de la Suprema Corte de Justicia de la Nación.

🌐 **Sitio de la sesión**: https://benjov.github.io/kit-ia-cide/ (caso completo, auditor de citas, simulador de kappa, calculadora de costos)

## ¿Por dónde empiezo?

| Si eres… | Empieza en |
|---|---|
| Participante de la sesión | [`docs/guia.html`](https://benjov.github.io/kit-ia-cide/guia.html) y las variables de [`ejercicio/README.md`](ejercicio/README.md) |
| Quieres entender los fundamentos (codebook, kappa, codificación humana, reproducibilidad) | [Conceptos y fundamentos](https://benjov.github.io/kit-ia-cide/conceptos.html), con referencias |
| Quieres verificar o reproducir el kit tú mismo | [`scripts/README.md`](scripts/README.md): prompts para que Cowork ejecute cada script, o comandos para terminal |
| Quieres ver el caso terminado | [`caso-completo/`](caso-completo/) o [en el sitio](https://benjov.github.io/kit-ia-cide/caso.html) |
| Quieres usarlo con tu corpus | [`plantilla-tu-corpus/README.md`](plantilla-tu-corpus/README.md) |
| Facilitas la sesión | [`facilitador/guion.md`](facilitador/guion.md) |
| Co-docente que va a revisar o adaptar el kit | [`facilitador/para-co-docente.md`](facilitador/para-co-docente.md) |

## Sin programar

**Toda la sesión se hace desde las aplicaciones de Claude.** No necesitas terminal, Python ni git.

| Herramienta | Dónde | Para qué fase |
|---|---|---|
| Chat con Proyecto | claude.ai o Claude Desktop | 1 · Codebook, 2 · Prompt (en un Proyecto de prueba, comparando modelos con el selector), 6 · Nota |
| Skills | Configuración → Capacidades → Skills (claude.ai o Desktop) | 3 · Skill |
| Cowork | **Solo Claude Desktop** | 3 · Armar el skill, 4 · Codificar, 5 · Validar |

Los scripts de verificación de citas y de kappa vienen dentro del skill y **los ejecuta Claude en Cowork**; detectan solos tu variable.

**¿Usas Claude Desktop en modo desarrollador con tu API key (inferencia de terceros)?** Todo el ejercicio funciona, haciendo cada fase en Cowork y sin instalar el skill: ver [guía → Si usas tu API key](https://benjov.github.io/kit-ia-cide/guia.html#modo-api).

La carpeta `scripts/` tiene todo lo demás: la descarga del corpus desde la SCJN, la verificación de hashes, la recodificación por API y la reproducción del caso completo. **Cualquiera puede pedirle a Cowork que los ejecute** para comprobar que funcionan y que el caso se reproduce (108 de 108 archivos idénticos). Quien prefiera la terminal tiene los comandos. Ver [`scripts/README.md`](scripts/README.md).

## La pregunta del caso

Cuando la SCJN protege derechos humanos, **¿argumenta distinto en control abstracto (acción de inconstitucionalidad) que en control concreto (amparo)?** Seis variables, tres modelos de Claude, validación contra una codificación de referencia y cada código respaldado por una cita verificable.

## El flujo

```
Pregunta y corpus → Codebook (Chat) → Prompt (Chat, Proyecto de prueba) → Skill → Escalar (Cowork) → Validar (kappa, en Cowork) → Memo (Chat)
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
