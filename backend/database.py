import os
import psycopg2
from dotenv import load_dotenv
import streamlit as st


def get_connection():
    """
    Cria conexão com o banco PostgreSQL.
    Funciona:
    - Localmente usando .env
    - No Streamlit Cloud usando st.secrets
    """

    # ==========================================
    # TENTA USAR STREAMLIT SECRETS (CLOUD)
    # ==========================================
    try:
        return psycopg2.connect(
            host=st.secrets["DB_HOST"],
            database=st.secrets["DB_NAME"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            port=st.secrets.get("DB_PORT", 5432)
        )

    except Exception:
        pass  # se não tiver secrets, tenta .env

    # ==========================================
    # USA .ENV (LOCAL)
    # ==========================================
    load_dotenv()

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", 5432)
    )