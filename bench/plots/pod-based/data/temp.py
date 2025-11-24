import pandas as pd
import os
import numpy as np

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
    Calculates Time to Inclusion (TTI) and groups transactions into time buckets.
    Saves the result to a CSV file named <source-csv-filename>_tti.csv.
    """
    print("\n--- 1. Analyzing Time to Inclusion (TTI) ---")
    
    # Calculate TTI (Time to Inclusion) in seconds
    df['tti'] = df['end_time'] - df['start_time']
    
    # Define TTI buckets (in seconds)
    # Buckets: 1-2s, 2-4s, 4-6s, 6-8s, >8s
    bins = [0, 2, 4, 6, 8, np.inf]
    labels = ['1-2s', '2-4s', '4-6s', '6-8s', '>8s']

    # Use pd.cut to assign transactions to buckets
    df['tti_bucket'] = pd.cut(df['tti'], bins=bins, labels=labels, right=False)
    
    # Group by the bucket and count the transactions
    tti_counts = df.groupby('tti_bucket', observed=True).size().reset_index(name='num_transactions')
    
    # Rename columns and add index
    tti_counts.columns = ['TTI_Bucket', 'Num_Transactions']
    tti_counts.insert(0, 'Row_Index', range(len(tti_counts)))
    
    # Save the result
    output_path = get_output_filepath(input_filepath, '_tti')
    tti_counts.to_csv(output_path, index=False)
    print(f"✅ TTI buckets saved to: {output_path}")


# --- Analysis Function 2: Pending Transactions Over Time ---

def analyze_pending_txs_over_time(df: pd.DataFrame, input_filepath: str, time_step: int = 2) -> None:
    """
    Calculates the number of pending transactions at regular time intervals.
    A transaction is pending if its 'end_time' is greater than the timestamp.
    Saves the result to a CSV file named <source-csv-filename>_pending_tx.csv.
    """
    print("\n--- 2. Analyzing Pending Transactions Over Time ---")

    # Determine the time range to analyze
    min_start_time = df['start_time'].min()
    max_end_time = df['end_time'].max()
    
    # Create time buckets based on the time_step (e.g., every 2 seconds)
    time_bins = np.arange(min_start_time, max_end_time + time_step, time_step)
    
    pending_data = []
    
    # Loop through each timestamp and count pending transactions
    for timestamp in time_bins:
        # A transaction is pending at 'timestamp' if its 'end_time' > 'timestamp'
        # The inclusion of a transaction implies it was pending until 'end_time'.
        num_pending = len(df[df['end_time'] > timestamp])
        
        pending_data.append({
            'timestamp': timestamp,
            'num_pending_transactions': num_pending
        })
        
    pending_df = pd.DataFrame(pending_data)
    
    # Add index and save
    pending_df.insert(0, 'Row_Index', range(len(pending_df)))

    output_path = get_output_filepath(input_filepath, '_pending_tx')
    pending_df.to_csv(output_path, index=False)
    print(f"✅ Pending transactions over time saved to: {output_path}")


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
    Groups individual transaction gas usage into a specified number of buckets.
    Saves the result to a CSV file named <source-csv-filename>_tx_gas_used.csv.
    """
    print("\n--- 4. Analyzing Transaction Gas Used Buckets ---")

    # Define gas buckets manually for better interpretation (in thousands)
    # Given the sample data, let's create a range that covers the observed values.
    # Min gas used is ~500k, Max is ~1250k.
    
    # Note: 'k' stands for thousand (1000)
    # The bins are inclusive on the lower bound and exclusive on the upper bound (right=False).
    bins = [500000, 650000, 800000, 950000, 1100000, 1300000] 
    labels = ['500k-650k', '650k-800k', '800k-950k', '950k-1100k', '1100k-1300k+']
    
    # Alternative: Use pd.cut with 'num_buckets' for automated equal-width binning
    # df['gas_bucket'] = pd.cut(df['gas_used'], bins=num_buckets)
    # labels = [str(interval) for interval in df['gas_bucket'].unique().categories] # Extract labels if using auto-binning

    # Use pd.cut to assign transactions to the manual buckets
    df['gas_bucket'] = pd.cut(df['gas_used'], bins=bins, labels=labels, right=False, include_lowest=True)
    
    # Group by the bucket and count the transactions
    gas_counts = df.groupby('gas_bucket', observed=True).size().reset_index(name='num_transactions')
    
    # Rename columns and add index
    gas_counts.columns = ['Gas_Bucket', 'Num_Transactions']
    gas_counts.insert(0, 'Row_Index', range(len(gas_counts)))

    # Save the result
    output_path = get_output_filepath(input_filepath, '_tx_gas_used')
    gas_counts.to_csv(output_path, index=False)
    print(f"✅ Gas used buckets saved to: {output_path}")


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

    # 2. Pending Transactions Over Time
    # Note: The raw times are large timestamps, the calculation uses differences.
    analyze_pending_txs_over_time(df.copy(), input_filepath, time_step=2)

    # 3. Gas Used Per Block
    analyze_gas_per_block(df.copy(), input_filepath)

    # 4. Transaction Gas Used Buckets
    analyze_tx_gas_used_buckets(df.copy(), input_filepath)
    
    print("\n\n--- All analysis tasks completed! ---")


