#!/usr/bin/env python3
"""Ensure JitPack is configured for dependency resolution in generated Capacitor Android projects."""
import re
import sys
from pathlib import Path

android_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("android")
settings = android_dir / "settings.gradle"
if not settings.exists():
    settings = android_dir / "settings.gradle.kts"
if not settings.exists():
    raise SystemExit(f"Não encontrei settings.gradle nem settings.gradle.kts em {android_dir}")

text = settings.read_text(encoding="utf-8")
kotlin = settings.suffix == ".kts"
repo_line = 'maven { url = uri("https://jitpack.io") }' if kotlin else 'maven { url "https://jitpack.io" }'

def block_bounds(source, match):
    opening = source.find("{", match.start(), match.end() + 1)
    if opening < 0:
        opening = source.find("{", match.start())
    if opening < 0:
        return None, None
    depth = 0
    for i in range(opening, len(source)):
        if source[i] == "{":
            depth += 1
        elif source[i] == "}":
            depth -= 1
            if depth == 0:
                return opening, i
    return opening, None

drm_match = re.search(r"\bdependencyResolutionManagement\s*\{", text)
if drm_match:
    drm_open, drm_close = block_bounds(text, drm_match)
    if drm_close is None:
        raise SystemExit(f"Bloco dependencyResolutionManagement incompleto em {settings}")
    drm_body = text[drm_open + 1:drm_close]
    repos_match = re.search(r"\brepositories\s*\{", drm_body)
    if repos_match:
        repos_open, repos_close = block_bounds(drm_body, repos_match)
        if repos_close is None:
            raise SystemExit(f"Bloco repositories incompleto em {settings}")
        repos_body = drm_body[repos_open + 1:repos_close]
        if "https://jitpack.io" not in repos_body:
            insertion = drm_open + 1 + repos_open + 1
            text = text[:insertion] + "\n        " + repo_line + text[insertion:]
            settings.write_text(text, encoding="utf-8")
            print(f"JitPack adicionado ao bloco de resolução de dependências em {settings}")
        else:
            print(f"JitPack já configurado para resolução de dependências em {settings}")
    else:
        block = "\n    repositories {\n        google()\n        mavenCentral()\n        " + repo_line + "\n    }\n"
        text = text[:drm_close] + block + text[drm_close:]
        settings.write_text(text, encoding="utf-8")
        print(f"Bloco repositories criado em dependencyResolutionManagement: {settings}")
else:
    block = (
        "\n\ndependencyResolutionManagement {\n"
        "    repositories {\n"
        "        google()\n"
        "        mavenCentral()\n"
        "        " + repo_line + "\n"
        "    }\n"
        "}\n"
    )
    settings.write_text(text.rstrip() + block, encoding="utf-8")
    print(f"Bloco dependencyResolutionManagement/repositories criado em {settings}")
