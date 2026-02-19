import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python cdf_plot.py <path/to/tx.csv>")
    sys.exit(1)

csv_path = Path(sys.argv[1])

# Load CSV
df = pd.read_csv(csv_path)

# Compute inclusion time (seconds)
t = df["end_time"] - df["start_time"]

# Sort values
x = np.sort(t.values)

# Empirical CDF
y = np.arange(1, len(x) + 1) / len(x)

# Plot
plt.figure(figsize=(8, 5))
plt.plot(x, y, marker='o', linestyle='-')
plt.xlabel("Time to inclusion (seconds)")
plt.ylabel("CDF")
plt.title(f"CDF of Transaction Inclusion Time\n{csv_path.name}")
plt.grid(True)
plt.ylim(0, 1)
plt.show()
