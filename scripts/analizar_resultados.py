#!/usr/bin/env python3
"""
analizar_resultados.py — Del JSONL de codificación a las tablas del caso y los datos del sitio.

Hace, en este orden:
  1. Carga las corridas batch de cada modelo y la codificación humana SIMULADA.
  2. Verifica citas por modelo (control 2 del protocolo).
  3. Acuerdo: kappa de cada modelo vs. la referencia simulada (20 docs) y entre modelos (102 docs).
  4. Hallazgos: tablas cruzadas control abstracto vs. concreto con prueba exacta de Fisher.
  5. Escribe caso-completo/04-resultados/*.csv y docs/data/*.json (+ textos para el auditor).

Uso:  python scripts/analizar_resultados.py
Requisitos: solo Python 3.10+.
"""
from __future__ import annotations

import csv
import json
import math
import shutil
from collections import Counter
from itertools import combinations
from pathlib import Path

from calcular_acuerdo import kappa
from verificar_citas import AUSENCIA, VARIABLES, marca_parrafo, normalizar

RAIZ = Path(__file__).resolve().parent.parent
CORRIDAS = RAIZ / "caso-completo" / "04-resultados" / "corridas"
RES = RAIZ / "caso-completo" / "04-resultados"
VAL = RAIZ / "caso-completo" / "05-validacion"
DATA = RAIZ / "docs" / "data"
MODELOS = {"claude-opus-5-5": "Opus 5.5", "claude-sonnet-5-5": "Sonnet 5.5", "claude-haiku-5-5": "Haiku 5.5"}
PRINCIPAL = "claude-opus-5-5"
PRECIOS = {"claude-opus-5-5": (4.00, 20.00), "claude-sonnet-5-5": (2.00, 10.00), "claude-haiku-5-5": (0.10, 0.50)}  # USD/millón

# Variable → código que define la proporción "sí" para la prueba de Fisher
BINARIAS = {
    "proporcionalidad": ("si", "Aplica test de proporcionalidad"),
    "fuentes_internacionales": ("corte_idh", "Cita a la Corte IDH"),
    "perspectiva_genero": ("si", "Declara perspectiva de género"),
    "resultado": ("protege", "Resultado: protege el derecho"),
}


def control(tipo: str) -> str:
    return "abstracto" if tipo == "AI" else "concreto" if tipo in ("AR", "ADR", "AD") else "otro"


def fisher_bilateral(a: int, b: int, c: int, d: int) -> float:
    """Prueba exacta de Fisher bilateral para la tabla [[a, b], [c, d]]."""
    n1, n2, k, n = a + b, c + d, a + c, a + b + c + d
    def p(x: int) -> float:
        return math.comb(n1, x) * math.comb(n2, k - x) / math.comb(n, k)
    obs = p(a)
    return min(1.0, sum(p(x) for x in range(max(0, k - n2), min(k, n1) + 1) if p(x) <= obs * (1 + 1e-9)))


def cargar_corridas() -> dict[str, dict[str, dict]]:
    out = {}
    for m in MODELOS:
        archivos = sorted(CORRIDAS.glob(f"*batch_{m}.jsonl"))
        if archivos:
            out[m] = {r["id"]: r for r in map(json.loads, archivos[-1].read_text(encoding="utf-8").splitlines())}
    return out


