using '../main.bicep'

param environment = 'prod'
param deployDatabricksFoundation = false
param databricksFoundation = {
  workspaceSku: 'premium'
  storageSku: 'Standard_ZRS'
  workspacePublicNetworkAccess: 'Disabled'
  storagePublicNetworkAccess: 'Disabled'
  requiredNsgRules: 'NoAzureDatabricksRules'
  enableNoPublicIp: true
  logRetentionDays: 365
}
param workloadName = 'contoso-freight'
param deployAzureSqlOperations = false
param azureSqlOperations = {
  subnetId: '/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-placeholder/providers/Microsoft.Network/virtualNetworks/vnet-placeholder/subnets/snet-sqlmi'
  administratorLogin: 'sqlmiadmin'
  serviceTier: 'GeneralPurpose'
  vCores: 16
  storageSizeInGB: 1024
  licenseType: 'LicenseIncluded'
  collation: 'requires-live-validation'
  timezoneId: 'UTC'
  publicDataEndpointEnabled: false
  minimalTlsVersion: '1.2'
  backupStorageRedundancy: 'Geo'
  maintenanceConfigurationId: ''
  logRetentionDays: 90
  keyVaultPublicNetworkAccess: 'Disabled'
  enableAlerts: true
  highCpuPercentThreshold: 80
}
