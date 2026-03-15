# Architecture Patterns

## Pattern 1: Layered Web Platform
Use for: web systems with clear client/service/data boundaries.

Suggested groups:
- Experience Layer
- Core Services
- Data and Messaging
- External Integrations

Direction: `RIGHT` or `DOWN`

## Pattern 2: Event-Driven Services
Use for: async architectures with queues/topics and consumers.

Suggested groups:
- Producers
- Event Backbone
- Consumer Domains
- Storage/Analytics

Direction: `RIGHT`

## Pattern 3: Multi-Environment Topology
Use for: development/staging/production views.

Suggested groups:
- Shared Platform Services
- Staging
- Production

Direction: `DOWN`

## Pattern 4: Domain-Centric Monolith Decomposition
Use for: legacy systems split by business capability.

Suggested groups:
- Customer Domain
- Order Domain
- Billing Domain
- Shared Infrastructure

Direction: `RIGHT`

## Anti-Patterns
- Single flat layer with 20+ sibling nodes.
- Containers that have both many children and heavy row metadata.
- Over-labeling every edge with sentence-length text.
- Mixing audience levels in one diagram (executive + code internals).
- Using non-canonical keys (`children`, `fields` wrappers) in raw `.todiagram`.
