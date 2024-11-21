# db.py
from sqlmodel import SQLModel, create_engine
from models import Coachs, Cours, CarteAcces, Membres, Inscriptions

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def init_db():
    #Création des tables
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    print(engine)
    init_db()