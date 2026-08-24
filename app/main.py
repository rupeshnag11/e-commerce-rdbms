from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")

engine = create_engine(database_url)

print("database connection is successful")

