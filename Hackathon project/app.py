import streamlit as st
from database import create_tables

st.set_page_config(
    page_title="Badshah Ka Wazeer Kon",
    page_icon="👑",
    layout="centered"
)

create_tables()

st.title("👑 Badshah Ka Wazeer Kon")

st.write("""
Welcome to **Badshah Ka Wazeer Kon**!

Use the navigation menu on the left to go to **Create or Join**.
""")