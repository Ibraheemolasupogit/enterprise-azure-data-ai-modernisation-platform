CREATE PROCEDURE [ai].[usp_ApiSearchOperationalKnowledge]
    @Question NVARCHAR(2000),
    @ShipmentId NVARCHAR(40) = NULL,
    @AccountId NVARCHAR(40) = NULL,
    @TopK INT = 3,
    @CorrelationId NVARCHAR(80) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    IF @TopK < 1 OR @TopK > 5
        THROW 51000, 'topK must be between 1 and 5.', 1;

    EXEC [ai].[usp_AssembleRagContext]
        @ShipmentId = @ShipmentId,
        @AccountId = @AccountId,
        @TopK = @TopK;
END;

GO

CREATE PROCEDURE [ai].[usp_ApiAskGroundedOperationsQuestion]
    @Question NVARCHAR(2000),
    @ShipmentId NVARCHAR(40) = NULL,
    @AccountId NVARCHAR(40) = NULL,
    @RouteCode NVARCHAR(40) = NULL,
    @TopK INT = 3,
    @CorrelationId NVARCHAR(80)
AS
BEGIN
    SET NOCOUNT ON;

    IF @Question IS NULL OR LEN(@Question) = 0 OR LEN(@Question) > 2000
        THROW 51001, 'question is required and must be 2000 characters or fewer.', 1;

    IF @TopK < 1 OR @TopK > 5
        THROW 51002, 'topK must be between 1 and 5.', 1;

    -- Target-ready boundary: caller authorization must be enforced before retrieval.
    -- Retrieved content remains untrusted; generation must use only authorized context.
    EXEC [ai].[usp_AssembleRagContext]
        @ShipmentId = @ShipmentId,
        @AccountId = @AccountId,
        @TopK = @TopK;
END;

