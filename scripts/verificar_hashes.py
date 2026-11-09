#!/usr/bin/env python3
"""
verificar_hashes.py — ¿El corpus del kit es idéntico al que publica la SCJN?

El SHA-256 es una "huella digital" de un archivo: si cambia un solo byte, la huella
cambia por completo. El manifiesto (corpus/manifiesto_emblematicas.csv) guarda la huella
de cada PDF tal como se descargó el 2026-11-06. Este script la vuelve a calcular y compara.

Tres maneras de usarlo:
  python scripts/verificar_hashes.py --muestra 3     # baja 3 documentos al azar de la SCJN (rápido)
  python scripts/verificar_hashes.py --ids AI-148-2017 AR-1064-2019
  python scripts/verificar_hashes.py                 # todos (204 PDF, unos 5 min)

  # Sin internet en el entorno: descarga tú el PDF desde el navegador (URL del manifiesto)
  # y verifica el archivo local. El script reconoce de qué documento es por su huella.
  python scripts/verificar_hashes.py --pdf ~/Downloads/"Resumen AR1064-2019 DGDH.pdf"

  python scripts/verificar_hashes.py --local         # contra las copias en corpus/pdf/

No necesitas saber programar: pídele a Claude en Cowork que lo ejecute (scripts/README.md).
Requisitos: solo Python 3.10+.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import random
import sys
import time
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MANIFIESTO = RAIZ / "corpus" / "manifiesto_emblematicas.csv"
UA = "kit-ia-cide/1.0 (material docente; verificación de integridad)"


def descargar(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        datos = r.read()
    if b"_Incapsula_Resource" in datos[:2000]:
        raise RuntimeError("bloqueado por protección anti-bots (no se intenta evadir, bitácora D1)")
    if not datos.startswith(b"%PDF"):
        raise RuntimeError("la respuesta no es un PDF")
    return datos


def verificar_locales(rutas: list[Path], filas: list[dict]) -> None:
    por_hash = {f[f"sha256_pdf_{c}"]: (f["id"], c) for f in filas for c in ("resumen", "sentencia") if f[f"sha256_pdf_{c}"]}
    for ruta in rutas:
        h = hashlib.sha256(ruta.expanduser().read_bytes()).hexdigest()
        if h in por_hash:
            ident, clase = por_hash[h]
            print(f"✓ {ruta.name}: idéntico al {clase} de {ident} registrado en el manifiesto")
        else:
            print(f"✗ {ruta.name}: su SHA-256 ({h[:16]}…) no coincide con ningún PDF del manifiesto.\n"
                  "  O no es un documento del corpus, o la SCJN lo modificó después del 2026-11-06.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--muestra", type=int, help="verificar N documentos al azar (semilla 2026)")
    ap.add_argument("--ids", nargs="*", help="verificar solo estos IDs")
    ap.add_argument("--local", action="store_true", help="usar las copias de corpus/pdf/ en vez de descargar")
    ap.add_argument("--pdf", nargs="+", type=Path, help="verificar PDF descargados a mano")
    args = ap.parse_args()

    filas = list(csv.DictReader(MANIFIESTO.open(encoding="utf-8")))
    if args.pdf:
        verificar_locales(args.pdf, filas)
        return
    if args.ids:
        filas = [f for f in filas if f["id"] in set(args.ids)]
    if args.muestra:
        random.seed(2026)
        filas = random.sample(filas, args.muestra)
    ok = mal = faltan = errores = 0
    for f in filas:
        for clase in ("resumen", "sentencia"):
            esperado, url = f[f"sha256_pdf_{clase}"], f[f"url_{clase}"]
            if not esperado:
                continue
            local = RAIZ / "corpus" / "pdf" / clase / f"{f['id']}.pdf"
            try:
                if args.local:
                    if not local.exists():
                        faltan += 1
                        continue
                    datos = local.read_bytes()
                else:
                    datos = descargar(url)
                    time.sleep(1)
            except RuntimeError as e:
                sys.exit(f"Detenido en {f['id']}: {e}")
            except OSError as e:
                errores += 1
                print(f"? {f['id']} {clase}: no se pudo descargar ({e}).")
                if errores == 1:
                    print("  Si estás en Cowork, quizá el entorno no tiene salida a internet hacia scjn.gob.mx.\n"
                          "  Alternativa: baja el PDF desde el navegador y usa --pdf <archivo>.")
                continue
            if hashlib.sha256(datos).hexdigest() == esperado:
                ok += 1
                print(f"✓ {f['id']} {clase}")
            else:
                mal += 1
                print(f"✗ {f['id']} {clase}: el hash no coincide ({url})")
    print(f"\nCoinciden: {ok} · No coinciden: {mal}"
          + (f" · Sin copia local: {faltan}" if faltan else "") + (f" · Sin descarga: {errores}" if errores else ""))


if __name__ == "__main__":
    main()
