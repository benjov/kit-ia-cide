#!/usr/bin/env python3
"""
calcular_acuerdo.py — Confiabilidad entre codificadores y métricas de evaluación por variable.

Compara dos codificaciones del mismo conjunto de documentos (humano vs. Claude,
o modelo A vs. modelo B) y reporta, por variable:
  · N y % de acuerdo;
  · kappa de Cohen con un intervalo de confianza del 95% (bootstrap, semilla fija);
  · alfa de Krippendorff (nominal) y AC1 de Gwet (menos sensible a la prevalencia);
  · la interpretación del kappa (Landis y Koch, 1977) y, con --desacuerdos, cada desacuerdo.
Con --detalle, además, tomando A como referencia (pon primero la hoja humana):
  · la matriz de confusión;
  · precisión, exhaustividad (recall) y F1 por código, y F1 macro;
  · el % de acuerdo según la confianza que declaró el modelo (si B la trae: .jsonl o columnas `<variable>_confianza`).
Las definiciones, con ejemplos, están en docs/conceptos.html#metricas.

Uso:
  python scripts/calcular_acuerdo.py A.csv B.jsonl
  python scripts/calcular_acuerdo.py caso-completo/05-validacion/gold-standard-SIMULADO.csv \\
         caso-completo/04-resultados/corridas/<opus>.jsonl --desacuerdos
  python scripts/calcular_acuerdo.py mi-hoja.csv resultados.csv --detalle   # matriz, F1, confianza

Formatos aceptados: .jsonl de codificar_api.py, o .csv con columna `id` y columnas
`<variable>_codigo` (o `<variable>` a secas, solo para las variables del caso).
**Detecta solas las variables**: no hay que editar el script para una variable nueva.
Acepta CSV separados por coma o por punto y coma (Excel en español), con o sin BOM.
Solo se comparan los IDs y las variables presentes en ambos archivos.

Si la hoja humana conserva el encabezado genérico (`variable_codigo`) y la de Claude usa
el nombre real (`evidencia_codigo`), empareja con --renombrar variable=evidencia.

Si lo ejecuta Claude dentro de un skill (Cowork o Chat con ejecución de código), tú no
necesitas instalar Python.
Requisitos: solo Python 3.10+.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from collections import Counter
from pathlib import Path

VARIABLES = ["promovente", "resultado", "derecho_principal", "fuentes_internacionales", "proporcionalidad", "perspectiva_genero"]


def leer_csv(path: Path) -> list[dict]:
    """Lee un CSV tolerando BOM y separador ';' (Excel en español)."""
    texto = path.read_text(encoding="utf-8-sig")
    primera = texto.splitlines()[0] if texto else ""
    sep = ";" if primera.count(";") > primera.count(",") else ","
    return [{(k or "").strip(): (v or "") for k, v in r.items()} for r in csv.DictReader(texto.splitlines(), delimiter=sep)]


CONFIANZAS: dict[tuple[str, str, str], str] = {}   # (archivo, id, variable) → confianza, si el archivo la trae


def cargar(path: Path, renombrar: dict[str, str] | None = None) -> dict[str, dict[str, str]]:
    renombrar = renombrar or {}
    out: dict[str, dict[str, str]] = {}
    if path.suffix == ".jsonl":
        for l in path.read_text(encoding="utf-8").splitlines():
            if l.strip():
                r = json.loads(l)
                out[r["id"]] = {renombrar.get(k, k): x["codigo"] for k, x in r.items() if isinstance(x, dict) and "codigo" in x}
                for k, x in r.items():
                    if isinstance(x, dict) and x.get("confianza"):
                        CONFIANZAS[(str(path), r["id"], renombrar.get(k, k))] = x["confianza"]
    else:
        for r in leer_csv(path):
            fila: dict[str, str] = {}
            for col, val in r.items():
                if col.endswith("_codigo"):
                    v = col[: -len("_codigo")]
                elif col in VARIABLES:
                    v = col
                else:
                    continue
                if val.strip():
                    fila[renombrar.get(v, v)] = val.strip()
            for col, val in r.items():
                if col.endswith("_confianza") and val.strip():
                    CONFIANZAS[(str(path), r["id"].strip(), renombrar.get(col[: -len("_confianza")], col[: -len("_confianza")]))] = val.strip()
            out[r["id"].strip()] = fila
    return out


def kappa(a: list[str], b: list[str]) -> float:
    """Kappa de Cohen. Si los dos usan un único código idéntico (azar = 1), devuelve 1.0."""
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def kappa_ic(a: list[str], b: list[str], reps: int = 2000, semilla: int = 2026) -> tuple[float, float] | None:
    """IC 95% del kappa por bootstrap de percentiles: remuestrea documentos con reemplazo.
    Omite las remuestras sin variación (kappa indefinido). Con n muy chico el intervalo es
    muy ancho, y ese es justamente el mensaje."""
    n = len(a)
    # Si uno de los dos usa un solo código en todos los documentos, el bootstrap no puede
    # mostrar variación (da [0, 0] o [1, 1] siempre): mejor no reportar intervalo.
    if n < 2 or len(set(a)) < 2 or len(set(b)) < 2:
        return None
    rng = random.Random(semilla)
    ks = []
    for _ in range(reps):
        idx = [rng.randrange(n) for _ in range(n)]
        ra, rb = [a[i] for i in idx], [b[i] for i in idx]
        ca, cb = Counter(ra), Counter(rb)
        pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
        if pe < 1:
            po = sum(x == y for x, y in zip(ra, rb)) / n
            ks.append((po - pe) / (1 - pe))
    if len(ks) < reps / 2:
        return None
    ks.sort()
    return ks[int(0.025 * len(ks))], ks[min(len(ks) - 1, int(0.975 * len(ks)))]


def alfa_nominal(a: list[str], b: list[str]) -> float:
    """Alfa de Krippendorff para dos codificadores, datos nominales y sin faltantes:
    α = 1 − D_observado / D_esperado, con el azar estimado de los valores de ambos juntos."""
    n = 2 * len(a)
    desacuerdos = sum(x != y for x, y in zip(a, b))
    marg = Counter(a) + Counter(b)
    esperado = n * n - sum(c * c for c in marg.values())
    return 1.0 if esperado == 0 else 1 - (n - 1) * 2 * desacuerdos / esperado


def ac1_gwet(a: list[str], b: list[str]) -> float:
    """AC1 de Gwet (2008): el azar se estima como π_k(1 − π_k), que es pequeño cuando una
    categoría domina; por eso no se desploma con prevalencias extremas como el kappa.
    Q = número de códigos observados en la variable."""
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    marg = Counter(a) + Counter(b)
    q = len(marg)
    if q < 2:
        return 1.0
    pe = sum((c / (2 * n)) * (1 - c / (2 * n)) for c in marg.values()) / (q - 1)
    return (po - pe) / (1 - pe)


def por_codigo(ref: list[str], otro: list[str]) -> list[dict]:
    """Precisión, exhaustividad (recall) y F1 de cada código, tomando `ref` como la verdad."""
    filas = []
    for c in sorted(set(ref) | set(otro)):
        vp = sum(r == c and o == c for r, o in zip(ref, otro))
        marcados, reales = otro.count(c), ref.count(c)
        p = vp / marcados if marcados else None
        r = vp / reales if reales else None
        # F1 = 0 si el código existe en la referencia y B nunca lo acierta (aunque nunca lo use).
        f1 = 2 * p * r / (p + r) if p and r else (0.0 if reales else None)
        filas.append({"codigo": c, "reales": reales, "marcados": marcados, "precision": p, "recall": r, "f1": f1})
    return filas


def detalle(v: str, a: list[str], b: list[str], ids: list[str], conf: dict[str, str]) -> float | None:
    """Imprime matriz de confusión, métricas por código y acuerdo por confianza. Devuelve el F1 macro."""
    codigos = sorted(set(a) | set(b))
    ancho = max(8, *(len(c) for c in codigos)) + 1
    col = max(5, len(str(len(codigos))) + 3)
    print(f"\n  ── {v}: matriz de confusión (filas = A, referencia · columnas = B, con el número del código)")
    print("  " + " " * (ancho + 5) + "".join(f"{'[' + str(j) + ']':>{col}}" for j in range(1, len(codigos) + 1)))
    for j, ca in enumerate(codigos, 1):
        celdas = "".join(f"{sum(x == ca and y == cb for x, y in zip(a, b)):>{col}}" for cb in codigos)
        print(f"  {'[' + str(j) + ']':>4} {ca:<{ancho}}{celdas}")
    print("  La diagonal son los acuerdos; fuera de ella, qué confunde B con qué.")
    f = lambda x: "   —" if x is None else f"{x:>4.2f}"
    print(f"\n  {'código':<{ancho}}{'en A':>6}{'en B':>6}  precisión  recall    F1")
    filas = por_codigo(a, b)
    for r in filas:
        print(f"  {r['codigo']:<{ancho}}{r['reales']:>6}{r['marcados']:>6}     {f(r['precision'])}   {f(r['recall'])}  {f(r['f1'])}")
    f1s = [r["f1"] for r in filas if r["reales"] and r["f1"] is not None]
    macro = sum(f1s) / len(f1s) if f1s else None
    print(f"  F1 macro (promedio simple sobre los códigos presentes en A): {f(macro).strip()}")
    if conf:
        print("\n  % de acuerdo según la confianza que declaró B:")
        for nivel in ("alta", "media", "baja"):
            pares = [(x, y) for x, y, i in zip(a, b, ids) if conf.get(i) == nivel]
            if pares:
                print(f"    {nivel:<6} n={len(pares):<4} acuerdo={sum(x == y for x, y in pares) / len(pares):.0%}")
    return macro


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
    ap.add_argument("--detalle", action="store_true",
                    help="matriz de confusión, precisión/recall/F1 por código (A = referencia) y acuerdo por confianza")
    ap.add_argument("--csv", type=Path, help="guardar la tabla de confiabilidad")
    ap.add_argument("--renombrar", nargs="*", default=[], metavar="VIEJO=NUEVO",
                    help="renombrar variables al leer (p. ej. variable=evidencia)")
    args = ap.parse_args()

    ren = dict(x.split("=", 1) for x in args.renombrar)
    A, B = cargar(args.a, ren), cargar(args.b, ren)
    comunes = sorted(set(A) & set(B))
    vars_a = {v for i in A for v in A[i]}
    vars_b = {v for i in B for v in B[i]}
    variables = [v for v in VARIABLES if v in vars_a & vars_b] + sorted((vars_a & vars_b) - set(VARIABLES))
    if not comunes or not variables:
        sys.exit(f"Nada que comparar. Documentos en común: {len(comunes)}. Variables en A: {sorted(vars_a)}; "
                 f"en B: {sorted(vars_b)}. Revisa los IDs y los encabezados (o usa --renombrar).")
    print(f"A = {args.a.name}  ·  B = {args.b.name}  ·  documentos en común: {len(comunes)}\n")
    print(f"{'variable':<26}{'N':>4}{'% acuerdo':>11}{'kappa':>7}{'IC 95%':>15}{'alfa':>7}{'AC1':>7}  interpretación (kappa)")
    tabla = []
    for v in variables:
        pares = [(A[i][v], B[i][v], i) for i in comunes if v in A[i] and v in B[i]]
        if not pares:
            continue
        a, b, ids = (list(t) for t in zip(*pares))
        k = kappa(a, b)
        ic = kappa_ic(a, b)
        al, ac1 = alfa_nominal(a, b), ac1_gwet(a, b)
        acuerdo = sum(x == y for x, y in zip(a, b)) / len(a)
        ic_txt = f"[{ic[0]:.2f}, {ic[1]:.2f}]" if ic else "—"
        print(f"{v:<26}{len(a):>4}{acuerdo:>10.0%}{k:>7.2f}{ic_txt:>15}{al:>7.2f}{ac1:>7.2f}  {interpretar(k)}")
        if args.desacuerdos:
            for x, y, i in pares:
                if x != y:
                    print(f"    · {i:<16} A={x:<28} B={y}")
        macro = None
        if args.detalle:
            conf = {i: c for (f, i, vv), c in CONFIANZAS.items() if f == str(args.b) and vv == v}
            macro = detalle(v, a, b, ids, conf)
            print()
        tabla.append({"variable": v, "n": len(a), "acuerdo": round(acuerdo, 3), "kappa": round(k, 3),
                      "kappa_ic95_inf": round(ic[0], 3) if ic else "", "kappa_ic95_sup": round(ic[1], 3) if ic else "",
                      "alfa_krippendorff": round(al, 3), "ac1_gwet": round(ac1, 3),
                      "f1_macro": round(macro, 3) if macro is not None else "", "interpretacion": interpretar(k)})
    if len(comunes) < 30:
        print(f"\nCon N = {len(comunes)} los coeficientes son ilustrativos: mira el ancho del IC 95%."
              "\n(IC «—»: uno de los dos usó un solo código, y el bootstrap no puede estimar la variación.)")
    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(tabla[0]))
            w.writeheader()
            w.writerows(tabla)
        print(f"\nTabla: {args.csv}")


if __name__ == "__main__":
    main()
