import sys
sys.path.append('../')
from text_and_embeddings.textsplitter import process_metadata
from text_and_embeddings.embeddings import generate_embeddings

def Generate_TextAndEmbeddings(directory_path: str, json_path: str):
    process_metadata(directory_path)

    #Embeddings

    # Define the path to the metadata JSON file
    metadata_json_path = json_path

    # Generate embeddings and update the metadata
    generate_embeddings(metadata_json_path)

    print(f"Metadata with embeddings has been updated in {metadata_json_path}.")