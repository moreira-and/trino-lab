#!/usr/bin/env python3
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
TEMPLATE_DIR = ROOT / "single" / "etc" / "templates"
OUTPUT_DIR = ROOT / "single" / "etc"

PLACEHOLDER_PATTERN = re.compile(r"\$\{([^}]+)\}")


def load_env(path: Path):
    env = {}
    if not path.exists():
        return env
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()
    return env


def substitute(text: str, env: dict):
    def repl(match):
        name = match.group(1)
        return env.get(name, os.getenv(name, ""))
    return PLACEHOLDER_PATTERN.sub(repl, text)


def render_template(source: Path, target: Path, env: dict):
    content = source.read_text()
    content = substitute(content, env)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    print(f"Rendered {source.relative_to(ROOT)} -> {target.relative_to(ROOT)}")


def main():
    env = load_env(ENV_PATH)
    env = {**os.environ, **env}

    templates = [
        (TEMPLATE_DIR / "config.properties.template", OUTPUT_DIR / "config.properties"),
        (TEMPLATE_DIR / "catalog" / "iceberg.properties.template", OUTPUT_DIR / "catalog" / "iceberg.properties"),
        (TEMPLATE_DIR / "catalog" / "postgresql.properties.template", OUTPUT_DIR / "catalog" / "postgresql.properties"),
    ]

    for source, target in templates:
        if not source.exists():
            raise FileNotFoundError(f"Template not found: {source}")
        render_template(source, target, env)

    print("\nConfig files generated successfully. Services can now start.")


if __name__ == "__main__":
    main()

