# Engineering Clarity Standard (ECS) — Agent Skill Kit

**Version:** 1.0.0 · **Status:** proposed team convention · **Date:** 2026-10-18

ECS is a vendor-neutral, **ASD-STE100-inspired** writing convention for software engineering. It helps authors and coding agents produce precise user stories, acceptance criteria, pull request descriptions, runbooks, architecture decisions, API documentation, and technical plans.

> **Not ASD-STE100 certified.** ECS applies selected principles of simplified technical writing. It does not reproduce the official ASD-STE100 dictionary, implement every official rule, or establish formal compliance. Refer to https://asd-ste100.org/ for the official standard.

## Start here

- **Introducing ECS to your team?** Read the [visual pitch](https://morenojesus.github.io/engineering-clarity-standard/): a before-and-after example, what the kit includes, and a three-step pilot proposal.
- **Ready to try it?** Follow the [quick start](#quick-start-windows--powershell).
- **Planning adoption?** Use the [adoption guide](docs/ADOPTION.md).

The visual pitch opens directly in your browser through GitHub Pages. To view it offline, clone or download this repository and open [`docs/pitch.html`](docs/pitch.html). Changes to that file on `main` automatically deploy through [the Pages workflow](.github/workflows/pages.yml).

## Why adopt ECS? See the difference

ECS replaces vague technical language with explicit intent, observable results, and visible unknowns. That makes requests easier to implement, review, and test—whether the author is a person or an AI coding agent.

**These are illustrative examples, not approved requirements or evidence of completed work.** The "after" versions demonstrate how to write a clearer *proposal*; actual behavior and test results must still be verified.

### 1. User story: define who needs what

**Before**

> As a user, I want better error handling so everything works smoothly.

**After**

> As a support engineer, I want to identify messages that the service could not process so that I can investigate failures.

Proposed acceptance criteria:

- **AC-01:** Given a message exceeds the configured delivery limit, when the messaging service applies its dead-letter policy, then the message is available in the dead-letter queue.
- **AC-02:** Given a message is in the dead-letter queue, when a support engineer opens its details, then the details show the message ID and recorded failure reason.
- **Open question:** Which tool displays those details, and which roles can access them?

**Why it helps:** The story identifies a real actor and business value. The criteria define observable results instead of relying on "works smoothly." The unanswered access decision stays visible.

### 2. Pull request: distinguish changes from proof

**Before**

> Improved message handling and fixed retry issues. Tests look good.

**After (illustrative PR description)**

- **Purpose:** Prevent a repeated message from updating the same database record twice.
- **Changes:** Added a message ID check before the update. Added error logging for failed database operations.
- **Validation:** Duplicate-message unit test — **Not run**. Service Bus integration test — **Not run**.
- **Risk:** Concurrent workers could pass the initial check. A unique constraint or transactional protection may be required.
- **Rollback:** Not yet defined. Confirm whether the change modifies persistent schema or state.

**Why it helps:** Reviewers can separate the intended fix, proposed implementation, missing test evidence, and unresolved risks. "Tests look good" is not a test result.

### 3. Runbook: replace guesswork with safe steps

**Before**

> If it breaks, restart everything and try again.

**After**

1. If the message handler stops processing, inspect its health check.
2. Review the most recent error log entry.
3. Identify the failed dependency, if the available evidence supports that conclusion.
4. Do not restart the service until the approved recovery procedure confirms that a restart is safe.

**Open question:** Which health check and recovery procedure apply to this service?

**Why it helps:** Operators know what evidence to collect before taking a potentially disruptive action. The procedure does not pretend that every failure needs a restart.

### 4. API contract: replace adjectives with observable behavior

**Before**

> The API returns a useful error when something goes wrong.

**After (proposed behavior)**

> If the request body fails validation, the API returns HTTP `400` with a machine-readable error code and the invalid field names.

**Why it helps:** Developers can implement a specific response, and QA can verify it. "Useful" is not an acceptance criterion. The response contract still needs approval and verification.

### 5. AI coding instructions: limit silent assumptions

**Before**

> Make the message handler more reliable. Fix duplicates and add tests.

**After (proposed task)**

- **Goal:** Prevent two database updates for the same message ID, including when multiple workers process messages concurrently.
- **Constraints:** Preserve the existing retry policy and message contract.
- **Verification:** Add tests for repeated delivery and concurrent processing. Run the relevant tests and report the actual results. If a test was not run, write **Not run**.
- **Open decision:** Identify how uniqueness is enforced across worker instances before selecting an implementation.

**Why it helps:** An AI agent receives a bounded objective, explicit constraints, verification expectations, and a decision it must not invent.

**The goal is not more documentation. It is less ambiguity.** For additional examples, see [Before and After — ECS Examples](.agents/skills/engineering-clarity/examples/before-after.md).

---

## What is included?

- **Agent Skill:** `.agents/skills/engineering-clarity/SKILL.md` is the canonical skill. Its `references/`, `assets/`, and `examples/` are the single editable source.
- **Claude Code adapter:** `.claude/skills/engineering-clarity/` is a generated mirror. `scripts/sync_skills.py` keeps it synchronized.
- **Always-on repository guidance:** `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md` are short instructions for supported AI agents.
- **Pull request templates:** `.github/PULL_REQUEST_TEMPLATE.md` for GitHub and `.azuredevops/pull_request_template.md` for Azure Repos. The Azure template mirrors the GitHub template.
- **GitHub issue template:** `.github/ISSUE_TEMPLATE/user-story.md`.
- **Reference documents:** The skill contains the ECS style standard, artifact-specific rules, glossary guidance, and examples.
- **Tools:** Installer, synchronization check, and an optional heuristic writing checker.

## Quick start (Windows / PowerShell)

Extract this archive into a folder (for example `C:\Tools\engineering-clarity-kit`). Install it into a **Git repository**:

```powershell
py .\scripts\install.py --scope repo --repo 'C:\src\my-project'
```

Or install the skills for your **user account** across local repositories:

```powershell
py .\scripts\install.py --scope user
```

If you use Python as `python` rather than `py`, substitute that command. Use `--dry-run` to preview changes.

For macOS / Linux:

```bash
python3 scripts/install.py --scope repo --repo ~/src/my-project
# or
python3 scripts/install.py --scope user
```

**Safe installation:** The installer never overwrites different existing files. It reports each skipped conflict. Manually merge changes into an existing `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Copilot instructions, or PR template. Do not blindly replace existing organizational guidance.

After installation, commit the new files if you want the standard shared with your team and cloud agents. Personal-level installation only affects the local machine and compatible local tools.

## Compatibility (verified 2026-10-18)

| Tool | Repository skill | Always-on / companion instructions |
| --- | --- | --- |
| OpenAI Codex | `.agents/skills/engineering-clarity/` | `AGENTS.md` |
| GitHub Copilot (supported agent surfaces) | `.agents/skills/engineering-clarity/` | `.github/copilot-instructions.md`; some surfaces also read `AGENTS.md` |
| Claude Code | `.claude/skills/engineering-clarity/` | `CLAUDE.md` |
| Cursor | `.agents/skills/engineering-clarity/` | Use compatible project rules if needed |
| Gemini CLI | `.agents/skills/engineering-clarity/` | `GEMINI.md` |
| Devin Desktop / Cascade | `.agents/skills/engineering-clarity/` | `AGENTS.md` |
| Other agents | Agent Skills-compatible `SKILL.md` directory | Import or map the relevant instructions using that product's documented mechanism |

**Important:** Compatibility does not guarantee activation on every request. Most agents select skills based on descriptions and task relevance. Always-on instruction files increase coverage, but acceptance criteria, tests, and review remain necessary. IDE and model support can change; validate the setup in the exact environment you use.

## Try it

With your chosen agent, ask:

> Use the `engineering-clarity` skill. Rewrite this user story and add testable acceptance criteria: "As a user, I want better error handling so everything works smoothly."

Or:

> Use the engineering clarity standard. Draft a PR description from the current git diff. Do not report tests as passed unless you have execution results.

Ask the agent to identify the source of its guidance; then review its output against `references/standard.md` and `references/artifact-rules.md`.

## Maintain one source of truth

Edit **only** `.agents/skills/engineering-clarity/`. Then generate and check mirrors:

```bash
python scripts/sync_skills.py
python scripts/sync_skills.py --check
python -m unittest discover -s tests -v
```

Copying the files by hand into each vendor directory creates drift. Synchronization is a packaging step, not a separate rule set.

## Optional writing check

```bash
python scripts/check_clarity.py path/to/finished-pr.md
python scripts/check_clarity.py --strict path/to/finished-story.md
```

The checker flags *possible* vague language, unresolved placeholders, and long prose sentences. It is heuristic; it does not prove STE compliance or evaluate whether behavior is technically correct. Review warnings before editing technical nouns or quoted requirements. Use `--strict` only after tailoring rules to your team.

## Adoption guidance

Read `docs/ADOPTION.md` for rollout, ownership, review responsibilities, and a practical adoption path. This kit defines writing conventions; it is **not** a substitute for security review, human judgment, QA, or CI verification.

## License

This kit is available under the [MIT License](LICENSE). The license covers this repository, not the official ASD-STE100 standard.

## Sources

- Agent Skills open specification: https://agentskills.io/specification
- OpenAI Codex skills: https://learn.chatgpt.com/docs/build-skills
- OpenAI AGENTS.md: https://learn.chatgpt.com/docs/agent-configuration/agents-md
- GitHub Copilot skills: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- Claude Code skills: https://code.claude.com/docs/en/skills
- Cursor skills: https://cursor.com/help/customization/skills
- Gemini CLI skills: https://geminicli.com/docs/cli/skills/
- Devin Desktop skills: https://docs.devin.ai/desktop/cascade/skills
- Azure Repos PR templates: https://learn.microsoft.com/en-us/azure/devops/repos/git/pull-request-templates?view=azure-devops
- Official ASD-STE100 site: https://asd-ste100.org/
