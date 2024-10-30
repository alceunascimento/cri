import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging
from dataclasses import dataclass
from decimal import Decimal
from contextlib import ExitStack

    # Configure logging
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

@dataclass
class UnitData:
        """Data class to store unit information"""
        especie_unidade: str
        tipo_unidade: str
        unidade_numero: str
        area_privativa: Decimal
        area_comum: Decimal
        area_total_construida: Decimal
        fracao_ideal_solo_condominio: Decimal
        quota_terreno_condominio: Decimal
        fracao_ideal_unidade_subcondominio: Decimal
        vaga_vinculada_descoberta: str
        area_vinculada_outras: Decimal
        area_comum_descoberta: Decimal

        def __post_init__(self):
            """Convert None values to appropriate defaults"""
            self.especie_unidade = self.especie_unidade or ''
            self.tipo_unidade = self.tipo_unidade or ''
            self.unidade_numero = self.unidade_numero or ''
            self.vaga_vinculada_descoberta = self.vaga_vinculada_descoberta or '0'
            
            # Convert None to Decimal('0') for numeric fields
            decimal_fields = [
                'area_privativa', 'area_comum', 'area_total_construida',
                'fracao_ideal_solo_condominio', 'quota_terreno_condominio',
                'fracao_ideal_unidade_subcondominio', 'area_vinculada_outras',
                'area_comum_descoberta'
            ]
            
            for field in decimal_fields:
                value = getattr(self, field)
                if value is None:
                    setattr(self, field, Decimal('0'))
                elif not isinstance(value, Decimal):
                    setattr(self, field, Decimal(str(value)))

