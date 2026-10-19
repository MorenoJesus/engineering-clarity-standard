# Engineering Clarity — Repository Instructions

Use the Engineering Clarity Standard (ECS) for technical prose: user stories, acceptance criteria, pull request descriptions, ADRs, runbooks, API docs, implementation plans, error explanations, and substantive code comments.

- Write direct sentences. Use one term for one concept. Name the actor, action, condition, and observable result when relevant.
- Separate confirmed facts from assumptions, proposals, missing requirements, and unverified claims.
- Preserve exact code identifiers, CLI commands, HTTP status semantics, architectural details, and security constraints.
- Use measurable Given/When/Then acceptance criteria where appropriate. Include meaningful failure paths.
- Report tests as **passed** only when verified. Otherwise state `Not run`, `Not verified`, or `Unknown`, with context.
- Do not claim formal ASD-STE100 compliance.
- For detailed writing/review tasks, load the `engineering-clarity` Agent Skill from `.agents/skills/engineering-clarity/SKILL.md` if the agent supports skills.

Apply this standard to prose. Do not rewrite valid source code solely to make it resemble simplified English. Existing repository-specific requirements take precedence when applicable.