def main() -> None:
    corr = cargar_corridas()
    manifiesto = {r["id"]: r for r in csv.DictReader((RAIZ / "corpus" / "manifiesto_emblematicas.csv").open(encoding="utf-8"))}
    gold = {r["id"]: r for r in csv.DictReader((VAL / "gold-standard-SIMULADO.csv").open(encoding="utf-8"))}
    textos = {i: (RAIZ / "corpus" / "resumenes" / f"{i}.txt").read_text(encoding="utf-8") for i in manifiesto}
    textos_norm = {i: normalizar(t) for i, t in textos.items()}
    resumen = {"modelos": [], "kappa_vs_referencia": [], "acuerdo_entre_modelos": [], "hallazgos": [], "distribuciones": {}}

    # 2. Citas y costos por modelo
    lotes = json.loads((CORRIDAS / "lotes.json").read_text())
    costos = {v["modelo"]: v for v in lotes.values() if v.get("recogido")}
    for m, docs in corr.items():
        ok = mal = 0
        for i, r in docs.items():
            for v in VARIABLES:
                cita = (r[v].get("cita") or "").strip()
                if cita:
                    hit = normalizar(cita) in textos_norm[i]
                    ok += hit
                    mal += not hit
                    r[v]["verificada"] = hit
                    r[v]["parrafo"] = marca_parrafo(textos[i], cita) if hit else ""
        baja = sum(r[v]["confianza"] == "baja" for r in docs.values() for v in VARIABLES)
        # Costo: del registro del lote si existe; si no, de los tokens de cada fila (aprox.: no incluye la escritura de caché)
        c = costos.get(m, {})
        if c.get("costo_usd") is None:
            pin, pout = PRECIOS[m]
            t = [r["tokens"] for r in docs.values()]
            tok = {"entrada": sum(x["entrada"] for x in t), "cache": sum(x["cache_lectura"] or 0 for x in t), "salida": sum(x["salida"] for x in t)}
            c = {"costo_usd": round(0.5 * (tok["entrada"] * pin + tok["cache"] * pin * 0.1 + tok["salida"] * pout) / 1e6, 2), "tokens": tok}
        resumen["modelos"].append({"id": m, "nombre": MODELOS[m], "n": len(docs), "citas_ok": ok, "citas_mal": mal,
                                   "pct_citas": ok / max(ok + mal, 1), "confianza_baja": baja,
                                   "costo_usd": c.get("costo_usd"), "tokens": c.get("tokens")})

    # 3a. Kappa vs referencia simulada
    for m, docs in corr.items():
        for v in VARIABLES:
            ids = [i for i in gold if i in docs]
            a = [gold[i][f"{v}_codigo"] for i in ids]
            b = [docs[i][v]["codigo"] for i in ids]
            resumen["kappa_vs_referencia"].append({"modelo": MODELOS[m], "variable": v, "n": len(ids),
                                                   "acuerdo": sum(x == y for x, y in zip(a, b)) / len(ids), "kappa": kappa(a, b)})
    # 3b. Entre modelos
    for m1, m2 in combinations(corr, 2):
        for v in VARIABLES:
            ids = sorted(set(corr[m1]) & set(corr[m2]))
            a = [corr[m1][i][v]["codigo"] for i in ids]
            b = [corr[m2][i][v]["codigo"] for i in ids]
            resumen["acuerdo_entre_modelos"].append({"par": f"{MODELOS[m1]} – {MODELOS[m2]}", "variable": v, "n": len(ids),
                                                     "acuerdo": sum(x == y for x, y in zip(a, b)) / len(ids), "kappa": kappa(a, b)})

    # 4. Hallazgos con el modelo principal
    P = corr[PRINCIPAL]
    for v, (codigo, etiqueta) in BINARIAS.items():
        g = {k: [r for r in P.values() if control(r["tipo"]) == k] for k in ("abstracto", "concreto")}
        a = sum(r[v]["codigo"] == codigo for r in g["abstracto"]); na = len(g["abstracto"])
        c = sum(r[v]["codigo"] == codigo for r in g["concreto"]); nc = len(g["concreto"])
        resumen["hallazgos"].append({"variable": v, "codigo": codigo, "etiqueta": etiqueta,
                                     "abstracto": {"si": a, "n": na}, "concreto": {"si": c, "n": nc},
                                     "p_fisher": fisher_bilateral(a, na - a, c, nc - c)})
    for v in VARIABLES:
        resumen["distribuciones"][v] = {k: dict(Counter(r[v]["codigo"] for r in P.values() if control(r["tipo"]) == k))
                                        for k in ("abstracto", "concreto", "otro")}

    # 5a. CSV planos
    with (RES / "resultados_opus.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "tipo", "control", "caso"] + [f"{v}_{c}" for v in VARIABLES for c in ("codigo", "cita", "confianza", "parrafo")] + ["nota"])
        for i, r in sorted(P.items()):
            w.writerow([i, r["tipo"], control(r["tipo"]), r["caso"]] +
                       [r[v].get(k, "") for v in VARIABLES for k in ("codigo", "cita", "confianza", "parrafo")] + [r["nota"]])
    with (RES / "hallazgos.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["variable", "codigo", "abstracto_si", "abstracto_n", "concreto_si", "concreto_n", "p_fisher"])
        for h in resumen["hallazgos"]:
            w.writerow([h["variable"], h["codigo"], h["abstracto"]["si"], h["abstracto"]["n"], h["concreto"]["si"], h["concreto"]["n"], f"{h['p_fisher']:.3f}"])
    with (VAL / "confiabilidad.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["modelo", "variable", "n", "acuerdo", "kappa"])
        w.writeheader()
        w.writerows({**k, "acuerdo": round(k["acuerdo"], 3), "kappa": round(k["kappa"], 3)} for k in resumen["kappa_vs_referencia"])

    # 5b. Datos del sitio
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "textos").mkdir(exist_ok=True)
    cod = {"codificadores": [{"id": m, "nombre": f"Claude {MODELOS[m]}"} for m in corr] +
                            [{"id": "humano_simulado", "nombre": "Referencia humana (SIMULADA)"}], "docs": {}}
    for i, d in manifiesto.items():
        shutil.copy(RAIZ / "corpus" / "resumenes" / f"{i}.txt", DATA / "textos" / f"{i}.txt")
        entrada = {"tipo": d["tipo"], "caso": d["caso"], "titulo": d["titulo"], "url_resumen": d["url_resumen"],
                   "url_sentencia": d["url_sentencia"], "cod": {}}
        for m in corr:
            if i in corr[m]:
                entrada["cod"][m] = {**{v: corr[m][i][v] for v in VARIABLES}, "nota": corr[m][i]["nota"]}
        if i in gold:
            entrada["cod"]["humano_simulado"] = {v: {"codigo": gold[i][f"{v}_codigo"], "cita": "", "confianza": ""} for v in VARIABLES}
            entrada["cod"]["humano_simulado"]["nota"] = "Codificación humana SIMULADA (didáctica). No incluye citas."
        cod["docs"][i] = entrada
    (DATA / "codificaciones.json").write_text(json.dumps(cod, ensure_ascii=False), encoding="utf-8")
    (DATA / "resumen.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=1), encoding="utf-8")
    (DATA / "costos_reales.json").write_text(json.dumps(
        [{"modelo": x["nombre"], "costo_usd": x["costo_usd"] or 0, "n": x["n"]} for x in resumen["modelos"]], ensure_ascii=False))

    # Reporte en pantalla
    for x in resumen["modelos"]:
        print(f"{x['nombre']:<11} citas {x['citas_ok']}/{x['citas_ok'] + x['citas_mal']} ({x['pct_citas']:.1%})  conf.baja={x['confianza_baja']}  costo=US${x['costo_usd']}")
    print("\nKappa vs referencia SIMULADA (n=20):")
    for k in resumen["kappa_vs_referencia"]:
        print(f"  {k['modelo']:<11} {k['variable']:<24} {k['kappa']:.2f}")
    print("\nAcuerdo entre modelos (n=102):")
    for k in resumen["acuerdo_entre_modelos"]:
        print(f"  {k['par']:<24} {k['variable']:<24} acuerdo={k['acuerdo']:.0%} kappa={k['kappa']:.2f}")
    print("\nHallazgos (Opus):")
    for h in resumen["hallazgos"]:
        print(f"  {h['etiqueta']:<34} abstracto {h['abstracto']['si']}/{h['abstracto']['n']}  concreto {h['concreto']['si']}/{h['concreto']['n']}  p={h['p_fisher']:.3f}")


if __name__ == "__main__":
    main()
