import pandas as pd
import os

def clean_data(df):
    while True:
        print("\n--- Cleaning Options ---")
        print("1. Remove duplicate rows")
        print("2. Remove empty rows")
        print("3. Strip extra spaces from text")
        print("4. Fill empty cells with a value")
        print("5. Do all basic cleaning")
        print("6. Done with this file")

        choice = input("\nChoose an option (1-6): ").strip()

        if choice == "1":
            before = len(df)
            df = df.drop_duplicates()
            print(f"Removed {before - len(df)} duplicate rows.")

        elif choice == "2":
            before = len(df)
            df = df.dropna(how="all")
            print(f"Removed {before - len(df)} empty rows.")

        elif choice == "3":
            for col in df.select_dtypes(include="object").columns:
                df[col] = df[col].astype(str).str.strip()
            print("Stripped extra spaces from text columns.")

        elif choice == "4":
            fill_value = input("Enter value to fill empty cells with: ").strip()
            df = df.fillna(fill_value)
            print(f"Filled empty cells with '{fill_value}'.")

        elif choice == "5":
            before = len(df)
            df = df.drop_duplicates()
            df = df.dropna(how="all")
            for col in df.select_dtypes(include="object").columns:
                df[col] = df[col].astype(str).str.strip()
            print(f"Basic cleaning complete. Rows before: {before}, after: {len(df)}")

        elif choice == "6":
            break

        else:
            print("Invalid option.")

    return df


def main():
    print("=== CSV / Excel Cleaner ===")
    print("Type 'quit' to exit.\n")

    while True:
        filepath = input("Enter the full path to your CSV or Excel file (or 'quit'): ").strip()

        if filepath.lower() == "quit":
            print("Goodbye!")
            break

        # Remove quotes if the user pasted a path with them
        filepath = filepath.strip('"').strip("'")

        if not os.path.exists(filepath):
            print("File not found. Please check the path.\n")
            continue

        try:
            if filepath.lower().endswith(".csv"):
                df = pd.read_csv(filepath)
            elif filepath.lower().endswith((".xlsx", ".xls")):
                df = pd.read_excel(filepath)
            else:
                print("Please use a .csv or .xlsx file.\n")
                continue
        except Exception as e:
            print(f"Error reading file: {e}\n")
            continue

        print(f"\nLoaded file with {len(df)} rows and {len(df.columns)} columns.")
        print("Columns:", list(df.columns))

        df = clean_data(df)

        # Save cleaned file
        folder = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(folder, f"{name}_cleaned{ext}")

        if ext.lower() == ".csv":
            df.to_csv(output_path, index=False)
        else:
            df.to_excel(output_path, index=False)

        print(f"\nCleaned file saved as:\n{output_path}\n")


if __name__ == "__main__":
    main()
    