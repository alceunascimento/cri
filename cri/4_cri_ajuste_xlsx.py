from spire.xls import Workbook, ExcelVersion

# Definir o arquivo de entrada e o arquivo de saída
inputFile = "./cri/tabelas_completas.xlsx"
outputFile = "./cri/tabelas_completas_com_cabecalho_paisagem.xlsx"

# Criar um objeto da classe Workbook
workbook = Workbook()

# Carregar o arquivo Excel existente
workbook.load_from_file(inputFile)

# Iterar sobre todas as planilhas do workbook para adicionar o cabeçalho e ajustar a página
for sheet in workbook.worksheets:
    # Definir o cabeçalho para cada aba
    sheet.page_setup.center_header = "&\"Calibri\"&14 INFORMAÇÕES PARA ARQUIVO NO REGISTRO DE IMÓVEIS\nQuadro II - Cálculo das Unidades Autônomas - Colunas 19 a 38"
    sheet.page_setup.left_header = "&\"Calibri\"&12 LOCAL DO IMÓVEL: Rua Afrindo - SN"
    sheet.page_setup.right_header = "&\"Calibri\"&12 FOLHA N°: 08 de 04 de 15"

    # Adicionar informações adicionais ao rodapé
    sheet.page_setup.left_footer = "&\"Calibri\"&12 Nome: XXX Empreendimentos Imobiliários SPE Ltda\nAssinatura: ___________"
    sheet.page_setup.center_footer = "&P"  # Número da página
    sheet.page_setup.right_footer = "&\"Calibri\"&12 Nome: Robson | Registro CREA: 123456\nData: 01/09/2021"

    # Ajustar a configuração da página para orientação paisagem
    sheet.page_setup.orientation = PageOrientationType.Landscape

    # Ajustar a configuração da página para que tudo seja impresso em uma única largura de página
    sheet.page_setup.fit_to_pages_wide = 1
    sheet.page_setup.fit_to_pages_tall = 0  # Definir como 0 faz o ajuste automático na altura

# Salvar o arquivo Excel resultante
workbook.save_to_file(outputFile, ExcelVersion.Version2010)
workbook.dispose()
