import re
import os
import json
from typing import Dict, Any
from datetime import datetime


def filter_filename(filename: str, id: bool) -> str:
    """
    Filter and format the filename based on the given parameters.

    Args:
        filename (str): The original filename.
        id (bool): If True, keep the '.' and '#' characters; otherwise, remove them.

    Returns:
        str: The filtered and formatted filename.
    """
    # Split the filename into name and extension
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')

    # Handle the case where there's no extension
    if ext:
        ext = '.' + ext
    
    # Remove special characters and spaces, keeping '.' and '#' if id is True
    if not id:
        name = re.sub(r'[^\w\s#.]', '', name)
    else:
        name = re.sub(r'[^\w\s.#]', '', name)

    # Remove spaces and capitalize the first letter of each word
    name = re.sub(r'\s+', '', name.title())

    # Reassemble the filename
    filtered_filename = name + ext
    
    return filtered_filename

def ReadFiles(folder_path: str) -> Dict[str, Dict[str, str]]:
    """
    Reads all text files in the specified folder and returns their contents along with metadata.

    Args:
        folder_path (str): The path to the folder containing text files.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary where keys are file names and values are dictionaries containing:
            - 'content': The file content as a string.
            - 'creation_date': The file creation date as a string in 'YYYY-MM-DD' format.
            - 'last_modified_date': The file last modified date as a string in 'YYYY-MM-DD' format.
            - 'file_path': The full path to the file.
            - 'file_size': The file size in bytes.
    """
    file_contents = {}
    for filename in os.listdir(folder_path):
        file_path_full = os.path.join(folder_path, filename)
        if os.path.isfile(file_path_full) and filename.endswith('.txt'):
            creation_date = datetime.fromtimestamp(os.path.getctime(file_path_full)).strftime('%Y-%m-%d')
            last_modified_date = datetime.fromtimestamp(os.path.getmtime(file_path_full)).strftime('%Y-%m-%d')
            file_size = os.path.getsize(file_path_full)
            
            with open(file_path_full, 'r', encoding='utf-8') as file:
                content = file.read()
                
            file_contents[filename] = {
                'content': content,
                'creation_date': creation_date,
                'last_modified_date': last_modified_date,
                'file_path': file_path_full,
                'file_size': file_size
            }
    return file_contents

def TextSplitter(file_contents: Dict[str, Dict[str, str]], chunk_size: int = 512) -> Dict[str, Dict[str, str]]:
    """
    Splits the text content of each file into smaller chunks and creates metadata for the split chunks.

    Args:
        file_contents (Dict[str, Dict[str, str]]): A dictionary where keys are file names and values are dictionaries containing:
            - 'content': The file content as a string.
            - 'creation_date': The file creation date as a string.
            - 'last_modified_date': The file last modified date as a string.
            - 'file_path': The full path to the file.
            - 'file_size': The file size in bytes.
        chunk_size (int): The size of each chunk. Default is 512.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary where keys are chunk IDs and values are dictionaries containing:
            - 'ID': The chunk ID.
            - 'text': The split text chunk.
            - 'creation_date': The file creation date.
            - 'file_name': The file name.
            - 'file_path': The file path.
            - 'file_size': The file size.
            - 'last_modified_date': The file last modified date.
    """
    metadata = {}
    
    for file_name, file_metadata in file_contents.items():
        content = file_metadata['content']
        words = content.split()
        chunks = [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)]
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{file_name}#chunk_{i}"
            metadata[chunk_id] = {
                'ID': chunk_id,
                'text': chunk,
                'creation_date': file_metadata['creation_date'],
                'file_name': os.path.basename(file_metadata['file_path']),
                'file_path': file_metadata['file_path'],
                'file_size': file_metadata['file_size'],
                'last_modified_date': file_metadata['last_modified_date']
            }
    
    return metadata

def WriteMetadataToJson(metadata: Dict[str, Dict[str, Any]], output_path: str) -> None:
    """
    Writes the metadata to a JSON file with a new structure.

    Args:
        metadata (Dict[str, Dict[str, Any]]): The metadata dictionary to be written to the JSON file.
        output_path (str): The path where the JSON file will be saved.
    """
    # Reformat the metadata to the new structure
    reformatted_data = []
    for chunk_id, chunk_metadata in metadata.items():
        reformatted_data.append({
            "id": filter_filename(chunk_id, id=True),
            "values": chunk_metadata.get('embedding', []),  # Include embeddings if available
            "metadata": {
                "text": chunk_metadata['text'],  # Include the text content in the metadata
                "creation_date": chunk_metadata['creation_date'],
                "file_name": chunk_metadata['file_name'],
                "file_path": chunk_metadata['file_path'],
                "file_size": chunk_metadata['file_size'],
                "last_modified_date": chunk_metadata['last_modified_date']
            }
        })
    
    # Write the reformatted data to the JSON file
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(reformatted_data, json_file, ensure_ascii=False, indent=4)

def process_metadata(directory_path: str) -> None:
    """
    Processes files in the specified directory to create metadata and write it to a JSON file.

    Args:
        base_path (str): The path to the directory containing files to process.
    """
    # Construct the path to the extracted_output folder in the specified base path
    extracted_output_path = directory_path

    # Ensure that the path exists and is a directory
    if os.path.isdir(extracted_output_path):
        print(f"Processing files in the directory: {extracted_output_path}")
        
        # Read all files in the extracted_output folder
        file_contents = ReadFiles(extracted_output_path)

        # Split the text and create metadata
        metadata = TextSplitter(file_contents)

        # Define the path for the JSON output file
        json_output_path = os.path.join(extracted_output_path, 'metadata.json')

        # Write the metadata to the JSON file
        WriteMetadataToJson(metadata, json_output_path)

        print(f"Metadata has been written to {json_output_path}.")
    else:
        print(f"The path {extracted_output_path} is not a valid directory.")
    
if __name__ == "__main__":
    process_metadata('../extracted_output')