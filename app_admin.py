import streamlit as st
from faker import Faker
from datetime import datetime, time
from init_db import engine
from sqlmodel import Session, select
from models import Coachs, Cours, CarteAcces, Membres, Inscriptions
from utils import del_instance, add_instance, select_table
from users import inscrire_a_un_cours, desinscrire_d_un_cours
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

def gestion_coachs(fake, l_specialite):
    afficher_coachs()
    left, middle, right = st.columns(3)
    
    if left.button('➕ Ajouter'):
        add_instance(Coachs(nom = fake.name_nonbinary(),
                        specialite = rd.choice(l_specialite)
                        ))
        left.markdown("Veuillez ajouter un coach")
        st.rerun()

    if middle.button('✏️ Modifier'):
        left.markdown("Vous pouvez modifier les informations d'un coach")
        st.rerun()
        
    if "show_delete" not in st.session_state:
        st.session_state.show_delete = False

    with right:
        # Bouton pour afficher l'interface de suppression
        if st.button('➖ Supprimer'):
            st.session_state.show_delete = True

        # Afficher le formulaire de suppression si l'état est activé
        if st.session_state.show_delete:
            with st.expander("🗑️ Supprimer un coach"):
                with Session(engine) as session:
                    coachs = session.exec(select(Coachs)).all()
                    if coachs:
                        nom_coach = st.selectbox(
                            "Entrez le nom du coach à supprimer",
                            [coach.nom for coach in coachs]
                            )
                        coach_to_del = session.exec(select(Coachs).where(Coachs.nom == nom_coach)).first()
                    if st.button("Confirmer la suppression?"):
                        session.delete(coach_to_del)
                        session.commit()
                        st.success(f"Le coach {nom_coach} a été supprimé")
                        
                        st.session_state.show_delete = False # Réinitialisation de l'état
                        st.rerun()

def ajouter_des_cours():
    nom_cours = st.text_input(label="Nom du Cours:", key="name_cours_gestion_cours")
    capacite_max_cours = st.number_input(label="Capacité Max", key="capacite_max_cours_gestion_cours")
    # Saisie de la date
    selected_date = st.date_input("Choisissez une date", value=datetime.today())
    # Saisie de l'heure
    selected_time = st.time_input("Choisissez une heure", value=time(12, 0))

    # Combiner la date et l'heure
    date_cours = datetime.combine(selected_date, selected_time)

    st.write("Date et heure sélectionnées :", date_cours)

    new_cours = Cours(nom=nom_cours, horaire=date_cours)
    add_instance()
def gestion_des_cours():
    afficher_cours_disponibles()
def lister_membres():
    """
    Retourne une liste d'objets Membres depuis la base de données.
    """
    with Session(engine) as session:
        membres = session.exec(select(Membres)).all()  # Liste d'objets Membres
        return membres
def gestion_membre_inscription():
    # Récupère la liste des membres
    liste_membres = lister_membres()  # Appel à la fonction
    
    # Crée une liste de noms des membres (avec ID pour plus de clarté)
    options = [f"{membre.id} - {membre.nom}" for membre in liste_membres]

    # Utilise un selectbox pour choisir un membre
    selected_option = st.selectbox(label="Sélectionnez un Membre", options=options)

    # Extraire l'ID du membre sélectionné
    selected_id = int(selected_option.split(" - ")[0])  # Récupère l'ID en convertissant la partie avant " - "
    
    # Récupère l'objet membre correspondant
    membre_selectionne = next((membre for membre in liste_membres if membre.id == selected_id), None)
    
    if membre_selectionne:
        st.write(f"Vous avez sélectionné : {membre_selectionne.nom} (Email : {membre_selectionne.email})")
        
        # Appeler les fonctions pour inscrire/désinscrire
        inscrire_a_un_cours(membre_selectionne)
        desinscrire_d_un_cours(membre_selectionne)
    else:
        st.error("Erreur : membre introuvable.")

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
        gestion_coachs(fake, l_specialite)
    elif page == "Gestion des Cours":
        st.title("Gestion des Cours")
        gestion_des_cours()
    elif page == "Gestion des Inscriptions":
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
        gestion_membre_inscription()



    st.markdown("""
        --- 
        💪 **La Poigne d'Acier** - Votre salle de sport !
        Contactez-nous à : contact@lapoigne.fr
    """)

if __name__ == "__main__":
    print("coucou")
    page_admin()