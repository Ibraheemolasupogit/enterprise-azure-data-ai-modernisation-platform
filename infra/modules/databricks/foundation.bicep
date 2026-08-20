targetScope = 'resourceGroup'

@description('Deployment environment name.')
param environment string

@description('Azure region.')
param location string

@description('Short workload name.')
param workloadName string

@description('Databricks foundation settings. Values must be supplied by environment parameters in a real deployment.')
param settings object

@description('Resource tags.')
param tags object

var namePrefix = '${workloadName}-${environment}'
var normalizedPrefix = replace(namePrefix, '-', '')
var workspaceName = 'adb-${namePrefix}-${location}'
var storageAccountName = take('st${normalizedPrefix}dbx', 24)
var accessConnectorName = '${namePrefix}-dbx-access-connector'
var logAnalyticsWorkspaceName = take('${normalizedPrefix}dbxlaw', 63)
var managedResourceGroupName = 'rg-${namePrefix}-databricks-managed'

resource lakeStorage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  tags: tags
  kind: 'StorageV2'
  sku: {
    name: string(settings.storageSku)
  }
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false
    isHnsEnabled: true
    minimumTlsVersion: 'TLS1_2'
    publicNetworkAccess: string(settings.storagePublicNetworkAccess)
  }
}

resource landingContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  name: '${lakeStorage.name}/default/landing'
  properties: {
    publicAccess: 'None'
  }
}

resource checkpointsContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  name: '${lakeStorage.name}/default/checkpoints'
  properties: {
    publicAccess: 'None'
  }
}

resource quarantineContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  name: '${lakeStorage.name}/default/quarantine'
  properties: {
    publicAccess: 'None'
  }
}

resource exchangeContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  name: '${lakeStorage.name}/default/exchange'
  properties: {
    publicAccess: 'None'
  }
}

resource accessConnector 'Microsoft.Databricks/accessConnectors@2023-05-01' = {
  name: accessConnectorName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
}

resource workspace 'Microsoft.Databricks/workspaces@2024-05-01' = {
  name: workspaceName
  location: location
  tags: tags
  sku: {
    name: string(settings.workspaceSku)
  }
  properties: {
    managedResourceGroupId: resourceId('Microsoft.Resources/resourceGroups', managedResourceGroupName)
    publicNetworkAccess: string(settings.workspacePublicNetworkAccess)
    requiredNsgRules: string(settings.requiredNsgRules)
    parameters: {
      enableNoPublicIp: {
        value: bool(settings.enableNoPublicIp)
      }
    }
  }
}

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logAnalyticsWorkspaceName
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: int(settings.logRetentionDays)
  }
}

resource workspaceDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'send-to-log-analytics'
  scope: workspace
  properties: {
    workspaceId: logAnalytics.id
    logs: [
      {
        category: 'accounts'
        enabled: true
      }
      {
        category: 'clusters'
        enabled: true
      }
      {
        category: 'jobs'
        enabled: true
      }
      {
        category: 'notebook'
        enabled: true
      }
      {
        category: 'dbfs'
        enabled: true
      }
    ]
  }
}

output foundationSummary object = {
  workspaceName: workspace.name
  storageAccountName: lakeStorage.name
  accessConnectorName: accessConnector.name
  logAnalyticsWorkspaceName: logAnalytics.name
  landingContainer: landingContainer.name
  checkpointsContainer: checkpointsContainer.name
  quarantineContainer: quarantineContainer.name
  exchangeContainer: exchangeContainer.name
  deploymentStatus: 'declared only - not executed locally'
}

