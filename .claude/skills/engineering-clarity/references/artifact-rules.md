# ECS Artifact Rules

Read `standard.md` first. Apply only the sections relevant to the requested artifact.

## User stories and work items

- Use `As a [role], I want [capability], so that [user or business value]` when the story describes a user-facing need. For platform/enabler work, use a precise problem statement rather than inventing a fictional user.
- Keep business outcomes distinct from the proposed technical solution.
- Put constraints in Business Rules. Use IDs when traceability is useful (`BR-01`, `AC-01`).
- Write each acceptance criterion as one independently observable behavior, preferably `Given / When / Then`.
- Specify test data and thresholds only when they are provided or approved. Flag unknowns explicitly.
- Cover at least the happy path and meaningful error path. Do not fabricate edge cases as requirements; list unapproved ones as questions.
- Add dependencies, out-of-scope statements, and a Definition of Done when the team needs them.

## Pull request descriptions

- **Purpose:** Which requirement, incident, defect, or measurable behavior motivated the change?
- **Changes:** Describe what actually changed, not how impressive it is. Distinguish behavior changes, database changes, config, migrations, APIs, security, and dependencies where relevant.
- **Validation:** List the test name/command, environment, and actual result where available. Use `Not run` for work not performed. Never manufacture coverage percentages or CI status.
- **Risk and impact:** Identify affected components, breaking changes, compatibility, migrations, and relevant failure scenarios. `No known risks` is a statement that requires an informed review.
- **Deployment and rollback:** Give the actual deployment or recovery plan if relevant. A git revert might not roll back database migrations, configuration, external side effects, or irreversible data changes.
- **Related work:** Link the ticket, incident, ADR, and acceptance criteria when available.
- Draft the description from actual code and available test evidence. If you did not inspect the diff, describe the input limitations.

## ADR / technical decisions

- Document context and decision separately.
- List options considered with concrete tradeoffs, not subjective labels.
- State impacts on reliability, security, performance, maintainability, cost, operations, and rollback where applicable.
- Make rejected options and unresolved decisions explicit.
- Record a decision status and date if known.

## Runbooks and troubleshooting

- State the intended audience, required privileges, environment, and preconditions.
- Use numbered steps for ordered operations. Put the verification result after each risky operation.
- State exact commands and configuration values. Never assume production access.
- Include stop conditions, failure branches, and escalation contacts or roles when known.
- Treat destructive or irreversible operations as separate, clearly marked steps requiring proper approval.
- Provide recovery actions that are verified, or label them as unverified procedures.

## API documentation

- State method, path, authentication, request properties, constraints, response status, error states, idempotency, rate limits, and example behavior as applicable.
- Preserve exact wire-format property names, enum values, case, types, and JSON shapes.
- Differentiate a documented contract from observed implementation behavior.

## Code comments and agent instructions

- Explain intent, invariants, constraints, and non-obvious risks; avoid comments that merely restate code.
- Use exact identifiers and order-sensitive instructions.
- Keep instructions idempotent where possible, and identify forbidden actions or required approvals.
- Do not put secrets into examples, issues, logs, prompts, or templates.
