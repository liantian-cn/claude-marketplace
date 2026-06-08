# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Claude Code plugin marketplace — a curated registry of plugins for enterprise due diligence and compliance risk control (企业尽职调查与合规风控). The marketplace is hosted on GitHub and also mirrored on Gitee.

**Remote**: `origin` = `https://github.com/liantian-cn/claude-marketplace.git`  
**Marketplace name**: `liantian-cc-market`

## Commands

There is no build step, test suite, or linter in this repo. It is a pure collection of plugin directories.

**Local validation** (matching CI):
```bash
# Validate marketplace.json structure
python -c "
import json
with open('.claude-plugin/marketplace.json') as f:
    data = json.load(f)
assert 'name' in data and 'owner' in data and 'plugins' in data
print(f'OK: {len(data[\"plugins\"])} plugin(s)')
"

# Check each bundled plugin has plugin.json and count skills
for d in plugins/*/; do
  name=$(basename "$d")
  echo "--- $name ---"
  [ -f "$d/.claude-plugin/plugin.json" ] && echo "  plugin.json: OK" || echo "  MISSING plugin.json"
  [ -d "$d/skills" ] && echo "  Skills: $(find "$d/skills" -name 'SKILL.md' | wc -l)"
done
```

**GitHub operations** — use `gh` CLI:
```bash
gh repo view liantian-cn/claude-marketplace   # repo info
gh pr list                                     # open PRs
gh pr create --title "..." --body "..."        # create PR
```

## Architecture

### Marketplace Registration

`.claude-plugin/marketplace.json` is the single source of truth for which plugins are included. To add a new plugin:

1. Create the plugin directory under `plugins/<name>/`
2. Add a `.claude-plugin/plugin.json` inside it
3. Add an entry to `marketplace.json` → `plugins` array with: `name`, `source` (relative path `./plugins/<name>`), `description`, `version`, `author`, `license`, `keywords`, `homepage`, `repository`, `category`

### Plugin Structure

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json       # name, version, description, author, license, keywords
├── .mcp.json             # MCP servers (optional — only if plugin needs MCP tools)
├── skills/               # skills auto-discovered from SKILL.md files
│   └── <skill-name>/
│       ├── SKILL.md      # YAML frontmatter + markdown body
│       ├── mcp-tools-map.md     # maps MCP tool names → cache file names
│       └── mcp-cache-guide.md   # MCP caching convention
└── README.md
```

### MCP Configuration Pattern

`.mcp.json` defines MCP servers that plugins depend on. All servers use HTTP transport with `Authorization: Bearer ${QCC_API_KEY}` — the token references a variable from `~/.claude/settings.json` `env` field (NOT an OS environment variable).

### Skill Conventions

Every `SKILL.md` uses YAML frontmatter with these fields:
- `name`, `description` — auto-discovery triggers
- `version` — date-based (`YYYY-MM-DD`)
- `category` — grouping label
- `mcp_servers` — array of required MCP server names
- `tags` — keyword array for matching
- `model` — default model override (typically `deepseek-v4-pro`)

Skills follow a consistent body structure: **定位** (purpose), **共享引用** (shared references), **工作流** (workflow), **输出模板** (output template), **参数** (parameters), **边界与免责** (boundaries & disclaimer).

### MCP Caching Pattern

All qcc-due-diligence skills use a consistent caching convention:
- Cache directory: `./[公司全名]MCP查询结果/`
- Before any MCP call, check if the cache file exists; if so, read it and skip the call
- Cache files include query timestamp, data source, and query subject headers
- Same-day cache reuse; delete the cache file to force refresh

### Skill Dependency Graph

`liantian-cc-env-setup` is a **foundational dependency** for all other plugins. It installs Python 3.12+, Pandoc 2.0+, markitdown, and configures API keys. Business skills in `qcc-due-diligence` assume this environment is already set up.

## CI

`.github/workflows/validate.yml` runs on push/PR to `main`:
1. Validates `.claude-plugin/marketplace.json` is valid JSON with required fields
2. Iterates `plugins/*/` directories, checks each has `plugin.json`, counts skills

## Plugins

| Plugin | Skills | Purpose |
|--------|--------|---------|
| `liantian-cc-env-setup` | 1 | Toolchain install (Python/Pandoc/markitdown) + API key config |
| `qcc-due-diligence` | 12 | Enterprise due diligence via QCC database (KYB, UBO, credit, litigation, etc.) |

## Repository Operations

When working in this repo, follow these commit conventions:
- Before modifying a file with uncommitted changes, create a backup commit first: `chore: backup before edit [filename]`
- Commit each modified file separately with both title and message
- Use `gh` CLI for all GitHub interactions (PRs, issues, repo queries)
