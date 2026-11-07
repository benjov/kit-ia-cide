#!/usr/bin/env python3
"""
calcular_acuerdo.py — Confiabilidad entre codificadores: kappa de Cohen por variable.

Compara dos codificaciones del mismo conjunto de documentos (humano vs. Claude,
o modelo A vs. modelo B) y reporta, por variable: N, % de acuerdo, kappa de Cohen,
su interpretación (Landis y Koch, 1977) y la lista de desacuerdos para revisarlos.

Uso:
  python scripts/calcular_acuerdo.py A.csv B.jsonl
  python scripts/calcular_acuerdo.py caso-completo/05-validacion/gold-standard.csv \\
         caso-completo/04-resultados/corridas/<opus>.jsonl --desacuerdos

Formatos aceptados: .jsonl de codificar_api.py, o .csv con columna `id` y columnas
`<variable>` o `<variable>_codigo`. Solo se comparan los IDs presentes en ambos.
Requisitos: solo Python 3.10+.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

VARIABLES = ["promovente", "resultado", "derecho_principal", "fuentes_internacionales", "proporcionalidad", "perspectiva_genero"]


def cargar(path: Path) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    if path.suffix == ".jsonl":
        for l in path.read_text(encoding="utf-8").splitlines():
            if l.strip():
                r = json.loads(l)
                out[r["id"]] = {v: r[v]["codigo"] for v in VARIABLES if v in r}
    else:
        for r in csv.DictReader(path.open(encoding="utf-8")):
            out[r["id"]] = {v: (r.get(f"{v}_codigo") or r.get(v) or "").strip() for v in VARIABLES
                            if (r.get(f"{v}_codigo") or r.get(v) or "").strip()}
    return out


def kappa(a: list[str], b: list[str]) -> float:
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def interpretar(k: float) -> str:
    for umbral, etiqueta in ((0.81, "casi perfecto"), (0.61, "sustancial"), (0.41, "moderado"), (0.21, "aceptable"), (0.0, "leve")):
        if k >= umbral:
            return etiqueta
    return "pobre"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("a", type=Path)
    ap.add_argument("b", type=Path)
    ap.add_argument("--desacuerdos", action="store_true", help="listar cada desacuerdo")
    ap.add_argument("--csv", type=Path, help="guardar la tabla de confiabilidad")
    args = ap.parse_args()

    A, B = cargar(args.a), cargar(args.b)
    comunes = sorted(set(A) & set(B))
    print(f"A = {args.a.name}  ·  B = {args.b.name}  ·  documentos en común: {len(comunes)}\n")
    print(f"{'variable':<26}{'N':>4}{'% acuerdo':>11}{'kappa':>8}  interpretación")
    tabla = []
    for v in VARIABLES:
        pares = [(A[i][v], B[i][v], i) for i in comunes if v in A[i] and v in B[i]]
        if not pares:
            continue
        a, b, ids = zip(*pares)
        k = kappa(list(a), list(b))
        acuerdo = sum(x == y for x, y in zip(a, b)) / len(a)
        tabla.append({"variable": v, "n": len(a), "acuerdo": round(acuerdo, 3), "kappa": round(k, 3), "interpretacion": interpretar(k)})
        print(f"{v:<26}{len(a):>4}{acuerdo:>10.0%}{k:>8.2f}  {interpretar(k)}")
        if args.desacuerdos:
            for x, y, i in pares:
                if x != y:
                    print(f"    · {i:<16} A={x:<28} B={y}")
    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(tabla[0]))
            w.writeheader()
            w.writerows(tabla)
        print(f"\nTabla: {args.csv}")


if __name__ == "__main__":
    main()
