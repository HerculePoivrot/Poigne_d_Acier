import random
import streamlit as st
from models import Membres, CarteAcces, Cours, Inscriptions
from datetime import datetime
from utils import add_instance, select_table, get_last_instance
from sqlmodel import select, Session
from init_db import engine


class PathernMembre:
    def __init__(self, name: str, mail: str):
        self._name = name
        self._mail = mail

    # Getter pour name
    @property
    def name(self):
        return self._name

    # Setter pour name
    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    # Getter pour mail
    @property
    def mail(self):
        return self._mail

    # Setter pour mail
    @mail.setter
    def mail(self, new_mail: str):
        self._mail = new_mail

    def generate_card_id(self):
        """
        Génère un ID unique basé sur le nom et l'adresse mail.
        Utilise les codes ASCII des caractères de manière aléatoire.
        """
        unique_id = "".join(
            str(ord(random.choice(self._name + self._mail)))
            for _ in range(len(self._name) * len(self._mail))
        )
        return int(unique_id)

    def __str__(self):
        return f"Membre: {self._name} ({self._mail})"


class PathernCarteAcces:
    def __init__(self, unique_id: int):
        self._unique_id = unique_id

    @property
    def unique_id(self):
        return self._unique_id

    def __str__(self):
        return f"Carte ID: {self._unique_id}"


def input_users():
    """
    Formulaire pour saisir le nom et le mail d'un utilisateur.
    """
    with st.form("add_user_form", clear_on_submit=True):
        name = st.text_input(label="Nom",
                             placeholder="Jean Dupont",
                             key="name_user")
        mail = st.text_input(label="Email",
                             placeholder="jean.dupont@gmail.com")
        submit = st.form_submit_button("Valider")

        if submit:
            if name and mail:
                membre = PathernMembre(name, mail)
                st.session_state.membre_inscription = membre
                st.success(f"Inscription réussie : {membre}")
            else:
                st.error("Veuillez remplir tous les champs.")


def create_user():
    """
    Page d'inscription : Saisie du nom et de l'email
    et génération d'une carte membre.
    """
    with st.form("form_register", clear_on_submit=True):
        name = st.text_input(label="Nom",
                             placeholder="Jean Dupont")
        mail = st.text_input(label="Email",
                             placeholder="jean.dupont@gmail.com")
        submit = st.form_submit_button("S'inscrire")

        if submit:
            if name and mail:
                membre = PathernMembre(name, mail)
                st.session_state.membre_inscription = membre
                unique_id = membre.generate_card_id()
                st.session_state.carte_membre = PathernCarteAcces(unique_id)

                st.success(
                    f"Inscription réussie ! Voici votre numéro de carte : \
                        {unique_id}"
                    )
                st.write("Step Add User and Carte Access")
                carte_access_sql = CarteAcces(numero_unique=str(unique_id))
                add_instance(carte_access_sql)
                last_carte_access = get_last_instance(CarteAcces)
                st.write(last_carte_access)
                membre_sql = Membres(nom=membre.name,
                                     email=membre.mail,
                                     carte_acces_id=last_carte_access.id)
                add_instance(membre_sql)
                for membresq in select_table(Membres):
                    st.dataframe(membresq)
                st.title("Phase Search")
                st.dataframe(search_card_id(str(unique_id)))
                st.write(search_card_id(str(unique_id)).id)
                st.dataframe(search_users_card(str(unique_id)))
            else:
                st.error("Veuillez remplir tous les champs.")


def connect_user():
    """
    Page de connexion : Saisie de l'ID de carte membre pour se connecter.
    """
    input_card = st.text_input(label="Numéro de carte membre",
                               placeholder="Entrez votre ID unique")
    if "state_connection" not in st.session_state:
        st.session_state.state_connection = False
    session = st.session_state
    if "carte_membre" not in st.session_state:
        st.error("il n'y a pas de membre veuilliez vous inscrires")

    if st.button("Se connecter"):
        st.write(f"Vous avez cliquez {input_card=}")
        st.write(f"état actuel de la connection: {session.state_connection=}")
        if int(input_card) == session.carte_membre.unique_id:
            st.session_state.state_connection = True
            st.rerun()
        st.write(
            f"état  après tentative d'authentification: \
                {session.state_connection=}")


def disconnect_user():
    """
    Permet à l'utilisateur de se déconnecter.
    """
    if st.button("Déconnexion"):
        st.session_state.state_connection = False
        st.success("Déconnexion réussie.")
        st.rerun()


