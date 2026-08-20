-- Target-ready external model pattern. Managed identity is preferred; no secrets are stored here.
-- Validate exact provider, model, and credential syntax in the target Azure SQL release.
CREATE DATABASE SCOPED CREDENTIAL [https://<azure-openai-resource>.openai.azure.com]
WITH IDENTITY = 'Managed Identity';

CREATE EXTERNAL MODEL [ai].[shipment_ops_embedding_model]
WITH
(
    LOCATION = 'https://<azure-openai-resource>.openai.azure.com/openai/deployments/<embedding-deployment>/embeddings?api-version=<api-version>',
    API_FORMAT = 'Azure OpenAI',
    MODEL_TYPE = EMBEDDINGS,
    MODEL = 'text-embedding-3-small',
    CREDENTIAL = [https://<azure-openai-resource>.openai.azure.com]
);

