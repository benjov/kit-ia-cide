#!/usr/bin/env python3
"""
codificar_api.py — Codifica el corpus con Claude vía API, aplicando el codebook.

OPCIONAL (carril B). En la sesión se hace lo mismo sin código, con el skill en Cowork.
Este script existe para que el caso completo sea reproducible y auditable:
cada corrida guarda modelo, versión del codebook, versión del prompt, tokens y costo.

Uso:
  # Pon tu key en un archivo .env en la raíz del kit:  ANTHROPIC_API_KEY=sk-ant-...
  # (o exporta la variable ANTHROPIC_API_KEY en tu terminal)
  python scripts/codificar_api.py --limite 3                     # prueba con 3 documentos
  python scripts/codificar_api.py                                # todo el corpus, Opus 5.5
  python scripts/codificar_api.py --modelo claude-haiku-5-5      # mismo corpus, otro modelo
  python scripts/codificar_api.py --ids AI-148-2017 AR-1064-2019 # documentos específicos

Salida: caso-completo/04-resultados/corridas/<fecha>_<modelo>.jsonl  (una línea por documento)
        y un resumen en pantalla con tokens y costo estimado.

Requisitos: pip install anthropic
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
from pathlib import Path

import anthropic

RAIZ = Path(__file__).resolve().parent.parent

# Lee ANTHROPIC_API_KEY de un archivo .env en la raíz del kit, si existe (nunca se sube a git).
_env = RAIZ / ".env"
if _env.exists():
    for _linea in _env.read_text(encoding="utf-8").splitlines():
        if "=" in _linea and not _linea.lstrip().startswith("#"):
            _k, _v = _linea.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))
CODEBOOK = RAIZ / "caso-completo" / "01-codebook.md"
PROMPT = RAIZ / "caso-completo" / "02-prompt" / "system-prompt.md"
MANIFIESTO = RAIZ / "corpus" / "manifiesto_emblematicas.csv"
SALIDA = RAIZ / "caso-completo" / "04-resultados" / "corridas"

PROMPT_VERSION = "1.0"
CODEBOOK_VERSION = "1.1"

# Precios por millón de tokens (USD, entrada/salida). Verifica en https://claude.com/pricing
PRECIOS = {
    "claude-opus-5-5": (4.00, 20.00),
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-haiku-5-5": (0.10, 0.50),
}
CON_FALLBACK = {"claude-opus-5-5", "claude-sonnet-5-5"}

VARIABLES = {
    "promovente": ["persona", "colectivo", "organo_autonomo", "fiscalia", "actor_politico", "autoridad", "no_identificable"],
    "resultado": ["protege", "no_protege", "mixto", "otro"],
    "derecho_principal": ["igualdad_no_discriminacion", "derechos_sexuales_reproductivos", "libertad_expresion_informacion",
                          "debido_proceso_acceso_justicia", "libertad_integridad_personal", "salud", "pueblos_indigenas",
                          "medio_ambiente", "ninez", "familia", "trabajo_seguridad_social", "privacidad_datos", "otro"],
    "fuentes_internacionales": ["ninguna", "tratados", "corte_idh", "otra_jurisprudencia"],
    "proporcionalidad": ["si", "no"],
    "perspectiva_genero": ["si", "no"],
}


def esquema() -> dict:
    """JSON Schema que obliga a Claude a responder exactamente con el formato del codebook."""
    def var(codigos: list[str]) -> dict:
        return {
            "type": "object",
            "properties": {
                "codigo": {"type": "string", "enum": codigos},
                "cita": {"type": "string"},
                "confianza": {"type": "string", "enum": ["alta", "media", "baja"]},
            },
            "required": ["codigo", "cita", "confianza"],
            "additionalProperties": False,
        }
    props = {k: var(v) for k, v in VARIABLES.items()}
    props["nota"] = {"type": "string"}
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


def codificar(client: anthropic.Anthropic, modelo: str, system: str, doc_id: str, texto: str) -> tuple[dict, object]:
    kwargs = dict(
        model=modelo,
        max_tokens=4000,
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],  # codebook en caché
        messages=[{"role": "user", "content": f"<documento id=\"{doc_id}\">\n{texto}\n</documento>\n\nCodifica este documento según el codebook."}],
        output_config={"effort": "medium", "format": {"type": "json_schema", "schema": esquema()}},
    )
    if modelo in CON_FALLBACK:
        # Si el modelo declina por un falso positivo de seguridad, la API reintenta con otro modelo.
        resp = client.beta.messages.create(betas=["server-side-fallback-2026-07-01"], fallbacks="default", **kwargs)
    else:
        resp = client.messages.create(**kwargs)
    if resp.stop_reason == "refusal":
        raise RuntimeError(f"El modelo declinó codificar {doc_id}")
    if resp.stop_reason == "max_tokens":
        raise RuntimeError(f"Respuesta truncada en {doc_id}; sube max_tokens")
    texto_json = next(b.text for b in resp.content if b.type == "text")
    return json.loads(texto_json), resp


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--modelo", default="claude-opus-5-5", choices=sorted(PRECIOS))
    ap.add_argument("--limite", type=int, help="codificar solo los primeros N documentos")
    ap.add_argument("--ids", nargs="*", help="codificar solo estos IDs")
    args = ap.parse_args()

    system = PROMPT.read_text(encoding="utf-8").replace("{{CODEBOOK}}", CODEBOOK.read_text(encoding="utf-8"))
    docs = [r for r in csv.DictReader(MANIFIESTO.open(encoding="utf-8")) if r["archivo_resumen"]]
    if args.ids:
        docs = [d for d in docs if d["id"] in set(args.ids)]
    if args.limite:
        docs = docs[: args.limite]
    if not docs:
        sys.exit("No hay documentos que codificar.")

    SALIDA.mkdir(parents=True, exist_ok=True)
    marca = dt.datetime.now().strftime("%Y%m%d-%H%M")
    destino = SALIDA / f"{marca}_{args.modelo}.jsonl"
    client = anthropic.Anthropic()
    tin = tout = tcache = 0
    errores = []

    with destino.open("w", encoding="utf-8") as fh:
        for i, d in enumerate(docs, 1):
            texto = (RAIZ / d["archivo_resumen"]).read_text(encoding="utf-8")
            try:
                codigos, resp = codificar(client, args.modelo, system, d["id"], texto)
            except (anthropic.APIStatusError, anthropic.APIConnectionError, RuntimeError, json.JSONDecodeError) as e:
                errores.append((d["id"], str(e)))
                print(f"[{i}/{len(docs)}] ✗ {d['id']}: {e}")
                continue
            u = resp.usage
            tin += u.input_tokens + (u.cache_creation_input_tokens or 0)
            tcache += u.cache_read_input_tokens or 0
            tout += u.output_tokens
            registro = {
                "id": d["id"], "tipo": d["tipo"], "caso": d["caso"],
                "modelo_solicitado": args.modelo, "modelo_respondio": resp.model,
                "codebook_version": CODEBOOK_VERSION, "prompt_version": PROMPT_VERSION,
                "fecha": dt.datetime.now().isoformat(timespec="seconds"),
                "sha256_fuente": d["sha256_pdf_resumen"],
                "tokens": {"entrada": u.input_tokens, "cache_lectura": u.cache_read_input_tokens, "salida": u.output_tokens},
                **codigos,
            }
            fh.write(json.dumps(registro, ensure_ascii=False) + "\n")
            print(f"[{i}/{len(docs)}] ✓ {d['id']}  resultado={codigos['resultado']['codigo']}")

    pin, pout = PRECIOS[args.modelo]
    costo = (tin * pin + tcache * pin * 0.1 + tout * pout) / 1e6
    print(f"\nSalida: {destino.relative_to(RAIZ)}")
    print(f"Tokens: entrada={tin:,}  caché={tcache:,}  salida={tout:,}  →  costo estimado ≈ US${costo:.2f}")
    if errores:
        print(f"Errores ({len(errores)}): " + ", ".join(e[0] for e in errores))


if __name__ == "__main__":
    main()
