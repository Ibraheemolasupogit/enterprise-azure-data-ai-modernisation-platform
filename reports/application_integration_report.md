# Secure Application and API Integration Report

Milestone 14 defines a secure application/API integration layer for selected Azure SQL, SQL AI, and governed application-facing data capabilities. It covers Data API Builder, REST, GraphQL, stored-procedure boundaries, Entra authentication, managed identity, Container Apps hosting, MCP-compatible tool consumption, observability, resilience, CI/CD validation, and deterministic evidence.

## Scope

The API surface is allowlisted and read-focused. It exposes shipment lookup, operational reference lookup, sanitized customer-service case retrieval, governed AI retrieval/RAG execution, and grounding source metadata. It does not expose arbitrary SQL, raw administrative tables, destructive tools, a chatbot UI, or autonomous operational actions.

## Runtime Boundary

Local validation checks configuration, catalogs, schemas, mappings, security scenarios, and evidence consistency. Azure SQL object execution, Data API Builder runtime behavior, Entra token validation, managed identity to SQL, Container Apps hosting, and Azure OpenAI integration require Azure or application runtime validation.
