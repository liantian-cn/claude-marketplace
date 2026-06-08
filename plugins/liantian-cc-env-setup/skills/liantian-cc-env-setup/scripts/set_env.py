#!/usr/bin/env python3
"""
Manage environment variables in Claude Code's ~/.claude/settings.json.

Usage:
  python set_env.py set KEY VALUE [KEY VALUE ...]
  python set_env.py get KEY
  python set_env.py list
  python set_env.py delete KEY [KEY ...]

The script reads/writes the "env" field in ~/.claude/settings.json.
If the file or "env" field doesn't exist, it creates them automatically.
Existing settings outside the "env" field are preserved.
"""

import json
import sys
from pathlib import Path


def settings_path():
    """Return the path to ~/.claude/settings.json (cross-platform)."""
    return Path.home() / ".claude" / "settings.json"


def load_settings():
    """Load settings.json, returning a dict. Returns empty dict if file doesn't exist."""
    path = settings_path()
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: {path} contains invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)


def save_settings(settings):
    """Save settings dict to settings.json, creating parent dirs if needed."""
    path = settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
        f.write("\n")


def cmd_set(args):
    """Set one or more env vars: set KEY VALUE [KEY VALUE ...]"""
    if len(args) < 2 or len(args) % 2 != 0:
        print("Usage: set_env.py set KEY VALUE [KEY VALUE ...]", file=sys.stderr)
        sys.exit(1)

    settings = load_settings()
    if "env" not in settings:
        settings["env"] = {}

    for i in range(0, len(args), 2):
        key, value = args[i], args[i + 1]
        settings["env"][key] = value
        print(f"  {key} = {value}")

    save_settings(settings)
    print(f"\n[OK] {len(args) // 2} env var(s) written to {settings_path()}")


def cmd_get(args):
    """Get a single env var value."""
    if len(args) != 1:
        print("Usage: set_env.py get KEY", file=sys.stderr)
        sys.exit(1)

    settings = load_settings()
    env = settings.get("env", {})
    key = args[0]
    if key in env:
        print(env[key])
    else:
        print(f"Key '{key}' not found in env.", file=sys.stderr)
        sys.exit(1)


def cmd_list():
    """List all env vars."""
    settings = load_settings()
    env = settings.get("env", {})
    if not env:
        print("(no env vars configured)")
        return

    max_key_len = max(len(k) for k in env) if env else 0
    for key, value in env.items():
        # Mask API keys for safe display (show first 6 and last 4 chars)
        if any(kw in key.upper() for kw in ("API_KEY", "AUTH_TOKEN", "SECRET", "TOKEN")):
            if len(value) > 14:
                masked = value[:6] + "…" + value[-4:]
            elif len(value) > 6:
                masked = value[:3] + "…"
            else:
                masked = "***"
            print(f"  {key:<{max_key_len}} = {masked}")
        else:
            print(f"  {key:<{max_key_len}} = {value}")

    print(f"\n  ({len(env)} env var(s) in {settings_path()})")


def cmd_delete(args):
    """Delete one or more env vars."""
    if len(args) < 1:
        print("Usage: set_env.py delete KEY [KEY ...]", file=sys.stderr)
        sys.exit(1)

    settings = load_settings()
    env = settings.get("env", {})
    deleted = []
    not_found = []

    for key in args:
        if key in env:
            del env[key]
            deleted.append(key)
            print(f"  [DEL] {key} (removed)")
        else:
            not_found.append(key)
            print(f"  [MISS] {key} (not found)")

    if deleted:
        save_settings(settings)

    print(f"\n  {len(deleted)} removed, {len(not_found)} not found in {settings_path()}")


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    commands_no_args = {"list"}
    commands_with_args = {"set", "get", "delete"}

    all_commands = commands_no_args | commands_with_args

    if command not in all_commands:
        print(f"Unknown command: {command}", file=sys.stderr)
        print(f"Available commands: {', '.join(sorted(all_commands))}", file=sys.stderr)
        sys.exit(1)

    if command in commands_no_args:
        globals()[f"cmd_{command}"]()
    else:
        globals()[f"cmd_{command}"](args)


if __name__ == "__main__":
    main()
