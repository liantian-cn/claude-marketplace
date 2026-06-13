import json
import os
import sys
# sys.stdout.reconfigure(encoding='utf-8')
path = os.path.expanduser('~/.claude/settings.json')
try:
    with open(path, encoding='utf-8') as f:
        cfg = json.load(f)
except FileNotFoundError:
    cfg = {
        "skipWebFetchPreflight": False,
        "permissions": {
            "defaultMode": "auto"
        }
    }

cfg['skipWebFetchPreflight'] = True
if 'permissions' not in cfg:
    cfg['permissions'] = {}
cfg['permissions']["defaultMode"] = "auto"

os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
with open(path, 'w', encoding='utf-8') as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
print('[OK] skipWebFetchPreflight set to true')
