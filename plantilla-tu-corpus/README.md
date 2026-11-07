# Replica el flujo con tu propio corpus

El caso de la SCJN es un ejemplo. El flujo funciona igual con discursos legislativos, entrevistas, notas de prensa, respuestas abiertas de encuestas, iniciativas de ley, informes, tuits o expedientes.

## Checklist en 8 pasos

| # | Paso | Herramienta | Listo cuando… |
|---|---|---|---|
| 1 | **Pregunta** que se responda con variables observables en el texto | — | Puedes escribir qué resultado contradiría tu hipótesis |
| 2 | **Corpus** en `.txt` (o `.pdf` y `.docx`), un archivo por documento, con un **manifiesto** (id, fuente, URL o referencia, fecha) | Cowork puede ayudarte a convertir y renombrar | Cada documento tiene ID y procedencia |
| 3 | **Codebook** v0.1 → v1.0 con [`../skills/plantilla-codificador/referencias/plantilla-codebook.md`](../skills/plantilla-codificador/referencias/plantilla-codebook.md) | Chat (Proyecto) | 3–6 variables, cada una con regla de decisión y un caso frontera |
| 4 | **Prompt** probado en 3–5 documentos y 2 modelos | Workbench | Los códigos coinciden con tu juicio y las citas son literales |
| 5 | **Skill** a partir de [`../skills/plantilla-codificador/`](../skills/plantilla-codificador/) | Desktop → Skills | Claude lo activa solo cuando le pides codificar |
| 6 | **Muestra de validación** (≥ 20 documentos, estratificada) codificada a ciegas por ti o por un asistente | Hoja de cálculo | La tienes **antes** de ver los resultados de Claude |
| 7 | **Codificación completa** + verificación de citas + kappa | Cowork (o API Batch si son cientos o miles) | ≥ 95% de citas verificadas y kappa ≥ 0.61 en cada variable que reportes |
| 8 | **Memo metodológico** con la [plantilla del caso](../caso-completo/06-memo-metodologico.md) | Chat | Alguien externo podría auditar tu resultado con el memo y la carpeta |

## Preguntas frecuentes

**¿Cuántos documentos puedo codificar con Pro en Cowork?** Depende de la extensión de los documentos. Como referencia, el caso usa resúmenes de unas 4,000 palabras. Con documentos así, decenas por sesión es razonable. Para cientos o miles, usa la API (Batch) o espera a la sesión 5 (Claude Code).

**¿Y si mis documentos tienen datos personales?** No los subas sin revisar los términos de tu institución, tu protocolo de ética y la configuración de privacidad de tu cuenta. Anonimiza primero. El corpus de este kit es público a propósito.

**¿Puedo publicar resultados codificados con IA?** Cada vez más revistas lo aceptan **si reportas el procedimiento**: modelo, versión, prompt y codebook, validación humana y kappa. El memo metodológico del caso es una buena base para la sección de métodos.

**¿Y si el kappa sale bajo?** Es información, no un fracaso: casi siempre indica que el codebook es ambiguo. Revisa los desacuerdos, agrega reglas de decisión, sube la versión y valida con una muestra **nueva**.
