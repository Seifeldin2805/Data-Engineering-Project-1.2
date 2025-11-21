import pandas as pd

def clean_persons():
    print("🔹 Loading persons dataset...")
    df = pd.read_csv("data/raw/persons.csv", low_memory=False)

    # ------------------------------
    # 1. Standardize column names
    # ------------------------------
    df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")

    # ------------------------------
    # 2. Convert COLLISION_ID to numeric
    # ------------------------------
    df["COLLISION_ID"] = pd.to_numeric(df["COLLISION_ID"], errors="coerce")

    # Drop rows with no collision ID
    df = df.dropna(subset=["COLLISION_ID"])
    df["COLLISION_ID"] = df["COLLISION_ID"].astype(int)

    # ------------------------------
    # 3. Fix PERSON_AGE
    # ------------------------------
    df["PERSON_AGE"] = pd.to_numeric(df["PERSON_AGE"], errors="coerce")
    df["PERSON_AGE"] = df["PERSON_AGE"].fillna(df["PERSON_AGE"].median())

    # ------------------------------
    # 4. Clean PERSON_SEX
    # ------------------------------
    df["PERSON_SEX"] = df["PERSON_SEX"].replace({" ": "Unknown", "": "Unknown"})
    df["PERSON_SEX"] = df["PERSON_SEX"].fillna("Unknown")

    # ------------------------------
    # 5. Clean PERSON_INJURY
    # ------------------------------
    injury_mapping = {
        "Fatal Injury": "Killed",
        "Killed": "Killed",
        "Incapacitating Injury": "Injured",
        "Non-Incapacitating Injury": "Injured",
        "Possible Injury": "Injured",
        "Injured": "Injured",
        "Unspecified": "Unknown",
        "Unknown": "Unknown"
    }

    df["PERSON_INJURY"] = df["PERSON_INJURY"].map(injury_mapping).fillna("Unknown")

    # ------------------------------
    # 6. Remove duplicates
    # ------------------------------
    df = df.drop_duplicates()

    # ------------------------------
    # 7. Save cleaned dataset
    # ------------------------------
    df.to_csv("data/cleaned/cleaned_persons.csv", index=False)
    print("✅ Saved cleaned persons → data/cleaned/cleaned_persons.csv")
