#
# Peterson Yuhala
# This python script has been generated with Google Gemini.
# It reads the .data file which I create manually from contender HTML reports for each system benchmarked
# See example data files to understand their structure.
# For each benchmark in the .data file, a CSV file is created with corresponding columns for the x and y values
# This CSV file is what is used to get the plot with Gnuplot
# 
# Run this script as follows: python3 data_transform.py file.data
#


import re
import json
import pandas as pd
import sys
from typing import List, Tuple, Dict

def parse_data_file(filepath: str) -> Tuple[str, List[Dict]]:
    """
    Parses a single .data file and extracts the type name and a list of benchmark data dictionaries.
    """
    print(f"Starting to process file: {filepath}")
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}. Please ensure the path is correct.")
        sys.exit(1)

    # 1. Extract the Type Name (Header)
    type_match = re.search(r'^#type-name:\s*(\w+)', content, re.MULTILINE)
    # Default to the filename base if the header is missing
    type_name = type_match.group(1).strip() if type_match else filepath.split('.')[0]
    
    
    # 2. Define the Benchmark Regex Pattern (MODIFIED)
    # The key change is using (?:$|\[) to look ahead for either the END of the string
    # or the start of the next benchmark, making the last one always match.
    benchmark_pattern = re.compile(
        r'^\[(.*?)\]\s*\n'                                      # Capture benchmark name [1]
        r'const\s+(.*?)\s*=\s*(\[.*?\])\s*;?\s*\n'             # Capture x_var_name [2] and x_array [3]
        r'const\s+.*?\s*=\s*(\[.*?\])\s*;?\s*(?:\s*|#|$)',     # Capture y_array [4], allow trailing content/EOF
        re.MULTILINE | re.DOTALL
    )
    benchmarks_data = []
    
    # 3. Iterate through all matches
    for match in benchmark_pattern.finditer(content):
        bench_name = match.group(1).strip()
        x_var_name = match.group(2).strip()
        x_array_str = match.group(3).strip()
        y_array_str = match.group(4).strip()
        
        try:
            # Clean up and safely load the JS arrays as JSON
            x_array_str = x_array_str.replace("'", "\"").replace("\n", "").replace("\r", "")
            y_array_str = y_array_str.replace("'", "\"").replace("\n", "").replace("\r", "")
            
            x_values = json.loads(x_array_str)
            y_values = json.loads(y_array_str)
        except json.JSONDecodeError as e:
            print(f"Warning: JSON decoding error for benchmark '{bench_name}': {e}. Skipping.")
            continue
            
        if len(x_values) != len(y_values):
            print(f"Warning: Benchmark '{bench_name}' has mismatched X/Y lengths ({len(x_values)} vs {len(y_values)}). Skipping.")
            continue
        
        benchmarks_data.append({
            'name': bench_name,
            'x_var_name': x_var_name,
            'x_values': x_values,
            'y_values': y_values
        })

    return type_name, benchmarks_data

def export_benchmarks_to_csv(type_name: str, benchmarks_data: List[Dict]):
    """
    Converts each extracted benchmark into a DataFrame and exports it to CSV.
    """
    generated_files = []
    
    for bench in benchmarks_data:
        # Create DataFrame
        df_data = {}
        
        # 1st column: 'id' (sequential count)
        df_data['id'] = list(range(1, len(bench['x_values']) + 1))
        
        # 2nd column: X-axis values
        df_data[bench['x_var_name']] = bench['x_values']
        
        # 3rd column: Y-axis values (named after the file's type)
        df_data[type_name] = bench['y_values']

        df = pd.DataFrame(df_data)
        
        # Clean up benchmark name for filename
        safe_bench_name = re.sub(r'[^\w\-]', '_', bench['name'])
        output_filename = f"{safe_bench_name}.csv"
        
        df.to_csv(output_filename, index=False)
        generated_files.append(output_filename)

    print(f"\nProcessing complete. Generated {len(generated_files)} CSV file(s) for type '{type_name}':")
    for f in generated_files:
        print(f"-> {f}")


# ----------------------------------------------------------------------
# --- Main Execution Block: Reads argument from command line (sys.argv) ---
# ----------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python single_file_processor_cli.py <data_file_path>")
        sys.exit(1)

    # The first argument (index 1) after the script name (index 0) is the file path
    data_file_path = sys.argv[1]
    
    type_name, benchmarks = parse_data_file(data_file_path)
    
    if benchmarks:
        export_benchmarks_to_csv(type_name, benchmarks)
    else:
        print("No valid benchmarks were found to export.")