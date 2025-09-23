import sqlite3
import pandas as pd
import logging
import os
import time
from ingestion_db import ingest_db  # your existing ingestion function

# -------------------------------
# 1️⃣ Setup dedicated logger
# -------------------------------
os.makedirs("logs", exist_ok=True)

vendor_logger = logging.getLogger("vendor_summary")
vendor_logger.setLevel(logging.DEBUG)
vendor_logger.propagate = False

# File handler
fh = logging.FileHandler("logs/get_vendor_summary.log")
fh.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)

vendor_logger.addHandler(fh)

# -------------------------------
# 2️⃣ Functions
# -------------------------------

def create_vendor_summary(conn):
    """Merge tables to get overall vendor summary"""
    query = """
    WITH FreightSummary AS (
        SELECT VendorNumber, SUM(Freight) AS FreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
    ),
    PurchaseSummary AS (
        SELECT
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price AS ActualPrice,
            pp.Volume,
            SUM(p.Quantity) AS TotalPurchaseQuantity,
            SUM(p.Dollars) AS TotalPurchaseDollars
        FROM purchases p
        JOIN purchase_prices pp ON p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
    ),
    SalesSummary AS (
        SELECT
            VendorNo,
            Brand,
            SUM(SalesQuantity) AS TotalSalesQuantity,
            SUM(SalesDollars) AS TotalSalesDollars,
            SUM(SalesPrice) AS TotalSalesPrice,
            SUM(ExciseTax) AS TotalExciseTax
        FROM sales
        GROUP BY VendorNo, Brand
    )
    SELECT
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.FreightCost
    FROM PurchaseSummary ps
    LEFT JOIN SalesSummary ss ON ps.VendorNumber = ss.VendorNo AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummary fs ON ps.VendorNumber = fs.VendorNumber
    ORDER BY ps.TotalPurchaseDollars DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def clean_data(df):
    """Clean and enrich the vendor summary DataFrame"""
    df['Volume'] = df['Volume'].astype(float)
    df.fillna(0, inplace=True)
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()
    
    # New columns
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (df['GrossProfit'] / df['TotalSalesDollars']) * 100
    df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
    df['SalestoPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars']
    
    return df

# -------------------------------
# 3️⃣ Main execution
# -------------------------------
if __name__ == '__main__':
    start_time = time.time()
    
    # Connect to database
    conn = sqlite3.connect('inventory.db')
    
    vendor_logger.info("Creating vendor summary table...")
    summary_df = create_vendor_summary(conn)
    vendor_logger.info(f"Preview:\n{summary_df.head()}")
    
    vendor_logger.info("Cleaning vendor summary data...")
    clean_df = clean_data(summary_df)
    vendor_logger.info(f"Preview after cleaning:\n{clean_df.head()}")
    
    vendor_logger.info("Ingesting cleaned data into DB...")
    ingest_db(clean_df, 'vendor_sales_summary', conn)
    vendor_logger.info("Ingestion completed successfully.")
    
    end_time = time.time()
    vendor_logger.info(f"Total execution time: {(end_time - start_time):.2f} seconds")
    
    # Close DB connection
    conn.close()

    
    
    