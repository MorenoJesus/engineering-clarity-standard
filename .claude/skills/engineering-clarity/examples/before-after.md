# Before and After — ECS Examples

These are illustrative drafts, not evidence of real implementations or test executions.

## User story

**Before:** `As a user, I want better error handling so everything works smoothly.`

**After (business value):** `As a support engineer, I want to identify messages that the service could not process so that I can investigate failures.`

**AC-01:** Given that a message exceeds the configured delivery limit, when the messaging service applies the dead-letter policy, then the message is available in the dead-letter queue.

**AC-02:** Given that a message is in the dead-letter queue, when a support engineer opens its details, then the details include the message ID and the recorded failure reason.

**Open question:** What user interface or tool will the support engineer use to see those details? What message data can that role access?

## Pull request

**Before:** `Improved message handling and fixed retry issues. Tests look good.`

**After (example structure):**

- **Purpose:** Prevent a duplicate message from updating the same record twice.
- **Changes:** Added a message ID check before the update transaction. Added an error log entry when the database operation fails.
- **Validation:** Unit test for duplicate handling: **Not run**. Integration test with Service Bus: **Not run**. These are not claims about test success.
- **Risk:** Concurrent workers may both pass the initial check. A unique constraint or transactional protection may be required.
- **Rollback:** Not yet defined. Confirm whether the change creates persistent schema or state before selecting a rollback path.

## Operational step

**Before:** `If it breaks, restart everything and try again.`

**After:** `If the message handler stops processing, inspect the service health check and the most recent error log entry. Do not restart the service until you confirm the failed dependency and the approved recovery procedure.`

## API behavior

**Before:** `The API returns a useful error when something goes wrong.`

**After:** `If the request body fails validation, the API returns HTTP 400 with a machine-readable error code and the invalid field names.`

**Note:** The after version is a proposed contract until validated against the implementation or approved requirements.
