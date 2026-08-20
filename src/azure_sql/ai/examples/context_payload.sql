-- Context JSON shape used by the prompt contract.
SELECT
    @Question AS [question],
    'use-context-only' AS [grounding_policy],
    JSON_QUERY((
        SELECT TOP (@TopK)
            c.ChunkId AS [chunk_id],
            c.DocumentId AS [document_id],
            c.Content AS [content],
            JSON_OBJECT(
                'shipment_id': c.ShipmentId,
                'account_id': c.AccountId,
                'depot_code': c.DepotCode,
                'route_code': c.RouteCode,
                'document_type': c.DocumentType
            ) AS [metadata],
            CONCAT(c.DocumentId, '#', c.ChunkOrdinal) AS [citation]
        FROM ai.DocumentChunk AS c
        WHERE c.ShipmentId = @ShipmentId
          AND c.AccountId = @AccountId
          AND c.LifecycleState = 'active'
          AND c.SensitivityLabel <> 'restricted'
        FOR JSON PATH
    )) AS [chunks]
FOR JSON PATH, WITHOUT_ARRAY_WRAPPER;
