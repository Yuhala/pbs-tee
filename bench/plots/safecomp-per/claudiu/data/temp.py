import pandas as pd
import os
import numpy as np
import io 
import sys # Added for command line arguments

# --- Helper Function ---

def get_output_filepath(input_filepath: str, suffix: str, output_dir: str = './analysis_output') -> str:
    """Constructs the output file path based on the input filename and desired suffix."""
    # Get the base filename without extension
    base_filename = os.path.basename(input_filepath).split('.')[0]
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Construct the final path
    output_filename = f"{base_filename}{suffix}.csv"
    return os.path.join(output_dir, output_filename)


# --- Analysis Function 1: Time to Inclusion (TTI) Buckets ---

def analyze_tti_buckets(df: pd.DataFrame, input_filepath: str) -> None:
    """
    Calculates Time to Inclusion (TTI) and groups transactions into the requested time buckets:
    1-2s, 2-3s, 3-4s, 4-5s, and 5s+.
    Saves the result to a CSV file named <source-csv-filename>_tti.csv.
    """
    print("\n--- 1. Analyzing Time to Inclusion (TTI) ---")
    
    # Calculate TTI (Time to Inclusion) in seconds
    df['tti'] = df['end_time'] - df['start_time']
    
    # Define the NEW TTI buckets: [1, 2), [2, 3), [3, 4), [4, 5), [5, inf)
    bins = [1, 2, 3, 4, 5, np.inf]
    labels = ['1-2s', '2-3s', '3-4s', '4-5s', '5s+']

    # Use pd.cut to assign transactions to buckets
    df['tti_bucket'] = pd.cut(df['tti'], bins=bins, labels=labels, right=False, include_lowest=True)
    
    # --- LOGIC to include zero-count buckets ---
    # Use value_counts with dropna=False to count all categories, including those with 0 transactions.
    # sort_index() ensures the categorical order defined by pd.cut is maintained.
    tti_counts = df['tti_bucket'].value_counts(dropna=False).sort_index().reset_index(name='Num_Transactions')
    
    # Rename columns and add index
    tti_counts.columns = ['TTI_Bucket', 'Num_Transactions']
    tti_counts.insert(0, 'Row_Index', range(len(tti_counts)))
    
    # Save the result
    output_path = get_output_filepath(input_filepath, '_tti')
    tti_counts.to_csv(output_path, index=False)
    print(f"✅ TTI buckets saved to: {output_path} (includes zero counts)")


# --- Analysis Function 2: Pending Transactions Over Time (Updated to 1-second step) ---

def analyze_pending_txs_over_time(df: pd.DataFrame, input_filepath: str, time_step: int = 1) -> None:
    """
    Calculates the number of pending transactions at regular time intervals (defaulting to 1 second).
    A transaction is pending if it has arrived ('start_time' <= timestamp) 
    AND has not yet been included ('end_time' > timestamp).
    Saves the result to a CSV file named <source-csv-filename>_pending_tx.csv.
    """
    print(f"\n--- 2. Analyzing Pending Transactions Over Time ({time_step}-second steps) ---")

    # Determine the time range to analyze
    min_start_time = df['start_time'].min()
    max_end_time = df['end_time'].max()
    
    # Create time bins based on the 1-second time_step
    time_bins = np.arange(min_start_time, max_end_time + time_step, time_step)
    
    pending_data = []
    
    # Loop through each timestamp and count pending transactions
    for timestamp in time_bins:
        # --- CORRECTED LOGIC ---
        # A transaction is pending if:
        # 1. It has arrived: df['start_time'] <= timestamp
        # 2. It has not yet been confirmed: df['end_time'] > timestamp
        num_pending = len(df[(df['start_time'] <= timestamp) & (df['end_time'] > timestamp)])
        
        pending_data.append({
            'timestamp': timestamp,
            'num_pending_transactions': num_pending
        })
        
    pending_df = pd.DataFrame(pending_data)
    
    # Add index and save
    pending_df.insert(0, 'Row_Index', range(len(pending_df)))

    output_path = get_output_filepath(input_filepath, '_pending_tx')
    pending_df.to_csv(output_path, index=False)
    print(f"✅ Pending transactions over time saved to: {output_path} (Using accurate arrival/inclusion logic)")