def panel_update_user():
    session = st.session_state
    if "carte_membre" in session and "membre_inscription" in session:
        if session.state_connection is True:
            st.write(
                f"Connecté en tant que : {session.membre_inscription.name}")
            name = st.text_input(label="Name",
                                 value=f"{session.membre_inscription.name}",
                                 key=f"panel_update_user_name\
                                 {session.membre_inscription.name}_\
                                 {session.carte_membre.unique_id}")
            mail = st.text_input(label="Mail",
                                 value=f"{session.membre_inscription.mail}",
                                 key=f"panel_update_user_mail\
                                 {session.membre_inscription.name}_\
                                 {session.carte_membre.unique_id}")
            if st.button("update_user"):
                if name not in [None, ""] and mail not in [None, ""]:
                    st.session_state.membre_inscription.name = name
                    st.session_state.membre_inscription.mail = mail
    else:
        st.error("pas possible de modifier car pas instancier")


def panel_user():
    if "state_connection" not in st.session_state:
        st.session_state.state_connection = False
    session = st.session_state
    if "carte_membre" in session and "membre_inscription" in session:
        if session.state_connection is True:
            st.write(
                f"Connecté en tant que : {session.membre_inscription.name}")
        else:
            connect_user()


def start_member():
    """
    Gestion principale des utilisateurs : inscription, connexion,
    ou déconnexion.
    """
    session = st.session_state

    if "state_connection" not in session:
        session.state_connection = False

    st.title("Espace Membre")

    if "carte_membre" in session and "membre_inscription" in session:
        if session.state_connection:
            st.write(
                f"Connecté en tant que : {session.membre_inscription.name}")
            disconnect_user()
        else:
            connect_user()
    else:
        create_user()


def search_card_id(card_unique_id) -> int:
    with Session(engine) as session:
        statement = select(CarteAcces).where(
            CarteAcces.numero_unique == card_unique_id)
        results = session.exec(statement)
        return results.first()


def search_users_card(card_unique_id):
    card_object_id = search_card_id(card_unique_id).id
    with Session(engine) as session:
        statement = select(Membres).where(
            Membres.carte_acces_id == str(card_object_id))
        results = session.exec(statement)
        return results.first()  # Récupérer tous les résultats de manière sûre


def afficher_cours_disponibles():
    """
    Affiche les cours disponibles avec leur capacité et nombre d'inscriptions.
    """
    with Session(engine) as session:
        statement = select(Cours)
        cours_disponibles = session.exec(statement).all()

        if cours_disponibles:
            st.title("Cours Disponibles")
            for cours in cours_disponibles:
                # Calculer les inscriptions actuelles
                inscriptions_count = len(session.exec(
                    select(Inscriptions).where(
                        Inscriptions.cours_id == cours.id)
                ).all())  # Utilisez all() et len() pour compter les inscriptions

                st.write(f"""
                **Cours** : {cours.nom}
                - Horaire : {cours.horaire.strftime('%Y-%m-%d %H:%M')}
                - Capacité : {inscriptions_count}/{cours.capacite_max}
                """)
        else:
            st.write("Aucun cours disponible.")


