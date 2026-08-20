@description('Deployment environment name.')
param environment string

@description('Azure region.')
param location string

@description('Short workload name.')
param workloadName string

@description('Container image for the Data API Builder/API runtime.')
param containerImage string = 'mcr.microsoft.com/azure-databases/data-api-builder:latest'

@description('Whether ingress is externally reachable. Use false for private/internal production ingress.')
param externalIngress bool = false

@description('Application integration settings. Values must not contain secrets.')
param settings object = {}

@description('Tags applied to resources.')
param tags object = {}

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${workloadName}-${environment}-api-law'
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${workloadName}-${environment}-api-ai'
  location: location
  kind: 'web'
  tags: tags
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

resource environmentResource 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: '${workloadName}-${environment}-apps'
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: ''
      }
    }
  }
}

resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: '${workloadName}-${environment}-api'
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    managedEnvironmentId: environmentResource.id
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: externalIngress
        targetPort: 5000
        transport: 'http'
      }
    }
    template: {
      containers: [
        {
          name: 'data-api-builder'
          image: containerImage
          env: [
            {
              name: 'APPLICATION_SQL_CONNECTION_STRING'
              value: '<managed-identity-sql-connection-string-from-secure-configuration>'
            }
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              value: appInsights.properties.ConnectionString
            }
          ]
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: int(coalesce(settings.maxReplicas, 3))
      }
    }
  }
}

output integrationSummary object = {
  status: 'application integration resources declared for controlled future deployment'
  hosting: 'Azure Container Apps'
  managedIdentity: containerApp.identity.principalId
  applicationInsights: appInsights.name
  logAnalytics: logAnalytics.name
}
