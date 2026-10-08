import streamlit as st

st.set_page_config(page_title="My Streamlit App", page_icon="👋", layout="centered")  
st.title("Welcome to Anvay's App! :wave:")
st.write("This is a simple Streamlit app.I built this while learning python")

st.divider()

name = st.text_input("What is your name?",placeholder="Type your name...")

if name:
    st.write(f"Hello, {name}! Welcome here.") 
    st.divider()

age = st.number_input("What is your age?", min_value=0, max_value=60, value=18)
st.write(f"You are **{age}** years old.")  

interests = st.multiselect("What are your learning ?", ["Python", "Data Science","Web Development", "Machine Learning"])
st.info(f"Great choice!{interests} are excellent skills to learn.")

st.divider()

agree = st.checkbox("I will practice code daily.")
if agree:
    st.success("That's the spirit! Keep up the good work.")

if st.button("Click for a motivational quote"):
    st.write("“ You dont have to be everyones cup of tea.\n Be gasoline\n Set shii on fire.\n ” - Anonymous")