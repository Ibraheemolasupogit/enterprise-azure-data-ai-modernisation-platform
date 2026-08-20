CREATE VIEW [dbo].[vw_ApiShipmentSummary]
AS
SELECT
    s.[ShipmentId],
    s.[AccountId],
    s.[Status],
    s.[OriginDepotId],
    s.[DestinationDepotId],
    s.[RouteId],
    s.[CreatedAt],
    s.[UpdatedAt],
    CAST(NULL AS NVARCHAR(20)) AS [DepotCode],
    CAST(NULL AS NVARCHAR(40)) AS [RouteCode],
    CAST(NULL AS DATETIME2(3)) AS [LastEventAt]
FROM [dbo].[Shipment] AS s;

GO

CREATE VIEW [dbo].[vw_ApiShipmentEvent]
AS
SELECT
    h.[ShipmentId],
    h.[EventSequence],
    h.[EventType],
    h.[EventOccurredAt],
    h.[RecordedAt],
    h.[LocationCode],
    h.[StatusAfterEvent]
FROM [dbo].[ShipmentEventHistory] AS h;

GO

CREATE VIEW [dbo].[vw_ApiRouteContext]
AS
SELECT
    r.[RouteCode],
    d.[DepotCode],
    d.[DepotName],
    r.[ServiceRegion],
    CAST(NULL AS NVARCHAR(40)) AS [CarrierCode]
FROM [dbo].[Route] AS r
JOIN [dbo].[Depot] AS d
  ON d.[DepotId] = r.[OriginDepotId];

GO

CREATE VIEW [dbo].[vw_ApiServiceCaseSummary]
AS
SELECT
    CAST('case-placeholder' AS NVARCHAR(80)) AS [CaseId],
    CAST(NULL AS NVARCHAR(40)) AS [ShipmentId],
    CAST(NULL AS NVARCHAR(40)) AS [AccountId],
    CAST('sanitized summary only; raw notes are not exposed' AS NVARCHAR(400)) AS [CaseSummary],
    CAST(NULL AS DATETIME2(3)) AS [OpenedAt],
    CAST(NULL AS NVARCHAR(40)) AS [CaseStatus];

GO

CREATE VIEW [ai].[vw_ApiGroundingSourceReference]
AS
SELECT
    CONVERT(NVARCHAR(80), ra.[RetrievalAuditId]) AS [ReferenceId],
    ra.[RetrievalAuditId],
    ra.[RequestedAt],
    ra.[RequestingPrincipal],
    ra.[ShipmentId],
    ra.[AccountId],
    ra.[RetrievedChunksJson],
    ra.[Status]
FROM [ai].[RetrievalAudit] AS ra;

