import csv
from collections import Counter

CSV_FILE = "" #add traffic file in csv

def load_packets(csv_file):
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def get_frame_sizes(packets):
    sizes = []
    for p in packets:
        try:
            length_val = int(p["Length"])
            
            if length_val > 100:  
                sizes.append(length_val)
        except:
            pass
    return sizes

def find_two_clusters_frequency(sizes):
    #Count how often each size occurs
    freq_map = Counter(sizes)
    #Get the two most common sizes
    top_two = freq_map.most_common(2)
    if len(top_two) < 2:
        return None, None
    #The size with the smaller numeric value => cluster S
    #The bigger => cluster L
    sizeA, _ = top_two[0]
    sizeB, _ = top_two[1]
    cluster_small = min(sizeA, sizeB)
    cluster_large = max(sizeA, sizeB)
    return cluster_small, cluster_large

def label_packets(packets, small_size, large_size, tolerance=5):
    """
    For each packet, if its 'Length' is near small_size => label 'S',
    if near large_size => label 'L'. Otherwise ignore.
    Returns a list of (time, label).
    """
    labeled = []
    for p in packets:
        length_val = int(p["Length"])
        t = float(p["Time"])
        if abs(length_val - small_size) <= tolerance:
            labeled.append((t, 'S'))
        elif abs(length_val - large_size) <= tolerance:
            labeled.append((t, 'L'))
    return labeled

def decode_sequence_tls(csv_file, tolerance=5):
    packets = load_packets(csv_file)
    #Identify the two main size clusters
    sizes = get_frame_sizes(packets)
    small_cluster, large_cluster = find_two_clusters_frequency(sizes)
    if small_cluster is None or large_cluster is None:
        print("Could not find two distinct clusters.")
        return ""

    print(f"Detected clusters: S ~ {small_cluster}, L ~ {large_cluster}")

    #Label each packet as 'S' or 'L' if within tolerance
    # Then sort by time
    labeled = label_packets(packets, small_cluster, large_cluster, tolerance)
    labeled.sort(key=lambda x: x[0])  # sort by time

    #Pair them up in chronological order
    bit_string = ""
    i = 0
    while i < len(labeled) - 1:
        t1, lbl1 = labeled[i]
        t2, lbl2 = labeled[i+1]

        pair_labels = {lbl1, lbl2}
        if pair_labels == {'S', 'L'}:
            #valid pair
            #if S is first => bit=0, else bit=1
            if t1 < t2 and lbl1 == 'S':
                bit_string += '0'
            elif t1 < t2 and lbl1 == 'L':
                bit_string += '1'
            elif t2 < t1 and lbl2 == 'S':
                bit_string += '0'
            else:
                bit_string += '1'
            i += 2
        else:
            #not a valid S-L pair, skip one
            i += 1

    return bit_string

def bits_to_ascii(bit_str):
    #truncate to multiple of 8
    r = len(bit_str) % 8
    if r:
        bit_str = bit_str[:-r]
    message = ""
    for i in range(0, len(bit_str), 8):
        chunk = bit_str[i:i+8]
        val = int(chunk, 2)
        message += chr(val)
    return message

bit_str = decode_sequence_tls(CSV_FILE, tolerance=5)
decoded_msg = bits_to_ascii(bit_str)

print("Recovered bits:", bit_str)
print("Decoded message:", decoded_msg)
