# Authoring Checklist

## Structural Validity
- Top-level has `nodes` array and `edges` array.
- Every node has unique `id`.
- Every edge `from` and `to` matches a known `id`.
- Direction uses `RIGHT`, `LEFT`, `UP`, or `DOWN`.
- Node nesting key is `nodes` (not `children`).
- Node metadata is direct properties (never use a `fields` wrapper key).
- Omit `imageUrl` / `iconUrl` when not used (do not set `null`).
- Omit node-level `nodes` for leaf nodes (do not send `nodes: []`).
- Run validator script:
  `python scripts/validate_todiagram_schema.py <file>.todiagram`

## Output Stability
- Prefer writing a `.todiagram` file over inline JSON.
- If no file path is given, derive a short kebab-case filename from the diagram's topic (e.g., `system-architecture.todiagram`, `user-onboarding-flow.todiagram`).
- Use deterministic file names for diagram sets (`overview.todiagram`, `domain-*.todiagram`).

## Rendering-Safe Node Rules
- Container nodes (`nodes` with children) do not use `imageUrl`.
- `imageUrl` nodes do not carry dense extra metadata properties.
- Use `iconUrl` when rows should stay visible.
- Labels are concise and scannable (2-4 words preferred).
- Prefer Iconify icon specs (`logos:*`, `fa7-solid:*`) over CDN URL icons.

## Readability Rules
- Group related nodes under parents.
- Avoid flat graphs when logical grouping exists.
- Edge labels are short verbs/protocols, not sentences.
- No edges from a parent to its own child unless explicitly required.

## Repair Sequence
1. Fix missing/duplicate IDs.
2. Fix broken edge references.
3. Normalize aliases (`children` to `nodes`, `source/target` to `from/to`).
4. Flatten `fields` wrappers (object or array) into direct node properties.
5. Reduce cluttered metadata on visual nodes.
6. Re-group nodes into clear containers.
7. Recheck direction and edge label clarity.
