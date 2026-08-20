FROM mcr.microsoft.com/azure-databases/data-api-builder:latest

COPY src/api/dab/dab-config.production.json /App/dab-config.production.json

ENV DAB_ENVIRONMENT=Production

CMD ["--ConfigFileName", "/App/dab-config.production.json"]

