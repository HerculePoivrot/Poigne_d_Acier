# db.py
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship
from faker import Faker
from datetime import datetime
# from models import *

fake = Faker(locale="fr_FR")

#Définition des modèles
class Coachs(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, unique=True)
    nom: str
    specialite: str

    cours : list["Cours"] = Relationship(back_populates="coachs")

class Cours(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, unique=True)
    nom: str
    horaire: datetime
    capacite_max: int
    coach_id: int = Field(default=None, foreign_key="coachs.id")

    coachs : Coachs | None = Relationship(back_populates="cours")
    inscriptions: list["Inscriptions"] = Relationship(back_populates="cours")


class CarteAcces(SQLModel, table=True):
    id:int | None = Field(default=None, primary_key=True)
    numero_unique:str

    membres: list["Membres"] = Relationship(back_populates= "carteaccess")

class Membres(SQLModel, table=True):
    id:int | None = Field(default=None, primary_key=True)
    nom:str
    email:str = Field(index = True, unique = True)
    carte_acces_id:str = Field(default=None, foreign_key="carteacces.id")

    carteacces: CarteAcces | None = Relationship(back_populates="membres")
    inscriptions: list["Inscriptions"] = Relationship(back_populates="membres")

class Inscriptions(SQLModel, table=True):
    id:int | None = Field(default=None, primary_key=True)
    membre_id:int = Field(default=None, foreign_key="membres.id", primary_key=True)
    cours_id:int = Field(default=None, foreign_key="cours.id", primary_key=True)
    date_inscription:datetime

    membres : Membres | None = Relationship(back_populates="inscriptions") 
    cours   : Cours   | None = Relationship(back_populates="inscriptions")





sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

#connexion à la BDD
engine = create_engine(sqlite_url, echo=True)

# création des tables
def create_db_and_tables():
    echo = SQLModel.metadata.create_all(engine)
    print(echo)

#Insertion des données
def create_membres():
    carteacces1 = CarteAcces(numero_unique = fake.unique.numerify(text='%%%%%%%%%%'))
    membre1 = Membres(nom = "John Rambo", email = "detruire@world.com",carte_acces_id = carteacces1)
    membre2 = Membres(nom = "Sarah Connor", email = fake.ascii_email(),carte_acces_id = fake.unique.numerify(text='Carte_Acces_id : %%%%%%%%%%'))
   
    coach1 = Coachs(nom = fake.name(),specialite = "Yoga")
    coach2 = Coachs(nom = fake.name(),specialite = "Pilates")

    cours1 = Cours(nom = 'Boxe 101', horaire = datetime(year=2021, month=10, day=22, hour=10, minute=0), capacite_max= 15, coach_id =1)
    
    



    with Session(engine) as session:
        session.add(carteacces1)
        #création d'un membre
        session.add(membre1)
        session.add(membre2)
        #création d'un coach
        session.add(coach1)
        session.add(coach2)
        #création d'un cours
        session.add(cours1)


        session.commit()
        session.refresh(carteacces1)
        session.refresh(membre1)
        session.refresh(membre2)
        session.refresh(coach1)
        session.refresh(coach2)
        session.refresh(cours1)

def select_membres():
    with Session(engine) as session:
        statement = select(Membres).where(Membres.nom != "John Rambo")
        results = session.exec(statement)
        for membre in results:
            print(membre)        

# where(Membres.nom == "John Rambo")


def main():
    create_db_and_tables()
    create_membres()
    select_membres()







if __name__ == "__main__":
    main()