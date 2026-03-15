# Schema Contract

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
- `direction` is optional but recommended.
- `configuration` is optional and only needed for custom key mapping.

## 1.1 Canonical Key Names (No Aliases)
- Use `nodes`, never `children`.
- Use `edges`, never `links`.
- Use `from` / `to`, never `source` / `target`.
- Put row data as direct node properties.
- Do not use a `fields` wrapper key (object or array).
- `imageUrl` and `iconUrl` are optional: omit keys when unused (do not send `null`).
- Node-level `nodes` is optional: include it only when the node has real children (no `nodes: []` on leaf nodes).

Bad:

```json
{
  "id": "page",
  "children": [],
  "fields": { "role": "Route entry" }
}
```

Good:

```json
{
  "id": "page",
  "role": "Route entry"
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
  "runtime": "nodejs",
  "port": 443
}
```

Parser behavior:
- `id` is required.
- `label` is strongly recommended.
- `nodes` makes a container/group node and should be omitted for leaf nodes.
- `imageUrl` creates image-focused rendering and should not be mixed with dense metadata properties.
- Additional properties are rendered as rows (primitives are most readable).
- Arrays/objects in properties become summary rows and can create linked child detail nodes.

## 2.1 Icon Values
- Prefer Iconify specs:
  - `logos:tech-name` (for example `logos:nextjs-icon`, `logos:react`)
  - `fa7-solid:icon-name` (for example `fa7-solid:lock`, `fa7-solid:database`)
- Use external `http(s)` URLs only when explicitly requested.

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
