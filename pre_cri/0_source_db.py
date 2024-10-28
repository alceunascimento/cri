import subprocess
import os

# Diretório contendo os scripts
script_dir = os.path.dirname(os.path.abspath(__file__))

# Lista de arquivos para execução em ordem
scripts = [
    "1_set_xlsx.py",
    "2_quadro00_infoprel.py",
    "2_quadro01.py",
    "2_quadro02.py",
    "2_quadro03.py",
    "2_quadro04A.py",
    "2_quadro04B.py",
    "2_quadro05.py",
    "2_quadro06.py",
    "2_quadro07.py",
    "2_quadro08.py",
    "3_quadro_resumo.py",
    "4_alvara_criar.py",
    "4_alvara_popular.py",
    "5_tabela_cri.py",
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