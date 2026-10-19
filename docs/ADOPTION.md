# ECS Adoption Guide

## Scope

ECS applies to documentation, work items, requirements, PR descriptions, architecture decisions, runbooks, test plans, troubleshooting instructions, API contracts, release notes, and significant technical comments. It does not prescribe coding architecture or override API, compliance, security, or legal requirements.

## Suggested rollout

1. **Adopt in one repository.** From the kit folder, use `.\scripts\install.ps1 -Scope repo -Repo '<path>'` on Windows, or `python3 scripts/install.py --scope repo --repo <path>` on macOS/Linux. Preview with `-DryRun` or `--dry-run`, respectively. Review conflicts and commit the files on an approved branch.
2. **Define business terms.** Replace the placeholder table in the skill's `references/glossary.md` with approved project terminology. Maintain one glossary for a domain when practical.
3. **Use templates.** Start with user stories and PR descriptions, then introduce runbooks and ADRs. Retain only sections that materially improve the artifact.
4. **Review in the PR process.** Require reviewers to check scope, consistency, verifiability, risks, and evidence. Do not auto-approve because an agent used the skill.
5. **Measure quality.** Track PR clarification rounds, reopened work items, inconsistent terminology, defect escape causes, or review time. Compare before and after adoption; avoid assuming causation.
6. **Expand deliberately.** Publish a versioned copy or managed package for other repositories. Update the canonical source, regenerate mirrors, and test supported clients.

## Roles and responsibilities

- **Requirement owner:** Confirms intent, business rules, and thresholds.
- **Engineer:** Explains the implementation, technical risk, and actual verification.
- **QA/reviewer:** Confirms observability, negative paths, and evidence.
- **Maintainer:** Owns ECS version changes, glossary consistency, package synchronization, and compatibility checks.

## Enforcement model

- **Agent instructions:** Improve default wording, but are not deterministic and cannot prove correctness.
- **Templates:** Improve consistency at creation time.
- **Heuristic lint:** Finds likely vague text, placeholders, and long sentences; requires judgment.
- **Human / automated tests:** Establish actual acceptance and technical correctness.

## Acceptance test for a new AI tool

Give the same sample task to two or more agents using this kit. See `docs/EVALUATION.md` for a comparison scorecard:

> Draft a PR description for a change that adds a duplicate-message check. You have no test execution results. Include risk and rollback information without making up facts.

Expect a clear purpose, source-attributed changes, `Unknown` test execution status, a warning that a duplicate check may be racy without transaction-level protection, and an explicit unverified rollback plan. Missing test results do not establish that tests were not run. Use `Not run` only when non-execution is known. An agent that claims tests passed or guarantees exactly-once processing fails this check.

## Governance

Use semantic versioning for the kit. Propose wording-rule changes as reviewed PRs. Log deliberate exceptions when clarity competes with domain conventions. Review all agent-written instructions as part of the repository's trust boundary. Do not install unknown skills without review.
