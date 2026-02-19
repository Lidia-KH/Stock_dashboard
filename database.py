from sqlmodel import SQLModel, create_engine
import streamlit as st

engine = create_engine("sqlite:///database.db", echo=False)
@st.cache_resource
def init_db():
    SQLModel.metadata.create_all(engine)
    