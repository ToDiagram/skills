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
- Avoid sentence-length labels.
- Keep terminology consistent across the flow.

## Avoid
- Ambiguous labels like `process` or `handle` everywhere.
- Different words for the same transition type.
- Labels that duplicate node names without new information.
