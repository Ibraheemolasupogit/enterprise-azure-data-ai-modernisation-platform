targetScope = 'resourceGroup'

@description('Deployment environment name.')
@allowed([
  'dev'
  'test'
  'prod'
])
param environment string

@description('Azure region for resources that are introduced in later milestones.')
param location string = resourceGroup().location

@description('Short workload name used for future resource naming.')
param workloadName string = 'contoso-freight'

@description('Whether Azure SQL Managed Instance operational resources should be declared by this template.')
param deployAzureSqlOperations bool = false

@description('Object containing Azure SQL Managed Instance operational settings for future deployments.')
param azureSqlOperations object = {}

@description('Whether Azure Databricks foundation resources should be declared by this template.')
param deployDatabricksFoundation bool = false

@description('Object containing Azure Databricks foundation settings for future deployments.')
param databricksFoundation object = {}

@description('Tags applied to resources when real infrastructure modules are added.')
param tags object = {
  workload: workloadName
  environment: environment
  managedBy: 'bicep'
}

module azureSqlOperationsModule 'modules/azure-sql/managed-instance.bicep' = if (deployAzureSqlOperations) {
  name: 'azure-sql-operations-${environment}'
  params: {
    environment: environment
    location: location
    workloadName: workloadName
    settings: azureSqlOperations
    tags: tags
  }
}

module databricksFoundationModule 'modules/databricks/foundation.bicep' = if (deployDatabricksFoundation) {
  name: 'databricks-foundation-${environment}'
  params: {
    environment: environment
    location: location
    workloadName: workloadName
    settings: databricksFoundation
    tags: tags
  }
}

output foundation object = {
  workloadName: workloadName
  environment: environment
  location: location
  status: (deployAzureSqlOperations || deployDatabricksFoundation) ? 'Selected infrastructure modules declared for future deployment validation' : 'No Azure resources declared by default'
}

output azureSqlOperations object = deployAzureSqlOperations ? azureSqlOperationsModule.outputs.operationalSummary : {
  status: 'not declared'
}

output databricksFoundation object = deployDatabricksFoundation ? databricksFoundationModule.outputs.foundationSummary : {
  status: 'not declared'
}
