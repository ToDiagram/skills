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

## Quality Checks
- Group nodes into layers when siblings exceed ~8; keep flat lists small.
- Choose either many children or rich metadata per container, not both.
- Keep edge labels to 1-3 words; reserve detail for node metadata.
- Target one audience level per diagram (split executive vs. engineering views).
- Use only canonical keys (`nodes`, `edges`, `from`, `to`) in raw `.todiagram`.
