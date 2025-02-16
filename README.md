# MegEnergySolution

This project is a Python-based dashboard solution for analyzing and visualizing historical congestion data in the SPP electricity market.

## Definitions
**Day-Ahead Market (DAM):** A market determining an LMP per node for each hour of the day, one day in advance.

**Hour Ending:** Identifying the 24 hours of the day by their end, e.g., HE2 from 1:01 to 2:00.

**Locational Marginal Price (LMP):** Price associated with 1 MW of electricity, composed of energy, congestion, and losses.

## Project Overview
The project involved four key phases:

### **Part 1 – Data Collection**
- Collected historical data from the SPP portal ([Binding Constraints](https://portal.spp.org/pages/da-binding-constraints) and [LMP by Location](https://portal.spp.org/pages/da-lmp-by-location)) using `DataCollection.py`.

### **Part 2 – Data Processing**
- Processed collected data to create `DA_BC_HOURLY.CSV` and `DA_LMP_HOURLY.CSV` using `DataProcessing.py`.

### **Part 3 – Database Creation**
- Created a local SQLite database with daily and monthly aggregated tables for BC and LMP data using `DatabaseSetup.py`.
  
### **Part 4 – Path Congestion Dashboard**
- Built an interactive Dash dashboard (`Dashboard.py`) to visualize monthly and hourly congestion data.

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
