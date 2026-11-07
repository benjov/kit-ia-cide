#!/usr/bin/env python3
"""
verificar_hashes.py — ¿El corpus del kit es idéntico al que publica la SCJN?

Vuelve a descargar cada PDF desde su URL oficial (o usa la copia local si existe)
y compara su SHA-256 con el registrado en corpus/manifiesto_emblematicas.csv.
Si la SCJN cambia o retira un documento, este script lo detecta.

Uso:
  python scripts/verificar_hashes.py               # verifica todo (resúmenes y sentencias)
  python scripts/verificar_hashes.py --muestra 10  # verifica 10 al azar (rápido, para clase)
  python scripts/verificar_hashes.py --local       # solo contra PDFs locales en corpus/pdf/

Requisitos: solo Python 3.10+.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import random
import time
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
UA = "kit-ia-cide/1.0 (material docente; verificación de integridad)"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--muestra", type=int)
    ap.add_argument("--local", action="store_true")
    args = ap.parse_args()

    filas = list(csv.DictReader((RAIZ / "corpus" / "manifiesto_emblematicas.csv").open(encoding="utf-8")))
    if args.muestra:
        random.seed(2026)
        filas = random.sample(filas, args.muestra)
    ok = mal = faltan = 0
    for f in filas:
        for clase in ("resumen", "sentencia"):
            esperado, url = f[f"sha256_pdf_{clase}"], f[f"url_{clase}"]
            if not esperado:
                continue
            local = RAIZ / "corpus" / "pdf" / clase / f"{f['id']}.pdf"
            if args.local:
                if not local.exists():
                    faltan += 1
                    continue
                datos = local.read_bytes()
            else:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=60) as r:
                    datos = r.read()
                time.sleep(1)
            obtenido = hashlib.sha256(datos).hexdigest()
            if obtenido == esperado:
                ok += 1
            else:
                mal += 1
                print(f"✗ {f['id']} {clase}: el hash no coincide ({url})")
    print(f"Coinciden: {ok} · No coinciden: {mal}" + (f" · Sin copia local: {faltan}" if faltan else ""))


if __name__ == "__main__":
    main()
