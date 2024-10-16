import subprocess
import time 

tick = time.time()

# List of script files to be executed
scripts = [
    "./producao_minima/1_create_db_from_xlsx_unbundle.py",
    "./producao_minima/1_1_insert_neighbors_from_xlsx.py",
    "./producao_minima/2_create_xlsx_from_db_unbundle.py",
    "./producao_minima/3_create_xml_from_db.py",
    "./producao_minima/4_report_cri.py",
    "./producao_minima/5_create_memorial.py"
]

# Run each script sequentially
for script in scripts:
    try:
        print(f"Running {script}...")
        subprocess.run(["python", script], check=True)
        print(f"{script} executed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing {script}: {e}\n")


tack = time.time()
execution_time = tack - tick
print(f"Tempo total de execução: {execution_time:.2f} segundos.")