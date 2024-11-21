import random
import streamlit as st


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
