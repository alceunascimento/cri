import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Any, NoReturn, Iterator, TypeVar, Tuple
from dataclasses import dataclass, field
import logging
from decimal import Decimal
from contextlib import contextmanager
import sys
from enum import Enum, auto
from abc import ABC, abstractmethod
import os

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler('memorial_generator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class MemorialError(Exception):
    """Base exception for memorial generator errors"""
    pass

class DatabaseError(MemorialError):
    """Database-related errors"""
    pass

class XMLError(MemorialError):
    """XML processing errors"""
    pass

class FileError(MemorialError):
    """File handling errors"""
    pass

class UnitType(Enum):
    """Enumeration for unit types"""
    APARTMENT = auto()
    PARKING = auto()
    STORE = auto()
    UNKNOWN = auto()

    @classmethod
    def from_str(cls, value: str) -> 'UnitType':
        """Convert string to UnitType"""
        mapping = {
            'APARTAMENTO': cls.APARTMENT,
            'VAGA': cls.PARKING,
            'LOJA': cls.STORE
        }
        return mapping.get(value.upper(), cls.UNKNOWN)

@dataclass
class UnitData:
    """Data class to store unit information with enhanced type safety"""
    especie_unidade: str
    unidade_numero: str
    subcondominio: str
    area_total_construida: Decimal
    area_privativa: Decimal
    area_comum: Decimal
    fracao_ideal_solo_condominio: Decimal
    fracao_ideal_unidade_subcondominio: Decimal
    quota_terreno_condominio: Decimal
    area_comum_descoberta: Decimal
    pavimento: str
    confrontacao_frente: str
    confrontacao_direita: str
    confrontacao_esquerda: str
    confrontacao_fundos: str
    tipo_vaga: Optional[str] = None
    area_vinculada_outras: Decimal = Decimal('0.0')
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UnitData':
        """Create UnitData instance from dictionary with validation"""
        try:
            return cls(
                especie_unidade=str(data.get('especie_unidade', '')).upper(),
                unidade_numero=str(data.get('unidade_numero', '')),
                subcondominio=str(data.get('subcondominio', '')).upper(),
                area_total_construida=Decimal(str(data.get('area_total_construida', 0))).quantize(Decimal('0.00000000')),
                area_privativa=Decimal(str(data.get('area_privativa', 0))).quantize(Decimal('0.00000000')),
                area_comum=Decimal(str(data.get('area_comum', 0))).quantize(Decimal('0.00000000')),
                fracao_ideal_solo_condominio=Decimal(str(data.get('fracao_ideal_solo_condominio', 0))).quantize(Decimal('0.00000000')),
                fracao_ideal_unidade_subcondominio=Decimal(str(data.get('fracao_ideal_unidade_subcondominio', 0))).quantize(Decimal('0.00000000')),
                quota_terreno_condominio=Decimal(str(data.get('quota_terreno_condominio', 0))).quantize(Decimal('0.00000000')),
                area_comum_descoberta=Decimal(str(data.get('area_comum_descoberta', 0))).quantize(Decimal('0.00000000')),
                pavimento=str(data.get('pavimento', '')),
                confrontacao_frente=str(data.get('confrontacao_frente', '')),
                confrontacao_direita=str(data.get('confrontacao_direita', '')),
                confrontacao_esquerda=str(data.get('confrontacao_esquerda', '')),
                confrontacao_fundos=str(data.get('confrontacao_fundos', '')),
                tipo_vaga=data.get('tipo_vaga'),
                area_vinculada_outras=Decimal(str(data.get('area_vinculada_outras', 0))).quantize(Decimal('0.00000000'))
            )
        except (ValueError, TypeError, decimal.InvalidOperation) as e:
            raise ValueError(f"Error creating UnitData from dictionary: {e}")

class UnitDescriptionGenerator(ABC):
    """Abstract base class for unit description generators"""
    @abstractmethod
    def generate(self, unit: UnitData) -> str:
        """Generate description for a unit"""
        pass

class ApartmentDescriptionGenerator(UnitDescriptionGenerator):
    def generate(self, unit: UnitData) -> str:
        return f"""APARTAMENTO {unit.unidade_numero}:
Subcondomínio: {unit.subcondominio}.
Áreas construídas: área total construída de {unit.area_total_construida:.8f} metros quadrados,
sendo a área privativa de {unit.area_privativa:.8f} metros quadrados
e a área comum de {unit.area_comum:.8f} metros quadrados.
Fração ideal nas partes comuns do subcondomínio: {unit.fracao_ideal_unidade_subcondominio:.8f};
Fração ideal de solo e partes comuns no condomínio: {unit.fracao_ideal_solo_condominio:.8f};
Quota de terreno: {unit.quota_terreno_condominio:.8f} metros quadrados.
Area comum descoberta: {unit.area_comum_descoberta:.8f} metros quadrados.
Localização: {unit.pavimento}, sendo que para quem entra na unidade,
confronta pela frente com {unit.confrontacao_frente},
pelo lado direito com {unit.confrontacao_direita},
pelo lado esquerdo com {unit.confrontacao_esquerda}
e pelo fundo com {unit.confrontacao_fundos}."""

class ParkingDescriptionGenerator(UnitDescriptionGenerator):
    def generate(self, unit: UnitData) -> str:
        tipo_vaga_str = "simples para (1)" if unit.tipo_vaga.lower() == 'simples' else "dupla para (2)"
        
        description = [
            f"VAGA {unit.unidade_numero}:",
            f"Subcondomínio: {unit.subcondominio}.",
            f"Capacidade e uso: {tipo_vaga_str} veículo(s) de passeio, de pequeno e médio porte.",
            "Áreas construídas:",
            f"área total construída de {unit.area_total_construida:.8f} metros quadrados,",
            f"sendo a área privativa de {unit.area_privativa:.8f} metros quadrados"
        ]

        if unit.area_vinculada_outras > 0:
            description.append(f", área de depósito nº {unit.unidade_numero} de {unit.area_vinculada_outras:.8f} metros quadrados")

        description.extend([
            f", e a área comum de {unit.area_comum:.8f} metros quadrados.",
            f"Fração ideal nas partes comuns do subcondomínio: {unit.fracao_ideal_unidade_subcondominio:.8f};",
            f"Fração ideal de solo e partes comuns no condomínio: {unit.fracao_ideal_solo_condominio:.8f};",
            f"Quota de terreno: {unit.quota_terreno_condominio:.8f} metros quadrados.",
            f"Localização: {unit.pavimento}, sendo que para quem entra na unidade,",
            f"confronta pela frente com {unit.confrontacao_frente},",
            f"pelo lado direito com {unit.confrontacao_direita},",
            f"pelo lado esquerdo com {unit.confrontacao_esquerda},",
            f"e pelo fundo com {unit.confrontacao_fundos}."
        ])

        return ' '.join(description)

class StoreDescriptionGenerator(UnitDescriptionGenerator):
    def generate(self, unit: UnitData) -> str:
        return f"""LOJA {unit.unidade_numero}:
Subcondomínio: {unit.subcondominio}.
Áreas construídas: área total construída de {unit.area_total_construida:.8f} metros quadrados,
sendo a área privativa de {unit.area_privativa:.8f} metros quadrados
e a área comum de {unit.area_comum:.8f} metros quadrados.
Fração ideal nas partes comuns do subcondomínio: {unit.fracao_ideal_unidade_subcondominio:.8f};
Fração ideal de solo e partes comuns no condoínio: {unit.fracao_ideal_solo_condominio:.8f};
Quota de terreno: {unit.quota_terreno_condominio:.8f} metros quadrados.
Localização: {unit.pavimento}, sendo que para quem entra na unidade,
confronta pela frente com {unit.confrontacao_frente},
pelo lado direito com {unit.confrontacao_direita},
pelo lado esquerdo com {unit.confrontacao_esquerda}
e pelo fundo com {unit.confrontacao_fundos}."""

@contextmanager
def database_connection(db_path: Path) -> Iterator[sqlite3.Connection]:
    """Context manager for database connections"""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        raise DatabaseError(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

class XMLDatabaseConverter:
    def __init__(self, xml_path: Path, db_path: Path):
        self.xml_path = xml_path
        self.db_path = db_path
        
    def convert_xml_to_db(self) -> None:
        """Convert XML file to SQLite database with improved error handling"""
        try:
            tree = ET.parse(self.xml_path)
            root = tree.getroot()
            
            with database_connection(self.db_path) as conn:
                self._create_table(conn, root)
                self._insert_data(conn, root)
                
            logger.info(f"Database '{self.db_path}' created and populated successfully")
            
        except ET.ParseError as e:
            raise XMLError(f"Error parsing XML file: {e}")
        except Exception as e:
            raise MemorialError(f"Error during XML to database conversion: {e}")

    def _create_table(self, conn: sqlite3.Connection, root: ET.Element) -> None:
        """Create database table with improved validation"""
        tabela = next((t for t in root.findall("Tabela") 
                      if t.attrib.get("nome") == "cri"), None)
        if tabela is None:  # Fixed deprecated warning
            raise XMLError("Required 'cri' table not found in XML")

        registro = tabela.find('Registro')
        if registro is None:
            raise XMLError("No 'Registro' element found in 'cri' table")

        colunas = [campo.tag for campo in registro]
        if not colunas:
            raise XMLError("No columns found in 'Registro' element")

        colunas_sql = [f"{coluna} TEXT" for coluna in colunas]
        colunas_sql_str = ', '.join(colunas_sql)
        
        conn.execute(f'''
            CREATE TABLE IF NOT EXISTS cri (
                {colunas_sql_str}
            )
        ''')

    def _insert_data(self, conn: sqlite3.Connection, root: ET.Element) -> None:
        """Insert data from XML into database with duplicate prevention"""
        try:
            cursor = conn.cursor()
            
            # First, clear existing data
            cursor.execute("DELETE FROM cri")
            
            # Track units we've seen to prevent duplicates
            seen_units = set()
            
            for tabela in root.findall("Tabela"):
                if tabela.attrib.get("nome") == "cri":
                    for registro in tabela.findall('Registro'):
                        unit_number = registro.find('unidade_numero')
                        
                        if unit_number is None or not unit_number.text:
                            logger.warning("Found record without unit number, skipping")
                            continue
                            
                        if unit_number.text in seen_units:
                            logger.warning(f"Duplicate unit number found in XML: {unit_number.text}")
                            continue
                            
                        seen_units.add(unit_number.text)
                        
                        valores = [campo.text for campo in registro]
                        colunas = [campo.tag for campo in registro]
                        
                        if not valores or not colunas:
                            logger.warning("Empty record found, skipping")
                            continue
                            
                        if len(valores) != len(colunas):
                            logger.warning(f"Mismatched columns and values for unit {unit_number.text}")
                            continue

                        placeholders = ', '.join(['?' for _ in valores])
                        
                        cursor.execute(f'''
                            INSERT INTO cri ({', '.join(colunas)})
                            VALUES ({placeholders})
                        ''', valores)
                        
                        logger.info(f"Inserted: Unit {unit_number.text}")
            
            conn.commit()
            
        except sqlite3.Error as e:
            raise DatabaseError(f"Error inserting data into database: {e}")
        except Exception as e:
            raise MemorialError(f"Error processing XML data: {e}")


class MemorialGenerator:
    def __init__(self, db_path: Path, output_dir: Path):
        self.db_path = db_path
        self.output_dir = output_dir
        self.description_generators = {
            UnitType.APARTMENT: ApartmentDescriptionGenerator(),
            UnitType.PARKING: ParkingDescriptionGenerator(),
            UnitType.STORE: StoreDescriptionGenerator()
        }
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_memorial(self) -> None:
        """Generate complete memorial description with improved error handling"""
        try:
            with database_connection(self.db_path) as conn:
                # Add the LOJA check here
                self.check_loja_entries(conn)
                
                units_data = self._fetch_unit_data(conn)
                if not units_data:
                    raise DatabaseError("No unit data found in database")

                descriptions = self._generate_descriptions(units_data)
                markdown_content = self._generate_markdown_content(descriptions, units_data[0])
                
                memorial_path = self.output_dir / 'memorial.md'
                memorial_path.write_text(markdown_content, encoding='utf-8')
                logger.info(f"Memorial description saved to: {memorial_path}")
                
        except Exception as e:
            raise MemorialError(f"Error generating memorial: {e}")

    def check_loja_entries(self, conn: sqlite3.Connection) -> None:
        """Check LOJA entries in database"""
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT unidade_numero, especie_unidade, subcondominio, pavimento 
                FROM cri 
                WHERE especie_unidade = 'LOJA'
                ORDER BY unidade_numero
            """)
            lojas = cursor.fetchall()
            
            logger.info(f"Found {len(lojas)} LOJA entries in database:")
            for loja in lojas:
                logger.info(f"LOJA {loja[0]} - Subcondominio: {loja[2]} - Pavimento: {loja[3]}")
                
        except sqlite3.Error as e:
            logger.error(f"Error checking LOJA entries: {e}")

    def _fetch_unit_data(self, conn: sqlite3.Connection) -> List[Dict[str, Any]]:
        """Fetch unit data with improved error handling and duplicate checking"""
        try:
            cursor = conn.cursor()
            
            # First, let's check for duplicates in the database
            cursor.execute("""
                SELECT unidade_numero, COUNT(*) as count 
                FROM cri 
                GROUP BY unidade_numero 
                HAVING count > 1
            """)
            
            duplicates = cursor.fetchall()
            if duplicates:
                for unit, count in duplicates:
                    logger.warning(f"Found {count} duplicates for unit {unit}")

            # Fetch all units
            cursor.execute("SELECT * FROM cri")
            units = [dict(row) for row in cursor.fetchall()]
            
            # Log each unit being fetched
            unit_numbers = [unit['unidade_numero'] for unit in units]
            logger.info(f"Fetched {len(units)} units: {', '.join(unit_numbers)}")

            # Sort units by number
            sorted_units = sorted(units, key=lambda x: int(''.join(filter(str.isdigit, x.get('unidade_numero', '0')))))
            return sorted_units
            
        except sqlite3.Error as e:
            raise DatabaseError(f"Error fetching unit data: {e}")

    def _generate_descriptions(self, units_data: List[Dict[str, Any]]) -> List[str]:
        """Generate descriptions for all units with added logging"""
        descriptions = []
        unit_counts = {'APARTAMENTO': 0, 'VAGA': 0, 'LOJA': 0}
        
        for unit_dict in units_data:
            try:
                # Log raw unit data
                logger.info(f"Processing unit: {unit_dict.get('especie_unidade')} - {unit_dict.get('unidade_numero')}")
                
                unit_data = UnitData.from_dict(unit_dict)
                unit_type = UnitType.from_str(unit_data.especie_unidade)
                
                # Count each type
                unit_counts[unit_data.especie_unidade] += 1
                
                generator = self.description_generators.get(unit_type)
                if generator is None:
                    logger.warning(f"Unknown unit type: {unit_data.especie_unidade}")
                    continue
                    
                description = generator.generate(unit_data)
                descriptions.append(description)
                logger.info(f"Generated description for {unit_data.especie_unidade} {unit_data.unidade_numero}")
                
            except Exception as e:
                logger.error(f"Error generating description for unit {unit_dict.get('unidade_numero')}: {e}")
                continue
        
        logger.info(f"Unit counts: {unit_counts}")
        logger.info(f"Total descriptions generated: {len(descriptions)}")
        return descriptions

    def _generate_markdown_content(self, descriptions: List[str], first_unit: Dict[str, Any]) -> str:
        """Generate complete markdown content with debug logging for galeria units"""
        # Group descriptions by subcondominium
        residencial = []
        galeria = []
        estacionamento = []
        
        # Log all descriptions before grouping
        logger.info(f"Total descriptions to process: {len(descriptions)}")
        
        for desc in descriptions:
            if desc.startswith("APARTAMENTO"):
                residencial.append(desc)
            elif desc.startswith("LOJA"):
                logger.info(f"Found LOJA description: {desc.split('\n')[0]}")
                galeria.append(desc)
            elif desc.startswith("VAGA"):
                estacionamento.append(desc)

        # Log counts after grouping
        logger.info(f"Grouped counts - Residencial: {len(residencial)}, Galeria: {len(galeria)}, Estacionamento: {len(estacionamento)}")

        # Sort the descriptions to ensure consistent ordering
        residencial.sort(key=lambda x: int(''.join(filter(str.isdigit, x.split(':')[0]))))
        galeria.sort(key=lambda x: int(''.join(filter(str.isdigit, x.split(':')[0]))))
        estacionamento.sort(key=lambda x: int(''.join(filter(str.isdigit, x.split(':')[0]))))

        # Read external files
        localizacao_residencial = self._read_external_file('./pre_cri/output/localizacao_apartamentos.txt')
        localizacao_estacionamento = self._read_external_file('./pre_cri/output/localizacao_vagas.txt')
        localizacao_galeria = self._read_external_file('./pre_cri/output/localizacao_lojas.txt')
        tipos_residencial = self._read_external_file('./pre_cri/output/tipos_apartamentos.txt')
        tipos_estacionamento = self._read_external_file('./pre_cri/output/tipos_vagas.txt')
        tipos_galeria = self._read_external_file('./pre_cri/output/tipos_lojas.txt')

        return f"""

# DADOS GERAIS
## Incorporador
{first_unit.get('incorporador', 'N/A')}

## Responsável técnico pela construção
{first_unit.get('responsavel_tecnico_construcao', 'N/A')}

## Responsável técnico pelo cálculo áreas NBR 12.721
{first_unit.get('responsavel_tecnico_nbr', 'N/A')}

## Matrícula
{first_unit.get('matricula', 'N/A')}

## Edifício
{first_unit.get('edificio', 'N/A')}

## Acesso ao edificio
{first_unit.get('acesso_edificio', 'N/A')}

# PARTES DE PROPRIEDADE EXCLUSIVA

São partes de propriedade exclusiva as seguintes unidades autônomas, agrupadas por subcondomínio.

## SUBCONDOMINIO RESIDENCIAL
{os.linesep + (os.linesep + os.linesep).join(residencial)}

## SUBCONDOMINIO GALERIA

{os.linesep + (os.linesep + os.linesep).join(galeria)}

## SUBCONDOMINIO ESTACIONAMENTO
{os.linesep + (os.linesep + os.linesep).join(estacionamento)}

# PARTES COMUNS
{first_unit.get('partes_comuns_base', 'N/A')}

## CONDOMINIO GERAL
{first_unit.get('partes_comuns_geral', 'N/A')}

## SUBCONDOMINIO RESIDENCIAL
{first_unit.get('partes_comuns_residencial', 'N/A')}

## SUBCONDOMINIO ESTACIONAMENTO
{first_unit.get('partes_comuns_estacionamento', 'N/A')}

## SUBCONDOMINIO RESIDENCIAL E ESTACIONAMENTO
{first_unit.get('partes_comuns_residencial_estacionamento', 'N/A')}

## SUBCONDOMINIO GALERIA
{first_unit.get('partes_comuns_galeria', 'N/A')}

# LOCALIZAÇÃO DAS UNIDADES AUTÔNMAS
## SUBCONDOMINIO RESIDENCIAL
{localizacao_residencial}

## SUBCONDOMINIO ESTACIONAMENTO
{localizacao_estacionamento}

## SUBCONDOMINIO GALERIA
{localizacao_galeria}

# TIPOLOGIA DAS UNIDADES AUTÔNMAS
## SUBCONDOMINIO RESIDENCIAL
{tipos_residencial}

## SUBCONDOMINIO ESTACIONAMENTO
{tipos_estacionamento}

## SUBCONDOMINIO GALERIA
{tipos_galeria}

******** Fim do documento ************
"""

    @staticmethod
    def _read_external_file(file_path: str) -> str:
        try:
            absolute_path = Path(file_path).absolute()
            logger.info(f"Reading file from: {absolute_path}")
            content = Path(file_path).read_text(encoding='utf-8').strip()
            logger.info(f"Content read from {file_path}:\n{content[:200]}...")  # Show more of the content
            return "\n".join(line.lstrip() for line in content.splitlines())
        except FileNotFoundError:
            logger.warning(f"File not found: {file_path}")
            return "File not found."
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return f"Error reading file: {e}"



def main() -> None:
    """Main function with improved error handling and logging"""
    try:
        # Configuration
        xml_path = Path('./pre_cri/base_real.xml')
        db_path = Path('./pre_cri/base_real_cri.db')
        output_dir = Path('./pre_cri/output')
        
        if not xml_path.exists():
            raise FileError(f"XML file not found: {xml_path}")

        # Convert XML to database
        converter = XMLDatabaseConverter(xml_path, db_path)
        converter.convert_xml_to_db()
        
        # Generate memorial
        generator = MemorialGenerator(db_path, output_dir)
        generator.generate_memorial()
        
        logger.info("Memorial generation completed successfully")
        
    except MemorialError as e:
        logger.error(f"Memorial generation failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()