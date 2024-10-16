from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import json
from time import sleep


def extract_table_data(table):
    headers = [th.get_text(strip=True) for th in table.find_all('tr')[0].find_all('td')]
    values = [td.get_text(strip=True) for td in table.find_all('tr')[1].find_all('td')]
    return dict(zip(headers, values))

def get_documentos(browser, indicacao_fiscal: str, sublote: str):
    home_url = 'http://www2.curitiba.pr.gov.br/gtm/pmat_consultardadosalvaraconstrucao/DefaultDinamico.htm'
    
    # Abrir navegador
    browser.get(home_url) 
    browser.switch_to.frame("fraMain")
    
    # Selecionar Opção de filtro por Indicação Fiscal e Sublote e enviar valores.
    browser.find_element(By.ID, 'rdoTipoPesquisa_3').click()
    browser.find_element(By.ID, 'strIndFiscal').send_keys(indicacao_fiscal)
    browser.find_element(By.ID, 'strSublote').send_keys(sublote)
    browser.find_element(By.NAME, 'WUCBarra1$Pesquisar').click()

    # Coletar numeros dos documentos
    browser.switch_to.default_content()
    browser.switch_to.frame("fraMain")
    result = browser.find_element(By.ID, 'dgDetalhesAlvLote')
    soup = BeautifulSoup(result.get_attribute('outerHTML'), 'html.parser')
    table = soup.find('table', {'id': 'dgDetalhesAlvLote'})
    documentos = [row.find('td').text.strip() for row in table.find_all('tr')[1:]]
    return documentos

