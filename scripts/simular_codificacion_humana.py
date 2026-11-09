#!/usr/bin/env python3
"""
simular_codificacion_humana.py — Genera una codificación "humana" SIMULADA para fines didácticos.

⚠️  ESTO NO ES UNA CODIFICACIÓN HUMANA REAL. ⚠️
El caso completo es material docente. Para mostrar el procedimiento de validación
(kappa, análisis de desacuerdos) sin pedir horas de codificación al equipo, simulamos
a un codificador humano así:

  1. Partimos de la codificación de Claude Opus 5.5 sobre la muestra de validación (20 documentos).
  2. Para cada variable, el "humano" discrepa con una probabilidad que depende de la
     confianza que Claude declaró: baja=60%, media=30%, alta=8%, multiplicada por 1.5
     en las variables más interpretativas (proporcionalidad, fuentes internacionales).
     (Supuesto: donde el modelo duda, el texto es ambiguo y un humano también dudaría.)
  3. Cuando discrepa, elige un código "vecino" plausible (p. ej. protege↔mixto,
     tratados↔corte_idh), no uno al azar.
  4. Semilla fija (2026) → el resultado es reproducible.

Consecuencia metodológica que se discute en clase: como el "humano" se deriva de Opus, el
kappa humano–Opus está inflado por construcción y no es evidencia de validez. Sirve para
ilustrar el procedimiento, no el resultado. En tu proyecto, la codificación humana debe ser
real, a ciegas y hecha antes de ver los códigos del modelo.

Uso:
  python scripts/simular_codificacion_humana.py caso-completo/04-resultados/corridas/<opus>.jsonl
"""
from __future__ import annotations

import csv
import json
import random
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MUESTRA = RAIZ / "ejercicio" / "muestra-20" / "muestra.csv"
SALIDA = RAIZ / "caso-completo" / "05-validacion" / "gold-standard-SIMULADO.csv"
P_DISCREPAR = {"baja": 0.60, "media": 0.30, "alta": 0.08}
# Variables más interpretativas: un humano discrepa más (supuesto didáctico)
MULTIPLICADOR = {"proporcionalidad": 1.5, "fuentes_internacionales": 1.5}
VECINOS = {
    "promovente": {"persona": ["colectivo"], "colectivo": ["persona"], "organo_autonomo": ["autoridad"], "fiscalia": ["autoridad"],
                   "actor_politico": ["autoridad"], "autoridad": ["organo_autonomo"], "no_identificable": ["persona"]},
    "resultado": {"protege": ["mixto"], "no_protege": ["mixto"], "mixto": ["protege", "no_protege"], "otro": ["no_protege"]},
    "derecho_principal": {"igualdad_no_discriminacion": ["familia", "otro"], "debido_proceso_acceso_justicia": ["libertad_integridad_personal"],
                          "libertad_integridad_personal": ["debido_proceso_acceso_justicia"], "salud": ["derechos_sexuales_reproductivos"],
                          "derechos_sexuales_reproductivos": ["salud", "igualdad_no_discriminacion"], "familia": ["ninez"], "ninez": ["familia"],
                          "libertad_expresion_informacion": ["privacidad_datos"], "privacidad_datos": ["libertad_expresion_informacion"],
                          "otro": ["igualdad_no_discriminacion"], "_": ["otro"]},
    "fuentes_internacionales": {"ninguna": ["tratados"], "tratados": ["corte_idh", "ninguna"], "corte_idh": ["tratados"], "otra_jurisprudencia": ["tratados"]},
    "proporcionalidad": {"si": ["no"], "no": ["si"]},
    "perspectiva_genero": {"si": ["no"], "no": ["si"]},
}
CODIFICADORES = ["H1-simulado", "H2-simulado"]


def main() -> None:
    if len(sys.argv) == 2 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    claude = {json.loads(l)["id"]: json.loads(l) for l in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines() if l.strip()}
    muestra = list(csv.DictReader(MUESTRA.open(encoding="utf-8")))
    rnd = random.Random(2026)
    filas, cambios = [], 0
    for k, d in enumerate(muestra):
        c = claude[d["id"]]
        fila = {"id": d["id"], "tipo": d["tipo"], "codificador": CODIFICADORES[k % 2], "simulado": "SI"}
        for v, vecinos in VECINOS.items():
            codigo = c[v]["codigo"]
            if rnd.random() < P_DISCREPAR[c[v]["confianza"]] * MULTIPLICADOR.get(v, 1):
                opciones = vecinos.get(codigo) or vecinos["_"]
                codigo = rnd.choice(opciones)
                cambios += 1
            fila[f"{v}_codigo"] = codigo
        fila["nota"] = "CODIFICACIÓN SIMULADA con fines didácticos; no es juicio humano real (ver scripts/simular_codificacion_humana.py)"
        filas.append(fila)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with SALIDA.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    print(f"{SALIDA.relative_to(RAIZ)}: {len(filas)} documentos, {cambios} discrepancias introducidas de {len(filas) * len(VECINOS)} códigos")


if __name__ == "__main__":
    main()
