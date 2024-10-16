import sqlite3
import pandas as pd
from openpyxl import Workbook

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('./cri/base_cri.db')

# Obter os nomes de todas as tabelas do banco de dados
query_tables = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql_query(query_tables, conn)['name'].tolist()

# Criar um arquivo Excel com o Pandas ExcelWriter e salvar cada tabela como uma aba diferente
with pd.ExcelWriter('./cri/tabelas_completas.xlsx', engine='openpyxl') as writer:
    for table in tables:
        # Obter os dados da tabela atual
        query = f"SELECT * FROM {table}"
        df = pd.read_sql_query(query, conn)
        
        # Escrever os dados da tabela na planilha, criando uma aba com o nome da tabela
        df.to_excel(writer, sheet_name=table, index=False)

# Fechar a conexão com o banco de dados
conn.close()
