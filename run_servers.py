import os

ports = [5000, 5001, 5002]
for port in ports:
    os.system(f"start python app.py --port={port}")
