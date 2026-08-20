CREATE PROCEDURE [ai].[usp_AssembleRagContext]
    @ShipmentId NVARCHAR(40),
    @AccountId NVARCHAR(40),
    @TopK INT = 5
AS
BEGIN
    SET NOCOUNT ON;

    SELECT TOP (@TopK)
        c.[ChunkId] AS [chunk_id],
        c.[DocumentId] AS [document_id],
        c.[ChunkOrdinal] AS [chunk_ordinal],
        c.[Content] AS [content],
        JSON_OBJECT(
            'shipment_id': c.[ShipmentId],
            'account_id': c.[AccountId],
            'depot_code': c.[DepotCode],
            'route_code': c.[RouteCode],
            'document_type': c.[DocumentType],
            'sensitivity': c.[SensitivityLabel],
            'lifecycle': c.[LifecycleState]
        ) AS [metadata],
        CONCAT(c.[DocumentId], '#', c.[ChunkOrdinal]) AS [citation]
    FROM [ai].[DocumentChunk] AS c
    WHERE c.[ShipmentId] = @ShipmentId
      AND c.[AccountId] = @AccountId
      AND c.[LifecycleState] = 'active'
      AND c.[SensitivityLabel] <> 'restricted'
    ORDER BY c.[UpdatedAt] DESC, c.[ChunkId]
    FOR JSON PATH, ROOT('chunks');
END;