# --- Analysis Function 3: Total Gas Used Per Block ---

def analyze_gas_per_block(df: pd.DataFrame, input_filepath: str) -> None:
    """
    Calculates the total gas used for each unique block number.
    Saves the result to a CSV file named <source-csv-filename>_gas_per_block.csv.
    """
    print("\n--- 3. Analyzing Gas Used Per Block ---")

    # Group by block_number and sum the gas_used for each group
    gas_per_block = df.groupby('block_number')['gas_used'].sum().reset_index()
    
    # Rename columns and add index
    gas_per_block.columns = ['Block_Number', 'Total_Gas_Used']
    gas_per_block.insert(0, 'Row_Index', range(len(gas_per_block)))

    # Save the result
    output_path = get_output_filepath(input_filepath, '_gas_per_block')
    gas_per_block.to_csv(output_path, index=False)
    print(f"✅ Total gas per block saved to: {output_path}")


# --- Analysis Function 4: Gas Used Buckets ---

def analyze_tx_gas_used_buckets(df: pd.DataFrame, input_filepath: str, num_buckets: int = 5) -> None:
    """
    Groups individual transaction gas usage into 5 manually defined buckets.
    Saves the result to a CSV file named <source-csv-filename>_tx_gas_used.csv.
    """
    print("\n--- 4. Analyzing Transaction Gas Used Buckets ---")

    # Define gas buckets manually (in thousands)
    # Changed the lowest bin from 300,000 to 0 to capture all transactions,
    # including those with low gas usage, thus eliminating the empty bucket.
    bins = [0, 500000, 650000, 850000, 1000000, 1300000, np.inf] 
    # Updated the label to reflect the new range start
    labels = ['0-500k', '500k-650k', '650k-850k', '850k-1000k', '1000k-1300k', '1300k+']
    
    # Use pd.cut to assign transactions to the manual buckets
    df['gas_bucket'] = pd.cut(df['gas_used'], bins=bins, labels=labels, right=False, include_lowest=True)
    
    # --- LOGIC to include zero-count buckets ---
    # Use value_counts with dropna=False to count all categories, including those with 0 transactions.
    # sort_index() ensures the categorical order defined by pd.cut is maintained.
    gas_counts = df['gas_bucket'].value_counts(dropna=False).sort_index().reset_index(name='Num_Transactions')
    
    # The empty/NaN bucket (index 6 in your output) should now be gone, 
    # with its transactions merged into the '0-500k' bucket.
    
    # Rename columns and add index
    gas_counts.columns = ['Gas_Bucket', 'Num_Transactions']
    gas_counts.insert(0, 'Row_Index', range(len(gas_counts)))

    # Save the result
    output_path = get_output_filepath(input_filepath, '_tx_gas_used')
    gas_counts.to_csv(output_path, index=False)
    print(f"✅ Gas used buckets saved to: {output_path} (includes zero counts, now starting from 0)")


# --- Main Execution Block ---

def main_analysis(input_filepath: str):
    """Loads the data and runs all four analysis functions."""
    try:
        # Load the CSV file. We only need the first 5 columns for analysis.
        df = pd.read_csv(
            input_filepath,
            usecols=['tx_hash', 'start_time', 'end_time', 'block_number', 'gas_used']
        )
    except FileNotFoundError:
        print(f"Error: The input file '{input_filepath}' was not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: The input file '{input_filepath}' is empty.")
        return
    
    print(f"Successfully loaded {len(df)} transactions from {input_filepath}.")

    # 1. TTI Buckets
    analyze_tti_buckets(df.copy(), input_filepath)

    # 2. Pending Transactions Over Time (Now using 1-second steps by default)
    analyze_pending_txs_over_time(df.copy(), input_filepath)

    # 3. Gas Used Per Block
    analyze_gas_per_block(df.copy(), input_filepath)

    # 4. Transaction Gas Used Buckets
    analyze_tx_gas_used_buckets(df.copy(), input_filepath)
    
    print("\n\n--- All analysis tasks completed! ---")


if __name__ == '__main__':
    # Check if an input file path was provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python data_analysis.py <path_to_input_csv_file>")
        sys.exit(1)
    
    # The input file path is the first argument after the script name
    input_file_path = sys.argv[1]
    main_analysis(input_file_path)