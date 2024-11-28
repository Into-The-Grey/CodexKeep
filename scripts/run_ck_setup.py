# CodexKeep/run_ck_setup.py

import subprocess

scripts = [
    "CodexKeep/scripts/env_setup.py",
    "CodexKeep/scripts/data_fetching.py",
    "CodexKeep/scripts/data_processing.py",
    "CodexKeep/scripts/batch_processing.py",
    "CodexKeep/scripts/validation.py",
]

for script in scripts:
    print(f"[INFO] Running {script}...")
    result = subprocess.run(["python3", script], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        print(f"[ERROR] {script} failed with error: {result.stderr}")
        break
    else:
        print(f"[INFO] {script} completed successfully.")
