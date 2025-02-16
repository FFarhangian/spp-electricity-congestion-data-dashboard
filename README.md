# MegEnergySolution

This project is a Python-based dashboard solution for analyzing and visualizing historical congestion data in the SPP electricity market.

## Project Overview
The project involved four key phases:

### **Part 1 – Data Collection**
- **What we did:** Collected historical data from the SPP portal ([Binding Constraints](https://portal.spp.org/pages/da-binding-constraints) and [LMP by Location](https://portal.spp.org/pages/da-lmp-by-location)) using `DataCollection.py`.
- **Challenges:** Handling different data formats, missing RePrice data.
- **Solution:** Adjusted scripts to merge available CSV files consistently.

### **Part 2 – Database Creation**
- **What we did:** Created a local SQLite database with daily and monthly aggregated tables for BC and LMP data using `DatabaseSetup.py`.
- **Challenges:** Ensuring date consistency across tables.
- **Solution:** Unified date formats and used `Interval` for hourly data.

### **Part 3 – Path Congestion Dashboard**
- **What we did:** Built an interactive Dash dashboard (`Dashboard.py`) to visualize monthly and hourly congestion data.
- **Challenges:** Incorrect x-axis formatting and database query mismatches.
- **Solution:** Used `Interval` column for hourly plots and added interactive components.

### **Part 4 – Binding Constraints Dashboard (Optional)**
- **What we did:** Proposed a scalable design approach.
- **Challenges:** Handling large datasets.
- **Solution:** Suggested using cloud storage and indexing for scalability.

---

## How to Run the Project

### **Requirements**
- Python 3.10
- Packages (in `requirements.txt`):
  - dash==2.9.3
  - pandas==2.2.0
  - sqlite3
  - plotly==5.16.1

### **Steps to Run**
```bash
# Clone the repository
git clone https://github.com/FFarhangian/PathCongestionDashboard.git
cd PathCongestionDashboard

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\\Scripts\\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the project step by step using main.py
python main.py
```

### **Project Files**
- `DataCollection.py`: Data collection and merging
- `DatabaseSetup.py`: Database creation
- `Dashboard.py`: Dash application
- `main.py`: Sequentially runs all scripts for full project setup
- `requirements.txt`: Packages required
