-- Audit review examples. Latency and token fields remain null until live Azure validation captures real values.
SELECT
    RetrievalAuditId,
    RequestedAt,
    RequestingPrincipal,
    ShipmentId,
    AccountId,
    TopK,
    RetrievalMode,
    Status,
    LatencyMs,
    ErrorClass
FROM ai.RetrievalAudit
WHERE RequestedAt >= DATEADD(day, -7, SYSUTCDATETIME());

SELECT
    GenerationAuditId,
    RetrievalAuditId,
    ModelDeployment,
    ModelVersion,
    Status,
    PromptTokens,
    CompletionTokens,
    ErrorClass
FROM ai.GenerationAudit
WHERE GeneratedAt >= DATEADD(day, -7, SYSUTCDATETIME());

