# ----------------------------------------------------------------------------
# Azure function to parse .edi and .xml files
# January 2022
# Peer Christensen - pch@kapacity.dk
# ----------------------------------------------------------------------------

import datetime
import logging
import pytz
import os
from glob import glob

import azure.functions as func
from azure.storage.blob import BlobServiceClient

from .azure_utils import get_engine, write_output, get_container, connect_key_vault
from .parse import parse_files

tz = pytz.timezone("Europe/Copenhagen")
temp_path = "/tmp" 
container_name = "certificatefiles"

env = os.environ["ENVIRONMENT"]
if env == "dev":
    key_vault_url = "https://kv-indeksretailbi-dev.vault.azure.net/"
elif env == "test":
    key_vault_url = "https://kv-indeksretailbi-test.vault.azure.net/"
else:
    key_vault_url = "https://kv-indeksretailbi-prod.vault.azure.net/"

# -------------------------------------------------------------------------
# Main function
# -------------------------------------------------------------------------

def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')

    logging.info("Connecting to keyVault")
    KeyVaultClient  = connect_key_vault(key_vault_url=key_vault_url)

    logging.info("Creating blob service client")
    blob_service_client = BlobServiceClient.from_connection_string(
        KeyVaultClient.get_secret("StorageAccountConnectionString").value)

    # -------------------------------------------------------------------------
    # Download files
    # -------------------------------------------------------------------------

    logging.info("Creating container client")
    container_client = get_container(
        blob_service_client=blob_service_client,
        container_name=container_name)

    logging.info("Downloading files")
    blob_list = container_client.list_blobs()
    dropped_dirs = ("Archive", "NewFiles/Backup/")

    for blob in blob_list:
        if not blob.name.startswith(dropped_dirs):
            blob_client = container_client.get_blob_client(blob.name)
            download_file_path = os.path.join(temp_path, blob.name.replace("NewFiles/", ""))
            with open(download_file_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())

    # -------------------------------------------------------------------------
    # List files
    # -------------------------------------------------------------------------

    glob_pattern = os.path.join(temp_path, '*')
    file_names = glob(glob_pattern)
    file_names = [name for name in file_names if name.endswith((".xml", ".edi"))]
    n_files = len(file_names)
    logging.info(f"{n_files} files were downloaded")

    if n_files == 0:
        return func.HttpResponse(
            "No files were found in NewFiles folder",
             status_code=500)

    # -------------------------------------------------------------------------
    # Parse files
    # -------------------------------------------------------------------------

    logging.info("Parsing files")
    df = parse_files(file_names)

    logging.info("Adding timestamp to output")
    now = datetime.datetime.now(tz)
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    df["DWCreatedDate"] = dt_string

    # -------------------------------------------------------------------------
    # Write to SQL
    # -------------------------------------------------------------------------

    logging.info("Creating engine")
    engine = get_engine(KeyVaultClient = KeyVaultClient)

    logging.info("Writing output")
    try:
        write_output(output=df, to_table="CertificatesFiles", engine=engine)
    except Exception as e:
        print(e)

    logging.info("End of function")
    return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200)
