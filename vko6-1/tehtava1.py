import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from unicodedata import name
from azure.storage.blob import BlobClient
import requests

SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
GROUP_NAME = "pietari-rg-checkpoint1"
STORAGE_ACCOUNT = "pietaricheckpoint1sa"
BLOB_CONTAINER = "pietaricheckpoint1blob"
LOCATION = 'westeurope'
CONNECTIONSTR = 'DefaultEndpointsProtocol=https;AccountName=pietaricheckpoint1sa;AccountKey=aP63dAbVnJmcCimD5+TL9hDuH2Pyr3BZ4g9qMOaeVgxmZR4U4r26v91CigT4qRDWGzS/+9cZVFUctp++TrhFJg==;EndpointSuffix=core.windows.net'
FILENAME = 'checkpoint.txt'

#Haetaan ja kirjoitetaan ensin json-datasta haetut kentät tiedostoon

r = requests.get('https://2ri98gd9i4.execute-api.us-east-1.amazonaws.com/dev/academy-checkpoint2-json')
data = r.json()

for d in data['items']:
    with open(FILENAME, 'a') as f:
        print(f'{d["parameter"]}', file=f)

#Luodaan uusi RG, Storage Account ja Blob Container, johon tiedosto uploadataan

resource_client = ResourceManagementClient(
    credential=DefaultAzureCredential(),
     subscription_id=SUBSCRIPTION_ID
)
storage_client = StorageManagementClient(
    credential=DefaultAzureCredential(),
    subscription_id=SUBSCRIPTION_ID
)

# Create resource group
resource_client.resource_groups.create_or_update(
    GROUP_NAME,
    {"location": LOCATION}
)
#create storage account
storage_client.storage_accounts.begin_create(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        {
          "sku": {
            "name": "Standard_GRS"
          },
          "kind": "StorageV2",
          "location": LOCATION,
          "encryption": {
            "services": {
              "file": {
                "key_type": "Account",
                "enabled": True
              },
              "blob": {
                "key_type": "Account",
                "enabled": True
              }
            },
            "key_source": "Microsoft.Storage"
          },
          "tags": {
            "key1": "pietari",
            "key2": "checkpoint1"
          }
        }
    ).result()

# Create blob container
blob_container = storage_client.blob_containers.create(
    GROUP_NAME,
    STORAGE_ACCOUNT,
    BLOB_CONTAINER,
    {}
)

#Upload cretaed file to blob container
blob = BlobClient.from_connection_string(conn_str=CONNECTIONSTR, container_name=BLOB_CONTAINER, blob_name=FILENAME)

with open("c:\\temp\\checkpoint1\\checkpoint.txt", "rb") as data:
    blob.upload_blob(data)