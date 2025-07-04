# Importing relevant libraries
import csv
import math
import os
from collections import defaultdict, Counter

# Creating a dict to easily handle data paths
DATASETS = {
    "Facebook Posts": "./2024_fb_posts_president_scored_anon.csv",
    "Twitter Posts": "./2024_tw_posts_president_scored_anon.csv",
    "Facebook Ads": "./2024_fb_ads_president_scored_anon.csv"
}

# Fucntion to check whether column is float or not
def is_float(val):
    try:
        float(val)
        return True
    except:
        return False

# Creating the main statistics function
def get_stats(data, headers):
    num = defaultdict(list)
    cat = defaultdict(list)

    # Separating numerical and categorical columns
    for row in data:
        for h in headers:
            v = row[h]
            if is_float(v):
                num[h].append(float(v))
            else:
                cat[h].append(v)

    # Generating descriptive statistics for numerical columns
    stats = {}
    for h in headers:
        if h in num:
            x = num[h]
            m = sum(x)/len(x)
            stats[h] = {
                'count': len(x),
                'mean': round(m, 2),
                'min': min(x),
                'max': max(x),
                'std': round(math.sqrt(sum((i - m) ** 2 for i in x) / len(x)), 2)
            }

    # Generating unique value counts and most frequent values for categorical columns
        else:
            c = Counter(cat[h])
            stats[h] = {
                'count': len(cat[h]),
                'unique': len(c),
                'top': c.most_common(1)[0],
                'top_2': c.most_common(2)
            }
    return stats

# Function to do the group by
def group_by(data, cols):
    out = defaultdict(list)
    for row in data:
        key = tuple(row[c] for c in cols)
        out[key].append(row)
    return out

# Function to display the group stats
def display_grouped_stats(grouped_data, headers):
    for k, group in list(grouped_data.items())[:3]:
        print(f"\nGroup: {k}")
        print(get_stats(group, headers))

# Run function to take in one csv file, store in dictionary and generate stats
def run(name, file):
    print(f"\n{name}")
    with open(file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = reader.fieldnames

        print("\nOverall Descriptive Stats:")
        print(get_stats(rows, headers))

        # Frequent value and unique value count
        print("\nTop Frequent (first 2 fields):")
        for h in headers:
            values = [r[h] for r in rows]
            c = Counter(values)
            print(f"{h} → Unique: {len(c)}, Top 2: {c.most_common(2)}")

        # Specific columns based on the file names
        if name == "Facebook Ads" and 'page_id' in headers and 'ad_id' in headers:
            grouped = group_by(rows, ['page_id', 'ad_id'])
            print("\nGrouped by ['page_id', 'ad_id'] (descriptive stats):")
            display_grouped_stats(grouped, headers)

        if name == "Facebook Posts" and "Type" in headers:
            grouped = group_by(rows, ['Type'])
            print("\nGrouped by 'Type' (descriptive stats):")
            display_grouped_stats(grouped, headers)

        if name == "Twitter Posts" and "lang" in headers:
            grouped = group_by(rows, ['lang'])
            print("\nGrouped by 'lang' (descriptive stats):")
            display_grouped_stats(grouped, headers)

# Main for loop for loading the csvs and calling the run function
for name, path in DATASETS.items():
    if os.path.exists(path):
        run(name, path)