import sqlite3

# Database connection
db_path = './pre_cri/base_real.db'
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# List of unidade_numero values to check
unidade_numeros = ['14', '16', '84/83', '218', '59', '220/221', '239', '24']

# Execute queries and print results
for unidade_numero in unidade_numeros:
    query = f"SELECT tipo_vaga FROM cri WHERE unidade_numero = '{unidade_numero}';"
    cursor.execute(query)
    result = cursor.fetchall()
    print(f"Result for unidade_numero {unidade_numero}: {result}")

# Close the connection
connection.close()
