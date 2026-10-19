# [Endpoint / operation name]

## Purpose

[Which capability does this API provide?]

## Contract

- **Method:** `[GET|POST|PUT|PATCH|DELETE]`
- **Path:** `[Exact URI path]`
- **Authentication / authorization:** [Verified requirements or Unknown]
- **Idempotency:** [Contract or Unknown]

## Request

| Field / header | Type | Required | Constraints |
| --- | --- | --- | --- |
| `[exactFieldName]` | [Type] | [Yes/No] | [Constraint] |

## Responses

| HTTP status | Condition | Body / behavior |
| --- | --- | --- |
| [200/201/204] | [Success condition] | [Exact expected behavior] |
| [4xx] | [Validation/auth/contract error] | [Exact expected behavior] |
| [5xx] | [Server failure] | [Documented behavior] |

## Examples

[Include exact request and response formats only when verified.]

## Open questions

[Unapproved fields, limits, error codes, and semantics.]
