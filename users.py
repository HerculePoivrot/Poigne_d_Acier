import random
import streamlit as st


class MembresInscription:
    def __init__(self, name: str, mail: str):
        self._name = name
        self._mail = mail

    @property
    def name(self):
        return self._name

    @property
    def mail(self):
        return self._mail

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


class CarteMembre:
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
        name = st.text_input(label="Nom", placeholder="Jean Dupont", key="name_user")
        mail = st.text_input(label="Email", placeholder="jean.dupont@gmail.com")
        submit = st.form_submit_button("Valider")

        if submit:
            if name and mail:
                membre = MembresInscription(name, mail)
                st.session_state.membre_inscription = membre
                st.success(f"Inscription réussie : {membre}")
            else:
                st.error("Veuillez remplir tous les champs.")


import random
import streamlit as st


class MembresInscription:
    def __init__(self, name: str, mail: str):
        self._name = name
        self._mail = mail

    @property
    def name(self):
        return self._name

    @property
    def mail(self):
        return self._mail

    def generate_card_id(self):
        """
        Génère un ID unique basé sur le nom et l'adresse email.
        """
        unique_id = "".join(
            str(ord(random.choice(self._name + self._mail)))
            for _ in range(len(self._name) * len(self._mail))
        )
        return int(unique_id)

    def __str__(self):
        return f"Membre: {self._name} ({self._mail})"


class CarteMembre:
    def __init__(self, unique_id: int):
        self._unique_id = unique_id

    @property
    def unique_id(self):
        return self._unique_id

    def __str__(self):
        return f"Carte ID: {self._unique_id}"


def create_user():
    """
    Page d'inscription : Saisie du nom et de l'email, et génération d'une carte membre.
    """
    with st.form("form_register", clear_on_submit=True):
        name = st.text_input(label="Nom", placeholder="Jean Dupont")
        mail = st.text_input(label="Email", placeholder="jean.dupont@gmail.com")
        submit = st.form_submit_button("S'inscrire")

        if submit:
            if name and mail:
                membre = MembresInscription(name, mail)
                st.session_state.membre_inscription = membre
                unique_id = membre.generate_card_id()
                st.session_state.carte_membre = CarteMembre(unique_id)

                st.success(f"Inscription réussie ! Voici votre numéro de carte : {unique_id}")
            else:
                st.error("Veuillez remplir tous les champs.")


def connect_user():
    """
    Page de connexion : Saisie de l'ID de carte membre pour se connecter.
    """
    input_card = st.text_input(label="Numéro de carte membre", placeholder="Entrez votre ID unique")
    session = st.session_state

    if st.button("Se connecter"):
        if "carte_membre" in session and session.carte_membre:
            try:
                if int(input_card) == session.carte_membre.unique_id:
                    st.success(f"Bienvenue, {session.membre_inscription.name} !")
                    session.state_connection = True
                    st.rerun()
                else:
                    st.error("ID incorrect. Veuillez réessayer.")
            except ValueError:
                st.error("Veuillez entrer un numéro valide.")
        else:
            st.error("Aucune carte membre trouvée. Inscrivez-vous d'abord.")


def disconnect_user():
    """
    Permet à l'utilisateur de se déconnecter.
    """
    if st.button("Déconnexion"):
        st.session_state.state_connection is False
        st.success("Déconnexion réussie.")
        st.rerun()


def start_member():
    """
    Gestion principale des utilisateurs : inscription, connexion, ou déconnexion.
    """
    session = st.session_state

    if "state_connection" not in session:
        session.state_connection = False

    st.title("Espace Membre")

    if "carte_membre" in session and "membre_inscription" in session:
        if session.state_connection:
            st.write(f"Connecté en tant que : {session.membre_inscription.name}")
            disconnect_user()
        else:
            connect_user()
    else:
        create_user()
