from azure.storage.blob import BlobClient
import os.path
import time
import argparse

CONNECTIONSTR = 'DefaultEndpointsProtocol=https;AccountName=pietaricheckpoint1sa;AccountKey=aP63dAbVnJmcCimD5+TL9hDuH2Pyr3BZ4g9qMOaeVgxmZR4U4r26v91CigT4qRDWGzS/+9cZVFUctp++TrhFJg==;EndpointSuffix=core.windows.net'
BLOB_CONTAINER = "pietaricheckpoint1blob"
FILENAME = 'checkpoint.txt'
FILEPATH = 'c:\\temp\\checkpoint1\\vko6-2\\downloaded_checkpoint.txt'

blob = BlobClient.from_connection_string(conn_str=CONNECTIONSTR, container_name=BLOB_CONTAINER, blob_name="checkpoint.txt")

with open(FILEPATH, "wb") as my_blob:
    blob_data = blob.download_blob()
    blob_data.readinto(my_blob)
    
file_present = False

while file_present == False:
    if os.path.isfile(FILEPATH):
       # read file in
       file_present = True
       break

    time.sleep(5)

parser = argparse.ArgumentParser()
parser.add_argument("luku1", help="Syötä luku, jolla määrität, monta riviä tulostetaan", type=int)
args = parser.parse_args()

f = open(FILEPATH, "r")
number_of_lines = args.luku1

for i in range(number_of_lines):
    line = f.readline()
    print(line)