if __name__ == '__main__':
    # --- Create a sample CSV file for demonstration ---
    # In a real scenario, replace 'sample_data.csv' with your actual benchmark file path.
    SAMPLE_DATA = """tx_hash,start_time,end_time,block_number,gas_used,kind,error
0x3d96031a572e8f173e1940ae4ce28d58a4364ceba990a95bff7136b3547786e0,1763930328,1763930331,8498,1083125,,
0xce06f2d3ae25d45788a7769f4e4de73183c892a10a1f5912795f6944f95ff8e3,1763930328,1763930331,8498,891213,,
0xcd2668f52dc68eb8c145641e61c48b39d93ae74a665d51be6240e3cd6345556e,1763930328,1763930331,8498,762184,,
0xe7b048b84ac8ee58510b0feb0658c21e134435851feaa4241f604d065e980b07,1763930328,1763930331,8498,870605,,
0x2c3da3d4efb87384a37b1957d3b109e78461a718f5a0bc495051071bbc996800,1763930329,1763930333,8499,638926,,
0xe0f6c063414f80ce411fada8e9b6fd69b1b6557e0faab8461209e24f7d8af590,1763930329,1763930333,8499,1122248,,
0x63df932007722ba2bb9a6835c0d0c7c47af0223bd12bd51c3efe0355805f1034,1763930329,1763930333,8499,983627,,
0xc7b13458117045a7c8ba3152019693411fb48a5969fdfd7c0dbd9250d791053e,1763930329,1763930333,8499,509321,,
0xa6ce38bff4a118d3b760dd1ebb2ba0a7d449e9b2b42b9585648364a8f6bcd8c7,1763930330,1763930333,8499,1250565,,
0x7c44517db65e52d0c39480a101edc88b024c4a4f945ea088f7e30dfcb2a3b2e4,1763930330,1763930333,8499,553113,,
0x959be7c29896538672c4ebb649c1c2ed00d3a51a7cccdee3b9bf642d6383e372,1763930330,1763930333,8499,593846,,
0x4708b7fc91802264e7be27192c541632240c13c018b34b03a823c7be2cf1764a,1763930330,1763930333,8499,543775,,
0xd64a9a8da9fc355a2190daa515c03cb358575041fb592274d56c7d0c48b79a33,1763930331,1763930335,8500,750016,,
0xcdc46623a1b2df91bf1953762c92e6f124ec18cdaae8b6cf7524c4a8664ff332,1763930331,1763930335,8500,1196791,,
0x64a9ef1ddf5ae638b72cf10440c7fde4fd27f2bba7e6a73f9d354d8d5a5bb3a1,1763930331,1763930335,8500,797028,,
0x22fd3c20c48a60656c8a8af33791c1018042d7dbb159a0fe948dce86b63dfbd1,1763930331,1763930335,8500,883002,,
0x74414e518bdc61bc4095cc8e12e996692c4ef1f335b5c9e24e728c3a162d96b7,1763930332,1763930335,8500,1094556,,
0xd6c47ef3c2231147af27fb7dd8b1d2dba005a08e832709c05c719b9d9e23e2b2,1763930332,1763930335,8500,1027741,,
0x5d5795dfe70ad891d0daa2a78aee0d9c0324e937c16075ff0b8ee0f37d0b1e71,1763930332,1763930335,8500,677405,,
0xba1fcdf9d4725aa3709e38d734429b99eb74407620c3ee15b8da9c02f57fc514,1763930333,1763930337,8501,520752,,
0xd4ff7587945fbc9edf27faa9703258fc6d049cf9e4a8e3e5eb0abf2615e5e2aa,1763930333,1763930337,8501,814577,,
0xd4ff7587945fbc9edf27faa9703258fc6d049cf9e4a8e3e5eb0abf2615e5e2aa,1763930333,1763930337,8501,814577,,
0x1111111111111111111111111111111111111111111111111111111111111111,1763930334,1763930342,8502,1500000,,
0x2222222222222222222222222222222222222222222222222222222222222222,1763930334,1763930342,8502,300000,,
"""

# The file path to use for demonstration
INPUT_FILE = 'stress/raw/nopbs_notee_stress.csv'

# Save the sample data to a file so the script can read it
with open(INPUT_FILE, 'w') as f:
    f.write(SAMPLE_DATA)

# Run the analysis on the sample file
main_analysis(INPUT_FILE)