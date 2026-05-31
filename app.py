import streamlit as st
st.title("Hello, Streamlit!")
st.write("Hellooooooo")
user_name = st.text_input("Can I have your name?")
st.write(f"Hello, {user_name}!")