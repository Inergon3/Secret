import os

from dotenv import load_dotenv

load_dotenv()
postgres_host = os.getenv("postgres_host")
postgres_db = os.getenv("postgres_db")
postgres_user = os.getenv("postgres_user")
postgres_password = os.getenv("postgres_password")
