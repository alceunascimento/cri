from markdown_pdf import MarkdownPdf, Section

# Criando o PDF com o nível de TOC até o nível 1
pdf = MarkdownPdf(toc_level=1)

# Lendo o conteúdo do arquivo memorial.md
with open("./pre_cri/memorial.md", "r", encoding="utf-8") as md_file:
    markdown_content = md_file.read()

# Adicionando o conteúdo do arquivo markdown ao PDF
pdf.add_section(Section(markdown_content))

# Configurando metadados do PDF
pdf.meta["title"] = "Memorial"
pdf.meta["author"] = "Nome do Autor"

# Salvando o PDF
pdf.save("./pre_cri/memorial.pdf")
