CREATE INDEX [IX_ai_Document_ShipmentAccount]
ON [ai].[Document] ([ShipmentId], [AccountId], [LifecycleState], [SensitivityLabel]);
