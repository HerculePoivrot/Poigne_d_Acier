import streamlit as st
from faker import Faker
from datetime import datetime
from init_db import engine
from sqlmodel import Session, select
from models import Coachs, Cours, CarteAcces, Membres, Inscriptions
from utils import del_instance, add_instance, select_table
import random as rd
import pandas as pd


#fake.name_nonbinary()
def ajouter_coach(nom, specialite):
    with Session(engine) as session:
        coach = Coachs(nom=nom, specialite=specialite)
        session.add(coach)
        session.commit()

# Fonction pour afficher les coachs
def afficher_coachs():
    with Session(engine) as session:
        coachs = session.exec(select(Coachs)).all()
    st.write("### Nos Coachs : ")
    for coach in coachs:
        if coach.specialite == "Yoga":
            st.write(f"{coach.nom} - Spécialité: {coach.specialite} ☮️")
        elif coach.specialite == "Biking":
            st.write(f"{coach.nom} - Spécialité: {coach.specialite} 🚴‍♂️")
        elif coach.specialite == "Karate":
            st.write(f"{coach.nom} - Spécialité: {coach.specialite} 🥷")
        elif coach.specialite == "Musculation":
            st.write(f"{coach.nom} - Spécialité: {coach.specialite} 🏋️‍♂️")
        else:
            st.write(f"{coach.nom} - Spécialité: {coach.specialite} 🥊")


# Fonction pour afficher les cours dispo
def afficher_cours_disponibles():
    with Session(engine) as session:
        cours_disponibles = session.exec(select(Cours)).all()
        for cours in cours_disponibles:
            st.write(f"{cours.nom} - {cours.horaire} - Places disponibles : {cours.capacite_max}")


def afficher_message(type_message, contenu):
    """Affiche un message de succès ou d'erreur."""
    if type_message == "success":
        st.success(contenu)
    elif type_message == "error":
        st.error(contenu)
    else:
        st.info(contenu)

def page_admin():
    fake = Faker(locale="fr_FR")

    l_specialite = ["Yoga", "Biking", "Karate", "Musculation", "Boxe"]

    # Titre de la page
    st.title("La Poigne d'Acier 💪")
    st.markdown("# Section Administration")


    # Sidebar pour naviguer entre les différentes sections
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Choisissez une section", ("Gestion des Coachs", "Gestion des Cours", "Gestion des Inscriptions"))
    if page == "Gestion des Coachs":
        afficher_coachs()
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('Ajouter'):
                add_instance(Coachs(nom = fake.name_nonbinary(),
                            specialite = rd.choice(l_specialite)
                            ))
                st.rerun()
        with col2:
            button2 = st.button('Modifier')
        with col3:
            if st.button('Supprimer'):
                with st.expander("🗑️ Supprimer un coach"):
                    with Session(engine) as session:
                        coachs = session.exec(select(Coachs)).all()
                        if coachs:
                            nom_coach = st.text_input("Entrez le nom du coach à supprimer")
                            if st.button("Supprimer le coach"):
                                coach_a_supprimer = next((coach for coach in coachs if coach.nom.lower() == nom_coach.lower()), None)
                                if coach_a_supprimer:
                                    session.delete(coach_a_supprimer)
                                    session.commit()
                                    afficher_message("success", f"Le coach {nom_coach} a été supprimé avec succès.")
                                    st.experimental_rerun()  # Recharge la page
                                else:
                                    afficher_message("error", f"Aucun coach trouvé avec le nom {nom_coach}.")
                        else:
                            st.warning("Aucun coach à supprimer.")


    elif page == "Gestion des cours":
        st.text('tada')
    elif page == "Gestion des inscriptions":
        st.header("Gestion des inscriptions 📝")

        with Session(engine) as session:
            inscriptions = session.exec(select(Inscriptions)).all()
            if inscriptions:
                st.table(
                    [
                        {
                            "Membre": inscription.membre_id,
                            "Cours": inscription.cours_id,
                            "Date": inscription.date_inscription
                        }
                        for inscription in inscriptions
                    ]
                )
            else:
                st.warning("Aucune inscription enregistrée.")



    st.markdown("""
        --- 
        💪 **La Poigne d'Acier** - Votre salle de sport !
        Contactez-nous à : contact@lapoigne.fr
    """)

if __name__ == "__main__":
    print("coucou")
    page_admin()