import pandas as pd

def merge_datasets():
    print("🔹 Loading cleaned datasets...")

    df_crashes = pd.read_csv("data/cleaned/cleaned_crashes.csv", low_memory=False)
    df_persons = pd.read_csv("data/cleaned/cleaned_persons.csv", low_memory=False)

    # Ensure COLLISION_ID numeric
    df_crashes["COLLISION_ID"] = pd.to_numeric(df_crashes["COLLISION_ID"], errors="coerce").astype(int)
    df_persons["COLLISION_ID"] = pd.to_numeric(df_persons["COLLISION_ID"], errors="coerce").astype(int)

    # ------------------------------
    # 1. AGGREGATE PERSONS TABLE
    # ------------------------------
    persons_agg = df_persons.groupby("COLLISION_ID").agg(
        TOTAL_PERSONS=("PERSON_ID", "count"),
        TOTAL_INJURED=("PERSON_INJURY", lambda x: (x == "Injured").sum()),
        TOTAL_KILLED=("PERSON_INJURY", lambda x: (x == "Killed").sum()),
        AVG_PERSON_AGE=("PERSON_AGE", "mean"),
        FEMALE_PERSONS=("PERSON_SEX", lambda x: (x == "F").sum()),
        MALE_PERSONS=("PERSON_SEX", lambda x: (x == "M").sum()),
        UNKNOWN_SEX=("PERSON_SEX", lambda x: (x == "Unknown").sum())
    ).reset_index()

    # ------------------------------
    # 2. MERGE INTO CRASHES (LEFT JOIN)
    # ------------------------------
    df_merged = df_crashes.merge(persons_agg, on="COLLISION_ID", how="left")

    # ------------------------------
    # 3. POST-INTEGRATION CLEANING
    # ------------------------------
    fill_zero_cols = [
        "TOTAL_PERSONS", "TOTAL_INJURED", "TOTAL_KILLED",
        "FEMALE_PERSONS", "MALE_PERSONS", "UNKNOWN_SEX"
    ]

    for col in fill_zero_cols:
        df_merged[col] = df_merged[col].fillna(0).astype(int)

    # AVG_PERSON_AGE: fill missing with crash median
    df_merged["AVG_PERSON_AGE"] = df_merged["AVG_PERSON_AGE"].fillna(
        df_merged["AVG_PERSON_AGE"].median()
    )

    # ------------------------------
    # 4. SAVE FINAL MERGED DATASET
    # ------------------------------
    df_merged.to_csv("data/final/df_merged_clean.csv", index=False)
    print("✅ Saved FINAL dataset → data/final/df_merged_clean.csv")
