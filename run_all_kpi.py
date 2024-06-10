import subprocess
import os
import sys

# Dodajemy ścieżkę do katalogu z plikami Python do sys.path, aby można było zaimportować filenames.py
base_path = r"//europe-data2.europe.root.corp/Debica/Manufacturing/Parametry maszyn/06. Bazy danych - parametry/programy/kpi_colormacher"
sys.path.append(base_path)

# Importujemy plik filenames.py
import filenames

# Definiowanie listy plików do uruchomienia w odpowiedniej kolejności
scripts = [
    "kpi_prepare_data_frame.py",
    "kpi_data_frame_quantity_checked.py",
    "kpi_data_frame_accuracy_checked.py",
    "charts_quantity_checked_date_day.py",
    "charts_quantity_checked_date_week.py",
    "charts_accuracy_checked_date_day.py",
    "charts_accuracy_checked_date_week.py",
    "kpi_data_frame_%_corrected.py"
]

# Uruchamiamy każdy skrypt po kolei
for script in scripts:
    script_path = os.path.join(base_path, script)
    print(f"Running {script_path}...")
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    print(f"Finished running {script_path}\n")

print("All scripts have been run.")