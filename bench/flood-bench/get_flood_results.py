import json
import pandas as pd
import os

def process_flood_report(input_filepath='report.json', output_filepath='data.csv'):
    """
    Reads a flood report from a JSON file, extracts core metrics, 
    and saves them to a CSV file.
    """
    # 1. Check if the input file exists
    if not os.path.exists(input_filepath):
        print(f"Error: Input file not found at '{input_filepath}'")
        return

    # 2. Read the JSON data from the file
    print(f"Reading report from: {input_filepath}")
    with open(input_filepath, 'r') as f:
        try:
            json_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file: {e}")
            return

    # 3. Extract the results for the primary node (assuming one node per report)
    # The 'results' key contains a dictionary where the key is the node name.
    if not json_data.get('results'):
        print("Error: 'results' key not found in JSON data.")
        return

    node_name = list(json_data['results'].keys())[0]
    results = json_data['results'][node_name]

    # 4. Select and map the core metrics
    # Note: We are using the keys from the 'results' dictionary (e.g., 'min', 'mean')
    core_metrics = {
        'target_rate': results['target_rate'],
        'actual_rate': results['actual_rate'],
        'throughput': results['throughput'],
        'success': results['success'],
        'min_latency': results['min'],
        'mean_latency': results['mean'],
        'p50_latency': results['p50'],
        'p90_latency': results['p90'],
        'p95_latency': results['p95'],
        'p99_latency': results['p99'],
        'max_latency': results['max'],
        'requests': results['requests']
    }

    # 5. Create a Pandas DataFrame
    df = pd.DataFrame(core_metrics)

    # 6. Insert the node name for context
    df.insert(0, 'node', node_name)

    # 7. Save the DataFrame to a CSV file
    df.to_csv(output_filepath, index=False)
    print(f"✅ Metrics successfully extracted and saved to {output_filepath}")
    print("\n--- Preview ---")
    print(df.head())

if __name__ == '__main__':
    # You would typically execute this script and pass the file path
    # For demonstration, we'll use the hardcoded default file name
    process_flood_report()