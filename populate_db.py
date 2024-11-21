from faker import Faker
from datetime import datetime
from sqlmodel import Session, select
from models import Coachs, Cours, CarteAcces, Membres, Inscriptions
from init_db import engine
import random as rd

fake = Faker(locale="fr_FR")
def populate_data():
    l_range = 15
    # Création Table Cartes d'Accès
    with Session(engine) as session:
        cartes = []  #Initialisation d'une liste vide
        for _ in range(l_range):
            carte = CarteAcces(numero_unique=fake.unique.numerify(text='%%%%%%%%%%'))
            session.add(carte)
            cartes.append(carte)
        session.commit()

    #création Table Membres
        membres = []
        for _ in range(l_range):
            membre = Membres(nom = fake.name(),
                             email = fake.email(),
                             carte_acces_id= carte.id)
            session.add(membre)
            membres.append(membre)
        session.commit()

    # Création Table Coachs
        coachs = []
        l_specialite = ["Yoga", "Pump", "Pilates", "Musculation", "Boxe"]
        for _ in range(l_range):
            coach = Coachs(nom = fake.name_nonbinary(),
                           specialite = rd.choice(l_specialite),
                           cours = single_cours.id
                           )
            session.add(coach)
            coachs.append(coach)
        session.commit

    # Création Table Cours
        cours = []
        #horaire_base = datetime(2024,12,1,6)
        for _ in range(l_range):
            single_cours = Cours(
                nom = coach.specialite,
                horaire= datetime(2024,12,fake.random_int(1,31),fake.random_int(6,22)),
                capacite_max= fake.random_int(10,30),
                coach_id= coach.id
            )
            session.add(single_cours)
            cours.append(single_cours)
        session.commit()

    # Création Table Inscriptions
        inscriptions = []
        for _ in range(l_range):
            inscription = Inscriptions(
                membre_id = membre.id,
                cours_id = single_cours.id,
                date_inscription= datetime(fake.random_int(2015,2024),fake.random_int(1,12),fake.random_int(1,31),fake.random_int(1,24),fake.random_int(1,60))
            )
            session.add(inscription)
            inscriptions.append(inscription)
        session.commit()




if __name__ == "__main__":
    populate_data()
    print('BDD éditée')