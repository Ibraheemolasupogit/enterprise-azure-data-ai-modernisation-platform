targetScope = 'resourceGroup'

@description('Deployment environment name.')
param environment string

@description('Azure region.')
param location string

@description('Short workload name.')
param workloadName string

@description('Operational settings object. Values must be supplied by environment parameters in a real deployment.')
param settings object

@description('Resource tags.')
param tags object

var namePrefix = '${workloadName}-${environment}'
var managedInstanceName = take(replace('${namePrefix}-sqlmi', '-', ''), 63)
var logAnalyticsWorkspaceName = take(replace('${namePrefix}-law', '-', ''), 63)
var userAssignedIdentityName = '${namePrefix}-sqlmi-ops-mi'
var keyVaultName = take(replace('${namePrefix}-kv', '-', ''), 24)
var subnetId = string(settings.subnetId)
var administratorLogin = string(settings.administratorLogin)
var administratorPassword = settings.administratorPassword

resource operationsIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: userAssignedIdentityName
  location: location
  tags: tags
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

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  tags: tags
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    enableRbacAuthorization: true
    publicNetworkAccess: string(settings.keyVaultPublicNetworkAccess)
  }
}

resource sqlMi 'Microsoft.Sql/managedInstances@2023-08-01-preview' = {
  name: managedInstanceName
  location: location
  tags: tags
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${operationsIdentity.id}': {}
    }
  }
  sku: {
    name: string(settings.serviceTier)
    tier: string(settings.serviceTier)
  }
  properties: {
    administratorLogin: administratorLogin
    administratorLoginPassword: administratorPassword
    subnetId: subnetId
    vCores: int(settings.vCores)
    storageSizeInGB: int(settings.storageSizeInGB)
    licenseType: string(settings.licenseType)
    collation: string(settings.collation)
    timezoneId: string(settings.timezoneId)
    publicDataEndpointEnabled: bool(settings.publicDataEndpointEnabled)
    minimalTlsVersion: string(settings.minimalTlsVersion)
    storageAccountType: string(settings.backupStorageRedundancy)
    maintenanceConfigurationId: string(settings.maintenanceConfigurationId)
  }
}

resource diagnosticSettings 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'send-to-log-analytics'
  scope: sqlMi
  properties: {
    workspaceId: logAnalytics.id
    logs: [
      {
        category: 'ResourceUsageStats'
        enabled: true
      }
      {
        category: 'DevOpsOperationsAudit'
        enabled: true
      }
      {
        category: 'SQLSecurityAuditEvents'
        enabled: true
      }
    ]
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
      }
    ]
  }
}

resource highCpuAlert 'Microsoft.Insights/metricAlerts@2018-03-01' = {
  name: '${managedInstanceName}-high-cpu'
  location: 'global'
  tags: tags
  properties: {
    description: 'Sustained CPU alert for SQL MI. Threshold requires live tuning.'
    severity: 3
    enabled: bool(settings.enableAlerts)
    scopes: [
      sqlMi.id
    ]
    evaluationFrequency: 'PT5M'
    windowSize: 'PT15M'
    criteria: {
      'odata.type': 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria'
      allOf: [
        {
          name: 'cpuPercent'
          metricName: 'avg_cpu_percent'
          operator: 'GreaterThan'
          threshold: int(settings.highCpuPercentThreshold)
          timeAggregation: 'Average'
          criterionType: 'StaticThresholdCriterion'
        }
      ]
    }
  }
}

output operationalSummary object = {
  managedInstanceName: managedInstanceName
  identityName: operationsIdentity.name
  logAnalyticsWorkspaceName: logAnalytics.name
  keyVaultName: keyVault.name
  publicDataEndpointEnabled: bool(settings.publicDataEndpointEnabled)
  deploymentStatus: 'declared only - not executed locally'
}
