import json
import sys
sys.path.append('../')
from constants import PINECONE_NAMESPACE, PINECONE_CLIENT, PINECONE_INDEX_NAME

index_name = PINECONE_INDEX_NAME
pc = PINECONE_CLIENT,
pc = pc[0]
name_space = PINECONE_NAMESPACE


def upsert_data(json_path: str, index_name: str) -> None:
    """
    Upserts data into a Pinecone index.

    Args:
        json_path (str): The path to the JSON file containing the embeddings.
        index_name (str): The name of the Pinecone index.
    """
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
    
    # Upsert vectors into Pinecone
    index.upsert(vectors=vectors)
    print(f"Data has been upserted into the Pinecone index '{index_name}'.")

# Example usage
if __name__ == "__main__":
    # Define paths and credentials
    metadata_json_path = '../extracted_output/metadata.json'

    # Upsert data
    upsert_data(metadata_json_path, index_name)
