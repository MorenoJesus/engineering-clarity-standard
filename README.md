# Engineering Clarity Standard (ECS) — Agent Skill Kit

**Version:** 1.0.0 · **Status:** proposed team convention · **Date:** 2026-10-18

ECS is a vendor-neutral, **ASD-STE100-inspired** writing convention for software engineering. It helps authors and coding agents produce precise user stories, acceptance criteria, pull request descriptions, runbooks, architecture decisions, API documentation, and technical plans.

> **Not ASD-STE100 certified.** ECS applies selected principles of simplified technical writing. It does not reproduce the official ASD-STE100 dictionary, implement every official rule, or establish formal compliance. Refer to https://asd-ste100.org/ for the official standard.

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