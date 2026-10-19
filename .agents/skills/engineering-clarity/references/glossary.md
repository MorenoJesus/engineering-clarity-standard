# ECS Terminology Guide

A project glossary is the preferred source of approved domain terms. If the project lacks a glossary, propose a small one and request approval for contested meanings.

| Term | Meaning in the document | Common confusion to avoid |
| --- | --- | --- |
| Requirement | Mandatory business or system behavior | Design suggestion |
| Acceptance criterion | Testable condition for accepting work | Implementation task |
| Verification | Evidence that a condition is satisfied | Prediction or expectation |
| Validation | Assessment that the delivered behavior meets a user need | Compilation alone |
| Retry | Another processing attempt under a defined policy | Guaranteed eventual success |
| Idempotent operation | An operation for which repetition has the same intended effect as one execution | Exactly-once delivery guarantee |
| Dead-letter queue | A queue for messages that are not processed successfully under specified conditions | Arbitrary error log |
| Rollback | A planned recovery to a prior supported state | Always equivalent to `git revert` |

**Project-specific table to complete:**

| Approved term | Definition | Owner / source | Discouraged synonyms |
| --- | --- | --- | --- |
| [Component or business term] | [One meaning] | [Approved reference] | [Confusable terms] |

When a word changes meaning between services or teams, explicitly scope it (`Service Bus message`, `HTTP request`, `domain event`). Never simplify distinct concepts into a single term.
