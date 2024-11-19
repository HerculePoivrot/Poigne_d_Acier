from sqlmodel import Field, SQLModel, create_engine

class Membre(SQLModel, table=True):
    id:int | None = Field(default=None, primary_key=True)
    nom:str
    email:str
    carte_acces_id:int


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)