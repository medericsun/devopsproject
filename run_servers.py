import os

# Start multiple Flask servers with different ports
ports = [5000, 5001, 5002]  # List of ports to run Flask instances
for port in ports:
    os.system(f"start python app.py --port={port}")
