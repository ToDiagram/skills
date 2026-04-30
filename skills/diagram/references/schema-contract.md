# Schema Contract

Authoritative source: `https://todiagram.com/schemas/todiagram.json`.

## 1. Default Raw `.todiagram` Shape

```json
{
  "direction": "RIGHT|LEFT|UP|DOWN",
  "configuration": {
    "schema": {
      "keys": {
        "nodes": "nodes",
        "edges": "edges",
        "direction": "direction"
      },
      "node": {
        "id": "id",
        "label": "label",
        "imageUrl": "imageUrl",
        "iconUrl": "iconUrl",
        "customTheme": "custom_theme"
      },
      "edge": {
        "from": "from",
        "to": "to",
        "label": "label"
      }
    }
  },
  "nodes": [],
  "edges": []
}
```

Notes:
- Top-level `nodes` and `edges` are required.
- `direction` is optional but recommended.
- `configuration` is optional and only needed for custom key mapping.

## 1.1 Canonical Key Names
- Use `nodes` for child arrays.
- Use `edges` for connections.
- Use `from` / `to` for edge endpoints.
- **Put display data inside the `fields` object** on a node. Direct properties on the node are accepted but **deprecated**.
- `imageUrl` and `iconUrl` are optional: omit the keys entirely when unused (do not set `null`).
- Node-level `nodes`: include only when the node has real children.

Bad (deprecated direct props + alias keys):

```json
{
  "id": "page",
  "children": [],
  "role": "Route entry"
}
```

Good (use `fields`):

```json
{
  "id": "page",
  "label": "Page",
  "fields": { "role": "Route entry" }
}
```

## 2. Node Shape

```json
{
  "id": "authService",
  "label": "Auth Service",
  "iconUrl": "fa7-solid:lock",
  "custom_theme": {
    "NODE": { "NODE": "#f8fafc", "HEADER": "#dbeafe" },
    "TEXT": { "PARENT_ROW_TEXT": "#1e3a8a" }
  },
  "fields": {
    "runtime": "nodejs",
    "port": 443
  }
}
```

Parser behavior:
- `id` is required.
- `label` is strongly recommended (renders in the header).
- `nodes` makes a container/group node and should be omitted for leaf nodes.
- `imageUrl` creates image-focused rendering; **cannot be combined with `fields`** (image replaces row display).
- `fields` renders key-value rows on the card. Values can be primitives, arrays, or nested objects (arrays/objects become summary rows that may expand into linked detail nodes).
- Properties placed directly on the node (outside `fields`) still render but are flagged deprecated by the schema; migrate them into `fields`.

## 2.1 Icon Values
- Prefer Iconify specs:
  - `logos:tech-name` (for example `logos:nextjs-icon`, `logos:react`)
  - `fa7-solid:icon-name` (for example `fa7-solid:lock`, `fa7-solid:database`)
  - Short forms such as `fa:gear` are also valid Iconify input.
- Use external `http(s)` URLs only when explicitly requested.

### Finding Iconify slugs
When unsure of an exact slug, query the Iconify search API directly:

```bash
curl -fsSL 'https://api.iconify.design/search?query=database&limit=10'
# optional: &prefix=logos  (restrict to one icon set)
```

Response is JSON with an `icons` array of `prefix:name` slugs ready to drop into `iconUrl`. Pick the first match from a set the project already uses (`logos:*` for brands, `fa7-solid:*` / `mdi:*` / `lucide:*` for generic UI) so the diagram stays visually consistent.

If a ToDiagram MCP server is available, prefer its icon-search tool — the curl path is the fallback for non-MCP environments.

## 2.2 `custom_theme` Overrides
Apply per-node theme overrides. Specify only the colors you want to change; omit the rest.

```json
{
  "custom_theme": {
    "NODE": {
      "NODE": "#0f172a",
      "HEADER": "#1e293b"
    },
    "EDGE": {
      "EDGE": "#22d3ee",
      "LABEL": "#e2e8f0"
    },
    "TEXT": {
      "TEXT": "#f1f5f9",
      "ROW_KEY": "#94a3b8",
      "NUMBER": "#fbbf24",
      "NULL": "#64748b",
      "BOOLEAN_TRUE": "#34d399",
      "BOOLEAN_FALSE": "#f87171",
      "PARENT_ROW_TEXT": "#f8fafc"
    }
  }
}
```

Allowed groups and keys:
- `NODE`: `NODE` (card background), `HEADER` (header row background).
- `EDGE`: `EDGE` (line color), `LABEL` (edge label text).
- `TEXT`: `TEXT`, `ROW_KEY`, `NUMBER`, `NULL`, `BOOLEAN_TRUE`, `BOOLEAN_FALSE`, `PARENT_ROW_TEXT`.

The default key on the node is `custom_theme`; it can be remapped via `configuration.schema.node.customTheme`.

## 3. Edge Shape

```json
{
  "from": "apiGateway",
  "to": "authService",
  "label": "JWT verify"
}
```

Rules:
- `from` and `to` are required.
- `label` is optional.
- IDs must resolve to existing nodes.

## 4. ID and Grouping Rules
- IDs must be unique across all nesting levels.
- Group with `nodes` for layers/domains/teams.
- Prefer 2-3 nesting levels for readability.
- Keep 3-8 children per container where possible.
