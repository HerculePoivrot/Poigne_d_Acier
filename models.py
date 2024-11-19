from sqlmodel import Field, SQLModel, create_engine, DateTime, Integer, String


class Coachs(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, unique=True)
    name: str
    specialite: str

class Cours(SQLModel, table=True):
    id: Integer | None = Field(default=None, primary_key=True, unique=True)
    name: String
    horaire: DateTime
    capacite_max: Integer
    coach_id: Integer = Field(default=None, foreign_key="coachs.id")

class Membre(SQLModel, table=True):
    id:int | None = Field(default=None, primary_key=True)
    nom:str
    email:str
    carte_acces_id:int
