import pandas as pd
import sqlite3

# Carregar a pasta de trabalho
workbook_path = './pre_cri/base_real_ajustada.xlsx'

# Criar um banco de dados SQLite
conn = sqlite3.connect('./pre_cri/base_real.db')

# Definindo um dicionário para armazenar as abas e os dataframes correspondentes
sheet_names = [
    'informacoes_preliminares', 'quadro_area_01', 'quadro_area_02', 
    'quadro_area_03', 'quadro_area_04A', 'quadro_area_04B', 
    'quadro_area_05', 'quadro_area_06', 'quadro_area_07', 
    'quadro_area_08', 'quadro_resumo'
]

# Carregar cada aba da planilha em um dataframe
dataframes = {}
for sheet in sheet_names:
    dataframes[sheet] = pd.read_excel(workbook_path, sheet_name=sheet)

# Aguardando as instruções para a criação de tabelas para cada aba
print("Estrutura base configurada. Vamos começar a trabalhar aba por aba.")

# Fechar conexão
conn.close()
