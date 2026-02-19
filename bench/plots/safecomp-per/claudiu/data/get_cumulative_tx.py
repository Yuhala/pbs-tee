import pandas as pd
import argparse
import os

def compute_inclusion_cdf(input_path):
    # 1. Handle File Paths
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found.")
        return

    # Extract directory and filename without extension
    file_dir = os.path.dirname(input_path)
    base_name = os.path.basename(input_path)
    name_only, _ = os.path.splitext(base_name)
    
    # Construct output name: name_cumulative_tx.csv
    output_name = f"{name_only}_cumulative_tx.csv"
    output_path = os.path.join(file_dir, output_name)

    # 2. Load the data
    try:
        # We only need start_time to find T=0 and end_time for inclusion
        df = pd.read_csv(input_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    if df.empty:
        print("The CSV file is empty.")
        return

    # 3. Define the global T=0 (earliest start_time) and T_last
    t_zero = df['start_time'].min()
    t_last = df['end_time'].max()
    total_txs = len(df)

    # 4. Count inclusions per absolute timestamp
    inclusion_counts = df.groupby('end_time').size().reset_index(name='count')

    # 5. Create continuous timeline from T=0 to final inclusion (T_last)
    # This ensures we don't have gaps in our time series
    full_timeline = pd.DataFrame({'real_timestamp': range(t_zero, t_last + 1)})

    # 6. Merge counts into timeline and calculate cumulative percentage
    cdf_df = pd.merge(full_timeline, inclusion_counts, left_on='real_timestamp', right_on='end_time', how='left')
    cdf_df['count'] = cdf_df['count'].fillna(0)
    cdf_df['cumulative_count'] = cdf_df['count'].cumsum()
    cdf_df['percentage_included'] = (cdf_df['cumulative_count'] / total_txs) * 100

    # 7. Add the relative timestamp column (Column 1)
    cdf_df['relative_timestamp'] = cdf_df['real_timestamp'] - t_zero

    # 8. Organize Columns: [Relative, Real, Percentage]
    output = cdf_df[['relative_timestamp', 'real_timestamp', 'percentage_included']]
    
    # 9. Save and Print
    output.to_csv(output_path, index=False)
    
    print(f"Success!")
    print(f"Input:  {input_path}")
    print(f"Output: {output_path}")
    print("-" * 50)
    #print(output.to_string(index=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute CDF of transaction inclusion.")
    parser.add_argument("file", help="Path to the source CSV file")
    
    args = parser.parse_args()
    compute_inclusion_cdf(args.file)