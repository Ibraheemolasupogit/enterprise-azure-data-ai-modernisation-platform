using '../main.bicep'

param environment = 'dev'
param workloadName = 'contoso-freight'
param deployAzureSqlOperations = false
param azureSqlOperations = {
  subnetId: '/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-placeholder/providers/Microsoft.Network/virtualNetworks/vnet-placeholder/subnets/snet-sqlmi'
  administratorLogin: 'sqlmiadmin'
  serviceTier: 'GeneralPurpose'
  vCores: 4
  storageSizeInGB: 256
  licenseType: 'LicenseIncluded'
  collation: 'requires-live-validation'
  timezoneId: 'UTC'
  publicDataEndpointEnabled: false
  minimalTlsVersion: '1.2'
  backupStorageRedundancy: 'Zone'
  maintenanceConfigurationId: ''
  logRetentionDays: 30
  keyVaultPublicNetworkAccess: 'Disabled'
  enableAlerts: true
  highCpuPercentThreshold: 80
}
