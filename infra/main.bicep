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

@description('Tags applied to resources when real infrastructure modules are added.')
param tags object = {
  workload: workloadName
  environment: environment
  managedBy: 'bicep'
}

output foundation object = {
  workloadName: workloadName
  environment: environment
  location: location
  status: 'Milestone 1 scaffold only - no Azure resources declared'
}

