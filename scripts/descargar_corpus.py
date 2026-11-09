#!/usr/bin/env python3
"""
descargar_corpus.py — Descarga reproducible del corpus de "Sentencias emblemáticas"
de la Dirección General de Derechos Humanos de la SCJN.

OPCIONAL. El kit ya incluye el corpus descargado en corpus/. Este script existe para
que cualquiera pueda reproducir (y auditar) cómo se obtuvo. No necesitas saber programar:
puedes pedirle a Claude en Cowork que lo ejecute (ver scripts/README.md).

Qué hace:
  1. Recorre las páginas públicas del índice de sentencias emblemáticas.
  2. Extrae de cada ficha: título, caso, temas y enlaces a resumen, sentencia y summary.
  3. Descarga los PDF (resumen y sentencia) desde www.scjn.gob.mx.
  4. Extrae el texto de cada PDF a .txt (con pypdf o, si existe, pdftotext).
  5. Escribe manifiesto_emblematicas.csv con URL de origen, fecha de descarga y SHA-256.

Uso:
  # Prueba rápida (menos de 1 min): baja 3 documentos a otra carpeta y los compara con el kit.
  python scripts/descargar_corpus.py --muestra 3 --destino mi-trabajo/corpus-prueba
  python scripts/descargar_corpus.py --ids AI-148-2017 AR-1064-2019 --destino mi-trabajo/corpus-prueba

  # Regenerar el corpus completo del kit (sobrescribe corpus/; tarda unos 10 min)
  python scripts/descargar_corpus.py
  python scripts/descargar_corpus.py --sin-sentencias  # solo resúmenes (más rápido)

Con --destino distinto de corpus/, el script no toca el kit y al final compara el SHA-256
de cada PDF y el texto extraído contra corpus/manifiesto_emblematicas.csv y corpus/*.txt.
Las descargas parciales (--muestra, --ids, --solo-ai) exigen --destino, para no reemplazar
el manifiesto del kit por uno incompleto.

Qué puede salir distinto y por qué:
  - SHA-256 distinto: la SCJN cambió o reemplazó el PDF (eso es lo que el hash detecta).
  - Texto distinto con el mismo PDF: el texto depende del extractor. El kit usó pdftotext
    (poppler) con -layout; pypdf produce otro texto. Por eso el hash se toma del PDF.

Límite ético: solo usa la colección pública de sentencias emblemáticas. Si el sitio
responde con una protección anti-bots, el script se detiene; no intentes evadirla
(bitácora D1). Espera 1 s entre solicitudes e identifica al cliente.

Requisitos: Python 3.10+. Para extraer texto: pdftotext (poppler) o `pip install pypdf`.
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


def extractor() -> str:
    if shutil.which("pdftotext"):
        return "pdftotext"
    try:
        import pypdf  # noqa: F401
        return "pypdf"
    except ImportError:
        return ""


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


def comparar_con_kit(filas: list[dict], destino: Path) -> None:
    """Compara lo descargado en `destino` con el manifiesto y los textos del kit."""
    kit = {r["id"]: r for r in csv.DictReader((CORPUS / "manifiesto_emblematicas.csv").open(encoding="utf-8"))}
    print("\nComparación con el corpus del kit:")
    print(f"  extractor de texto usado ahora: {extractor()} (el kit usó pdftotext -layout)")
    ok_hash = mal_hash = ok_txt = mal_txt = 0
    for f in filas:
        k = kit.get(f["id"])
        if not k:
            print(f"  ? {f['id']}: no está en el manifiesto del kit (¿documento nuevo en la SCJN?)")
            continue
        for clase, carpeta in (("resumen", "resumenes"), ("sentencia", "sentencias")):
            nuevo = f.get(f"sha256_pdf_{clase}")
            if not nuevo:
                continue
            if nuevo == k[f"sha256_pdf_{clase}"]:
                ok_hash += 1
            else:
                mal_hash += 1
                print(f"  ✗ {f['id']} {clase}: el PDF cambió (SHA-256 distinto)")
            t_nuevo = destino / carpeta / f"{f['id']}.txt"
            t_kit = CORPUS / carpeta / f"{f['id']}.txt"
            if t_kit.exists() and t_nuevo.exists():
                if t_nuevo.read_text(encoding="utf-8") == t_kit.read_text(encoding="utf-8"):
                    ok_txt += 1
                else:
                    mal_txt += 1
                    print(f"  · {f['id']} {clase}: el texto extraído difiere del kit")
    print(f"  PDF idénticos (SHA-256): {ok_hash} · distintos: {mal_hash}")
    print(f"  Textos idénticos: {ok_txt} · distintos: {mal_txt}")
    if mal_txt and not mal_hash:
        print("  Los PDF son los mismos; la diferencia de texto viene del extractor, no de la fuente.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--solo-ai", action="store_true", help="solo acciones de inconstitucionalidad")
    ap.add_argument("--sin-sentencias", action="store_true", help="no descargar sentencias completas")
    ap.add_argument("--max-paginas", type=int, default=60)
    ap.add_argument("--muestra", type=int, help="descargar solo N documentos (elegidos con semilla 2026)")
    ap.add_argument("--ids", nargs="*", help="descargar solo estos IDs (p. ej. AI-148-2017)")
    ap.add_argument("--destino", type=Path, help="carpeta de salida; si no es corpus/, no toca el kit y compara")
    args = ap.parse_args()

    destino = (args.destino or CORPUS).resolve()
    es_kit = destino == CORPUS.resolve()
    if es_kit and (args.muestra or args.ids or args.solo_ai):
        sys.exit("Las descargas parciales necesitan --destino (p. ej. --destino mi-trabajo/corpus-prueba) "
                 "para no reemplazar el manifiesto del kit por uno incompleto.")
    if not extractor():
        sys.exit("Falta un extractor de texto: instala pdftotext (poppler) o `pip install pypdf`.")

    for sub in ("pdf/resumen", "pdf/sentencia", "resumenes", "sentencias"):
        (destino / sub).mkdir(parents=True, exist_ok=True)

    # 1. Índice
    fichas, vistos = [], set()
    for p in range(args.max_paginas):
        try:
            pagina = get(f"{INDICE}?page={p}").decode("utf-8", "replace")
        except RuntimeError as e:
            sys.exit(f"Detenido: {e}. No se intenta evadir la protección (bitácora D1).")
        except OSError as e:
            sys.exit(f"Sin acceso a {BASE} ({e}). Si estás en Cowork, puede que el entorno no tenga salida a "
                     "internet para ese dominio. Alternativa: descarga el PDF a mano desde el navegador y "
                     "verifica su hash con verificar_hashes.py --pdf.")
        nuevas = [f for f in parsear_indice(pagina) if f["caso"] + f["titulo"] not in vistos]
        if not nuevas:
            break
        for f in nuevas:
            vistos.add(f["caso"] + f["titulo"])
        fichas += nuevas
        print(f"página {p}: {len(nuevas)} fichas")
        time.sleep(PAUSA)
        if args.ids and {tipo_y_id(f["caso"])[1] for f in fichas} >= set(args.ids):
            break
    print(f"Total de fichas en el índice: {len(fichas)}")

    if args.ids:
        fichas = [f for f in fichas if tipo_y_id(f["caso"])[1] in set(args.ids)]
        faltan = set(args.ids) - {tipo_y_id(f["caso"])[1] for f in fichas}
        if faltan:
            print(f"⚠ No encontré en el índice: {', '.join(sorted(faltan))}")
    if args.muestra:
        import random
        random.seed(2026)
        fichas = random.sample(fichas, min(args.muestra, len(fichas)))

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
            pdf = destino / "pdf" / clase / f"{ident}.pdf"
            txt = destino / carpeta / f"{ident}.txt"
            try:
                if not pdf.exists():
                    pdf.write_bytes(get(url))
                    time.sleep(PAUSA)
                pdf_a_texto(pdf, txt)
                fila[f"sha256_pdf_{clase}"] = sha256(pdf)
                fila[f"archivo_{clase}"] = str(txt.relative_to(RAIZ)) if es_kit else str(txt)
                print(f"  ✓ {ident} {clase}")
            except Exception as e:  # noqa: BLE001 — registramos y seguimos
                print(f"  ✗ {ident} {clase}: {e}")
        fila["url_summary_en"] = f.get("url_summary", "")
        filas.append(fila)

    if not filas:
        sys.exit("No se descargó ningún documento.")

    # 3. Manifiesto
    destino_m = destino / "manifiesto_emblematicas.csv"
    with destino_m.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    print(f"Manifiesto: {destino_m} ({len(filas)} documentos)")
    if not es_kit:
        comparar_con_kit(filas, destino)


if __name__ == "__main__":
    main()
