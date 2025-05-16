import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

#Load the CSV file
df = pd.read_csv("")#add file

#Count packet sizes
all_sizes = df["Length"].astype(int)
all_counts = Counter(all_sizes)

#Filter only TLSv1.2 packets
tls_df = df[df["Protocol"] == "TLSv1.2"]
tls_sizes = tls_df["Length"].astype(int)
tls_counts = Counter(tls_sizes)

#Find top 2 most common TLSv1.2 packet sizes
top_tls_sizes = [size for size, _ in tls_counts.most_common(2)]

#X-axis range
x_range = list(range(0, 150))
frequencies_all = [all_counts.get(x, 0) for x in x_range]

#Plot all traffic
plt.figure(figsize=(14, 6))
plt.bar(x_range, frequencies_all, color='lightgray', edgecolor='black', label='All Traffic')

#Overlay TLSv1.2 top sizes in full blue (not stacked)
for size in top_tls_sizes:
    if size in x_range:
        plt.bar(size, all_counts.get(size, 0), color='blue', edgecolor='blue', label='Top TLSv1.2 Sizes')

#Avoid duplicates
handles, labels = plt.gca().get_legend_handles_labels()
unique_labels = dict(zip(labels, handles))
plt.legend(unique_labels.values(), unique_labels.keys())

plt.title("TLSv1.2 Packet Size Distribution with Highlighted Clusters")
plt.xlabel("Packet Size (Bytes)")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()
plt.show()