def inscrire_a_un_cours(member_focus: Membres = None):
    """
    Permet à l'utilisateur connecté de s'inscrire à un cours avec vérification
    des places disponibles et des conflits horaires.
    """
    session = st.session_state
    if member_focus is None:
        if "membre_inscription" not in session or not session.state_connection:
            st.error("Vous devez être connecté pour vous inscrire à un cours.")
            return
    else:
        session.membre_inscription = PathernMembre(name=member_focus.nom,
                                                   mail=member_focus.email)

    membre = session.membre_inscription

    with Session(engine) as db_session:
        # Afficher les cours disponibles
        statement = select(Cours)
        cours_disponibles = db_session.exec(statement).all()

        if not cours_disponibles:
            st.error("Aucun cours disponible.")
            return

        # Sélectionner un cours
        cours_options = {
            f"{cours.nom} - {cours.horaire.strftime('%Y-%m-%d %H:%M')}":
                cours.id for cours in cours_disponibles}
        choix_cours = st.selectbox("Choisissez un cours",
                                   options=list(cours_options.keys()))

        if st.button("S'inscrire"):
            # Obtenir l'ID du cours sélectionné
            cours_id = cours_options[choix_cours]
            cours_selectionne = db_session.get(Cours, cours_id)

            # Vérifier si le cours est complet
            inscriptions_count = len(db_session.exec(
                select(Inscriptions).where(Inscriptions.cours_id == cours_id)
            ).all())  # Compter le nombre d'inscriptions

            if inscriptions_count >= cours_selectionne.capacite_max:
                st.error("Ce cours est complet. Impossible de s'inscrire.")
                return

            # Récupérer l'objet 'Membres' à partir de l'email du membre
            membre_sql = db_session.exec(
                select(Membres).where(Membres.email == membre.mail)
            ).first()

            if membre_sql:
                # Vérifier les inscriptions existantes du membre
                inscriptions_existantes = db_session.exec(
                    select(Inscriptions, Cours).join(Cours).where(
                        Inscriptions.membre_id == membre_sql.id
                    )
                ).all()

                # Vérifier les conflits horaires
                for inscription, cours_inscrit in inscriptions_existantes:
                    if cours_inscrit.horaire == cours_selectionne.horaire:
                        st.error(
                            f"Conflit horaire détecté avec le cours : "
                            f"{cours_inscrit.nom} à {
                                cours_inscrit.horaire.strftime(
                                    '%Y-%m-%d %H:%M')}."
                        )
                        return

                # Vérifier si le membre est déjà inscrit
                inscription_existante = db_session.exec(
                    select(Inscriptions).where(
                        (Inscriptions.membre_id == membre_sql.id) & (
                            Inscriptions.cours_id == cours_id)
                    )
                ).first()

                if inscription_existante:
                    st.error("Vous êtes déjà inscrit à ce cours.")
                    return

                # Créer l'inscription
                nouvelle_inscription = Inscriptions(
                    membre_id=membre_sql.id,
                    cours_id=cours_id,
                    date_inscription=datetime.now()
                )
                db_session.add(nouvelle_inscription)
                db_session.commit()
                st.success(f"Inscription réussie au cours : {cours_selectionne.nom}")
                if member_focus is not None:
                    st.rerun()


def desinscrire_d_un_cours(member_focus: Membres = None):
    """
    Permet à un utilisateur connecté de se désinscrire d'un cours
    auquel il est inscrit.
    """
    session = st.session_state
    if member_focus is None:
        if "membre_inscription" not in session or not session.state_connection:
            st.error("Vous devez être connecté pour vous désinscrire d'un cours.")
            return
    else:
        session.membre_inscription = PathernMembre(name=member_focus.nom,
                                                   mail=member_focus.email)        

    membre = session.membre_inscription

    with Session(engine) as db_session:
        # Récupérer l'objet 'Membres' à partir de l'email du membre
        membre_sql = db_session.exec(
            select(Membres).where(Membres.email == membre.mail)
        ).first()

        if not membre_sql:
            st.error("Utilisateur non trouvé dans la base de données.")
            return

        # Récupérer les inscriptions actuelles du membre
        inscriptions_existantes = db_session.exec(
            select(Inscriptions, Cours).join(Cours).where(
                Inscriptions.membre_id == membre_sql.id
            )
        ).all()

        if not inscriptions_existantes:
            st.info("Vous n'êtes inscrit à aucun cours.")
            return

        # Afficher les cours auxquels l'utilisateur est inscrit
        cours_options = {
            f"{cours.nom} - {cours.horaire.strftime('%Y-%m-%d %H:%M')}":
                (inscription.membre_id, inscription.cours_id)
            for inscription, cours in inscriptions_existantes
        }
        choix_inscription = st.selectbox("Sélectionnez un cours à quitter",
                                         options=list(cours_options.keys()))

        if st.button("Se désinscrire"):
            # Obtenir les clés primaires de l'inscription sélectionnée
            membre_id, cours_id = cours_options[choix_inscription]

            # Rechercher l'inscription à supprimer
            inscription_a_supprimer = db_session.exec(
                select(Inscriptions).where(
                    (Inscriptions.membre_id == membre_id) &
                    (Inscriptions.cours_id == cours_id)
                )
            ).first()
            if inscription_a_supprimer:
                db_session.delete(inscription_a_supprimer)
                db_session.commit()
                st.success("Vous avez été désinscrit du cours avec succès.")
                st.rerun()
            else:
                st.error("Erreur lors de la désinscription.")


def start_member_with_cours():
    """
    Ajoute la gestion des cours dans le tableau de bord utilisateur.
    """
    session = st.session_state

    if "state_connection" not in session:
        session.state_connection = False

    st.title("Espace Membre et Cours")

    if "carte_membre" in session and "membre_inscription" in session:
        if session.state_connection:
            st.write(
                f"Connecté en tant que : {session.membre_inscription.name}")
            st.divider()
            afficher_cours_disponibles()
            inscrire_a_un_cours()
            st.divider()
            desinscrire_d_un_cours()  # Intégrer la désinscription ici
        else:
            connect_user()
    else:
        create_user()


"""
 TODO : Consulter l'historique des  inscriptions
"""