class UnitDescriptionGenerator:
        def __init__(self, db_path: str = './pre_cri/base_real.db', output_dir: str = './pre_cri/output'):
            self.db_path = Path(db_path)
            self.output_dir = Path(output_dir)
            self.conn: Optional[sqlite3.Connection] = None
            
            # Ensure output directory exists
            self.output_dir.mkdir(parents=True, exist_ok=True)

        def connect_database(self) -> None:
            """Establish database connection"""
            try:
                self.conn = sqlite3.connect(str(self.db_path))
                logging.info(f"Connected to database: {self.db_path}")
            except sqlite3.Error as e:
                logging.error(f"Database connection error: {e}")
                raise

        def fetch_unit_data(self) -> Dict[Tuple[str, str], List[UnitData]]:
            """Fetch and organize unit data from database"""
            try:
                cursor = self.conn.cursor()
                query = """
                SELECT especie_unidade, tipo_unidade, unidade_numero, area_privativa, 
                    area_comum, area_total_construida, fracao_ideal_solo_condominio, 
                    quota_terreno_condominio, fracao_ideal_unidade_subcondominio, 
                    vaga_vinculada_descoberta, area_vinculada_outras, area_comum_descoberta
                FROM cri
                WHERE especie_unidade IS NOT NULL
                ORDER BY especie_unidade, tipo_unidade;
                """
                cursor.execute(query)
                units = cursor.fetchall()
                
                # Log any rows with NULL especie_unidade for debugging
                cursor.execute("""
                SELECT unidade_numero, tipo_unidade 
                FROM cri 
                WHERE especie_unidade IS NULL;
                """)
                null_units = cursor.fetchall()
                if null_units:
                    logging.warning(f"Found {len(null_units)} units with NULL especie_unidade: {null_units}")
                
                # Organize data by unit type
                units_dict: Dict[Tuple[str, str], List[UnitData]] = {}
                for unit in units:
                    if any(x is None for x in unit[:2]):  # Check especie_unidade and tipo_unidade
                        continue
                        
                    unit_data = UnitData(*unit)
                    key = (unit_data.especie_unidade, unit_data.tipo_unidade)
                    if key not in units_dict:
                        units_dict[key] = []
                    units_dict[key].append(unit_data)
                    
                return units_dict
                
            except sqlite3.Error as e:
                logging.error(f"Error fetching unit data: {e}")
                raise

        @staticmethod
        def format_decimal(value: Decimal) -> str:
            """Format decimal values with 8 decimal places and comma separator"""
            return f"{float(value):.8f}".replace('.', ',')

        def generate_apartment_description(self, units: List[UnitData]) -> str:
            """Generate description for apartment units"""
            first_unit = units[0]
            unit_numbers = ', '.join(str(unit.unidade_numero) for unit in units)
            
            return f"""APARTAMENTO TIPO {first_unit.tipo_unidade}: {len(units)} unidades, 
                correspondentes aos apartamentos nº {unit_numbers}, 
                possuindo cada unidade as seguintes áreas construídas: 
                área total construída de {self.format_decimal(first_unit.area_total_construida)} metros quadrados,
                sendo a área privativa de {self.format_decimal(first_unit.area_privativa)} metros quadrados
                e a área comum de {self.format_decimal(first_unit.area_comum)} metros quadrados.
                Fração ideal nas partes comuns do subcondomínio: {self.format_decimal(first_unit.fracao_ideal_unidade_subcondominio)};
                Fração ideal de solo e partes comuns no condomínio: {self.format_decimal(first_unit.fracao_ideal_solo_condominio)};
                Quota de terreno: {self.format_decimal(first_unit.quota_terreno_condominio)} metros quadrados.
                Area comum descoberta: {self.format_decimal(first_unit.area_comum_descoberta)} metros quadrados."""

        def generate_parking_description(self, units: List[UnitData]) -> str:
            """Generate description for parking units"""
            first_unit = units[0]
            unit_numbers = ', '.join(str(unit.unidade_numero) for unit in units)
            
            base_text = f"""VAGA TIPO {first_unit.tipo_unidade}: {len(units)} unidades, 
                correspondentes às vagas nº {unit_numbers}, 
                possuindo cada unidade as seguintes áreas construídas: 
                área total construída de {self.format_decimal(first_unit.area_total_construida)} metros quadrados,
                sendo a área privativa de {self.format_decimal(first_unit.area_privativa)} metros quadrados 
                e a área comum de {self.format_decimal(first_unit.area_comum)} metros quadrados"""
            
            if first_unit.area_vinculada_outras != Decimal('0'):
                base_text += f", área de depósito vinculado {unit_numbers}, respectivamente, de {self.format_decimal(first_unit.area_vinculada_outras)} metros quadrados"
            
            base_text += f""".
                Fração ideal nas partes comuns do subcondomínio: {self.format_decimal(first_unit.fracao_ideal_unidade_subcondominio)};
                Fração ideal de solo e partes comuns no condomínio: {self.format_decimal(first_unit.fracao_ideal_solo_condominio)};
                Quota de terreno: {self.format_decimal(first_unit.quota_terreno_condominio)} metros quadrados."""
            
            return base_text

        def generate_store_description(self, units: List[UnitData]) -> str:
            """Generate description for store units"""
            first_unit = units[0]
            unit_numbers = ', '.join(str(unit.unidade_numero) for unit in units)
            
            return f"""LOJA TIPO {first_unit.tipo_unidade}: {len(units)} unidades, 
                correspondentes ao Comércio e Serviço Vicinal  nº {unit_numbers}, 
                possuindo cada unidade as seguintes áreas construídas: 
                área total construída de {self.format_decimal(first_unit.area_total_construida)} metros quadrados,
                sendo a área privativa de {self.format_decimal(first_unit.area_privativa)} metros quadrados
                e a área comum de {self.format_decimal(first_unit.area_comum)} metros quadrados.
                Fração ideal nas partes comuns do subcondomínio: {self.format_decimal(first_unit.fracao_ideal_unidade_subcondominio)};
                Fração ideal de solo e partes comuns no condomínio: {self.format_decimal(first_unit.fracao_ideal_solo_condominio)};
                Quota de terreno: {self.format_decimal(first_unit.quota_terreno_condominio)} metros quadrados."""

        def generate_descriptions(self) -> None:
            """Generate and save unit descriptions to files"""
            try:
                units_dict = self.fetch_unit_data()
                
                if not units_dict:
                    logging.error("No valid unit data found in database")
                    return
                
                # Process each unit type with separate file handlers
                with open(self.output_dir / 'tipos_apartamentos.txt', 'w', encoding='utf-8') as f_apartamento, \
                    open(self.output_dir / 'tipos_vagas.txt', 'w', encoding='utf-8') as f_vaga, \
                    open(self.output_dir / 'tipos_lojas.txt', 'w', encoding='utf-8') as f_loja:
                    
                    # Process each unit type
                    for (especie, tipo), units in units_dict.items():
                        try:
                            especie_lower = especie.lower() if especie else ''
                            
                            if not especie_lower:
                                logging.warning(f"Empty especie_unidade found for tipo: {tipo}")
                                continue
                            
                            if especie_lower == 'apartamento':
                                description = self.generate_apartment_description(units)
                                f_apartamento.write(description + '\n')
                            elif especie_lower == 'vaga':
                                description = self.generate_parking_description(units)
                                f_vaga.write(description + '\n')
                            elif especie_lower == 'loja':
                                description = self.generate_store_description(units)
                                f_loja.write(description + '\n')
                            else:
                                logging.warning(f"Unknown especie_unidade: {especie}")
                                
                        except Exception as e:
                            logging.error(f"Error processing unit type {especie} {tipo}: {e}")
                            continue
                            
                logging.info("Unit descriptions generated successfully")
                
            except Exception as e:
                logging.error(f"Error generating descriptions: {e}")
                raise

        def close(self) -> None:
            """Close database connection"""
            if self.conn:
                self.conn.close()
                logging.info("Database connection closed")

def main():
        generator = UnitDescriptionGenerator()
        try:
            generator.connect_database()
            generator.generate_descriptions()
        except Exception as e:
            logging.error(f"Application error: {e}")
            raise
        finally:
            generator.close()

if __name__ == "__main__":
        main()
