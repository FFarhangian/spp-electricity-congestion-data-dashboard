import os
import pandas as pd
import sqlite3

def create_and_populate_db(csv_files, db_name="energy_data.db"):
    conn = sqlite3.connect(db_name)
    for csv in csv_files:
        table_name = os.path.splitext(os.path.basename(csv))[0]
        df = pd.read_csv(csv)
        if 'Interval' in df.columns:
            df['DATE'] = pd.to_datetime(df['Interval']).dt.strftime('%Y-%m-%d')
            df['MONTH'] = pd.to_datetime(df['Interval']).dt.strftime('%Y-%m-01')
        df.to_sql(table_name, conn, if_exists='replace', index=False)

    queries = {
        "DA_BC_DAILY": "CREATE TABLE IF NOT EXISTS DA_BC_DAILY AS SELECT DATE, [Constraint Name], SUM([Shadow Price]) as [Shadow Price] FROM DA_BC_HOURLY GROUP BY DATE, [Constraint Name];",
        "DA_LMP_DAILY": "CREATE TABLE IF NOT EXISTS DA_LMP_DAILY AS SELECT DATE, [Settlement Location], SUM(LMP) as LMP, SUM(MLC) as MLC, SUM(MCC) as MCC, SUM(MEC) as MEC FROM DA_LMP_HOURLY GROUP BY DATE, [Settlement Location];",
        "DA_BC_MONTHLY": "CREATE TABLE IF NOT EXISTS DA_BC_MONTHLY AS SELECT MONTH, [Constraint Name], SUM([Shadow Price]) as [Shadow Price] FROM DA_BC_HOURLY GROUP BY MONTH, [Constraint Name];",
        "DA_LMP_MONTHLY": "CREATE TABLE IF NOT EXISTS DA_LMP_MONTHLY AS SELECT MONTH, [Settlement Location], SUM(LMP) as LMP, SUM(MLC) as MLC, SUM(MCC) as MCC, SUM(MEC) as MEC FROM DA_LMP_HOURLY GROUP BY MONTH, [Settlement Location];"
    }

    for name, query in queries.items():
        try:
            conn.execute(query)
        except Exception as e:
            print(f"Error creating table {name}: {e}")

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in database:")
    for table in tables:
        print(table[0])

    conn.close()

if __name__ == "__main__":
    csv_files = ["./Results/DA_BC_HOURLY.CSV", "./Results/DA_LMP_HOURLY.CSV"]
    create_and_populate_db(csv_files)




