from sqlalchemy import create_engine

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def connect_key_vault(key_vault_url: str):

    # Get credentials
    credentials = DefaultAzureCredential()
    # Create a secret client
    secret_client = SecretClient(
        key_vault_url,
        credentials
        )
    return secret_client


def get_engine(KeyVaultClient):
    
    #KeyVaultClient  = _connect_key_vault(key_vault_name = key_vault_name)
    connectionstring = 'mssql+pyodbc://{uid}:{password}@{server}.database.windows.net:1433/{database}?driver={driver}'.format(
    
    uid              = KeyVaultClient.get_secret("SQLUserName").value,
    password         = KeyVaultClient.get_secret("SQLUserPassword").value,
    server           = KeyVaultClient.get_secret("SSMSServerName").value,
    database         = KeyVaultClient.get_secret("SSMSDatabaseName").value,
    driver           = 'ODBC Driver 17 for SQL Server'.replace(' ', '+')
    )

    engine = create_engine(connectionstring)    
    return engine


def write_output(output, to_table, engine):
    
    output.to_sql(f"{to_table}", engine, if_exists='append', index=False, schema="SourceAI")

    
def get_container(container_name, blob_service_client):

    container_client = blob_service_client.get_container_client(container_name)
    return container_client
    