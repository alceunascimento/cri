import sqlite3
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
import logging
from dataclasses import dataclass


import logging
import sqlite3
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Set
from dataclasses import dataclass
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def extract_numbers(s):
    """Extract numbers from a string for sorting."""
    nums = re.findall(r'\d+', s)
    return [int(n) for n in nums] if nums else [float('inf')]

@dataclass
class UnitSummary:
    """Class to store unit summary information"""
    total_count: int
    locations: Dict[str, List[str]]
    first_floor: Optional[str] = None
    last_floor: Optional[str] = None

class BuildingUnitLocations:
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

    def execute_query(self, query: str, params: tuple = ()) -> List[Tuple]:
        """Execute SQL query and return results"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Query execution error: {e}\nQuery: {query}")
            raise

    @staticmethod
    def extract_floor_number(floor_str: str) -> int:
        """Extract numerical floor number from string"""
        match = re.match(r"(\d+)", floor_str)
        return int(match.group(1)) if match else float('inf')

    @staticmethod
    def format_unit_numbers(units: List[str]) -> str:
        """Format unit numbers with proper separators"""
        if not units:
            return ""
        if len(units) == 1:
            return str(units[0])
        return ', '.join(map(str, units[:-1])) + f' e {units[-1]}'

    def get_parking_data(self) -> Tuple[UnitSummary, int]:
        """Fetch and process parking data"""
        total_spaces_result = self.execute_query("""
            SELECT vagas_total FROM informacoes_preliminares LIMIT 1
        """)
        total_spaces = total_spaces_result[0][0] if total_spaces_result else 0

        parking_data = self.execute_query("""
            SELECT pavimento, unidade_numero, tipo_vaga
            FROM cri
            WHERE especie_unidade = 'VAGA'
            ORDER BY pavimento, unidade_numero
        """)

        locations: Dict[str, Dict[str, List[str]]] = {}
        for floor, unit, park_type in parking_data:
            if floor not in locations:
                locations[floor] = {'simples': [], 'dupla': []}
            locations[floor][park_type].append(unit)

        return (
            UnitSummary(
                total_count=len(parking_data),
                locations=locations
            ),
            total_spaces
        )

    def get_apartment_data(self) -> UnitSummary:
        """Fetch and process apartment data"""
        apartment_data = self.execute_query("""
            SELECT pavimento, unidade_numero
            FROM cri
            WHERE especie_unidade = 'APARTAMENTO'
            ORDER BY pavimento, unidade_numero
        """)

        locations: Dict[str, List[str]] = {}
        floors: Set[str] = set()

        for floor, unit in apartment_data:
            if floor not in locations:
                locations[floor] = []
            locations[floor].append(unit)
            floors.add(floor)

        sorted_floors = sorted(floors, key=self.extract_floor_number)

        return UnitSummary(
            total_count=len(apartment_data),
            locations=locations,
            first_floor=sorted_floors[0] if sorted_floors else None,
            last_floor=sorted_floors[-1] if sorted_floors else None
        )

    def get_store_data(self) -> UnitSummary:
        """Fetch and process store data"""
        store_data = self.execute_query("""
            SELECT pavimento, unidade_numero
            FROM cri
            WHERE especie_unidade = 'LOJA'
            ORDER BY pavimento, unidade_numero
        """)

        locations: Dict[str, List[str]] = {}
        for floor, unit in store_data:
            if floor not in locations:
                locations[floor] = []
            locations[floor].append(unit)

        return UnitSummary(
            total_count=len(store_data),
            locations=locations
        )

    def get_kitinete_data(self) -> UnitSummary:
        """Fetch and process kitinete data"""
        kitinete_data = self.execute_query("""
            SELECT pavimento, unidade_numero
            FROM cri
            WHERE especie_unidade = 'KITINETE'
            ORDER BY pavimento, unidade_numero
        """)

        locations: Dict[str, List[str]] = {}
        floors: Set[str] = set()

        for floor, unit in kitinete_data:
            if floor not in locations:
                locations[floor] = []
            locations[floor].append(unit)
            floors.add(floor)

        sorted_floors = sorted(floors, key=self.extract_floor_number)

        return UnitSummary(
            total_count=len(kitinete_data),
            locations=locations,
            first_floor=sorted_floors[0] if sorted_floors else None,
            last_floor=sorted_floors[-1] if sorted_floors else None
        )

    def generate_parking_text(self, summary: UnitSummary, total_spaces: int) -> str:
        """Generate formatted text for parking spaces"""
        simple_count = sum(len(floor_data['simples']) for floor_data in summary.locations.values())
        double_count = sum(len(floor_data['dupla']) for floor_data in summary.locations.values())

        text = (f"As vagas localizam-se nos {', '.join(summary.locations.keys())}, "
                f"num total de {summary.total_count} unidades autônomas, "
                f"comportando {total_spaces} veículos sendo {simple_count} "
                f"vagas simples e {double_count} vagas duplas.\n")

        for floor in sorted(summary.locations.keys()):
            floor_data = summary.locations[floor]
            simple_units = sorted(floor_data['simples'], key=extract_numbers)
            double_units = sorted(floor_data['dupla'], key=extract_numbers)
            simple = self.format_unit_numbers(simple_units)
            double = self.format_unit_numbers(double_units)

            text += f"\nNo {floor} serão {len(floor_data['simples']) + len(floor_data['dupla'])} "
            text += f"vagas autônomas de nº {simple} (vagas simples)"
            if double_units:
                text += f" e {double} (vagas duplas)"
            text += "."

        return text

    def generate_apartment_text(self, summary: UnitSummary) -> str:
        """Generate formatted text for apartments"""
        text = (f"Os apartamentos estão localizados do {summary.first_floor} ao {summary.last_floor}, "
                f"num total de {summary.total_count} unidades autônomas, sendo:\n")

        for floor in sorted(summary.locations.keys(), key=self.extract_floor_number):
            units = self.format_unit_numbers(sorted(summary.locations[floor], key=extract_numbers))
            text += f"{floor}: apartamentos nº {units};\n"

        return text

    def generate_store_text(self, summary: UnitSummary) -> str:
        """Generate formatted text for stores"""
        floors = list(summary.locations.keys())

        if not floors:
            return "Não há lojas disponíveis."

        first_floor_text = floors[0]
        units_first_floor = sorted(summary.locations[first_floor_text], key=extract_numbers)
        units_on_the_first_floor = ", ".join(units_first_floor)

        if len(floors) > 1:
            second_floor_text = floors[1]
            units_second_floor = sorted(summary.locations[second_floor_text], key=extract_numbers)
            units_on_the_second_floor = ", ".join(units_second_floor)
            text = (f"As lojas, num total de {summary.total_count} "
                    f"unidades autônomas, são as Lojas nº {units_on_the_first_floor}, {units_on_the_second_floor}. "
                    f"Destas, as Lojas nº {units_on_the_first_floor} estão no {first_floor_text} e as "
                    f"Lojas nº {units_on_the_second_floor} estão no {second_floor_text}.")
        else:
            text = (f"As lojas, num total de {summary.total_count} "
                    f"unidades autônomas, são as Lojas nº {units_on_the_first_floor} "
                    f"no {first_floor_text}.")

        return text

    def generate_kitinete_text(self, summary: UnitSummary) -> str:
        """Generate formatted text for kitinetes"""
        text = (f"As kitinetes estão localizadas do {summary.first_floor} ao {summary.last_floor}, "
                f"num total de {summary.total_count} unidades autônomas, sendo:\n")

        for floor in sorted(summary.locations.keys(), key=self.extract_floor_number):
            units = self.format_unit_numbers(sorted(summary.locations[floor], key=extract_numbers))
            text += f"{floor}: kitinetes nº {units};\n"

        return text

    def generate_all_texts(self) -> None:
        """Generate and save all unit location texts"""
        try:
            # Get data
            parking_summary, total_spaces = self.get_parking_data()
            apartment_summary = self.get_apartment_data()
            store_summary = self.get_store_data()
            kitinete_summary = self.get_kitinete_data()

            # Generate texts
            parking_text = self.generate_parking_text(parking_summary, total_spaces)
            apartment_text = self.generate_apartment_text(apartment_summary)
            store_text = self.generate_store_text(store_summary)
            kitinete_text = self.generate_kitinete_text(kitinete_summary)

            # Save texts
            text_files = {
                'localizacao_vagas.txt': parking_text,
                'localizacao_apartamentos.txt': apartment_text,
                'localizacao_lojas.txt': store_text,
                'localizacao_kitinetes.txt': kitinete_text
            }

            for filename, content in text_files.items():
                filepath = self.output_dir / filename
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                logging.info(f"Generated {filename}")

            # Print texts (optional)
            print(parking_text)
            print(apartment_text)
            print(store_text)
            print(kitinete_text)

        except Exception as e:
            logging.error(f"Error generating texts: {e}")
            raise

    def close(self) -> None:
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logging.info("Database connection closed")


def main():
    # Specify the correct path to the database and output folder
    generator = BuildingUnitLocations(
        db_path='./pre_cri/base_real.db',
        output_dir='./pre_cri/output'
    )

    try:
        generator.connect_database()
        generator.generate_all_texts()
    except Exception as e:
        logging.error(f"Application error: {e}")
        raise
    finally:
        generator.close()

if __name__ == "__main__":
    main()
