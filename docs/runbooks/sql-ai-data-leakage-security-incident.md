# SQL AI Data Leakage or Security Incident

## Trigger

Suspected cross-customer retrieval, sensitive data exposure, restricted content leakage, or unauthorized audit access.

## Response

1. Disable affected retrieval or generation procedure access.
2. Preserve audit metadata and relevant security logs.
3. Confirm caller identity, filters, RLS alignment, sensitivity labels, and returned chunk IDs.
4. Identify whether source projection, chunking, retrieval filters, or prompt assembly caused exposure.
5. Remediate grants, filters, source redaction, and affected embeddings before re-enabling.

## Evidence Boundary

Local matrices define controls. Incident scope and remediation require live environment evidence.

