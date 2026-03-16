# Labeling Guide

## Node Labels
- Prefer action + object: `Validate Token`, `Create Invoice`, `Publish Event`.
- Keep 2-4 words.
- Use `\n` for long labels to avoid wide nodes.

## Edge Labels
Use edge labels when they add meaning, not for obvious adjacency.

Good label categories:
- Protocol: `HTTP`, `gRPC`, `Kafka`
- Outcome: `success`, `error`, `timeout`
- Intent: `fetch`, `retry`, `notify`
- State transfer: `approved`, `needs review`

## Tone and Length
- 1-3 words is ideal.
- Keep labels to a short phrase (1-3 words).
- Keep terminology consistent across the flow.

## Label Quality Checks
- Use specific verbs (`validate`, `route`, `persist`) over generic ones (`process`, `handle`).
- Use the same word for the same transition type throughout the diagram.
- Ensure each label adds information beyond the connected node names.
