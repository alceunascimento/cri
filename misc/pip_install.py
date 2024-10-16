import os
import subprocess
import requests

def download_get_pip():
    url = "https://bootstrap.pypa.io/get-pip.py"
    file_name = "get-pip.py"
    
    print("Baixando get-pip.py...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)
        print("Download concluído com sucesso.")
        return file_name
    else:
        print(f"Erro ao baixar o get-pip.py: {response.status_code}")
        return None

def run_get_pip(file_name):
    print("Executando o get-pip.py...")
    try:
        subprocess.run(["python", file_name], check=True)
        print("pip instalado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o get-pip.py: {e}")

def main():
    file_name = download_get_pip()
    if file_name:
        run_get_pip(file_name)
        
        # Verificar se o pip foi instalado corretamente
        print("Verificando a instalação do pip...")
        try:
            subprocess.run(["pip", "--version"], check=True)
        except FileNotFoundError:
            print("pip não está instalado ou não foi encontrado no PATH.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao verificar a instalação do pip: {e}")

if __name__ == "__main__":
    main()