#!/usr/bin/env python3
"""Arma la historieta de un flujo en la casa del Gran Harness.

Uso:
    python3 build.py historia.json salida.html

Lee el JSON de la historia (formato en references/formato.md), lo valida y
escribe un HTML autocontenido. Solo usa la biblioteca estándar de Python.
Sale con código 1 y una lista de errores si el JSON no es válido.
"""
import json
import sys
from pathlib import Path

PIEZAS = {
    "vos", "mente", "reglamento", "caja", "mensajero", "cuaderno", "biblio", "arenero",
    "inspectora", "portero", "camara", "examinador", "skills", "mcp", "sub",
    "grafo", "memlarga",
}
# Alias en castellano para que el JSON sea fácil de escribir.
ALIAS = {
    "usuario": "vos", "usuaria": "vos", "genia": "mente", "modelo": "mente",
    "instrucciones": "reglamento", "system_prompt": "reglamento", "reglas": "reglamento",
    "tools": "caja", "herramientas": "caja", "loop": "mensajero",
    "memoria": "cuaderno", "bibliotecaria": "biblio", "contexto": "biblio",
    "patio": "arenero", "sandbox": "arenero", "verificacion": "inspectora",
    "permisos": "portero", "observabilidad": "camara", "examinadora": "examinador",
    "evals": "examinador", "recetario": "skills", "enchufe": "mcp",
    "otras_genias": "sub", "subagentes": "sub", "plano": "grafo",
    "archivo": "memlarga", "memoria_largo_plazo": "memlarga",
}
ESTADOS = {"ok", "mejorar", "incompleto", "falla", "revisar", "ausente"}
TIPOS = {"observado", "inferido", "sin_evidencia"}
MOODS = {"happy", "neutral", "think", "worried", "surprised", "confused", "talk"}
PRIORIDADES = {"alta", "media", "baja"}
QUIEN = {"agente", "humano"}


def pid(x):
    if not isinstance(x, str):
        return x
    k = x.strip().lower().replace(" ", "_").replace("-", "_")
    return ALIAS.get(k, k)


