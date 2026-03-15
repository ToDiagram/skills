# Flow Patterns

## Pattern 1: Linear Pipeline
Use when: each step has one dominant next step.

Structure:
- Start
- Stage A
- Stage B
- Stage C
- End

Direction: `RIGHT` or `DOWN`

## Pattern 2: Decision Branching
Use when: outcomes diverge based on validation or approval.

Structure:
- Input
- Validate
- Branch A (success)
- Branch B (failure)
- Merge or terminal states

Edge labels:
- `valid` / `invalid`
- `approved` / `rejected`

## Pattern 3: Parallel Work + Join
Use when: two or more steps happen concurrently.

Structure:
- Trigger
- Parallel Branch 1
- Parallel Branch 2
- Join
- Finalize

Tip: keep branch labels symmetric.

## Pattern 4: Retry Loop
Use when: temporary failure can be retried safely.

Structure:
- Attempt
- Check result
- Success path
- Retry path with cap/escalation

Tip: clearly label retry conditions and exit criteria.

## Pattern 5: Human-in-the-Loop
Use when: automated path requires manual review at checkpoints.

Structure:
- Automated processing
- Human approval/review
- Approved path
- Rework path

Tip: visually separate automated and manual stages.
