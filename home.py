import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(layout="centered", page_title="Streamble Data Editor")

# Load authorized usernames and passwords from environment variables
AUTHORIZED_USERS = {os.getenv("STREAMLIT_USERNAME"): os.getenv("STREAMLIT_PASSWORD")}

def authenticate(username, password):
    """
    Authenticates the user by checking if the username and password match the authorized users.
    """    
    return username in AUTHORIZED_USERS and password == AUTHORIZED_USERS[username]

def login():
    """
    Displays a login form and authenticates the user before showing the Streamlit app.
    """
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.success("You have successfully logged in!")
            st.write("Choose a sheet from the side bar to get started.")      
        else:
            st.error("Invalid username or password.")

# Authenticate the user before showing the Streamlit app
business_line = login()
if business_line:
    if business_line == "Enterprise":
        st.title("Enterprise page")
        st.write("This is the enterprise page.")
    elif business_line == "Agency":
        st.title("Agency page")
        st.write("This is the agency page.")