def validar(s):
    err, warn = [], []
    for campo in ("titulo", "pedido", "piezas", "vinietas"):
        if not s.get(campo):
            err.append(f"Falta el campo «{campo}».")
    if s.get("modo", "plan") not in ("traza", "plan"):
        err.append("«modo» tiene que ser «traza» (ejecución real) o «plan» (simulación).")

    piezas = {}
    for k, v in (s.get("piezas") or {}).items():
        k2 = pid(k)
        if k2 not in PIEZAS:
            err.append(f"Pieza desconocida: «{k}».")
            continue
        if k2 in ("vos", "mente"):
            warn.append(f"«{k}» no es una pieza del harness: se ignora en el diagnóstico.")
            continue
        if not isinstance(v, dict):
            err.append(f"La pieza «{k}» tiene que ser un objeto.")
            continue
        e = v.get("estado")
        if e not in ESTADOS:
            err.append(f"«{k}»: estado «{e}» no válido. Usá uno de: {', '.join(sorted(ESTADOS))}.")
        t = v.get("tipo")
        if t is not None and t not in TIPOS:
            err.append(f"«{k}»: tipo de evidencia «{t}» no válido. Usá: {', '.join(sorted(TIPOS))}.")
        if e == "ok" and t != "observado":
            err.append(f"«{k}» está en «ok» sin evidencia observada. Marcala como «revisar» o agregá evidencia con tipo «observado».")
        if e in ("falla", "incompleto", "mejorar") and not v.get("accion"):
            warn.append(f"«{k}» está en «{e}» pero no dice qué hacer («accion»).")
        if not v.get("nota"):
            warn.append(f"«{k}» no tiene «nota».")
        piezas[k2] = v
    s["piezas"] = piezas

    viñetas = s.get("vinietas") or []
    if viñetas and not 4 <= len(viñetas) <= 20:
        warn.append(f"Hay {len(viñetas)} viñetas; lo ideal es entre 6 y 14.")
    presentes = set(piezas) | {"vos", "mente"}
    for i, b in enumerate(viñetas, 1):
        if not isinstance(b, dict):
            err.append(f"Viñeta {i}: tiene que ser un objeto.")
            continue
        for k in ("a", "b", "pieza"):
            if k in b:
                b[k] = pid(b[k])
        if b.get("b") in (None, ""):
            b.pop("b", None)
        sp = b.get("habla", b.get("sp", "a"))
        b["sp"] = sp
        b.pop("habla", None)
        if sp not in ("a", "b"):
            err.append(f"Viñeta {i}: «habla» tiene que ser «a» o «b».")
        for k in ("a", "b"):
            if k in b:
                if b[k] not in PIEZAS:
                    err.append(f"Viñeta {i}: personaje «{b[k]}» desconocido.")
                elif b[k] not in presentes:
                    err.append(f"Viñeta {i}: «{b[k]}» aparece pero no está en «piezas». Agregala (aunque sea con estado «ausente»).")
                elif piezas.get(b[k], {}).get("estado") == "ausente":
                    err.append(f"Viñeta {i}: «{b[k]}» está ausente y no puede actuar. Contalo desde el Narrador o desde otro personaje.")
        if "a" not in b:
            err.append(f"Viñeta {i}: falta «a» (el primer personaje).")
        if sp == "b" and "b" not in b:
            err.append(f"Viñeta {i}: habla «b» pero no hay personaje «b».")
        if not b.get("dice") and not b.get("say"):
            err.append(f"Viñeta {i}: falta «dice» (lo que dice quien habla).")
        b["say"] = b.pop("dice", b.get("say"))
        if "reaccion" in b:
            b["re"] = b.pop("reaccion")
        if "nota" in b:
            b["note"] = b.pop("nota")
        if b.get("mono") is True:
            b["mono"] = 1
        if "animo_a" in b:
            b["ma"] = b.pop("animo_a")
        if "animo_b" in b:
            b["mb"] = b.pop("animo_b")
        for k in ("ma", "mb"):
            if k in b and b[k] not in MOODS:
                err.append(f"Viñeta {i}: ánimo «{b[k]}» no válido. Usá: {', '.join(sorted(MOODS))}.")
        if b.get("estado") and b["estado"] not in ESTADOS:
            err.append(f"Viñeta {i}: estado «{b['estado']}» no válido.")
        if b.get("pieza") and b["pieza"] not in piezas:
            err.append(f"Viñeta {i}: «pieza» «{b['pieza']}» no está en «piezas».")
        if b.get("estado") and not (b.get("alerta") or b.get("pieza")):
            warn.append(f"Viñeta {i}: tiene estado pero no «alerta» ni «pieza»; la alerta va a quedar vacía.")
        if len(b.get("narrador", "")) > 220:
            warn.append(f"Viñeta {i}: el Narrador tiene {len(b['narrador'])} caracteres; conviene no pasar de 200.")
        if len(b.get("say") or "") > 240:
            warn.append(f"Viñeta {i}: el globo tiene {len(b['say'])} caracteres; conviene no pasar de 200.")

    pasos = s.get("proximos_pasos") or []
    for i, p in enumerate(pasos, 1):
        if not p.get("accion"):
            err.append(f"Paso {i}: falta «accion».")
        if p.get("pieza"):
            p["pieza"] = pid(p["pieza"])
            if p["pieza"] not in PIEZAS:
                err.append(f"Paso {i}: pieza «{p['pieza']}» desconocida.")
        if p.get("prioridad") and p["prioridad"] not in PRIORIDADES:
            err.append(f"Paso {i}: prioridad tiene que ser alta, media o baja.")
        if p.get("quien") and p["quien"] not in QUIEN:
            err.append(f"Paso {i}: «quien» tiene que ser «agente» o «humano».")
    problemas = [k for k, v in piezas.items() if v.get("estado") in ("falla", "incompleto", "ausente", "revisar")]
    if problemas and not pasos:
        warn.append("Hay piezas con problemas pero no hay «proximos_pasos».")
    return err, warn


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    try:
        story = json.loads(src.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"El JSON no es válido: {e}")
        sys.exit(1)
    err, warn = validar(story)
    for w in warn:
        print("Aviso:", w)
    if err:
        print("\nNo se generó el HTML. Corregí esto:")
        for e in err:
            print(" -", e)
        sys.exit(1)
    tpl = (Path(__file__).resolve().parent.parent / "assets" / "template.html").read_text(encoding="utf-8")
    data = json.dumps(story, ensure_ascii=False).replace("</", "<\\/")
    title = story["titulo"].replace("&", "&amp;").replace("<", "&lt;")
    html = tpl.replace("/*STORY*/", data, 1).replace("__TITLE__", title, 1)
    out.write_text(html, encoding="utf-8")
    n = len(story["piezas"])
    print(f"Listo: {out} ({len(story['vinietas'])} viñetas, {n} piezas diagnosticadas).")


if __name__ == "__main__":
    main()
