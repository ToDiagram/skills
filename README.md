# ToDiagram Skills

This repository contains Codex skills for [todiagram.com](https://todiagram.com).
Each skill packages focused instructions, references, and scripts so agents can produce consistent ToDiagram outputs.

## Current Skills

- `todiagram-diagramming`: Creates and repairs `.todiagram` JSON for architecture and flow diagrams, with schema + canonical validation support.

## Quick Validation

Use the built-in validator from this repo:

```bash
python3 skills/todiagram-diagramming/scripts/validate_todiagram_schema.py path/to/diagram.todiagram
```

If needed, install dependency:

```bash
python3 -m pip install --user jsonschema
```

## Adding a New Skill

1. Create a new folder under `skills/<your-skill-name>/`.
2. Add `SKILL.md` with YAML front matter (`name`, `description`) and clear operating rules.
3. Add `references/` docs only when they are required by the skill workflow.
4. Add `scripts/` for repeatable checks or conversions instead of embedding long procedures in prompts.
5. Keep output contracts explicit (file paths, format keys, validation steps).

## Conventions

- Prefer deterministic, file-first outputs when the skill generates artifacts.
- Keep key names and schema contracts canonical; avoid aliases unless explicitly supported.
- Include a validation step in each production skill.
- Keep references concise and task-specific to minimize prompt bloat.

## Goal

Build a small, high-quality skill set that helps ToDiagram users create readable, valid diagrams quickly and consistently.
