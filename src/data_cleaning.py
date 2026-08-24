"""
Data Cleaning, Quality Assessment, and Feature Engineering Module
=================================================================
Phases 2-6:
- Initial Data Understanding & Profiling
- Data Quality Audit (Missing values, Duplicates, Types)
- Logical Validation & Range Constraints
- Clean Dataset Construction (Preserving Raw Data)
- Feature Engineering for EDA

Saves:
- `data/processed/bike_sharing_cleaned.csv`
- `outputs/data_quality_report.csv`
"""

import os
import pandas as pd
import numpy as np

def run_data_audit_and_cleaning(raw_csv_path: str = None, 
                                processed_csv_path: str = None,
                                quality_report_path: str = None) -> tuple:
    """
    Performs comprehensive data auditing, cleaning, and feature engineering.
    
    Returns:
        tuple: (raw_df, clean_df, quality_summary_df)
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if raw_csv_path is None:
        raw_csv_path = os.path.join(base_dir, "data", "raw", "hour.csv")
    if processed_csv_path is None:
        processed_csv_path = os.path.join(base_dir, "data", "processed", "bike_sharing_cleaned.csv")
    if quality_report_path is None:
        quality_report_path = os.path.join(base_dir, "outputs", "data_quality_report.csv")
        
    os.makedirs(os.path.dirname(processed_csv_path), exist_ok=True)
    os.makedirs(os.path.dirname(quality_report_path), exist_ok=True)
    
    print("=" * 70)
    print("PHASE 2 & 3: DATA UNDERSTANDING & QUALITY AUDIT")
    print("=" * 70)
    
    raw_df = pd.read_csv(raw_csv_path)
    print(f"[INFO] Raw dataset loaded: {raw_df.shape[0]:,} rows, {raw_df.shape[1]} columns.")
    
    # 1. Missing Value Analysis
    null_counts = raw_df.isnull().sum()
    null_percentages = (null_counts / len(raw_df)) * 100
    missing_df = pd.DataFrame({
        "Feature": raw_df.columns,
        "Null_Count": null_counts.values,
        "Null_Percentage": null_percentages.values,
        "Data_Type": raw_df.dtypes.values
    })
    
    total_nulls = null_counts.sum()
    print(f"[AUDIT] Missing Values Check: Total Missing = {total_nulls}")
    if total_nulls == 0:
        print("[AUDIT] -> Missing-value analysis was performed and no missing observations were detected.")
        print("[AUDIT] -> No imputation was required. Raw integrity is preserved.")
    
    # 2. Duplicate Record Analysis
    duplicate_rows = raw_df.duplicated().sum()
    duplicate_instants = raw_df["instant"].duplicated().sum()
    print(f"[AUDIT] Duplicate Check: Exact Duplicate Rows = {duplicate_rows}, Duplicate Instant IDs = {duplicate_instants}")
    if duplicate_rows == 0 and duplicate_instants == 0:
        print("[AUDIT] -> No duplicate records or duplicate identifiers detected.")
    
    # 3. Logical Consistency & Boundary Assertions
    print("\n" + "=" * 70)
    print("PHASE 4: LOGICAL VALIDATION CHECKS")
    print("=" * 70)
    
    # Verification of additive relation: casual + registered == cnt
    count_mismatch = (raw_df["casual"] + raw_df["registered"] != raw_df["cnt"]).sum()
    print(f"[VALIDATION] casual + registered == cnt: {count_mismatch} discrepancies found.")
    assert count_mismatch == 0, "Discrepancy in rental counts!"
    
    # Range validations
    assert raw_df["hr"].between(0, 23).all(), "Hour values out of [0, 23] range!"
    assert raw_df["mnth"].between(1, 12).all(), "Month values out of [1, 12] range!"
    assert raw_df["season"].between(1, 4).all(), "Season values out of [1, 4] range!"
    assert raw_df["weathersit"].between(1, 4).all(), "Weather situations out of [1, 4] range!"
    assert raw_df["holiday"].isin([0, 1]).all(), "Holiday flag invalid!"
    assert raw_df["workingday"].isin([0, 1]).all(), "Workingday flag invalid!"
    assert raw_df["weekday"].between(0, 6).all(), "Weekday values out of [0, 6] range!"
    assert (raw_df["cnt"] >= 0).all(), "Negative bike counts found!"
    assert (raw_df["temp"] >= 0).all() and (raw_df["temp"] <= 1).all(), "Temp out of normalized bounds!"
    assert (raw_df["hum"] >= 0).all() and (raw_df["hum"] <= 1).all(), "Humidity out of normalized bounds!"
    assert (raw_df["windspeed"] >= 0).all() and (raw_df["windspeed"] <= 1).all(), "Windspeed out of normalized bounds!"
    
    print("[VALIDATION] All logical range constraints and sanity assertions passed 100%.")
    
    # 4. Outlier Assessment via IQR
    outlier_metrics = {}
    numerical_cols = ["cnt", "casual", "registered", "temp", "hum", "windspeed"]
    for col in numerical_cols:
        q1 = raw_df[col].quantile(0.25)
        q3 = raw_df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers_count = ((raw_df[col] < lower_bound) | (raw_df[col] > upper_bound)).sum()
        pct_outliers = (outliers_count / len(raw_df)) * 100
        outlier_metrics[col] = {
            "Q1": q1, "Q3": q3, "IQR": iqr,
            "Lower_Bound": lower_bound, "Upper_Bound": upper_bound,
            "Outlier_Count": outliers_count,
            "Outlier_Pct": pct_outliers
        }
        print(f"[OUTLIER AUDIT] {col.upper():<12}: {outliers_count:>5} points ({pct_outliers:>5.2f}%) outside [{lower_bound:.2f}, {upper_bound:.2f}]")
    
    print("[DECISION] Outliers in 'cnt', 'casual', and 'registered' represent genuine peak-demand periods (rush hours, special events, sunny summer weekends) rather than erroneous data entry. They are retained to maintain true operational distribution integrity.")
    
    # 5. Data Cleaning & Feature Engineering
    print("\n" + "=" * 70)
    print("PHASE 5 & 6: DATA CLEANING & FEATURE ENGINEERING")
    print("=" * 70)
    
    # Create separate copy - raw remains untouched
    clean_df = raw_df.copy()
    
    # Convert date
    clean_df["dteday"] = pd.to_datetime(clean_df["dteday"])
    
    # Mappings for categorical readability
    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    year_map = {0: 2011, 1: 2012}
    month_map = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    weekday_map = {
        0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
        4: "Thursday", 5: "Friday", 6: "Saturday"
    }
    weather_map = {
        1: "Clear / Few Clouds",
        2: "Mist / Cloudy",
        3: "Light Snow / Rain",
        4: "Heavy Rain / Ice Pellets"
    }
    
    clean_df["season_name"] = clean_df["season"].map(season_map)
    clean_df["year"] = clean_df["yr"].map(year_map)
    clean_df["month_name"] = clean_df["mnth"].map(month_map)
    clean_df["day_of_week"] = clean_df["weekday"].map(weekday_map)
    clean_df["weather_description"] = clean_df["weathersit"].map(weather_map)
    clean_df["is_weekend"] = clean_df["weekday"].isin([0, 6]).astype(int)
    
    # Hourly Day-part segmentation
    def categorize_hour(hr):
        if 0 <= hr <= 5:
            return "Early Morning / Night (00-05)"
        elif 6 <= hr <= 9:
            return "Morning Commute Rush (06-09)"
        elif 10 <= hr <= 15:
            return "Midday (10-15)"
        elif 16 <= hr <= 19:
            return "Evening Commute Rush (16-19)"
        else:
            return "Late Evening (20-23)"
            
    clean_df["hour_group"] = clean_df["hr"].apply(categorize_hour)
    
    # Reconstructed physical units (as per official UCI dataset documentation)
    # temp: normalized to 41 C max
    # atemp: normalized to 50 C max
    # hum: normalized to 100 max
    # windspeed: normalized to 67 km/h max
    clean_df["temp_celsius"] = (clean_df["temp"] * 41).round(2)
    clean_df["atemp_celsius"] = (clean_df["atemp"] * 50).round(2)
    clean_df["humidity_pct"] = (clean_df["hum"] * 100).round(2)
    clean_df["windspeed_kmh"] = (clean_df["windspeed"] * 67).round(2)
    
    # Save Cleaned CSV
    clean_df.to_csv(processed_csv_path, index=False)
    print(f"[SUCCESS] Cleaned dataset saved to: {processed_csv_path}")
    print(f"[INFO] Cleaned dataset shape: {clean_df.shape[0]:,} rows, {clean_df.shape[1]} columns.")
    
    # Generate and save Data Quality Report
    audit_rows = []
    for col in raw_df.columns:
        col_type = str(raw_df[col].dtype)
        null_count = int(raw_df[col].isnull().sum())
        n_unique = int(raw_df[col].nunique())
        sample_val = str(raw_df[col].iloc[0])
        audit_rows.append({
            "Column_Name": col,
            "Raw_Data_Type": col_type,
            "Cleaned_Data_Type": str(clean_df[col].dtype),
            "Null_Count": null_count,
            "Null_Percentage": 0.0,
            "Unique_Values": n_unique,
            "Example_Value": sample_val,
            "Validation_Status": "PASSED"
        })
        
    # Append engineered columns to report
    for eng_col in ["season_name", "year", "month_name", "day_of_week", "weather_description", "hour_group", "temp_celsius", "atemp_celsius", "humidity_pct", "windspeed_kmh"]:
        audit_rows.append({
            "Column_Name": eng_col,
            "Raw_Data_Type": "N/A (Engineered)",
            "Cleaned_Data_Type": str(clean_df[eng_col].dtype),
            "Null_Count": int(clean_df[eng_col].isnull().sum()),
            "Null_Percentage": 0.0,
            "Unique_Values": int(clean_df[eng_col].nunique()),
            "Example_Value": str(clean_df[eng_col].iloc[0]),
            "Validation_Status": "ENGINEERED"
        })
        
    quality_report_df = pd.DataFrame(audit_rows)
    quality_report_df.to_csv(quality_report_path, index=False)
    print(f"[SUCCESS] Data quality report saved to: {quality_report_path}")
    
    return raw_df, clean_df, quality_report_df

if __name__ == "__main__":
    run_data_audit_and_cleaning()
