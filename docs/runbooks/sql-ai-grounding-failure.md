# SQL AI Suspected Grounding Failure

## Trigger

An answer cites unsupported content, omits insufficiency, or appears to use model prior knowledge instead of retrieved context.

## Response

1. Preserve `RetrievalAuditId`, `GenerationAuditId`, cited chunks, prompt contract version, and model deployment.
2. Review whether retrieved chunks actually support the answer.
3. Check prompt-injection text in retrieved notes and carrier updates.
4. Disable or revise the affected prompt/ranking path if needed.
5. Add the case to the evaluation dataset before re-enabling.

## Evidence Boundary

Local context assembly is validated. Live model grounding requires Azure OpenAI validation and human review.

