import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import argparse

try:
    print("Azure Blob Storage Python quickstart sample")

    parser = argparse.ArgumentParser(description='Upload Model')
    parser.add_argument('-c', '--connection', required=True, help="azure storage connection string")
    args = parser.parse_args()

    blob_service_client = BlobServiceClient.from_connection_string(args.connection)

    exists = False
    suffix = 0
    containers = blob_service_client.list_containers(include_metadata=True)
    for container in containers:
        existing_container_name = container['name']
        print(existing_container_name, container['metadata'])
        if existing_container_name.startswith("anime-model"):
            parts = existing_container_name.split("-")
            if len(parts) == 2:
                try:
                    new_suffix = int(parts[-1])
                except ValueError:
                    print(f"Unable to convert '{parts[-1]}' to an integer")
                    continue  # Skip this container
                if new_suffix >= suffix:
                    suffix = new_suffix + 1  # Increment suffix

    # Create container with the next available suffix
    container_name = f"anime-model-{suffix}"

    for container in containers:
        print("\t" + container['name'])
        if container_name == container['name']:
            print("Container already exists!")
            exists = True
            break

    if not exists:
        container_client = blob_service_client.create_container(container_name)

    local_file_name = "anime_model.pkl"
    upload_file_path = os.path.join(".", local_file_name)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)

except Exception as ex:
    print('Exception:')
    print(ex)
    exit(1)

