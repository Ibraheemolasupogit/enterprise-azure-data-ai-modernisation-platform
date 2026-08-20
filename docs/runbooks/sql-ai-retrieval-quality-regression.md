# SQL AI Retrieval Quality Regression

## Trigger

Precision@K, Recall@K, MRR, or human review indicates degraded grounded retrieval.

## Response

1. Freeze model, chunking, and ranking changes until classified.
2. Compare current dataset results against the previous deterministic evidence.
3. Check source freshness, stale embeddings, filters, full-text terms, and vector search mode.
4. Add representative queries and expected chunks before changing ranking logic.
5. Promote only after the regression gate is accepted.

## Evidence Boundary

Local fixtures detect deterministic regressions. Live relevance requires Azure SQL and Azure OpenAI validation.

