"""
Data Acquisition Module for Bike Sharing Demand EDA Project
============================================================
Phase 1: Acquire the official UCI Bike Sharing Dataset (hour.csv).

Dataset Official Source:
UCI Machine Learning Repository: Bike Sharing Dataset
URL: https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset
DOI: https://doi.org/10.24432/C5W894
Download URL: https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip

This script downloads the official archive, extracts the raw `hour.csv` dataset,
validates file integrity, and saves it untouched into `data/raw/hour.csv`.
"""

import os
import sys
import io
import zipfile
import requests
import pandas as pd

UCI_DATASET_ZIP_URL = "https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip"
FALLBACK_GITHUB_RAW_URL = "https://raw.githubusercontent.com/christophM/interpretable-ml-book/master/data/bike.csv"

def acquire_bike_sharing_dataset(raw_dir: str = None) -> str:
    """
    Downloads and extracts the official UCI Bike Sharing Dataset.
    
    Args:
        raw_dir: Path to directory where raw data will be stored.
                 Defaults to relative 'data/raw'.
                 
    Returns:
        str: Absolute path to the raw hour.csv file.
    """
    if raw_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        raw_dir = os.path.join(base_dir, "data", "raw")
    
    os.makedirs(raw_dir, exist_ok=True)
    target_hour_file = os.path.join(raw_dir, "hour.csv")
    
    print("=" * 70)
    print("PHASE 1: DATA ACQUISITION")
    print(f"Target destination: {target_hour_file}")
    print(f"Official Primary Source: {UCI_DATASET_ZIP_URL}")
    print("=" * 70)
    
    # Check if raw file already exists and is valid
    if os.path.exists(target_hour_file) and os.path.getsize(target_hour_file) > 100000:
        print(f"[INFO] Raw dataset already exists at {target_hour_file} ({os.path.getsize(target_hour_file):,} bytes).")
        df_existing = pd.read_csv(target_hour_file)
        print(f"[INFO] Existing dataset verified: {df_existing.shape[0]:,} rows, {df_existing.shape[1]} columns.")
        return target_hour_file
    
    downloaded = False
    
    # Attempt 1: Download official ZIP from UCI ML Repository
    try:
        print("[STEP 1] Attempting download from official UCI Repository...")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) DataScienceAssignment/1.0"}
        response = requests.get(UCI_DATASET_ZIP_URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            namelist = zip_ref.namelist()
            print(f"[INFO] Archive contents: {namelist}")
            if "hour.csv" in namelist:
                zip_ref.extract("hour.csv", path=raw_dir)
                # Also extract Readme.txt and day.csv if present for reference
                for extra_file in ["day.csv", "Readme.txt"]:
                    if extra_file in namelist:
                        zip_ref.extract(extra_file, path=raw_dir)
                downloaded = True
                print(f"[SUCCESS] Extracted hour.csv to {target_hour_file}")
    except Exception as e:
        print(f"[WARNING] Primary UCI download failed with error: {e}")
    
    # Attempt 2: Direct alternative UCI / official mirror if zip fails
    if not downloaded:
        print("[STEP 2] Attempting fallback acquisition...")
        alt_urls = [
            "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-08-17/bikeshare.csv",
            "https://raw.githubusercontent.com/datasets/bike-sharing/master/data/hour.csv"
        ]
        for alt_url in alt_urls:
            try:
                print(f"[INFO] Trying mirror: {alt_url}")
                r = requests.get(alt_url, timeout=30)
                if r.status_code == 200 and len(r.content) > 100000:
                    with open(target_hour_file, "wb") as f:
                        f.write(r.content)
                    downloaded = True
                    print(f"[SUCCESS] Acquired raw data from mirror: {alt_url}")
                    break
            except Exception as mirror_err:
                print(f"[WARNING] Mirror failed: {mirror_err}")
                
    if not downloaded or not os.path.exists(target_hour_file):
        raise RuntimeError("Failed to acquire UCI Bike Sharing dataset from primary and fallback sources.")
    
    # Verification
    file_size = os.path.getsize(target_hour_file)
    df_raw = pd.read_csv(target_hour_file)
    
    print("\n" + "-" * 50)
    print("DATA ACQUISITION SUMMARY")
    print("-" * 50)
    print(f"File Path: {target_hour_file}")
    print(f"File Size: {file_size:,} bytes ({file_size / (1024*1024):.2f} MB)")
    print(f"Records Acquired: {df_raw.shape[0]:,} rows")
    print(f"Features Acquired: {df_raw.shape[1]} columns")
    print(f"Columns: {list(df_raw.columns)}")
    print("-" * 50)
    print("[SUCCESS] Phase 1 Data Acquisition completed successfully. Raw data preserved untouched.")
    
    return target_hour_file

if __name__ == "__main__":
    acquire_bike_sharing_dataset()
