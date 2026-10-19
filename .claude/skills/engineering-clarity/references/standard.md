# ECS Writing Standard — normative rules

**Version:** 1.0.0 · **Applies to:** technical prose created or revised by people and AI coding agents.

## Intent

A reader should be able to answer: What is required? Under which conditions? Who or what acts? What result is observable? How was it verified? What remains unknown?

ECS draws from simplified technical writing principles associated with ASD-STE100. It is **not** the official aerospace standard, a substitute for the official dictionary, or a compliance certification. We do not reproduce the ASD-STE100 controlled dictionary.

## Required rules

**ECS-01 — Use one name for each concept.** Define component and domain terms once. Use them consistently throughout an artifact. For example, do not switch among `message`, `event`, `request`, and `job` when they refer to the same object. Do not conflate them if they are different objects.

**ECS-02 — Identify the actor when it affects meaning.** State whether a user, service, handler, database, administrator, or automation performs the action. Active voice is preferred for instructions. Passive voice is acceptable when the state or result matters more than the actor.

**ECS-03 — State one primary action per instruction.** Split steps that have independent prerequisites, failures, or results. Keep sentences short enough to follow; target approximately 25 words or fewer for routine instructions, without sacrificing precision.

**ECS-04 — Prefer explicit conditions.** Use `If`, `When`, `Before`, `After`, `Given`, and `Then` when they make a requirement testable. Specify ordering, retry limits, and time windows when those details matter.

**ECS-05 — State observable results.** Replace words such as `properly`, `quickly`, `robust`, `seamlessly`, `efficiently`, and `as needed` with the specific behavior or measurable requirement. If the requirement is unknown, label it as a question or assumption.

**ECS-06 — Use requirement language consistently.** `Must` = mandatory requirement. `Should` = recommendation, not an acceptance requirement. `May` = permission or option. `Can` = capability. Do not hide mandatory behavior under `should`.

**ECS-07 — Preserve exact technical meaning.** Do not rename classes, methods, endpoints, message properties, CLI options, HTTP codes, configuration keys, service names, security controls, or units for readability. Use code formatting for identifiers. A technically wrong simple sentence is worse than a precise complex one.

**ECS-08 — Separate evidence from expectation.** `Implemented` is not `Tested`. `Unit tests passed` requires actual test output. A future behavior described by acceptance criteria is not a current verified result. Record `Not run`, `Not verified`, or `Unknown` when appropriate.

**ECS-09 — Explain failure behavior.** Where relevant, describe invalid input, authorization failures, retries, cancellation, timeouts, duplicate requests, partial success, data recovery, logging, and operational handoff. Do not invent decisions that a product owner must make.

**ECS-10 — Use exact numbers and units.** Prefer `within 2 seconds at the 95th percentile under an agreed workload` over `fast`. When a threshold is not known, use `Open question: required latency target` instead of guessing.

**ECS-11 — Make assumptions visible.** Label assumptions, proposed behavior, dependencies, risks, and open decisions. Do not present inferred requirements as approved facts.

**ECS-12 — Respect artifact boundaries.** User stories describe user value; acceptance criteria describe outcomes; design notes explain choices; PRs describe actual changes and verified results; runbooks describe operational actions and safe recovery. Do not turn a business user story into a low-level implementation checklist unless technically required.

## Writing decisions

- Prefer a numbered list for ordered operations. Use bullets for independent items.
- Use one meaning for `retry`, `dead-letter`, `complete`, `abandon`, and `duplicate`. Define service-specific semantics if required.
- Keep error messages actionable without exposing secrets, credentials, stack traces, or personal data to unauthorized users.
- Prefer specific positive instructions. Use `Do not` for prohibited actions or dangerous failure modes.
- Use direct sentences rather than marketing adjectives. Avoid needless formality.
- Preserve quoted evidence and original requirement text when editing could misrepresent a source. Explain the proposed rewrite separately.
- Do not expand every simple task into a long document. Required sections may be marked `Not applicable` with a reason.

## Release quality gate

A finished artifact passes a human review only if:

1. Its purpose, audience, and scope are clear.
2. Technical terms and identifiers are consistent and correct.
3. Conditions and results are explicit where needed.
4. Each requirement and acceptance criterion is verifiable.
5. Failure behavior and dependencies are covered when relevant.
6. Test and operational claims are supported by evidence.
7. Unknowns and assumptions are labeled.
8. No sentence was simplified at the expense of accuracy or security.

A rule-based linter may flag possible issues, but it cannot certify this gate or formal ASD-STE100 compliance.
