from weasyprint import HTML

# Convertendo HTML para PDF
HTML('tabela.html').write_pdf('tabela_final.pdf')
