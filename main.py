#app.py
import recommendations
import analysis
import streamlit as st

PAGES = {
    "Home": recommendations,
    "Analysis": analysis
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()