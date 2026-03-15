# Complexity Budgets

## Overview Tier
Use for: leadership communication, quick onboarding, system orientation.

Targets:
- Nodes: 8-18
- Edges: 8-24
- Nesting depth: up to 2
- Metadata properties per leaf: 0-2
- Edge labels: only high-value interactions

## Working Tier
Use for: planning, implementation alignment, cross-team operations.

Targets:
- Nodes: 15-35
- Edges: 15-45
- Nesting depth: 2-3
- Metadata properties per leaf: 1-4 on critical nodes
- Edge labels: protocol/action labels on key paths

## Deep-Dive Tier
Use for: one subsystem, one flow, one domain boundary.

Targets:
- Nodes: 12-30 within that subsystem
- Edges: 12-40
- Nesting depth: up to 3
- Metadata properties per leaf: 2-6 when needed for implementation clarity
- Scope: one bounded context only

## Hard Stop Signals
Split diagrams when any of these occur:
- More than 40 nodes in one view.
- More than 55 edges in one view.
- More than 3 nesting levels.
- Frequent edge crossings despite regrouping.
- Users cannot summarize flow in one sentence after viewing.
