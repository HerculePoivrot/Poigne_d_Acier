import streamlit as st
import random
class MembresInscription:
    def __init__(self, name: str, mail: str):
        self.name = name  # Utilise les valeurs passées en argument
        self.mail = mail
    def get_name(self):
        return self.name
    def get_mail(self):
        return self.mail
    def generate_card_id(self):
        unique_id = ""
        len_name = len(self.name)
        len_mail = len(self.mail)
        for i in range(len_name * len_mail):
            id_choice_phase = random.choice([self.name,self.mail])
            unique_id += str(ord(random.choice(id_choice_phase)))
        print(unique_id)
        return int(unique_id)
class CarteMembre:
    def __init__(self,unique_id):
        self.unique_id = unique_id
    def get_unique_id(self):
        return self.unique_id
class InsciptionMembre:
    def __init__(self):
        

def input_users():
    # Crée un formulaire avec un bouton de soumission
    with st.form("add_question_form", clear_on_submit=True):
        name = st.text_input(label="Name", placeholder="Jean Dupont")
        mail = st.text_input(label="Mail", placeholder="toto@gmail.com")  # Retirer type="email"
        submit = st.form_submit_button("Submit")  # Bouton de soumission
        if submit:
            # Crée une instance avec les valeurs saisies
            membre = MembresInscription(name, mail)
            # Stocke dans la session pour réutilisation
            st.session_state.membre_inscription = membre
            st.write(f"Membre ajouté : {membre.get_name()} ({membre.get_mail()})")  # Affiche le membre ajouté
def create_user():
    if "membre_inscription" not in st.session_state:
        st.session_state.membre_inscription = None
    
    input_users()
    if st.session_state.membre_inscription is not None:
        if "carte_membre" not in st.session_state:
            st.session_state.carte_membre = None
        unique_id = st.session_state.membre_inscription.generate_card_id()
        st.session_state.carte_membre = CarteMembre(unique_id)
        if type(st.session_state.carte_membre) == CarteMembre:
            st.write(f"{st.session_state.carte_membre.get_unique_id()=}")
def connect_user():
    input_card  = st.text_input(label="IdUser:")
    if st.button("Connection"):
        if int(input_card) == st.session_state.carte_membre.get_unique_id():
            st.write("Connection Success")
            st.session_state.state_connection = True
            st.rerun()
        else:
            st.write(f"{st.session_state.carte_membre.get_unique_id()=}")
            st.write(f"{int(input_card)=}")
            st.write("Connection Failed")
            st.session_state.state_connection = False
def disconnect_user():
    if st.button("Déconnexion"):
        st.session_state.state_connection = False
        st.rerun()
    

if __name__ == "__main__":
    if "state_connection" not in st.session_state:
        st.session_state.state_connection = False
    st.title("Users:")
    if "carte_membre" in st.session_state and "membre_inscription" in st.session_state:
        
        if st.session_state.state_connection == True:
            st.write("Je suis en état connecté")
            disconnect_user()
        else:
            connect_user()
            st.write("Je ne suis pas en état connecté")
    else:
        create_user()
