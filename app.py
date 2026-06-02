import streamlit as st
from database import add_user, login_user, create_tables

create_tables()
st.set_page_config(page_title="Warranty Tracker", layout="wide") 

st.title("Warranty Tracker")
st.subheader("Manage product warranties and expiry dates")

menu= st.sidebar.selectbox("Menu",["Login","Register"])
if menu == "Login":
    st.subheader("Login Section")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.success(f"Welcome {user[1]}!")
            # Here you can add the functionality for logged-in users
        else:
            st.error("Invalid username or password")
elif menu == "Register":
    st.subheader("Create New Account")
    new_username = st.text_input("Username", key="new_username")
    new_password = st.text_input("Password", type='password', key="new_password")
    role = st.selectbox("Role", ["User"])
    if st.button("Register"):
        add_user(new_username, new_password, role)
        st.success("Account created successfully! Please login.")
