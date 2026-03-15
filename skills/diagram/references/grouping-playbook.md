# Grouping Playbook

## Step 1: Choose Grouping Axis
Pick one primary axis:
- Business capability
- Runtime layer
- Team ownership
- Environment

Avoid mixing all axes in one diagram.

## Step 2: Assign Node Roles
- Parent container: context boundary.
- Leaf service/component: executable or externally visible unit.
- External system: separate boundary node.

## Step 3: Set Detail Level
- Overview: visual leaves, minimal metadata properties, essential edges only.
- Working architecture: moderate metadata properties on critical nodes.
- Deep dive: use a separate diagram per domain slice.

## Step 4: Enforce Budgets
- Total nodes: 8-30 preferred.
- Container depth: 2-3 levels preferred.
- Children per parent: 3-8 preferred.
- Fields per leaf: 0-3 in architecture mode.

## Step 5: Final Readability Gate
Ask:
1. Can someone identify system entry points in 5 seconds?
2. Are ownership/boundary lines obvious?
3. Do edge labels explain interaction type?
4. Is any group overloaded and better split?
