import json
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

def generate_embeddings(metadata_path: str) -> None:
    """
    Generate embeddings for text chunks and update the metadata JSON file with these embeddings.

    Args:
        metadata_path (str): The path to the JSON file containing the metadata and where embeddings will be added.
    """
    # Initialize the embeddings
    embeddings = FastEmbedEmbeddings()
    
    # Load the metadata
    with open(metadata_path, 'r', encoding='utf-8') as file:
        metadata = json.load(file)
    
    # Prepare the texts for embedding
    texts = [entry['text'] for entry in metadata.values()]
    
    # Generate embeddings for the texts
    document_embeddings = embeddings.embed_documents(texts)
    
    # Update the metadata with embeddings
    for (chunk_id, chunk_metadata), embedding in zip(metadata.items(), document_embeddings):
        chunk_metadata['embedding'] = embedding  # Directly assign the embedding
    
    # Save the updated metadata with embeddings back to the same JSON file
    with open(metadata_path, 'w', encoding='utf-8') as file:
        json.dump(metadata, file, ensure_ascii=False, indent=4)

# Example usage
if __name__ == "__main__":
    # Define the path to the metadata JSON file
    metadata_json_path = '../extracted_output/metadata.json'
    
    # Generate embeddings and update the metadata
    generate_embeddings(metadata_json_path)
    
    print(f"Metadata with embeddings has been updated in {metadata_json_path}.")
