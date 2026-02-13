import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- Main Plotting Function ---

def plot_csv_data(csv_files, x_val_col, y_col):
    """
    Reads multiple CSVs, plots them as line graphs, shades the area under each,
    and displays the area's calculated value. 
    
    Args:
        csv_files (list): List of paths to the CSV files.
        x_val_col (str): The column name for the NUMERIC X-axis values (e.g., 'id').
        y_col (str): The column name for the Y-axis (Number of Transactions, e.g., 'nopbs_tee').
        
        The X-axis tick labels are derived from the 'buckets' column, which is 
        assumed to be the second column in the CSV.
    """
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))

    # Define a set of distinct colors for the plots and shading
    colors = plt.cm.Dark2.colors 
    
    # Variables to store the final tick positions and labels (taken from the last file)
    final_x_indices = None
    final_x_labels = None

    for i, file_path in enumerate(csv_files):
        try:
            df = pd.read_csv(file_path)
            
            # CRITICAL FIX: Convert all column names to lowercase to prevent KeyErrors
            df.columns = df.columns.str.lower()
            
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}. Skipping.")
            continue
        except Exception as e:
            print(f"Error reading {file_path}: {e}. Skipping.")
            continue

        label = os.path.basename(file_path).replace('.csv', '')
        color = colors[i % len(colors)]
        
        # 1. Data extraction and assignment based on user request:
        
        # X-indices: The numeric column for plotting positions (e.g., 'id')
        x_indices = pd.to_numeric(df[x_val_col], errors='coerce').values
        
        # X-labels: The string column for tick labels (assumed to be 'buckets')
        # We assume the user's structure ('id', 'buckets', 'nopbs_tee') is maintained.
        x_labels = df['buckets'].values
        
        # Y data remains the number of transactions
        y_data = pd.to_numeric(df[y_col], errors='coerce').values 
        
        # 2. Calculate the area under the curve using the x_indices
        area = np.trapezoid(y_data, x_indices)
        
        # 3. Plot the line using the numeric index
        ax.plot(x_indices, y_data, 
                label=label, 
                color=color, 
                linewidth=2.5)
        
        # 4. Shade the area under the line
        ax.fill_between(x_indices, y_data, color=color, alpha=0.2)
        
        # 5. Add text label for the area value
        # Position calculation is now based on the numeric x_indices
        text_x = np.mean(x_indices)
        text_y = np.mean(y_data) 
        
        ax.text(text_x, text_y, 
                f'Area: {area:.2f}', 
                color=color, 
                fontsize=10, 
                fontweight='bold', 
                ha='center', va='center',
                bbox=dict(facecolor='white', alpha=0.6, boxstyle='round,pad=0.5'))

        # Store the current indices and labels for the final tick setting
        final_x_indices = x_indices
        final_x_labels = x_labels


    # --- Set up the final plot aesthetics ---
    
    # 6. Set Ticks and Labels: Use the final numeric indices for positions and bucket strings for labels
    if final_x_indices is not None and final_x_labels is not None:
        ax.set_xticks(final_x_indices)
        ax.set_xticklabels(final_x_labels, rotation=45, ha='right')

    title = 'Transaction Volume Over Time Buckets'
    x_label = 'Time Buckets (Mapped from ID)'
    y_label = 'Number of Transactions'
    
    ax.set_title(title, fontsize=16)
    ax.set_xlabel(x_label, fontsize=14)
    ax.set_ylabel(y_label, fontsize=14)
    ax.legend(loc='upper left', fontsize=10, frameon=True, shadow=True)
    
    # Ensure Y axis starts at zero
    ax.set_ylim(bottom=0)
    ax.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # List of CSV files to process
    # REMINDER: Update these file names to match your actual data files!
    files_to_plot = ['nopbs-tti.csv', 'pbs-tti.csv']
    
    # Column names updated per user request:
    plot_csv_data(
        csv_files=files_to_plot,
        x_val_col='id',       # X-axis for plotting/calculation (the first column)
        y_col='num-txs'     # Y-axis for Number of Transactions
    )

