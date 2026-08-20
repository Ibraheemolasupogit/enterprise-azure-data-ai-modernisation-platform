# SQL AI Azure OpenAI Invocation Failure

## Trigger

`sp_invoke_external_rest_endpoint` returns timeout, throttling, authorization, endpoint, or malformed response errors.

## Response

1. Record failure in `ai.GenerationAudit`.
2. Return a grounded unavailable or insufficiency response; do not fabricate an answer.
3. Validate managed identity, approved endpoint, deployment name, API version, timeout, and retry policy.
4. Retry with bounded backoff only when the error class is retryable.
5. Escalate persistent failures to platform and AI owners.

## Evidence Boundary

Local assets define the invocation boundary. Real endpoint behavior requires Azure OpenAI validation.

