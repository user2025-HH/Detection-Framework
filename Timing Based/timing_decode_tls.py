import csv
import math
from collections import Counter

CSV_FILE = "" #add traffic file in csv

# A smaller factor (e.g. 1.0) removes more outliers; bigger (e.g. 3.0) is less aggressive.
IQR_FACTOR = 1.5

#Number of histogram bins to separate short vs. long
NUM_BINS = 20

def load_csv(csv_file):
    rows = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def is_valid_row(row):
    length_str = row.get('Length', '')
    if length_str.isdigit():
        length = int(length_str)
        if 90 <= length <= 120:
            return True
    return False

def remove_outliers_iqr(data, factor=1.5):
    if len(data) < 4:
        return data
    data_sorted = sorted(data)
    n = len(data_sorted)
    q1 = data_sorted[int(0.25 * n)]
    q3 = data_sorted[int(0.75 * n)]
    iqr = q3 - q1
    lower_bound = q1 - factor * iqr
    upper_bound = q3 + factor * iqr
    return [x for x in data if lower_bound <= x <= upper_bound]

def compute_deltas(filtered_rows):
    filtered_rows.sort(key=lambda r: float(r["Time"]))
    deltas = []
    for i in range(1, len(filtered_rows)):
        t_now = float(filtered_rows[i]["Time"])
        t_prev = float(filtered_rows[i-1]["Time"])
        delta = t_now - t_prev
        if delta > 0:
            deltas.append(delta)
        else:
            pass
    return deltas

def find_two_histogram_peaks(deltas, bins=NUM_BINS):
    if len(deltas) < 2:
        return None, None

    dmin, dmax = min(deltas), max(deltas)
    if dmin == dmax:
        return dmin, dmax

    bin_size = (dmax - dmin) / bins
    if bin_size == 0:
        return dmin, dmax

    histogram = Counter()
    for d in deltas:
        idx = int((d - dmin) / bin_size)
        if idx == bins:  #edge case if d == dmax
            idx = bins - 1
        histogram[idx] += 1

    #top 2 bins by frequency
    top_two = histogram.most_common(2)
    if len(top_two) < 2:
        return dmin, dmax

    bin1, bin2 = top_two[0][0], top_two[1][0]
    if bin1 > bin2:
        bin1, bin2 = bin2, bin1

    short_center = dmin + (bin1 + 0.5) * bin_size
    long_center  = dmin + (bin2 + 0.5) * bin_size
    return short_center, long_center

def decode_timing(csv_file):
    rows = load_csv(csv_file)
    valid_rows = [r for r in rows if is_valid_row(r)]

    #Compute deltas
    deltas = compute_deltas(valid_rows)

    #Remove outliers using IQR
    deltas = remove_outliers_iqr(deltas, factor=IQR_FACTOR)
    if len(deltas) < 2:
        print("Not enough intervals to decode.")
        return ""

    #Find short & long cluster centers via histogram
    short_c, long_c = find_two_histogram_peaks(deltas, NUM_BINS)
    if short_c is None or long_c is None:
        print("Could not determine two distinct peaks.")
        return ""

    #Set threshold to the midpoint
    threshold = (short_c + long_c) / 2
    print(f"Short cluster ~ {short_c:.3f}, Long cluster ~ {long_c:.3f}, threshold ~ {threshold:.3f}")

    #Convert each delta into '0' or '1'
    bit_string = ""
    for d in deltas:
        if d < threshold:
            bit_string += '0'
        else:
            bit_string += '1'

    return bit_string

def bits_to_ascii(bit_str):
    r = len(bit_str) % 8
    if r:
        bit_str = bit_str[:-r]
    message = ""
    for i in range(0, len(bit_str), 8):
        byte = bit_str[i:i+8]
        val = int(byte, 2)
        message += chr(val)
    return message

# ------------------------------------------
bit_str = decode_timing(CSV_FILE)
decoded_msg = bits_to_ascii(bit_str)

print("Recovered bits:", bit_str)
print("Decoded message:", decoded_msg)
