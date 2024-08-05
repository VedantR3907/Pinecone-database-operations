import os
import sys
import json
sys.path.append('../')
from constants import PINECONE_NAMESPACE, PINECONE_CLIENT, PINECONE_INDEX_NAME
from text_and_embeddings.main import Generate_TextAndEmbeddings
from pinecone import ServerlessSpec

index_name = PINECONE_INDEX_NAME
pc = PINECONE_CLIENT
namespace = PINECONE_NAMESPACE

def upsert_data(json_path: str, index_name: str) -> None:
    """
    Upserts data into a Pinecone index and removes these records from the metadata file.

    Args:
        json_path (str): The path to the JSON file containing the embeddings.
        index_name (str): The name of the Pinecone index.
    """

    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=512,
            metric="cosine",
            spec=ServerlessSpec(
                cloud='aws', 
                region='us-east-1'
            )
        )

        print("INDEX CREATED SUCCESSFULLY")
    else:
        print("INDEX ALREADY EXISTS")
    index = pc.Index(index_name)
    
    # Load the data from JSON
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Prepare vectors for upsertion
    vectors = [
        {
            "id": entry["id"],
            "values": entry["values"],
            "metadata": {
                "text": entry["metadata"]["text"],
                "creation_date": entry["metadata"]["creation_date"],
                "file_name": entry["metadata"]["file_name"],
                "file_path": entry["metadata"]["file_path"],
                "file_size": entry["metadata"]["file_size"],
                "last_modified_date": entry["metadata"]["last_modified_date"]
            }
        }
        for entry in data
    ]
    
    # Extract IDs for the records to be upserted
    ids_to_upsert = [entry["id"] for entry in data]
    
    # Upsert vectors into Pinecone
    index.upsert(vectors=vectors, namespace=namespace)
    print(f"Data has been upserted into the Pinecone index '{index_name}'.")

    # Remove records from metadata that were upserted
    updated_metadata = [entry for entry in data if entry["id"] not in ids_to_upsert]
    
    # Write the updated metadata back to the JSON file
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(updated_metadata, file, indent=4)
    
    print("Records that were upserted have been removed from the metadata file.")

if __name__ == "__main__":
    # Define paths and credentials
    metadata_json_path = '../extracted_output/metadata.json'
    directory_path = os.path.dirname(metadata_json_path)

    Generate_TextAndEmbeddings(directory_path, metadata_json_path)

    # Upsert data
    upsert_data(metadata_json_path, index_name)
