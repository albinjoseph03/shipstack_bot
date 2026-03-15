from __future__ import annotations

import json
import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PROJECTS_DIR = ROOT_DIR / "projects"
REPO_CACHE_DIR = PROJECTS_DIR / "_repo_cache"
DEFAULT_OPENCLAW_CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"


def load_env() -> None:
    env_path = ROOT_DIR / ".env"
    if not env_path.exists():
        return
    with env_path.open(encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def ensure_projects_dirs() -> None:
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    REPO_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def get_env(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)


def resolve_openai_api_key() -> str | None:
    return get_env("OPENAI_API_KEY_1") or get_env("OPENAI_API_KEY")


def resolve_openclaw_config_path() -> Path:
    explicit = get_env("OPENCLAW_CONFIG_PATH")
    if explicit:
        return Path(explicit).expanduser()
    workspace_config = ROOT_DIR / "openclaw.json"
    if workspace_config.exists():
        return workspace_config
    return DEFAULT_OPENCLAW_CONFIG_PATH


def _coerce_openclaw_json(raw: str) -> str:
    lines: list[str] = []
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("//"):
            continue
        lines.append(line)
    content = "\n".join(lines)
    while ",]" in content or ",}" in content:
        content = content.replace(",]", "]").replace(",}", "}")
    return content


def load_openclaw_config() -> dict:
    config_path = resolve_openclaw_config_path()
    if not config_path.exists():
        return {}
    try:
        raw = config_path.read_text(encoding="utf-8")
        return json.loads(_coerce_openclaw_json(raw))
    except Exception:
        try:
            import json5  # type: ignore

            raw = config_path.read_text(encoding="utf-8")
            parsed = json5.loads(raw)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}


def resolve_openclaw_default_model_ref(config: dict | None = None) -> str | None:
    config = config if config is not None else load_openclaw_config()
    model = ((config.get("agents") or {}).get("defaults") or {}).get("model")
    if isinstance(model, str) and model.strip():
        return model.strip()
    if isinstance(model, dict):
        primary = model.get("primary")
        if isinstance(primary, str) and primary.strip():
            return primary.strip()
    return None
