CREATE ROLE [shipment_reader];
CREATE ROLE [operations_reader];
CREATE ROLE [customer_service_user];
CREATE ROLE [ai_query_user];
CREATE ROLE [ai_auditor];
CREATE ROLE [api_runtime_identity];
CREATE ROLE [api_deployment_identity];

GRANT SELECT ON [dbo].[vw_ApiShipmentSummary] TO [shipment_reader];
GRANT SELECT ON [dbo].[vw_ApiShipmentEvent] TO [shipment_reader];
GRANT SELECT ON [dbo].[vw_ApiRouteContext] TO [operations_reader];
GRANT SELECT ON [dbo].[vw_ApiShipmentSummary] TO [customer_service_user];
GRANT SELECT ON [dbo].[vw_ApiShipmentEvent] TO [customer_service_user];
GRANT SELECT ON [dbo].[vw_ApiRouteContext] TO [customer_service_user];
GRANT SELECT ON [dbo].[vw_ApiServiceCaseSummary] TO [customer_service_user];
GRANT EXECUTE ON [ai].[usp_ApiSearchOperationalKnowledge] TO [ai_query_user];
GRANT EXECUTE ON [ai].[usp_ApiAskGroundedOperationsQuestion] TO [ai_query_user];
GRANT SELECT ON [ai].[vw_ApiGroundingSourceReference] TO [ai_query_user];
GRANT SELECT ON [ai].[vw_ApiGroundingSourceReference] TO [ai_auditor];

