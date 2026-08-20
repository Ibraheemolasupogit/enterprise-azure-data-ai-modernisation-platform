CREATE ROLE [ai_app_executor];
CREATE ROLE [ai_data_curator];
CREATE ROLE [ai_auditor];
CREATE ROLE [embedding_worker_identity];

GRANT EXECUTE ON SCHEMA::[ai] TO [ai_app_executor];
GRANT SELECT ON [ai].[Document] TO [ai_data_curator];
GRANT SELECT, INSERT, UPDATE ON [ai].[Document] TO [ai_data_curator];
GRANT SELECT, INSERT, UPDATE ON [ai].[DocumentChunk] TO [ai_data_curator];
GRANT SELECT ON [ai].[RetrievalAudit] TO [ai_auditor];
GRANT SELECT ON [ai].[GenerationAudit] TO [ai_auditor];
GRANT SELECT, UPDATE ON [ai].[DocumentChunk] TO [embedding_worker_identity];
GRANT SELECT, INSERT, UPDATE ON [ai].[EmbeddingMetadata] TO [embedding_worker_identity];

