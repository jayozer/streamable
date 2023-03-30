import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="centered", page_title="Data Editor", page_icon="🧮")

# Define the authorized usernames and passwords
authorized_users = {"enterprise_user": "password1", "agency_user": "password2"}

def authenticate(username, password):
    """
    Authenticates the user by checking if the username and password match the authorized users.
    """    
    if username in authorized_users and password == authorized_users[username]:
        return True
    else:
        return False

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
            return True
        else:
            st.error("Invalid username or password.")
            return False

# Authenticate the user before showing the Streamlit app
if login():
    pages = ["enterprise", "agency"]

    # Show pages once user is authenticated
    switch_page(pages)

    @st.cache
    def icon(emoji: str):
        """Shows an emoji as a Notion-style page icon."""
        st.write(
            f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
            unsafe_allow_html=True,
        )

    icon(":partying_face:")
    st.title("Streamable - Data Input @ DOMA")

    st.markdown(
        "Streamable looks just like a dataframe but it's editable! Users can click on"
        " cells and edit them. The lists are used in Associate Scorecard Dashboards"
    )

    st.sidebar.markdown(
        """
        Read more ...
        """
    )

    # Conditionally show pages based on authentication status
    if authenticate("username", "password"):
        for page in pages:
            if page == "enterprise":
                switch_page(page)
            elif page == "agency":
                switch_page(page)