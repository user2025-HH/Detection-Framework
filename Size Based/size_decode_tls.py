import csv
from collections import Counter

CSV_FILE = "" #add traffic file in csv

def load_packets(csv_file):
    rows = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def find_top_2_frequent_sizes(rows):
    sizes = [int(r["Length"]) for r in rows]
    freq_map = Counter(sizes)
    #Sort by frequency descending
    by_freq = sorted(freq_map.items(), key=lambda x: x[1], reverse=True)

    #Extract the top 2 most common sizes
    small_size = min(by_freq[0][0], by_freq[1][0])
    large_size = max(by_freq[0][0], by_freq[1][0])
    return small_size, large_size

def decode_packets(rows, small_size, large_size, tolerance=1):
    
    #filter
    filtered = []
    for r in rows:
        size_val = int(r["Length"])
        packet_time = float(r["Time"])
        if abs(size_val - small_size) <= tolerance:
            filtered.append((packet_time, '0'))
        elif abs(size_val - large_size) <= tolerance:
            filtered.append((packet_time, '1'))
        

    #sort by timestamp
    filtered.sort(key=lambda x: x[0])

    #build the full bit string
    bit_string = ''.join(bit for _, bit in filtered)

    remainder = len(bit_string) % 8
    if remainder != 0:
        bit_string = bit_string[:-remainder]

    return bit_string

def bits_to_ascii(bit_string):
    result = []
    for i in range(0, len(bit_string), 8):
        byte_bits = bit_string[i:i+8]
        val = int(byte_bits, 2)
        result.append(chr(val))
    return ''.join(result)

#-----------------------------------------------------------------

rows = load_packets(CSV_FILE)
small_cluster, large_cluster = find_top_2_frequent_sizes(rows)
bit_str = decode_packets(rows, small_cluster, large_cluster, tolerance=1)
decoded_msg = bits_to_ascii(bit_str)

print("Bit string:", bit_str)
print("Decoded:", decoded_msg)
