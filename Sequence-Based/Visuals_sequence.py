import pandas as pd
import matplotlib.pyplot as plt

#Load both files
full_df = pd.read_csv("full_file.csv")#add filtered file
filtered_df = pd.read_csv("sequence_capture_tls.csv")#add unfiltered file

#Convert time to float and sort
full_df['Time'] = full_df['Time'].astype(float)
filtered_df['Time'] = filtered_df['Time'].astype(float)

#Sort by time
full_df.sort_values("Time", inplace=True)
filtered_df.sort_values("Time", inplace=True)

#Plotting
plt.figure(figsize=(12, 6))
plt.plot(full_df['Time'], full_df['Length'], label='All Packets', color='gray', linewidth=0.8)

#Highlight filtered sequence used for decoding
plt.plot(filtered_df['Time'], filtered_df['Length'], label='Filtered TLS Stego Sequence', color='blue', linewidth=2)

plt.xlabel("Time (s)")
plt.ylabel("Packet Size (Bytes)")
plt.title("Packet Size Over Time (Full vs. Filtered TLS Sequence)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
