import streamlit as st
from faker import Faker
from datetime import datetime
from init_db import engine
from sqlmodel import Session, select
from models import Coachs, Cours, CarteAcces, Membres, Inscriptions
from utils import del_instance, add_instance

fake = Faker(locale="fr_FR")
# Titre de la page
st.markdown("# Poigne d'Acier - Page Administration")


with Session(engine) as session:
    
    carte = CarteAcces(numero_unique=fake.unique.numerify(text='COINCOIN%%%%%%%%%%'))
    session.add(carte)
    session.commit()

if st.button("Gérer les coachs", type="primary") is True:
    st.success('Format correct, question ajoutée', icon="✅")


if st.button("Gérer les cours", type="primary") is True:
    st.success('Format correct, question ajoutée', icon="✅")

if st.button("Voir les membres inscrits à un cours", type="primary") is True:
    st.success('Format correct, question ajoutée', icon="✅")

if st.button("Annuler un cours", type="primary") is True:
    st.success('Format correct, question ajoutée', icon="✅")

if __name__ == "__main__":
    print("coucou")