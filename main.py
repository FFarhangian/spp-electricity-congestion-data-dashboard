import os
import subprocess

# Step 1: Data Collection
print("Running Data Collection...")
subprocess.run(["python", "DataCollection.py"])

# Step 2: Data Processing
print("Running Data Processing...")
subprocess.run(["python", "DataProcessing.py", "--input_dir", "./data/BC/2020", "--output_dir", "./Results", "--output_file", "DA_BC_HOURLY.CSV"])
subprocess.run(["python", "DataProcessing.py", "--input_dir", "./data/lmp/2020", "--output_dir", "./Results", "--output_file", "DA_LMP_HOURLY.CSV"])

# Step 3: Database Setup
print("Setting up Database...")
subprocess.run(["python", "DatabaseSetup.py"])

# Step 4: Run Dashboard
print("Starting Dashboard...")
subprocess.run(["gunicorn", "Dashboard:app.server", "--bind", "0.0.0.0:8080"])
