import subprocess
import os

# Diretório contendo os scripts
script_dir = os.path.dirname(os.path.abspath(__file__))

# Lista de arquivos para execução em ordem
scripts = [
    "7_cria_tipologia_unidade.py",
    "8_cria_pavimentos.py",
    "9_cria_memorial2.py",
    "9_md_to_docx.py",
    "9_cria_edificio.py",
    "10_criar_quadro00.py",
    "10_criar_quadro01.py",
    "10_criar_quadro02.py",
    "10_criar_quadro03.py",
    "10_criar_quadro04A.py",
    "10_criar_quadro04B.py",
    "10_criar_quadro05.py",
    "10_criar_quadro06.py",
    "10_criar_quadro07.py",
    "10_criar_quadro08.py",
    "10_criar_quadro_resumo.py"
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