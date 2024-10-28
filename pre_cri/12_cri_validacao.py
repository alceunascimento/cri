import sqlite3
import pandas as pd
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Tuple, Union, Optional

class RealEstateAnalyzer:
    def __init__(self, db_path: str):
        """Initialize the analyzer with database path."""
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
    
    def close(self):
        """Close the database connection."""
        self.conn.close()

    def get_total_area(self) -> float:
        """Get the total area from alvara table."""
        query = "SELECT area_remanescente FROM alvara LIMIT 1"
        result = self.cursor.execute(query).fetchone()
        if result and result[0] is not None:
            try:
                return float(result[0])
            except (ValueError, TypeError):
                return 0.0
        return 0.0

    def get_unit_quotas(self) -> pd.DataFrame:
        """Get all unit quotas from quadro_resumo."""
        query = """
        SELECT subcondominio, unidade_numero, unidade_tipo, quota_terreno, fracao_ideal_solo_condominio
        FROM quadro_resumo
        """
        df = pd.read_sql_query(query, self.conn)
        # Convert quota_terreno to float, replacing non-numeric values with NaN
        df['quota_terreno'] = pd.to_numeric(df['quota_terreno'], errors='coerce')
        df['fracao_ideal_solo_condominio'] = pd.to_numeric(df['fracao_ideal_solo_condominio'], errors='coerce')
        return df

    def validate_total_quotas(self) -> Tuple[bool, float, float]:
        """Validate if sum of quotas equals total area."""
        total_area = self.get_total_area()
        df = self.get_unit_quotas()
        sum_quotas = df['quota_terreno'].sum()
        
        # Ensure both values are float
        try:
            total_area = float(total_area)
            sum_quotas = float(sum_quotas)
        except (ValueError, TypeError):
            return False, 0.0, 0.0
            
        return (
            abs(total_area - sum_quotas) < 0.01,  # Using 0.01 tolerance
            total_area,
            sum_quotas
        )

    def validate_fractions(self) -> Tuple[bool, float]:
        """Validate if sum of fractions equals 1."""
        df = self.get_unit_quotas()
        sum_fractions = df['fracao_ideal_solo_condominio'].sum()
        
        try:
            sum_fractions = float(sum_fractions)
        except (ValueError, TypeError):
            return False, 0.0
            
        return (abs(1.0 - sum_fractions) < 0.0001, sum_fractions)

    def get_parking_info(self) -> Dict:
        """Get parking space information."""
        # Get total parking spaces from informacoes_preliminares
        query_total = """
        SELECT vagas_total FROM informacoes_preliminares LIMIT 1
        """
        result = self.cursor.execute(query_total).fetchone()
        total_spaces = int(result[0]) if result and result[0] is not None else 0

        # Get autonomous parking units from quadro_resumo
        query_units = """
        SELECT COUNT(*) FROM quadro_resumo 
        WHERE subcondominio = 'estacionamento'
        """
        result = self.cursor.execute(query_units).fetchone()
        autonomous_units = int(result[0]) if result and result[0] is not None else 0

        return {
            'total_spaces': total_spaces,
            'autonomous_units': autonomous_units
        }

    def get_area_comparisons(self) -> Dict:
        """Compare areas between different tables."""
        query = """
        SELECT 
            a.areas_computaveis_total as alvara_area,
            SUM(CAST(qr.area_total AS FLOAT)) as quadro_area
        FROM alvara a
        CROSS JOIN quadro_resumo qr
        GROUP BY a.areas_computaveis_total
        """
        try:
            result = self.cursor.execute(query).fetchone()
            if result and result[0] is not None and result[1] is not None:
                alvara_area = float(result[0])
                quadro_area = float(result[1])
                return {
                    'alvara_area': alvara_area,
                    'quadro_area': quadro_area,
                    'match': abs(alvara_area - quadro_area) < 0.01
                }
        except (ValueError, TypeError):
            pass
        
        return {
            'alvara_area': 0.0,
            'quadro_area': 0.0,
            'match': False
        }

    def check_duplicate_units(self) -> List[Dict]:
        """Check for duplicate unit numbers."""
        query = """
        SELECT unidade_numero, subcondominio, COUNT(*) as count
        FROM quadro_resumo
        GROUP BY unidade_numero, subcondominio
        HAVING count > 1
        """
        try:
            duplicates = self.cursor.execute(query).fetchall()
            return [{'unit': d[0], 'subcondominio': d[1], 'count': d[2]} for d in duplicates]
        except sqlite3.Error:
            return []

    def get_building_info(self) -> Dict:
        """Get building information from alvara and informacoes_preliminares."""
        query = """
        SELECT 
            a.qtde_pavimentos as alvara_pavimentos,
            a.qtde_blocos as alvara_blocos,
            i.numero_pavimentos as info_pavimentos
        FROM alvara a
        CROSS JOIN informacoes_preliminares i
        LIMIT 1
        """
        try:
            result = self.cursor.execute(query).fetchone()
            if result:
                return {
                    'alvara_pavimentos': result[0] if result[0] is not None else 0,
                    'alvara_blocos': result[1] if result[1] is not None else 0,
                    'info_pavimentos': result[2] if result[2] is not None else 0
                }
        except sqlite3.Error:
            pass
    
        return {
            'alvara_pavimentos': 0,
            'alvara_blocos': 0,
            'info_pavimentos': 0
        }

    def analyze_sequential_units(self) -> Dict:
        """Analyze if unit numbers are sequential within each subcondominio."""
        query = """
        SELECT subcondominio, unidade_numero 
        FROM quadro_resumo
        ORDER BY subcondominio, CAST(unidade_numero AS INTEGER)
        """
        try:
            df = pd.read_sql_query(query, self.conn)
            results = {}
        
            for subcondominio in df['subcondominio'].unique():
                units = df[df['subcondominio'] == subcondominio]['unidade_numero']
                # Filter out non-numeric values before converting
                unit_numbers = []
                for u in units:
                    try:
                        if u and str(u).strip():  # Check if value exists and is not empty
                            unit_numbers.append(int(str(u).strip()))
                    except (ValueError, TypeError):
                        continue
            
                if unit_numbers:
                    start = min(unit_numbers)
                    end = max(unit_numbers)
                    expected = set(range(start, end + 1))
                    actual = set(unit_numbers)
                    missing = sorted(expected - actual)
                
                    results[subcondominio] = {
                        'start': start,
                        'end': end,
                        'sequential': len(missing) == 0,
                        'missing': missing
                    }
        
            return results
        except (sqlite3.Error, pd.errors.DatabaseError):
            return {}
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive report answering all questions."""
        report = {}
        
        # A.1 & A.2: Area validations
        quota_valid, total_area, sum_quotas = self.validate_total_quotas()
        report['area_validation'] = {
            'total_area': total_area,
            'sum_quotas': sum_quotas,
            'match': quota_valid
        }
        
        # A.4: Parking regime
        parking_info = self.get_parking_info()
        report['parking'] = parking_info
        
        # Check for duplicate units
        duplicates = self.check_duplicate_units()
        report['duplicate_units'] = duplicates
        
        # Building information
        building_info = self.get_building_info()
        report['building_info'] = building_info
        
        # Sequential unit analysis
        sequential_analysis = self.analyze_sequential_units()
        report['sequential_units'] = sequential_analysis
        
        # Area comparisons
        area_comparisons = self.get_area_comparisons()
        report['area_comparisons'] = area_comparisons
        
        return report

def analyze_database(db_path: str) -> Dict:
    """Main function to analyze the database and generate report."""
    analyzer = RealEstateAnalyzer(db_path)
    try:
        report = analyzer.generate_report()
        return report
    finally:
        analyzer.close()

if __name__ == "__main__":
    db_path = "./pre_cri/base_real.db"  # Adjust path as needed
    try:
        results = analyze_database(db_path)
        
        # Print results in a formatted way
        print("\n=== Real Estate Development Analysis Report ===\n")
        
        print("Area Validation:")
        print(f"Total Area: {results['area_validation']['total_area']:.2f}m²")
        print(f"Sum of Quotas: {results['area_validation']['sum_quotas']:.2f}m²")
        print(f"Match: {'Yes' if results['area_validation']['match'] else 'No'}")
        
        print("\nParking Information:")
        print(f"Total Spaces: {results['parking']['total_spaces']}")
        print(f"Autonomous Units: {results['parking']['autonomous_units']}")
        
    
        print("\nDuplicate Units:")
        if not results['duplicate_units']:
            print("No duplicate units found")
        else:
            for dup in results['duplicate_units']:
                print(f"Unit {dup['unit']} in {dup['subcondominio']}: {dup['count']} occurrences")
    
        print("\nBuilding Information:")
        print(f"Floors (Alvará): {results['building_info']['alvara_pavimentos']}")
        print(f"Blocks (Alvará): {results['building_info']['alvara_blocos']}")
        print(f"Floors (Info): {results['building_info']['info_pavimentos']}")
    
        print("\nSequential Unit Analysis:")
        for subcondominio, info in results['sequential_units'].items():
            print(f"\n{subcondominio}:")
            print(f"Range: {info['start']} to {info['end']}")
            print(f"Sequential: {'Yes' if info['sequential'] else 'No'}")
            if info['missing']:
                print(f"Missing numbers: {info['missing']}")
    
        print("\nArea Comparisons:")
        print(f"Alvará Area: {results['area_comparisons']['alvara_area']:.2f}m²")
        print(f"Quadro Area: {results['area_comparisons']['quadro_area']:.2f}m²")
        print(f"Match: {'Yes' if results['area_comparisons']['match'] else 'No'}")
    
    except Exception as e:
        print(f"Error analyzing database: {str(e)}")