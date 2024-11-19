# db.py
from sqlmodel import SQLModel, create_engine
from models import *

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

if __name__ == "__main__":
    print(engine)