#!/usr/bin/env python3
"""
verificar_citas.py — Auditoría automática: ¿cada cita que dio Claude existe en el documento?

Un LLM puede "parafrasear" una cita o inventarla. Este script busca cada cita en el
texto fuente (ignorando diferencias de espacios, saltos de línea y guiones de corte
de palabra) y reporta las que no aparecen. Además, cuando el resumen trae la marca de
párrafo de la sentencia ("p.21-22"), la anota para que puedas ir a la fuente primaria.

Uso:
  python scripts/verificar_citas.py caso-completo/04-resultados/corridas/<archivo>.jsonl
  python scripts/verificar_citas.py <archivo>.jsonl --csv auditoria/reporte_citas.csv

Funciona con la salida de codificar_api.py y con el CSV que produce el skill en Cowork
(columnas <variable>_codigo y <variable>_cita).
Requisitos: solo Python 3.10+ (sin dependencias).
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VARIABLES = ["promovente", "resultado", "derecho_principal", "fuentes_internacionales", "proporcionalidad", "perspectiva_genero"]
AUSENCIA = {"ninguna", "no", "no_identificable"}


def normalizar(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"-\s*\n\s*", "", s)          # palabras cortadas con guion al final de línea
    s = re.sub(r"[“”«»\"]", '"', s)
    s = re.sub(r"[‘’']", "'", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def marca_parrafo(texto: str, cita: str) -> str:
    """Devuelve la marca 'p.N' más cercana antes de la cita en el texto original, si existe."""
    t = normalizar(texto)
    i = t.find(normalizar(cita))
    if i < 0:
        return ""
    marcas = list(re.finditer(r"\bp\.\s?(\d+(?:-\d+)?)", t[:i]))
    return f"p.{marcas[-1].group(1)}" if marcas else ""


def cargar(path: Path) -> list[dict]:
    if path.suffix == ".jsonl":
        return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    filas = []
    for r in csv.DictReader(path.open(encoding="utf-8")):
        fila = {"id": r["id"]}
        for v in VARIABLES:
            if f"{v}_codigo" in r:
                fila[v] = {"codigo": r[f"{v}_codigo"], "cita": r.get(f"{v}_cita", "")}
        filas.append(fila)
    return filas


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("resultados", type=Path)
    ap.add_argument("--corpus", type=Path, default=RAIZ / "corpus" / "resumenes")
    ap.add_argument("--csv", type=Path, help="guardar el detalle en un CSV")
    args = ap.parse_args()

    filas = cargar(args.resultados)
    detalle, ok, mal, vacias_indebidas = [], 0, 0, 0
    for f in filas:
        fuente = args.corpus / f"{f['id']}.txt"
        if not fuente.exists():
            print(f"⚠ No encuentro el texto fuente de {f['id']}")
            continue
        texto = fuente.read_text(encoding="utf-8")
        tnorm = normalizar(texto)
        for v in VARIABLES:
            if v not in f:
                continue
            codigo, cita = f[v]["codigo"], (f[v].get("cita") or "").strip()
            if not cita:
                estado = "sin_cita_ok" if codigo in AUSENCIA else "sin_cita_FALTA"
                vacias_indebidas += estado == "sin_cita_FALTA"
            elif normalizar(cita) in tnorm:
                estado = "verificada"
                ok += 1
            else:
                estado = "NO_ENCONTRADA"
                mal += 1
            detalle.append({"id": f["id"], "variable": v, "codigo": codigo, "estado": estado,
                            "parrafo_sentencia": marca_parrafo(texto, cita) if estado == "verificada" else "",
                            "cita": cita})

    total = ok + mal
    print(f"Citas verificadas: {ok}/{total} ({(ok / total * 100) if total else 0:.1f}%)")
    print(f"Citas NO encontradas en el texto: {mal}")
    print(f"Códigos sustantivos sin cita: {vacias_indebidas}")
    for d in detalle:
        if d["estado"] in ("NO_ENCONTRADA", "sin_cita_FALTA"):
            print(f"  ✗ {d['id']:<16} {d['variable']:<24} {d['estado']:<15} «{d['cita'][:80]}»")
    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(detalle[0]))
            w.writeheader()
            w.writerows(detalle)
        print(f"Detalle: {args.csv}")
    sys.exit(1 if mal else 0)


if __name__ == "__main__":
    main()
