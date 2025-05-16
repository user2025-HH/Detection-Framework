import csv
import matplotlib.pyplot as plt
import numpy as np

#Define both CSV files manually
UNFILTERED_CSV = "full_file.csv" #add filtered file
FILTERED_CSV = "timing_capture_tls.csv" #add unfiltered file

#Settings
highlight_bins = [0.2, 1.0]  #Delays to highlight
tolerance = 0.05
bins = 30

def extract_time_deltas(csv_file):
    deltas = []
    prev_time = None

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                current_time = float(row["Time"])
                if prev_time is not None:
                    delta = current_time - prev_time
                    if delta > 0:
                        deltas.append(delta)
                prev_time = current_time
            except:
                continue
    return deltas

def plot_histogram(deltas, title, highlight_bins):
    counts, edges = np.histogram(deltas, bins=bins)
    bin_centers = 0.5 * (edges[:-1] + edges[1:])
    
    colors = []
    handles = {"gray": None, "blue": None}

    for center in bin_centers:
        if any(abs(center - ref) <= tolerance for ref in highlight_bins):
            colors.append("blue")
        else:
            colors.append("gray")

    for center, count, color in zip(bin_centers, counts, colors):
        bar = plt.bar(center, count, width=(edges[1] - edges[0]), color=color, edgecolor='black')
        if handles[color] is None:
            handles[color] = bar[0]

    plt.title(title)
    plt.xlabel("Time Delta (seconds)")
    plt.ylabel("Frequency")
    plt.yscale("log")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend([handles["gray"], handles["blue"]], ["All Traffic", "Top TLSv1.2 Delays"])

#Load and plot
unfiltered_deltas = extract_time_deltas(UNFILTERED_CSV)
filtered_deltas = extract_time_deltas(FILTERED_CSV)

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plot_histogram(unfiltered_deltas, "Unfiltered Capture", highlight_bins)

plt.subplot(1, 2, 2)
plot_histogram(filtered_deltas, "Filtered TLS Traffic", highlight_bins)

plt.tight_layout()
plt.show()