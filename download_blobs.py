import os, uuid
from azure.storage.blob import BlobClient, ContainerClient, BlobServiceClient
from pathlib import Path, PureWindowsPath

connect_str = "azure_connection_string"

blob_service_client = BlobServiceClient.from_connection_string(connect_str)

container_client = blob_service_client.get_container_client("container_name")

print("\nListing blobs...")

# List the blobs in the container
blob_list = container_client.list_blobs()
for blob in blob_list:
    print("\t" + blob.name)

local_path = "./Downloads/Azure-Test"

# Connect to the container
container = ContainerClient.from_connection_string(connect_str, container_name="container_name")

new = None
# Get our list of blobs, and compare date modified values so we can find the report which ran this month
blob_list = container.list_blobs()
for blob in blob_list:
    #print(blob.name + '\n')
    if new == None:
        new = blob
    if new.last_modified > blob.last_modified:
        new = blob

# Create the local filepath we are downloading the blob to
download_file_path = PureWindowsPath(local_path, new.name)
download_file_path.joinpath()
print("Latest blob is: " + new.name)
print("\nDownloading blob to \n\t" + (download_file_path))

with open(download_file_path, "wb") as download_file:
    download_file.write(new.download_blob().readall())