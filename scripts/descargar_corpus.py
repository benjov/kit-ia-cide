#!/usr/bin/env python3
"""
descargar_corpus.py — Descarga reproducible del corpus de "Sentencias emblemáticas"
de la Dirección General de Derechos Humanos de la SCJN.

OPCIONAL. El kit ya incluye el corpus descargado en corpus/. Este script existe para
que cualquiera pueda reproducir (y auditar) cómo se obtuvo.

Qué hace:
  1. Recorre las páginas públicas del índice de sentencias emblemáticas.
  2. Extrae de cada ficha: título, caso, temas y enlaces a resumen, sentencia y summary.
  3. Descarga los PDF (resumen y sentencia) desde www.scjn.gob.mx.
  4. Extrae el texto de cada PDF a .txt (con pypdf o, si existe, pdftotext).
  5. Escribe corpus/manifiesto.csv con URL de origen, fecha de descarga y SHA-256.

Uso:
  python scripts/descargar_corpus.py                 # todo el corpus
  python scripts/descargar_corpus.py --solo-ai       # solo acciones de inconstitucionalidad
  python scripts/descargar_corpus.py --sin-sentencias  # solo resúmenes (más rápido)
  python scripts/descargar_corpus.py --help

Requisitos: Python 3.10+. Para extraer texto: `pip install pypdf` (o tener pdftotext).
Buenas prácticas: el script espera 1 s entre solicitudes e identifica al cliente.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import html
import re
import shutil
import subprocess
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://www.scjn.gob.mx"
INDICE = BASE + "/derechos-humanos/sentencias-emblem-ticas-de-dh-summaries-of-significant-hr-decisions"
UA = "kit-ia-cide/1.0 (material docente; descarga respetuosa)"
PAUSA = 1.0

RAIZ = Path(__file__).resolve().parent.parent
CORPUS = RAIZ / "corpus"

TIPOS = {
    "Acción de Inconstitucionalidad": "AI",
    "Amparo Directo en Revisión": "ADR",
    "Amparo en Revisión": "AR",
    "Amparo Directo": "AD",
    "Controversia Constitucional": "CC",
    "Contradicción de Tesis": "CT",
    "Declaratoria General de Inconstitucionalidad": "DGI",
    "Facultad de Atracción": "FA",
    "Solicitud de Ejercicio de la Facultad de Atracción": "SEFA",
    "Recurso de Reclamación": "RR",
    "Varios": "VAR",
}


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
        ctype = r.headers.get("Content-Type", "")
    if b"_Incapsula_Resource" in data[:2000]:
        raise RuntimeError(f"Bloqueado por protección anti-bots: {url}")
    if url.lower().endswith(".pdf") and not data.startswith(b"%PDF"):
        raise RuntimeError(f"No es un PDF ({ctype}): {url}")
    return data


def limpiar(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def parsear_indice(pagina: str) -> list[dict]:
    """Devuelve las fichas de una página del índice."""
    fichas = []
    bloques = pagina.split('<h2 class="title-sentencias')[1:]
    for b in bloques:
        titulo = limpiar(b.split("</h2>")[0].split(">", 1)[1]).removeprefix("Título:").strip()
        caso = re.search(r'title-sentencias">Caso</p>\s*<p>(.*?)</p>', b, re.S)
        temas = re.search(r'title-sentencias">Temas</p>\s*<p>(.*?)</p>', b, re.S)
        links = {}
        for clase in ("resumen", "sentencia", "summary"):
            m = re.search(rf'href="([^"]*sentencias-emblematicas/{clase}/[^"]*)"', b)
            if m:
                links[clase] = urllib.parse.urljoin(BASE, m.group(1).strip())
        if not caso:  # cada ficha tiene un bloque en inglés sin "Caso": lo omitimos
            continue
        fichas.append({
            "titulo": titulo,
            "caso": limpiar(caso.group(1)) if caso else "",
            "temas": limpiar(temas.group(1)) if temas else "",
            **{f"url_{k}": v for k, v in links.items()},
        })
    return fichas


def tipo_y_id(caso: str) -> tuple[str, str]:
    """'Acción de Inconstitucionalidad 148/2017' -> ('AI', 'AI-148-2017')."""
    tipo = "OTRO"
    for nombre, sigla in sorted(TIPOS.items(), key=lambda x: -len(x[0])):
        if caso.lower().startswith(nombre.lower()):
            tipo = sigla
            break
    num = re.search(r"(\d+)\s*/\s*(\d{4})", caso)
    ident = f"{tipo}-{num.group(1)}-{num.group(2)}" if num else f"{tipo}-{hashlib.md5(caso.encode()).hexdigest()[:6]}"
    return tipo, ident


def pdf_a_texto(pdf: Path, txt: Path) -> None:
    if shutil.which("pdftotext"):
        subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), str(txt)], check=True)
        # Algunos PDF traen acentos "descompuestos" (NFD); los normalizamos para que las búsquedas funcionen.
        txt.write_text(unicodedata.normalize("NFC", txt.read_text(encoding="utf-8")), encoding="utf-8")
        return
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit("Instala pypdf (pip install pypdf) o pdftotext para extraer texto.")
    texto = "\n\n".join((p.extract_text() or "") for p in PdfReader(pdf).pages)
    txt.write_text(unicodedata.normalize("NFC", texto), encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--solo-ai", action="store_true", help="solo acciones de inconstitucionalidad")
    ap.add_argument("--sin-sentencias", action="store_true", help="no descargar sentencias completas")
    ap.add_argument("--max-paginas", type=int, default=60)
    args = ap.parse_args()

    for sub in ("pdf/resumen", "pdf/sentencia", "resumenes", "sentencias"):
        (CORPUS / sub).mkdir(parents=True, exist_ok=True)

    # 1. Índice
    fichas, vistos = [], set()
    for p in range(args.max_paginas):
        pagina = get(f"{INDICE}?page={p}").decode("utf-8", "replace")
        nuevas = [f for f in parsear_indice(pagina) if f["caso"] + f["titulo"] not in vistos]
        if not nuevas:
            break
        for f in nuevas:
            vistos.add(f["caso"] + f["titulo"])
        fichas += nuevas
        print(f"página {p}: {len(nuevas)} fichas")
        time.sleep(PAUSA)
    print(f"Total de fichas: {len(fichas)}")

    # 2. Descarga y extracción
    hoy = dt.date.today().isoformat()
    filas, ids = [], {}
    for f in fichas:
        tipo, ident = tipo_y_id(f["caso"])
        if args.solo_ai and tipo != "AI":
            continue
        ids[ident] = ids.get(ident, 0) + 1
        if ids[ident] > 1:
            ident = f"{ident}-v{ids[ident]}"
        fila = {"id": ident, "tipo": tipo, "caso": f["caso"], "titulo": f["titulo"], "temas": f["temas"],
                "fuente": "SCJN-DGDH sentencias emblemáticas", "metodo_obtencion": "script",
                "fecha_descarga": hoy}
        for clase, carpeta in (("resumen", "resumenes"), ("sentencia", "sentencias")):
            url = f.get(f"url_{clase}", "")
            fila[f"url_{clase}"] = url
            fila[f"sha256_pdf_{clase}"] = ""
            fila[f"archivo_{clase}"] = ""
            if not url or (clase == "sentencia" and args.sin_sentencias):
                continue
            pdf = CORPUS / "pdf" / clase / f"{ident}.pdf"
            txt = CORPUS / carpeta / f"{ident}.txt"
            try:
                if not pdf.exists():
                    pdf.write_bytes(get(url))
                    time.sleep(PAUSA)
                pdf_a_texto(pdf, txt)
                fila[f"sha256_pdf_{clase}"] = sha256(pdf)
                fila[f"archivo_{clase}"] = str(txt.relative_to(RAIZ))
                print(f"  ✓ {ident} {clase}")
            except Exception as e:  # noqa: BLE001 — registramos y seguimos
                print(f"  ✗ {ident} {clase}: {e}")
        fila["url_summary_en"] = f.get("url_summary", "")
        filas.append(fila)

    # 3. Manifiesto
    destino = CORPUS / "manifiesto_emblematicas.csv"
    with destino.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    print(f"Manifiesto: {destino} ({len(filas)} documentos)")


if __name__ == "__main__":
    main()
