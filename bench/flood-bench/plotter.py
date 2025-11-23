import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Configuration Variables ---

# 1. ENTER THE PATH TO YOUR CSV FILE HERE.
# Example: 'bench_output/metrics.csv' or just 'flood_metrics_data.csv'
csv_filename = 'data.csv'

# 2. Define the column name for the X-axis (independent variable)
xaxis = 'target_rate'

# 3. Define the column name for the Y-axis (dependent variable/metric to analyze)
# Change this to 'mean_latency', 'p95_latency', 'throughput', etc.
yaxis = 'p90_latency'

# 4. Define the output image file name and format (e.g., .png, .jpg, .svg)
output_image_filename = 'flood_plot.png'


# --- Plotting Logic ---

def create_plot(file_path, x_col, y_col, output_file):
    """
    Reads data from a CSV file specified by file_path, 
    creates a DataFrame, and plots x_col vs y_col, saving the result 
    to the specified output_file.
    """
    try:
        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        print("Please ensure the file path in 'csv_filename' is correct.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return
    
    # Check if the required columns exist
    if x_col not in df.columns or y_col not in df.columns:
        print(f"Error: One or both columns ('{x_col}', '{y_col}') not found in the CSV file.")
        print(f"Available columns: {list(df.columns)}")
        return

    # Create the plot
    plt.figure(figsize=(10, 6))
    
    # Plotting x vs y
    plt.plot(df[x_col], df[y_col], marker='o', linestyle='-', color='indigo', linewidth=2)
    
    # Add titles and labels
    # Uses .replace("_", " ").title() for nice formatting (e.g., 'mean_latency' -> 'Mean Latency')
    plt.title(f'Performance: {y_col.replace("_", " ").title()} vs. {x_col.replace("_", " ").title()}', 
              fontsize=16, fontweight='bold')
    
    plt.xlabel(x_col.replace("_", " ").title(), fontsize=14)
    plt.ylabel(y_col.replace("_", " ").title(), fontsize=14)
    
    # Add a grid for better readability
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Set x-axis to log scale (common for rate benchmarks)
    if 'rate' in x_col:
        plt.xscale('log', base=2)
    
    # Add a legend
    plt.legend([f'{y_col} Data'], loc='best')

    # Save the plot to the specified file (e.g., PNG)
    plt.tight_layout()
    try:
        plt.savefig(output_file)
        print(f"✅ Plot successfully saved to {output_file}")
    except Exception as e:
        print(f"Error saving file to {output_file}: {e}")


# Run the plotting function with the defined variables
create_plot(csv_filename, xaxis, yaxis, output_image_filename)