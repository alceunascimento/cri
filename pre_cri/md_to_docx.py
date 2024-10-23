import subprocess

# Função para converter markdown para docx
def convert_md_to_docx(input_file, output_file):
    try:
        subprocess.run(['pandoc', input_file, '-o', output_file], check=True)
        print(f"Arquivo {output_file} criado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao converter {input_file} para {output_file}: {e}")

# Função para converter docx para pdf
def convert_docx_to_pdf(input_file, output_file):
    try:
        subprocess.run(['pandoc', input_file, '-o', output_file], check=True)
        print(f"Arquivo {output_file} criado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao converter {input_file} para {output_file}: {e}")

# Caminho do arquivo markdown
md_file = './pre_cri/memorial.md'

# Convertendo markdown para docx
docx_file = './pre_cri/memorial.docx'
convert_md_to_docx(md_file, docx_file)

