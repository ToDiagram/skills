# Split Strategies

## Strategy 1: Overview + Domain Slices
- Diagram A: platform overview with main domains.
- Diagram B/C/D: one domain each with internal detail.

Use when: architecture has many bounded contexts.

## Strategy 2: Lifecycle Stages
- Diagram A: request/ingestion stage.
- Diagram B: processing/orchestration stage.
- Diagram C: persistence/analytics/serving stage.

Use when: flow is temporal and stage-based.

## Strategy 3: Environment Separation
- Diagram A: shared services.
- Diagram B: staging topology.
- Diagram C: production topology.

Use when: infra differs significantly by environment.

## Strategy 4: Audience Split
- Diagram A: executive overview (minimal detail).
- Diagram B: engineering working view.
- Diagram C: operations incident/runbook view.

Use when: one diagram cannot serve all audiences.

## Cross-Diagram Consistency Rules
- Keep shared IDs and naming stable across diagrams.
- Keep direction conventions consistent unless there is a strong reason.
- Reuse group names for equivalent boundaries.
- Document what moved from overview into each deep-dive diagram.
