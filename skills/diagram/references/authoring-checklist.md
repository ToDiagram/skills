# Authoring Checklist

## Structural Validity
- Top-level has `nodes` array and `edges` array.
- Every node has unique `id`.
- Every edge `from` and `to` matches a known `id`.
- Direction uses `RIGHT`, `LEFT`, `UP`, or `DOWN`.
- Node nesting key is `nodes`.
- Node display data lives inside the `fields` object (direct properties are deprecated).
- A node never has both `imageUrl` and `fields`.
- Include `imageUrl` / `iconUrl` only when used; omit the keys entirely otherwise.
- Include node-level `nodes` only for containers with real children.
- Run validator script:
  `python scripts/validate_todiagram_schema.py <file>.todiagram`

## Output Stability
- Prefer writing a `.todiagram` file over inline JSON.
- If no file path is given, derive a short kebab-case filename from the diagram's topic (e.g., `system-architecture.todiagram`, `user-onboarding-flow.todiagram`).
- Use deterministic file names for diagram sets (`overview.todiagram`, `domain-*.todiagram`).

## Rendering-Safe Node Rules
- Use `iconUrl` (instead of `imageUrl`) on container nodes to keep child rows visible.
- Keep `imageUrl` nodes minimal — image rendering replaces row display.
- Use `iconUrl` when rows should stay visible.
- Labels are concise and scannable (2-4 words preferred).
- Prefer Iconify icon specs (`logos:*`, `fa7-solid:*`) over CDN URL icons.

## Readability Rules
- Group related nodes under parents.
- Group related nodes under parents when logical grouping exists.
- Edge labels are short verbs/protocols, not sentences.
- No edges from a parent to its own child unless explicitly required.

## Repair Sequence
1. Fix missing/duplicate IDs.
2. Fix broken edge references.
3. Normalize aliases (`children` to `nodes`, `source/target` to `from/to`).
4. Move deprecated direct properties into the `fields` object.
5. Resolve `imageUrl` + `fields` conflicts on the same node.
6. Reduce cluttered metadata on visual nodes.
7. Re-group nodes into clear containers.
8. Recheck direction and edge label clarity.
