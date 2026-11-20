#!/usr/bin/env python3
"""Agrega el marco común (menú y efectos: herramientas/marco.css y marco.js) a las páginas de una entidad y a la portada.

Uso: python herramientas/insertar_marco.py <id>
Las páginas del informe las genera el núcleo y se reemplazan en cada actualización; esta herramienta vuelve a poner
las dos líneas del marco en su <head>. Si una página ya las tiene, no la toca (se puede correr las veces que haga falta).
"""
import glob
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINEA = '<link rel="stylesheet" href="/herramientas/marco.css"><script src="/herramientas/marco.js"></script>\n'

eid = sys.argv[1] if len(sys.argv) > 1 else ""
if not eid or not os.path.isdir(os.path.join(RAIZ, eid)):
    sys.exit(f"Entidad desconocida: «{eid}»")
paginas = [os.path.join(RAIZ, "index.html")] + sorted(glob.glob(os.path.join(RAIZ, eid, "*.html"))) + \
    sorted(glob.glob(os.path.join(RAIZ, eid, "ro", "*.html")))
for p in paginas:
    if not os.path.isfile(p):
        continue
    s = open(p, encoding="utf-8").read()
    if "/herramientas/marco.js" in s:
        continue
    i = s.lower().find("</head>")
    if i < 0:
        print(f"sin <head>, no se cambia: {os.path.relpath(p, RAIZ)}")
        continue
    open(p, "w", encoding="utf-8").write(s[:i] + LINEA + s[i:])
    print(f"marco agregado: {os.path.relpath(p, RAIZ)}")
