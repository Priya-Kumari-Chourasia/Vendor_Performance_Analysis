import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

chunk_size = 10000
folder_path = "../data/data"
engine = create_engine('sqlite:///inventory.db')

def ingest_db(df, table_name, engine):
    #this function will ingest the dataframe into database table
    df.to_sql(table_name, con = engine, if_exists = 'replace', index = False, chunksize = 10000)

def load_raw_data():
    """Load CSVs in chunks and ingest into the database"""
    start = time.time()

    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            table_name = file[:-4]

            logging.info(f"Starting ingestion for {file}")

            first = True
            for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                if first:
                    # Replace table for the first chunk (fresh start each run)
                    chunk.to_sql(table_name, con=engine, index=False, if_exists="replace")
                    first = False
                else:
                    # Append for subsequent chunks
                    chunk.to_sql(table_name, con=engine, index=False, if_exists="append")

                #logging.info(f"Chunk of {len(chunk)} rows ingested into {table_name}")

            logging.info(f"Finished ingestion for {file}")

    end = time.time()
    total_time = (end - start) / 60
    logging.info("---------------Ingestion Complete----------------")
    logging.info(f"Total Time Taken: {total_time:.2f} minutes")


if __name__ == '__main__':
    load_raw_data()
