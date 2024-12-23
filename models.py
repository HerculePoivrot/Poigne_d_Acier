from sqlmodel import Field, SQLModel, create_engine, DateTime, Integer, String, Relationship
from datetime import datetime
from typing import List, Optional

# Définition des modèles
# Table 1 : Coachs


class Coachs(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    specialite: str
    # Relation vers Cours
    cours: List["Cours"] = Relationship(back_populates="coach")


class Cours(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    horaire: datetime
    capacite_max: int
    coach_id: Optional[int] = Field(default=None, foreign_key="coachs.id")
    # Relation inverse vers Coachs
    coach: "Coachs" = Relationship(back_populates="cours")
    # Ajouter la relation vers Inscriptions
    inscriptions: List["Inscriptions"] = Relationship(back_populates="cours")



# Table 3 : Cartes d'accès
class CarteAcces(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    id:int | None = Field(default=None, primary_key=True)
    numero_unique: str

    membres: list["Membres"] = Relationship(back_populates="carteacces")


#Table 4 : Membres
class Membres(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    id:int | None = Field(default=None, primary_key=True)
    nom:str
    email:str = Field(index = True, unique = True)
    carte_acces_id:str = Field(default=None, foreign_key="carteacces.id")

    carteacces: CarteAcces | None = Relationship(back_populates="membres")
    inscriptions: list["Inscriptions"] = Relationship(back_populates="membres")


# Table 5 : Inscriptions (many to many | membre / cours)
class Inscriptions(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    # On enlève la colonne 'id' comme clé primaire
    # Et on définit une clé primaire composée (membre_id, cours_id)
    membre_id: int = Field(foreign_key="membres.id", primary_key=True)
    cours_id: int = Field(foreign_key="cours.id", primary_key=True)
    date_inscription: datetime

    membres: Membres = Relationship(back_populates="inscriptions")
    cours: Cours = Relationship(back_populates="inscriptions")
