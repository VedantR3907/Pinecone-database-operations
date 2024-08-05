import os
from dotenv import load_dotenv
from pinecone.grpc import PineconeGRPC as Pinecone

load_dotenv()

PINECONE_CLIENT = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
PINECONE_INDEX_NAME = 'groqappchatbot'
PINECONE_NAMESPACE = 'vedant'