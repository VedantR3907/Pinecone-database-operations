
from pinecone import ServerlessSpec
from constants import PINECONE_CLIENT, PINECONE_INDEX_NAME

pc = PINECONE_CLIENT
index_name = PINECONE_INDEX_NAME

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