import streamlit as st

st.title("Welcome")

# Track authentication and page state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

choice = st.sidebar.selectbox("Login / Register", ["Login", "Register"])

if choice == "Login":
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            # Add your verification logic here
            if username == "admin" and password == "password":
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
            else:
                st.error("Invalid credentials")

elif choice == "Register":
    with st.form("register_form"):
        new_user = st.text_input("Choose Username")
        new_pass = st.text_input("Choose Password", type="password")
        confirm_pass = st.text_input("Confirm Password", type="password")
        reg_submit = st.form_submit_button("Register")
        
        if reg_submit:
            if new_pass == confirm_pass and len(new_user) > 0:
                # Add your database insertion / hashing logic here
                st.success("Account created! Please log in.")
            else:
                st.error("Passwords do not match or fields are empty.")
