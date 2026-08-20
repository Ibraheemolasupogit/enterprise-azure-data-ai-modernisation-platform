# ADR-0003: Database-Native AI vs External AI Search

- Status: Accepted
- Date: 2026-08-20

## Context

Azure SQL is gaining native AI and vector capabilities, while enterprise RAG often requires cross-domain retrieval, orchestration, evaluation, safety controls, and integration with broader AI services. Treating either side as the only AI architecture would create poor boundaries.

## Decision

Use database-native AI capabilities for close-to-operational-data scenarios where SQL security, locality, and transactional context are important. Use external search, vector, hybrid retrieval, and Azure OpenAI orchestration for broader grounded RAG scenarios that span curated data products, operational knowledge, and documents.

## Consequences

The platform can demonstrate both SQL-native intelligence and AI-platform responsibilities without conflating them. Future milestones must define explicit data contracts, security trimming, embedding generation boundaries, and evaluation methods.

## Alternatives Considered

- Put all AI retrieval inside Azure SQL: attractive for locality but too narrow for cross-domain RAG.
- Put all AI retrieval outside the database: flexible but risks duplicating sensitive data and bypassing SQL governance.
- Build an ungrounded assistant first: faster demo value but not enterprise credible.

