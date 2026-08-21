CREATE INDEX [IX_ai_DocumentChunk_Metadata]
ON [ai].[DocumentChunk] ([ShipmentId], [AccountId], [DepotCode], [RouteCode], [DocumentType], [LifecycleState], [SensitivityLabel]);
