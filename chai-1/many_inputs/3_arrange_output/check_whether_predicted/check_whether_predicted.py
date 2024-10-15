import pandas as pd
import argparse
import os

def read_protein_ids(csv_file, output_folder):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)  # Assuming the file is tab-delimited
    #print(df.columns)

    # Check for the existence of prediction files and add a new column
    df['Chai-1 predicted'] = df['Protein ID'].apply(
        lambda protein_id: os.path.exists(os.path.join(output_folder, f"{protein_id}_pred.model_idx_0.cif"))
    )

    return df

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Check if prediction files exist for proteins in a CSV file.")
    parser.add_argument('--csv_file', type=str, required=True, help="Path to the input CSV file")
    parser.add_argument('--output_folder', type=str, required=True, help="Path to the output folder where prediction files are stored")

    # Parse the arguments
    args = parser.parse_args()

    # Read the protein IDs and check for the existence of prediction files
    df = read_protein_ids(args.csv_file, args.output_folder)

    # Print the DataFrame with the new column
    #print(df)

    # Optionally, save the updated DataFrame to a new CSV file
    df.to_csv("updated_protein_predictions.csv", index=False)
