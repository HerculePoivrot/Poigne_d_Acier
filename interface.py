import streamlit as st

from users import start_member
from admin_panel import connection_admin, admin_pannel
def switch_interface(interface:str):
    st.session_state.focus_interface = interface
    st.rerun()
def switch_member():
    switch_interface("member")
def switch_admin():
    switch_interface("admin")
def switch_acceuil():
    switch_interface("default")
def switch_connection():
    switch_interface("connect_member")
def switch_register():
    switch_interface("register_member")

def interface_admin():
    if st.button("Acceuil"):
        switch_acceuil()
    connection_admin()
    admin_pannel()
    
def interface_register():
    start_member()
    if st.button("Souhaitez vous plutôt vous connecter ?"):
        switch_connection()
    if st.button("Acceuil"):
        switch_acceuil()
def interface_member():
    if st.button("Je m'inscrit"):
        switch_register()
    elif st.button("connection"):
        switch_connection()
    elif st.button("Acceuil"):
        switch_acceuil()
def interface_connection():
    start_member()
    if st.button("Pas encore inscrit ? Inscrivez vous!"):
        switch_register()
    if st.button("Acceuil"):
        switch_acceuil()
def interface_acceuil():
    if st.button("Espace Membre"):
        switch_member()
    elif st.button("Espace Admin"):
        switch_admin()
def interface():
    st.write("Bienvenue à la Poigne d'acier")
    if "focus_interface" not in st.session_state:
        st.session_state.focus_interface = "default"
    if st.session_state.focus_interface == "default":
        interface_acceuil()
    elif st.session_state.focus_interface == "member":
        interface_member()
    elif st.session_state.focus_interface == "register_member":
        interface_register()
    elif st.session_state.focus_interface == "connect_member":
        interface_connection()
    elif st.session_state.focus_interface == "admin":
        interface_admin()

if __name__ == "__main__":
    interface()