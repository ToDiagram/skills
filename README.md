# ToDiagram Skills

A library of AI skills for [todiagram.com](https://todiagram.com). Each skill follows the Agent Skills open standard, for compatibility with coding agents such as Gemini CLI, Claude Code, and Cursor.

## Installation

Install any skill from this repository using the `skills` CLI. This command will automatically detect your active coding agents and place the skill in the appropriate directory.

```bash
# List all available skills in this repository
npx skills add todiagram/skills --list

# Install a specific skill
npx skills add todiagram/skills --skill diagram
```

## Available Skills

### diagram

Creates, repairs, and calibrates `.todiagram` JSON for architecture and flow diagrams, with schema and canonical validation support.

```bash
npx skills add todiagram/skills --skill diagram
```

## Adding New Skills

All new skills need to follow the file structure below to implement the Agent Skills open standard.

```text
skills/<skill-name>/
├── SKILL.md           — The main skill prompt and rules
├── scripts/           — Validation and automation scripts
├── references/        — Knowledge base (checklists, guides, patterns)
└── agents/            — Agent configurations (e.g. OpenAI, Gemini)
```
