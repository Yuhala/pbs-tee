import json
import pandas as pd
import os
from typing import List

# --- Configuration ---
# NOTE: Replace '/path/tofolder' with the actual root directory path 
# where your benchmark results (eth_call, eth_getBalance, etc.) are located.
ROOT_BENCHMARK_DIR = './bench-output/nopbs-native' 

# The folder where the final CSV files will be saved.
OUTPUT_CSV_DIR = './csv_output'

# The list of subfolders (RPC methods) to process, corresponding to your flood runs.
RPC_METHODS = [
    'eth_call',
    'eth_getBalance',
    'eth_getBlockByNumber',
    'eth_getCode',
    'eth_getStorageAt',
    'eth_getTransactionByHash',
    'eth_getTransactionCount',
    'eth_getTransactionReceipt',
]
# --- End Configuration ---


def process_flood_report(input_filepath: str, output_filepath: str, method_name: str) -> None:
    """
    Reads a flood report from a JSON file, extracts core metrics, 
    and saves them to a CSV file.
    
    Args:
        input_filepath: Full path to the 'report.json' file.
        output_filepath: Full path for the resulting CSV file.
        method_name: The name of the RPC method (e.g., 'eth_call').
    """
    # 1. Check if the input file exists
    if not os.path.exists(input_filepath):
        print(f" Skipping '{method_name}': Input file not found at '{input_filepath}'")
        return

    # 2. Read the JSON data from the file
    print(f"\nProcessing {method_name}... Reading report from: {input_filepath}")
    with open(input_filepath, 'r') as f:
        try:
            json_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file '{input_filepath}': {e}")
            return

    # 3. Extract the results for the primary node
    if not json_data.get('results'):
        print(f"Error: 'results' key not found in JSON data for {method_name}.")
        return

    # Assuming only one node was benchmarked (as in your shell script)
    node_name = list(json_data['results'].keys())[0]
    results = json_data['results'][node_name]

    # 4. Select and map the core metrics
    # We create a list of dictionaries, where each dictionary represents a single data row 
    # for a specific target rate from the flood output.
    
    # Check if target_rate exists and is iterable
    if not isinstance(results.get('target_rate'), List):
        print(f"Error: 'target_rate' not in expected list format for {method_name}.")
        return

    data = []
    for i in range(len(results['target_rate'])):
        data.append({
            'node': node_name,
            'rpc_method': method_name, # Add the RPC method as a metric
            'target_rate': results['target_rate'][i],
            'actual_rate': results['actual_rate'][i],
            'throughput': results['throughput'][i],
            'success_rate': results['success'][i],
            'min_latency': results['min'][i],
            'mean_latency': results['mean'][i],
            'p50_latency': results['p50'][i],
            'p90_latency': results['p90'][i],
            'p95_latency': results['p95'][i],
            'p99_latency': results['p99'][i],
            'max_latency': results['max'][i],
            'requests': results['requests'][i]
        })

    # 5. Create a Pandas DataFrame
    df = pd.DataFrame(data)

    # 6. Save the DataFrame to a CSV file
    df.to_csv(output_filepath, index=False)
    print(f"Metrics successfully extracted and saved to {output_filepath}")
    
    # Optional: Print a short preview
    # print(df[['rpc_method', 'target_rate', 'mean_latency', 'throughput']].head())


def main():
    """
    Main function to orchestrate the processing of all RPC benchmark subfolders.
    """
    print(f"Starting Flood Report Processing from root directory: {ROOT_BENCHMARK_DIR}")

    # 1. Ensure the output directory exists
    os.makedirs(OUTPUT_CSV_DIR, exist_ok=True)
    print(f"Output directory ensured: {OUTPUT_CSV_DIR}")

    # 2. Iterate through all defined RPC methods (subfolders)
    for method in RPC_METHODS:
        # Construct the path to the input JSON file
        # Flood saves the report as 'report.json' inside the output folder.
        input_filepath = os.path.join(ROOT_BENCHMARK_DIR, method, 'results.json')
        
        # Construct the path for the output CSV file
        output_filename = f"{method}.csv"
        output_filepath = os.path.join(OUTPUT_CSV_DIR, output_filename)
        
        # Process the file
        process_flood_report(input_filepath, output_filepath, method)

    print("\n\n--- All Processing Complete ---")
    print(f"All resulting CSV files are located in the '{OUTPUT_CSV_DIR}' directory.")


if __name__ == '__main__':
    # Call the main orchestration function
    main()