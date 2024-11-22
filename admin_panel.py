from admin_session import ADMIN_ID, ADMIN_PASSWORD
from app_admin import page_admin
import streamlit as st


def connection_admin():
    """Fonction pour gérer la connexion administrateur."""
    if "admin_authentified" not in st.session_state:
        st.session_state.admin_authentified = False

    if st.session_state.admin_authentified is True:
        st.write("Vous êtes connecté en tant qu'administrateur.")
        return  # Évite de recréer les champs si déjà authentifié

    # Champs de connexion avec des clés dynamiques uniques
    name = st.text_input(
        label="Name",
        key=f"name_admin_connection_{st.session_state.focus_interface}")
    password = st.text_input(
        label="Password",
        type="password",
        key=f"password_admin_connection_{st.session_state.focus_interface}")

    # Bouton de connexion
    if st.button("Connection", key="connection_button"):
        if name == ADMIN_ID and password == ADMIN_PASSWORD:
            st.session_state.admin_authentified = True
            st.rerun()  # Recharge pour afficher le panneau admin
        else:
            st.error("Échec de la connexion. Vérifiez vos identifiants.")


def admin_pannel():
    """Panneau administrateur principal."""
    if "admin_authentified" not in st.session_state:
        st.session_state.admin_authentified = False

    if st.session_state.admin_authentified is False:
        connection_admin()  # Affiche le formulaire de connexion
    else:
        # Affiche le panneau admin après authentification
        st.success("Bienvenue dans le panneau administrateur.")
        if st.button(label="Deconnexion",
                     key=f"\
                     deconnexion_button_{st.session_state.focus_interface}"):
            st.session_state.admin_authentified = False
            st.rerun()  # Recharge pour retourner au formulaire de connexion
        page_admin()
            
