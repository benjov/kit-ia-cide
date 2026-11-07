#!/usr/bin/env python3
"""
codificar_batch.py — Igual que codificar_api.py, pero con la Batch API: 50% más barato.

La Batch API procesa solicitudes de forma asíncrona (la mayoría termina en menos de una hora).
Es la forma natural de escalar un análisis de contenido: no necesitas la respuesta al instante.

Uso (dos pasos):
  python scripts/codificar_batch.py enviar --modelos claude-opus-5-5 claude-sonnet-5-5 claude-haiku-5-5
  python scripts/codificar_batch.py recoger          # espera a que terminen y escribe los .jsonl

Los IDs de los lotes se guardan en caso-completo/04-resultados/corridas/lotes.json,
así que puedes cerrar la terminal y recoger después.
Requisitos: pip install anthropic
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
import time

import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

from codificar_api import (CODEBOOK, CODEBOOK_VERSION, MANIFIESTO, PRECIOS, PROMPT, PROMPT_VERSION, RAIZ, SALIDA,
                           esquema)

LOTES = SALIDA / "lotes.json"


def enviar(modelos: list[str], limite: int | None) -> None:
    system = PROMPT.read_text(encoding="utf-8").replace("{{CODEBOOK}}", CODEBOOK.read_text(encoding="utf-8"))
    docs = [r for r in csv.DictReader(MANIFIESTO.open(encoding="utf-8")) if r["archivo_resumen"]][:limite]
    client = anthropic.Anthropic()
    registro = json.loads(LOTES.read_text()) if LOTES.exists() else {}
    for modelo in modelos:
        requests = [
            Request(custom_id=d["id"], params=MessageCreateParamsNonStreaming(
                model=modelo,
                max_tokens=4000,
                system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content":
                           f"<documento id=\"{d['id']}\">\n{(RAIZ / d['archivo_resumen']).read_text(encoding='utf-8')}\n</documento>\n\n"
                           "Codifica este documento según el codebook."}],
                output_config={"effort": "medium", "format": {"type": "json_schema", "schema": esquema()}},
            ))
            for d in docs
        ]
        lote = client.messages.batches.create(requests=requests)
        registro[lote.id] = {"modelo": modelo, "enviado": dt.datetime.now().isoformat(timespec="seconds"), "n": len(docs)}
        print(f"Lote enviado: {lote.id}  modelo={modelo}  documentos={len(docs)}")
    SALIDA.mkdir(parents=True, exist_ok=True)
    LOTES.write_text(json.dumps(registro, indent=2))


def recoger() -> None:
    client = anthropic.Anthropic()
    registro = json.loads(LOTES.read_text())
    meta = {r["id"]: r for r in csv.DictReader(MANIFIESTO.open(encoding="utf-8"))}
    for lote_id, info in registro.items():
        if info.get("recogido"):
            continue
        while (lote := client.messages.batches.retrieve(lote_id)).processing_status != "ended":
            c = lote.request_counts
            print(f"{info['modelo']}: en proceso={c.processing} ok={c.succeeded} error={c.errored} … espero 60 s")
            time.sleep(60)
        destino = SALIDA / f"{info['enviado'][:10].replace('-', '')}-batch_{info['modelo']}.jsonl"
        tin = tcache = tout = 0
        errores = []
        with destino.open("w", encoding="utf-8") as fh:
            for res in client.messages.batches.results(lote_id):
                if res.result.type != "succeeded":
                    errores.append((res.custom_id, res.result.type))
                    continue
                msg = res.result.message
                if msg.stop_reason != "end_turn":
                    errores.append((res.custom_id, msg.stop_reason))
                    continue
                u = msg.usage
                tin += u.input_tokens + (u.cache_creation_input_tokens or 0)
                tcache += u.cache_read_input_tokens or 0
                tout += u.output_tokens
                d = meta[res.custom_id]
                codigos = json.loads(next(b.text for b in msg.content if b.type == "text"))
                fh.write(json.dumps({
                    "id": d["id"], "tipo": d["tipo"], "caso": d["caso"],
                    "modelo_solicitado": info["modelo"], "modelo_respondio": msg.model, "via": "batch", "lote": lote_id,
                    "codebook_version": CODEBOOK_VERSION, "prompt_version": PROMPT_VERSION,
                    "fecha": info["enviado"], "sha256_fuente": d["sha256_pdf_resumen"],
                    "tokens": {"entrada": u.input_tokens, "cache_lectura": u.cache_read_input_tokens, "salida": u.output_tokens},
                    **codigos,
                }, ensure_ascii=False) + "\n")
        pin, pout = PRECIOS[info["modelo"]]
        costo = 0.5 * (tin * pin + tcache * pin * 0.1 + tout * pout) / 1e6
        info.update(recogido=True, archivo=str(destino.relative_to(RAIZ)), costo_usd=round(costo, 2),
                    tokens={"entrada": tin, "cache": tcache, "salida": tout}, errores=errores)
        print(f"✓ {info['modelo']}: {destino.name}  costo≈US${costo:.2f}  errores={errores or 'ninguno'}")
    LOTES.write_text(json.dumps(registro, indent=2, ensure_ascii=False))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("enviar")
    e.add_argument("--modelos", nargs="+", default=["claude-opus-5-5"], choices=sorted(PRECIOS))
    e.add_argument("--limite", type=int)
    sub.add_parser("recoger")
    args = ap.parse_args()
    enviar(args.modelos, args.limite) if args.cmd == "enviar" else recoger()


if __name__ == "__main__":
    sys.exit(main())
