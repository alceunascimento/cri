import subprocess
import os

# Diretório contendo os scripts
script_dir = os.path.dirname(os.path.abspath(__file__))

# Lista de arquivos para execução em ordem
scripts = [
    "set_xlsx.py",
    "1_create_aba01_insert_data.py",
    "2_.py",
    "4A_.py",
    "4B_.py",
    "5_.py",
    "6_.py",
    "7_.py",
    "8_.py",
    "9_create_xml_from_db.py",
    "10_xml_to_xlxs.py"
]

# Executar cada script
for script in scripts:
    script_path = os.path.join(script_dir, script)
    try:
        print(f"Executando {script}...")
        result = subprocess.run(["python", script_path], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar {script}: {e.stderr}")