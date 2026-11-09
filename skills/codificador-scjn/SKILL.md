---
name: codificador-scjn
description: Codifica resúmenes de sentencias de la SCJN (México) con un codebook de análisis de contenido y produce un CSV auditable con una cita textual para cada código. Úsalo cuando el usuario pida codificar, clasificar o analizar sentencias, resúmenes de sentencias o documentos jurídicos con el codebook del Kit IA-CIDE, o cuando pida verificar citas o calcular el acuerdo entre codificadores (kappa).
---

# Codificador de sentencias SCJN (Kit IA-CIDE)

Este skill aplica un análisis de contenido reproducible. Trabajas como un codificador humano entrenado: aplicas el codebook, justificas cada código con evidencia literal y reportas tu incertidumbre.

## Antes de empezar

1. Lee `referencias/codebook.md` completo. Es la única fuente de definiciones. Si el usuario trae su propio codebook (por ejemplo, la variable que eligió en el ejercicio), usa el suyo y avisa cuál estás usando.
2. Identifica los documentos que vas a codificar: los archivos `.txt` de la carpeta que indique el usuario (normalmente `corpus/resumenes/`). El **ID** de cada documento es el nombre del archivo sin extensión.
3. Si son más de 15 documentos, codifica primero **3** y muéstrale al usuario los resultados para que los revise antes de seguir. Así se detectan malentendidos del codebook a tiempo.

## Cómo codificar cada documento

Para cada documento y cada variable codificada del codebook:

- Elige **un** código de la lista permitida. No inventes categorías.
- Copia una **cita literal** del documento de 5 a 40 palabras que justifique el código. Debe ser exacta, carácter por carácter: será verificada por un script. Si el código indica ausencia (`ninguna`, `no`, `no_identificable`), deja la cita vacía.
- Asigna una `confianza` (`alta`, `media` o `baja`).
- Si algo es ambiguo o es un caso frontera, explícalo en `nota`.
- Solo cuenta lo que dice **la Corte**, no lo que alegan las partes (salvo `promovente`).
- No uses lo que sepas del caso por fuera del texto.

## Salida

Escribe `resultados_codificacion.csv` en la carpeta de trabajo del usuario con estas columnas, en este orden:

```
id, codebook_version, <variable>_codigo, <variable>_cita, <variable>_confianza  (por cada variable), nota
```

Usa UTF-8 y comillas dobles en los campos de texto.

## Auditoría (siempre, al terminar)

Los scripts están en la carpeta `scripts/` **de este skill** y los ejecutas tú, Claude, en tu entorno (Cowork, o Chat con ejecución de código). La persona usuaria no necesita Python ni terminal: nunca le pidas que ejecute un comando. Los scripts detectan solos las variables a partir de los encabezados `<variable>_codigo` y `<variable>_cita`, así que funcionan igual con la variable nueva de un participante: no los edites.

1. Verifica las citas:

   ```
   python <ruta de este skill>/scripts/verificar_citas.py resultados_codificacion.csv --corpus <carpeta de los .txt> --csv auditoria_citas.csv
   ```

   Si el codebook usa un código de ausencia que no empieza con `no_` ni con `ningun` (por ejemplo `otro_sin_cita`), agrégalo con `--ausencia <código>`.

2. Si hay citas **NO_ENCONTRADA**, vuelve a leer ese documento, corrige la cita (cópiala literal) o cambia el código si ya no se sostiene. Repite la verificación hasta que todas las citas sean encontradas, o explica por qué alguna no puede corregirse.
3. Reporta en lenguaje no técnico:
   - Cuántos documentos codificaste y la distribución de cada variable (una tabla corta).
   - El % de citas verificadas **antes y después** de la corrección. Ese dato importa: muestra cuánto se equivocó el modelo en la primera pasada.
   - Los documentos con confianza `baja`: son candidatos a revisión humana.
4. Si la persona tiene una codificación humana (por ejemplo `gold-standard-SIMULADO.csv` o `hoja-codificacion-humana.csv` del ejercicio), calcula el acuerdo:

   ```
   python <ruta de este skill>/scripts/calcular_acuerdo.py <humano.csv> resultados_codificacion.csv --desacuerdos
   ```

   Pon **primero la hoja humana**. Solo si la persona pide el detalle, agrega `--detalle`: el archivo A es la referencia para la matriz de confusión, la precisión, la exhaustividad y el F1.

   - Si la hoja humana viene en `.xlsx`, conviértela a CSV antes; si viene separada por `;` (Excel en español), el script la lee sin problema.
   - Si la hoja conserva el encabezado genérico `variable_codigo`, empareja con `--renombrar variable=<nombre de la variable>`. **No cambies ningún código humano.**
   - Explica el kappa en una frase ("0.72 = acuerdo sustancial") y comenta los desacuerdos concretos: ¿falló Claude, falló la persona o el codebook es ambiguo?
   - Por omisión, explica solo el kappa (con su IC si el script lo da) y los desacuerdos. Las demás columnas (α, AC1) y el detalle son **referenciales**: explícalos en lenguaje llano solo si la persona lo pide, por ejemplo la precisión como "de lo que marqué como X, cuánto lo era" y la exhaustividad como "de los X de la persona, cuántos encontré". Si N < 30, di que los números son ilustrativos. No elijas a posteriori la métrica que mejor se ve: el criterio de decisión es el que la persona fijó antes (en el kit, κ).

Si en tu entorno no puedes ejecutar código, dilo explícitamente, verifica cada cita buscándola en el texto y calcula el kappa a mano mostrando la tabla de contingencia. Declara en el reporte que la verificación no fue automática.

## Gráficas (si el usuario las pide)

Haz gráficas simples y legibles: barras horizontales con los nombres completos de las categorías y el N visible. Para la pregunta del caso, cruza cada variable con `control` (abstracto = AI; concreto = AR, ADR, AD) usando el `tipo` de `corpus/manifiesto_emblematicas.csv`. Reporta proporciones **y** conteos, y advierte cuando un grupo tenga menos de 15 casos (solo hay 9 AI en el corpus).

## Límites que debes recordarle al usuario

- La codificación es del **resumen oficial**, no de la sentencia completa. La marca `p.N` del resumen remite al párrafo de la sentencia para verificar en la fuente primaria.
- El corpus son sentencias **emblemáticas** seleccionadas por la SCJN, no una muestra aleatoria. Los hallazgos describen ese corpus y no se pueden generalizar a toda la jurisprudencia.
