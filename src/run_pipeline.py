from clean_crashes import clean_crashes
from clean_persons import clean_persons
from merge_datasets import merge_datasets

if __name__ == "__main__":
    print("🚀 Starting Data Engineering Pipeline...\n")
    clean_crashes()
    clean_persons()
    merge_datasets()
    print("\n🎉 Pipeline complete! All datasets saved successfully.")
