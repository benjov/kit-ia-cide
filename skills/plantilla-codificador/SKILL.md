---
name: mi-codificador
description: REEMPLAZA ESTA DESCRIPCIÓN. Di qué documentos codifica (p. ej. "discursos legislativos", "respuestas abiertas de encuesta", "notas de prensa") y cuándo debe usarse (p. ej. "cuando el usuario pida codificar o clasificar discursos con mi codebook de polarización"). Claude decide si activar el skill leyendo SOLO esta línea, así que sé específico.
---

# Mi codificador · plantilla del Kit IA-CIDE

> **Cómo usar esta plantilla**
> 1. Cambia `name` (minúsculas y guiones) y `description` arriba.
> 2. Sustituye `referencias/codebook.md` por tu codebook (usa `referencias/plantilla-codebook.md` como guía).
> 3. Ajusta la sección **Salida** para que liste tus variables.
> 4. Comprime la carpeta en .zip y súbela en Claude Desktop → Configuración → Capacidades → Skills.
> 5. Borra este recuadro.

Trabajas como un codificador humano entrenado: aplicas el codebook, justificas cada código con evidencia literal y reportas tu incertidumbre.

## Antes de empezar

1. Lee `referencias/codebook.md` completo.
2. Identifica los documentos (archivos `.txt`, `.pdf` o `.docx` en la carpeta que indique el usuario). El ID es el nombre del archivo.
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

1. Ejecuta `python scripts/verificar_citas.py resultados_codificacion.csv --corpus <carpeta> --csv auditoria_citas.csv`. Antes, edita la lista `VARIABLES` al inicio del script con tus variables.
2. Corrige las citas no encontradas y vuelve a verificar.
3. Reporta la distribución por variable, el % de citas verificadas antes y después, y los casos de confianza baja.
4. Si hay codificación humana: `python scripts/calcular_acuerdo.py humano.csv resultados_codificacion.csv --desacuerdos`.
