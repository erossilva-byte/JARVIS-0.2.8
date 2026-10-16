#!/usr/bin/env python3
"""Add JitPack to the app module repositories, which take precedence in this project."""
import re
import sys
from pathlib import Path

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("android/app/build.gradle")
if not path.exists():
    raise SystemExit(f"Arquivo Gradle não encontrado: {path}")
text = path.read_text(encoding="utf-8")
url = "https://jitpack.io"
if url in text:
    print(f"JitPack já está configurado no módulo: {path}")
    raise SystemExit(0)

# Find a top-level repositories block, or add one before dependencies.
match = re.search(r"(?m)^repositories\s*\{", text)
if match:
    opening = text.find("{", match.start())
    depth = 0
    closing = None
    for i in range(opening, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                closing = i
                break
    if closing is None:
        raise SystemExit(f"Bloco repositories incompleto em {path}")
    body = text[opening + 1:closing]
    if "google()" not in body:
        body = "\n    google()" + body
    if "mavenCentral()" not in body:
        body += "\n    mavenCentral()\n"
    body += '    maven { url "https://jitpack.io" }\n'
    text = text[:opening + 1] + body + text[closing:]
else:
    block = 'repositories {\n    google()\n    mavenCentral()\n    maven { url "https://jitpack.io" }\n}\n\n'
    dep = re.search(r"(?m)^dependencies\s*\{", text)
    if dep:
        text = text[:dep.start()] + block + text[dep.start():]
    else:
        text = block + text

path.write_text(text, encoding="utf-8")
print(f"JitPack adicionado aos repositórios do módulo Android: {path}")
