import os
from dotenv import load_dotenv

from datamanagement import ELT
from datamanagement.dataclient import DataClientConfig

# Load environment variables from the .env file
load_dotenv()

# Extract variables from .env
mongo_uri = os.getenv("MONGODB_URI")
database_name = os.getenv("DATABASE_NAME")
source_collection = os.getenv("SOURCE_COLLECTION")
target_collection = os.getenv("TARGET_COLLECTION")

# Create source and target DataClientConfig objects
source_db_config = DataClientConfig(
    db_type="mongodb", 
    uri=mongo_uri, 
    db_name=database_name, 
    collection=source_collection
)

target_db_config = DataClientConfig(
    db_type="mongodb", 
    uri=mongo_uri, 
    db_name=database_name, 
    collection=target_collection
)

# Example transformationss
transformations = ['vader', 'textblob', 'lda']

# Initialize the ELT process with source_db and target_db
elt_process = ELT(source_db=source_db_config, target_db=target_db_config, transformations=transformations)

# Execute the ELT process
elt_process.execute()