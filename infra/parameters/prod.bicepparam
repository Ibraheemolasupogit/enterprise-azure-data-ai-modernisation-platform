using '../main.bicep'

param environment = 'prod'
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
