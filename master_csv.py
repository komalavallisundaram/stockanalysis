import os
import yaml
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

DB_USER = "postgres"
DB_PASSWORD = "Mahivalli@24"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "stockhost"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
root_path = "data"   

if not os.path.exists(root_path):
    raise FileNotFoundError(f"The path '{root_path}' does not exist. Please paste the correct folder path.")

all_dataframes = []

for date_folder in os.listdir(root_path):
    date_path = os.path.join(root_path, date_folder)
    if os.path.isdir(date_path):  
        for file in os.listdir(date_path):
            if file.endswith(".yaml") or file.endswith(".yml"):
                file_path = os.path.join(date_path, file)
                with open(file_path, 'r') as f:
                    try:
                        content = yaml.safe_load(f)
                        df = pd.DataFrame(content)
                        
                        all_dataframes.append(df)
                    except Exception as e:
                        print(f"⚠️ Error reading {file_path}: {e}")
-
if all_dataframes:
    master_df = pd.concat(all_dataframes, ignore_index=True)

    master_df = master_df.drop_duplicates()
    master_df.to_csv("master_csv.csv", index=False)
    print(" Cleaned master CSV saved as master_csv.csv")
    print(" Master data stored in PostgreSQL table: master_csv")

    