def get_alvara_contrucao(browser, documento):
    record_url = 'http://www2.curitiba.pr.gov.br/gtm/pmat_consultardadosalvaraconstrucao/DetalheAlvaraConstrucao.aspx?strNrDocumento={}&rdoTipoPesquisa=0'
    browser.get(record_url.format(documento))
    browser.switch_to.default_content()

    # Parse dos dados da div1
    result = browser.find_element(By.ID, 'DIV_1')
    soup = BeautifulSoup(result.get_attribute('outerHTML'), 'html.parser')
    div1 = {}
    # Iterate over all rows in the relevant table
    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        # If the row has 4 columns, it's a sub-object with specific fields
        if len(tds) == 4:
            main_key = tds[0].get_text(strip=True).replace('\xa0', ' ')
            sub_object = {
                "Nome": tds[1].get_text(strip=True),
                tds[2].get_text(strip=True).replace('\xa0', ' '): tds[3].get_text(strip=True)
            }
            div1[main_key] = sub_object
        # If the row has 2 columns, it's a simple key-value pair
        elif len(tds) == 2:
            key = tds[0].get_text(strip=True).replace('\xa0', ' ')
            value = tds[1].get_text(strip=True)
            div1[key] = value

    # Parse dos dados da div2
    result = browser.find_element(By.ID, 'DIV_2')
    soup = BeautifulSoup(result.get_attribute('outerHTML'), 'html.parser')
    div2 = {}
    # Iterate over all rows in the relevant table
    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        # If the row has 2 columns, it's a key-value pair
        if len(tds) == 2:
            key = tds[0].get_text(strip=True).replace('\xa0', ' ')
            value = tds[1].get_text(strip=True)
            div2[key] = value


    # Parse dos dados da div3
    result = browser.find_element(By.ID, 'DIV_3')
    soup = BeautifulSoup(result.get_attribute('outerHTML'), 'html.parser')
    # Main data dictionary
    div3 = {}

    dados_lote_table = soup.find('table', {'id': 'dgDadosLote'})
    dados_lote = extract_table_data(dados_lote_table)
    div3['DadosLote'] = dados_lote

    # Get data from first block
    for tr in soup.find_all('table')[2].find_all('table')[3].find_all('tr'):
        tds = tr.find_all('td')
        # If the row has 4 columns, it's a sub-object with specific fields
        if len(tds) == 5:
            div3[tds[0].get_text(strip=True).replace('\xa0', ' ')] = tds[1].get_text(strip=True).replace('\xa0', ' ')
            div3[tds[3].get_text(strip=True).replace('\xa0', ' ')] = tds[4].get_text(strip=True).replace('\xa0', ' ')
        # If the row has 2 columns, it's a key-value pair
        if len(tds) == 3:
            key = tds[0].get_text(strip=True).replace('\xa0', ' ')
            value = tds[1].get_text(strip=True)
            div3[key] = value

    dados_edificacao_table = soup.find('table', {'id': 'dgDadosEdificacao'})
    dados_edificacao = extract_table_data(dados_edificacao_table)
    div3['DadosEdificacao'] = dados_edificacao

    # Get data from the second block
    div3['Áreas Computáveis (m2)'] = {}
    div3['Áreas Não Computáveis (m2)'] = {}

    for tr in soup.find_all('table')[2].find_all('table')[6].find_all('tr')[1:6]:
        tds = tr.find_all('td')
        div3['Áreas Computáveis (m2)'][tds[0].get_text(strip=True).replace('\xa0', ' ')] = tds[1].get_text(strip=True).replace('\xa0', ' ')
        div3['Áreas Não Computáveis (m2)'][tds[3].get_text(strip=True).replace('\xa0', ' ')] = tds[4].get_text(strip=True).replace('\xa0', ' ')

    for tr in soup.find_all('table')[2].find_all('table')[6].find_all('tr')[6:]:
        tds = tr.find_all('td')
        div3['Áreas Não Computáveis (m2)'][tds[3].get_text(strip=True).replace('\xa0', ' ')] = tds[4].get_text(strip=True).replace('\xa0', ' ')

    div3['Áreas De Recreção (m2)'] = {}
    div3['Outras Áreas (m2)'] = {}
    div3['Parâmentros Do Zoneamento'] = {}

    for tr in soup.find_all('table')[2].find_all('table')[7].find_all('tr'):
        tds = tr.find_all('td')
        # If the row has 4 columns, it's a sub-object with specific fields
        if len(tds) == 5:
            div3['Áreas De Recreção (m2)'][tds[0].get_text(strip=True).replace('\xa0', ' ')] = tds[1].get_text(strip=True).replace('\xa0', ' ')
            div3['Áreas De Recreção (m2)'][tds[3].get_text(strip=True).replace('\xa0', ' ')] = tds[4].get_text(strip=True).replace('\xa0', ' ')
        # If the row has 2 columns, it's a key-value pair
        if len(tds) == 3:
            key = tds[0].get_text(strip=True).replace('\xa0', ' ')
            value = tds[1].get_text(strip=True)
            div3['Áreas De Recreção (m2)'][key] = value

    for tr in soup.find_all('table')[2].find_all('table')[8].find_all('tr'):
        tds = tr.find_all('td')
        # If the row has 4 columns, it's a sub-object with specific fields
        if len(tds) == 5:
            div3['Outras Áreas (m2)'][tds[0].get_text(strip=True).replace('\xa0', ' ')] = tds[1].get_text(strip=True).replace('\xa0', ' ')
            div3['Outras Áreas (m2)'][tds[3].get_text(strip=True).replace('\xa0', ' ')] = tds[4].get_text(strip=True).replace('\xa0', ' ')
        # If the row has 2 columns, it's a key-value pair
        if len(tds) == 3:
            key = tds[0].get_text(strip=True).replace('\xa0', ' ')
            value = tds[1].get_text(strip=True)
            div3['Outras Áreas (m2)'][key] = value

    for tr in soup.find_all('table')[2].find_all('table')[9].find_all('tr'):
        tds = tr.find_all('td')
        # If the row has 4 columns, it's a sub-object with specific fields
        if len(tds) == 5:
            div3['Parâmentros Do Zoneamento'][tds[0].get_text(strip=True).replace('\xa0', ' ')] = tds[1].get_text(strip=True).replace('\xa0', ' ')
            div3['Parâmentros Do Zoneamento'][tds[3].get_text(strip=True).replace('\xa0', ' ')] = tds[4].get_text(strip=True).replace('\xa0', ' ')
        # If the row has 2 columns, it's a key-value pair
        if len(tds) == 3:
            key = tds[0].get_text(strip=True).replace('\xa0', ' ')
            value = tds[1].get_text(strip=True)
            div3['Parâmentros Do Zoneamento'][key] = value

    alvara = div1
    alvara.update(div2)
    alvara.update(div3)
    return alvara
    
def buscar_alvara(documentos):
    for documento in documentos:
        try:
            #documento=142303
            # Set up Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Ensure GUI is off
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            # chrome_service = Service(executable_path="./chromedriver.exe")

            browser = webdriver.Chrome()
            doc = get_alvara_contrucao(browser, str(documento))

            with open(f'{documento}.json', 'w', encoding='utf-8') as f:
                json.dump(doc, f, ensure_ascii=False)
        except:
            pass