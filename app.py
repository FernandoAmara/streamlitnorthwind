import streamlit as st
import pandas as pd
import sqlite3


def list_tables():
    db_connection = sqlite3.connect('northwind.db')
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql_query(query, db_connection)
    db_connection.close()
    return tables['name'].tolist()


def list_table_columns(table_name):
    db_connection = sqlite3.connect('northwind.db')
    query = f"PRAGMA table_info({table_name});"
    columns = pd.read_sql_query(query, db_connection)
    db_connection.close()
    return columns['name'].tolist()


def run_query(query):
    db_connection = sqlite3.connect('northwind.db')
    query_result = pd.read_sql_query(query, db_connection)
    db_connection.close()
    return query_result


st.set_page_config(layout="wide")


def main():
    st.title('Executar consulta banco Northwind')


    st.sidebar.title("Tabelas e Campos do Banco de Dados")
    tables = list_tables()
    for table in tables:
        if st.sidebar.checkbox(table):
            columns = list_table_columns(table)
            for column in columns:
                st.sidebar.text(f"   - {column}")


    query = st.text_area("Insira sua consulta SQL aqui:", height=150)


    if st.button('Executar'):
        if query:
            try:

                result = run_query(query)
                st.dataframe(result, use_container_width=True)
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
        else:
            st.error("Por favor, insira uma consulta SQL.")

if __name__ == "__main__":
    main()
