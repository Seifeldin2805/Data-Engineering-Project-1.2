import pandas as pd
import re

def clean_crashes():
    print("🔹 Loading crashes dataset...")
    df = pd.read_csv("data/raw/crashes.csv", low_memory=False)

    # ------------------------------
    # 1. Standardize column names
    # ------------------------------
    df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")

    # ------------------------------
    # 2. Parse CRASH_DATE correctly
    # ------------------------------
    df["CRASH_DATE"] = pd.to_datetime(df["CRASH_DATE"], errors="coerce")

    # ------------------------------
    # 3. Parse CRASH_TIME with flexible regex
    # ------------------------------
    def parse_time(t):
        if pd.isna(t):
            return None
        t = str(t).strip()

        # match formats like 1:3 , 14:5 , 03:45 , 9:07
        match = re.match(r"^(\d{1,2}):(\d{1,2})$", t)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                return f"{hour:02d}:{minute:02d}"
        return None

    df["CRASH_TIME"] = df["CRASH_TIME"].apply(parse_time)

    # ------------------------------
    # 4. Create datetime-based features
    # ------------------------------
    df["CRASH_DATETIME"] = pd.to_datetime(
        df["CRASH_DATE"].dt.strftime("%Y-%m-%d") + " " + df["CRASH_TIME"].fillna("00:00"),
        errors="coerce"
    )

    # Extract hour, weekday, month, year
    df["CRASH_HOUR"] = df["CRASH_DATETIME"].dt.hour
    df["CRASH_DAY"] = df["CRASH_DATETIME"].dt.day
    df["CRASH_WEEKDAY"] = df["CRASH_DATETIME"].dt.day_name()
    df["CRASH_MONTH"] = df["CRASH_DATETIME"].dt.month
    df["CRASH_YEAR"] = df["CRASH_DATETIME"].dt.year
    df["IS_WEEKEND"] = df["CRASH_DATETIME"].dt.weekday >= 5

    # ------------------------------
    # 5. Remove duplicates
    # ------------------------------
    df = df.drop_duplicates()

    # ------------------------------
    # 6. Fix geo coordinates
    # ------------------------------
    df["LATITUDE"] = pd.to_numeric(df["LATITUDE"], errors="coerce")
    df["LONGITUDE"] = pd.to_numeric(df["LONGITUDE"], errors="coerce")

    df = df[
        (df["LATITUDE"].between(40, 41)) &
        (df["LONGITUDE"].between(-75, -72))
    ]

    # ------------------------------
    # 7. Drop useless columns
    # ------------------------------
    drop_cols = [
        "VEHICLE_TYPE_CODE_3", "VEHICLE_TYPE_CODE_4", "VEHICLE_TYPE_CODE_5",
        "CONTRIBUTING_FACTOR_VEHICLE_3", "CONTRIBUTING_FACTOR_VEHICLE_4",
        "CONTRIBUTING_FACTOR_VEHICLE_5"
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # ------------------------------
    # 8. Handle missing values
    # ------------------------------
    df = df.dropna(subset=["COLLISION_ID", "CRASH_DATE"])
    df["CRASH_TIME"] = df["CRASH_TIME"].fillna("Unknown")
    df["CRASH_HOUR"] = df["CRASH_HOUR"].fillna(-1)
    df = df.fillna("Unknown")

    # ------------------------------
    # 9. Save cleaned dataset
    # ------------------------------
    df.to_csv("data/cleaned/cleaned_crashes.csv", index=False)
    print("✅ Saved cleaned crashes → data/cleaned/cleaned_crashes.csv")
