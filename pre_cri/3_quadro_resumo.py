import pandas as pd
import sqlite3
import re
from typing import List, Union
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def desagregar_unidades(texto: str) -> List[Union[str, int]]:
    """
    Desagrega unidades de texto em uma lista de números ou strings.
    Trata casos especiais como 'Comércio e Serviço Vicinal X'.
    
    Args:
        texto (str): Texto contendo os números das unidades
        
    Returns:
        List[Union[str, int]]: Lista com os números das unidades
    """
    if not isinstance(texto, str):
        return []
        
    unidades = []
    
    # Verificar primeiro se é um caso de "Comércio e Serviço Vicinal"
    comercio_match = re.match(r'Comércio e Serviço Vicinal (\d+)', texto, re.IGNORECASE)
    if comercio_match:
        # Retornar o número formatado com zero à esquerda
        numero = int(comercio_match.group(1))
        return [f"{numero:02d}"]
    
    # Processar outros casos normalmente
    grupos = re.findall(r'\d+(?:/\d+)?(?: a \d+)?', texto)
    for grupo in grupos:
        if '/' in grupo:
            unidades.append(grupo)
        elif ' a ' in grupo:
            inicio, fim = map(int, grupo.split(' a '))
            unidades.extend(range(inicio, fim + 1))
        else:
            unidades.append(int(grupo))
            
    return unidades

def process_quadro_resumo(workbook_path: str, sheet_name: str) -> pd.DataFrame:
    """
    Process the quadro_resumo sheet and create expanded DataFrame
    
    Args:
        workbook_path (str): Path to Excel file
        sheet_name (str): Name of the sheet to process
        
    Returns:
        pd.DataFrame: Processed and expanded DataFrame
    """
    try:
        # Ler a aba "quadro_resumo" do arquivo Excel
        df = pd.read_excel(workbook_path, sheet_name=sheet_name, header=11)
        
        # Definir nomes das colunas
        column_names = [
            'subcondominio', 'unidade_tipo', 'unidade_quantidade',
            'area_alvara_privativa', 'area_alvara_deposito_vinculado',
            'area_alvara_comum', 'area_alvara_total',
            'fracao_ideal_solo_subcondominio', 'area_comum_descoberta',
            'area_total', 'fracao_ideal_solo_condominio',
            'quota_terreno', 'numeros_unidades'
        ]
        df.columns = column_names
        
        # Expandir as unidades
        linhas_expandidas = []
        for idx, row in df.iterrows():
            unidades = desagregar_unidades(row['numeros_unidades'])
            for unidade in unidades:
                nova_linha = row.copy()
                nova_linha['numeros_unidades'] = unidade
                linhas_expandidas.append(nova_linha)
        
        # Criar DataFrame expandido
        df_expanded = pd.DataFrame(linhas_expandidas)
        
        # Renomear e reorganizar colunas
        df_expanded = df_expanded.rename(columns={'numeros_unidades': 'unidade_numero'})
        cols = df_expanded.columns.tolist()
        cols.remove('unidade_numero')
        cols.insert(1, 'unidade_numero')
        df_expanded = df_expanded[cols]
        
        return df_expanded
        
    except Exception as e:
        logging.error(f"Error processing quadro_resumo: {str(e)}")
        raise

def validate_unit_counts(df_expanded: pd.DataFrame, df_original: pd.DataFrame) -> None:
    """
    Validate that the number of units matches the expected quantities
    
    Args:
        df_expanded (pd.DataFrame): Expanded DataFrame with individual units
        df_original (pd.DataFrame): Original DataFrame with unit counts
    """
    for unidade_tipo, grupo in df_expanded.groupby('unidade_tipo'):
        quantidade_esperada = df_original.loc[
            df_original['unidade_tipo'] == unidade_tipo, 
            'unidade_quantidade'
        ].iloc[0]
        quantidade_real = len(grupo)
        
        if quantidade_esperada != quantidade_real:
            error_msg = (f"Erro de validação: {unidade_tipo} deveria ter "
                        f"{quantidade_esperada} unidades, mas tem {quantidade_real} unidades.")
            logging.error(error_msg)
            raise ValueError(error_msg)

def main():
    try:
        # Configurar caminhos
        workbook_path = './pre_cri/data/base_real_ajustada.xlsx'
        sheet_name = 'quadro_resumo'
        db_path = './pre_cri/base_real.db'
        
        # Processar dados
        df = pd.read_excel(workbook_path, sheet_name=sheet_name, header=11)
        df_expanded = process_quadro_resumo(workbook_path, sheet_name)
        
        # Validar dados
        validate_unit_counts(df_expanded, df)
        
        # Salvar no banco de dados
        with sqlite3.connect(db_path) as conn:
            df_expanded.to_sql('quadro_resumo', conn, if_exists='replace', index=False)
            logging.info("Tabela `quadro_resumo` criada e populada com sucesso.")
            
    except Exception as e:
        logging.error(f"Erro no processamento: {str(e)}")
        raise

if __name__ == "__main__":
    main()