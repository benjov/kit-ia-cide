---
name: mi-codificador
description: REEMPLAZA ESTA DESCRIPCIÓN. Di qué documentos codifica (p. ej. "discursos legislativos", "respuestas abiertas de encuesta", "notas de prensa") y cuándo debe usarse (p. ej. "cuando el usuario pida codificar o clasificar discursos con mi codebook de polarización"). Claude decide si activar el skill leyendo SOLO esta línea, así que sé específico.
---

# Mi codificador · plantilla del Kit IA-CIDE

> **Si te piden seguir este archivo desde una carpeta, sin instalar el skill** (por ejemplo, en Claude Desktop con inferencia de terceros), las rutas `referencias/` y `scripts/` son relativas a la carpeta donde está este `SKILL.md`. Todo lo demás funciona igual.

> **Cómo usar esta plantilla** (sin programar)
> 1. Cambia `name` (minúsculas y guiones) y `description` arriba.
> 2. Sustituye `referencias/codebook.md` por tu codebook (usa `referencias/plantilla-codebook.md` como guía).
> 3. Ajusta la sección **Salida** para que liste tus variables.
> 4. Borra este recuadro.
> 5. Comprime la carpeta en .zip y súbela en Claude (Desktop o claude.ai) → Configuración → Capacidades → Skills.
>
> Los pasos 1 a 4 y el .zip del paso 5 los puede hacer **Cowork** por ti: dale acceso a la carpeta del kit y pídele que copie esta plantilla, la adapte con tu codebook y te deje el .zip listo. Solo te queda subirlo. Los scripts **no se editan**: detectan solas tus variables.

Trabajas como un codificador humano entrenado: aplicas el codebook, justificas cada código con evidencia literal y reportas tu incertidumbre.

## Antes de empezar

1. Lee `referencias/codebook.md` completo.
2. Identifica los documentos (archivos `.txt` en la carpeta que indique el usuario). El ID es el nombre del archivo. Si vienen en `.pdf` o `.docx`, extrae primero el texto a un `.txt` con el mismo nombre: la verificación de citas busca `<id>.txt`.
3. Si son más de 15, codifica primero 3 y pide revisión antes de seguir.

## Cómo codificar cada documento

- Un código por variable, solo de la lista permitida.
- Una **cita literal** de 5 a 40 palabras por código. Si el código indica ausencia, la cita va vacía.
- Confianza: `alta`, `media` o `baja`.
- Casos frontera y dudas: en `nota`.
- Solo el texto del documento, sin conocimiento externo.

## Salida

Escribe `resultados_codificacion.csv` con las columnas:

```
id, codebook_version, <variable>_codigo, <variable>_cita, <variable>_confianza (por cada variable), nota
```

## Auditoría (siempre)

Los scripts están en `scripts/` de este skill y los ejecutas tú, Claude, en tu entorno (Cowork, o Chat con ejecución de código). Nunca le pidas a la persona usuaria que ejecute comandos. Detectan solos las variables por los encabezados `<variable>_codigo`: no los edites.

1. Ejecuta `python <ruta de este skill>/scripts/verificar_citas.py resultados_codificacion.csv --corpus <carpeta> --csv auditoria_citas.csv`. Si un código de ausencia no empieza con `no_` ni con `ningun`, agrégalo con `--ausencia <código>`.
2. Corrige las citas no encontradas y vuelve a verificar.
3. Reporta la distribución por variable, el % de citas verificadas antes y después, y los casos de confianza baja.
4. Si hay codificación humana: `python <ruta de este skill>/scripts/calcular_acuerdo.py humano.csv resultados_codificacion.csv --desacuerdos` (la hoja humana va primero; agrega `--detalle` solo si la persona pide la matriz de confusión, la precisión y la exhaustividad). Si la hoja humana tiene encabezados genéricos (`variable_codigo`), usa `--renombrar variable=<tu variable>`; si viene en .xlsx, conviértela a CSV. No cambies ningún código humano. Explica el kappa y los desacuerdos; α, AC1 y el detalle son referenciales y se explican solo si la persona los pide. Si N < 30, di que los números son ilustrativos.

Si no puedes ejecutar código, dilo, verifica las citas buscándolas en el texto y declara que la verificación no fue automática.
