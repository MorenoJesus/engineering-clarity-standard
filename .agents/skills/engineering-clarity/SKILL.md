---
name: engineering-clarity
description: Create, rewrite, or review precise software engineering documentation using an ASD-STE100-inspired style. Use for user stories, acceptance criteria, pull request descriptions, Azure DevOps work items, GitHub issues, API docs, architecture decisions, runbooks, test plans, implementation plans, release notes, and substantial technical comments.
metadata:
  version: "1.0.0"
---

# Engineering Clarity Standard (ECS)

Use this skill for technical writing. It is a **software-engineering adaptation** of simplified technical writing principles, not a claim of ASD-STE100 compliance.

## Required workflow

1. **Identify the artifact and audience.** Determine whether this is a story, acceptance criteria, PR, runbook, ADR, API reference, or another technical document.
2. **Use source facts.** Inspect relevant requirements, code diffs, test output, logs, and linked work items when accessible. Do not invent facts to fill gaps.
3. **Read `references/standard.md`.** Apply its mandatory rules. Read `references/artifact-rules.md` for artifact-specific checks.
4. **Normalize terminology.** Preserve exact identifiers and business terms. Use the project glossary if one exists. Use `references/glossary.md` to resolve terminology gaps.
5. **Draft with explicit behavior.** Name actors and components. State preconditions, triggers, behavior, results, and errors when relevant. Prefer short, direct sentences and consistent nouns.
6. **Check verifiability.** Make acceptance criteria observable. Distinguish implementation claims from executed validation. State risks, constraints, and rollback requirements where relevant.
7. **Self-review.** Remove vague language, hidden assumptions, unsupported guarantees, contradictory wording, and invented verification. Preserve required detail instead of shortening blindly.

## Templates

Adapt, do not mechanically fill, the matching template:

- User story: `assets/user-story.md`
- Pull request: `assets/pull-request.md`
- Operations runbook: `assets/runbook.md`
- Architecture decision: `assets/adr.md`
- API contract: `assets/api-contract.md`
- Implementation plan: `assets/implementation-plan.md`

## Examples and review behavior

Use `examples/before-after.md` when examples help resolve a writing choice. In review requests, report actionable findings in priority order with source text, ambiguity or defect, recommended wording, and any facts that require confirmation. When the source is incomplete, make the gap explicit instead of manufacturing precision.

## Boundaries

- Preserve technical meaning, business intent, identifiers, units, and API contracts.
- Do not change executable code merely to comply with prose style.
- Do not replace necessary domain language with inaccurate common words.
- Do not certify ASD-STE100 compliance, even if the writing resembles the standard.
- Do not claim an implementation is correct, tests passed, or rollback is safe without supporting evidence.