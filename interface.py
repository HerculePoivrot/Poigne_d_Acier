import streamlit as st

from users import create_user, panel_user, panel_update_user, disconnect_user
from admin_panel import admin_pannel


# --- Gestion des transitions entre interfaces ---
def switch_interface(interface: str):
    st.session_state.focus_interface = interface
    st.rerun()


# --- Interface Administrateur ---
def interface_admin():
    if st.button("Retour à l'Accueil"):
        switch_interface("default")
    admin_pannel()


# --- Interface Inscription ---
def interface_register():
    create_user()
    if st.button("Déjà inscrit ? Connectez-vous"):
        switch_interface("connect_member")
    if st.button("Retour à l'Accueil"):
        switch_interface("default")


# --- Interface Espace Membre ---
def interface_member():
    if st.button("Inscription"):
        switch_interface("register_member")
    if st.button("Connexion"):
        switch_interface("connect_member")
    if st.button("Retour à l'Accueil"):
        switch_interface("default")


# --- Interface Connexion ---
def interface_connection():
    panel_user()
    if "state_connection" in st.session_state:
        if st.session_state.state_connection is True:
            if st.button("Edit User"):
                switch_interface("panel_update_user")
            disconnect_user()
    if st.button("Pas encore inscrit ? Inscrivez-vous"):
        switch_interface("register_member")
    if st.button("Retour à l'Accueil"):
        switch_interface("default")


def interface_update_user():
    if st.session_state.state_connection is False:
        switch_interface("connect_member")
    if st.button("Retour à l'Accueil"):
        switch_interface("default")
    if st.button("Retour aux profils"):
        switch_interface("connect_member")
    panel_update_user()


# --- Interface Accueil ---
def interface_acceuil():
    st.title("Bienvenue à la Poigne d'acier")
    if st.button("Espace Membre"):
        switch_interface("member")
    if st.button("Espace Administrateur"):
        switch_interface("admin")


# --- Gestion de l'interface principale ---
def interface():
    if "focus_interface" not in st.session_state:
        st.session_state.focus_interface = "default"

    focus = st.session_state.focus_interface
    interface_choice = {
                        "default":interface_acceuil,
                        "member":interface_member,
                        "register_member":interface_register,
                        "connect_member":interface_connection,
                        "panel_update_user":interface_update_user,
                        "admin":interface_admin
                        }
    if focus  in interface_choice:
        interface_choice[focus]()


if __name__ == "__main__":
    interface()
