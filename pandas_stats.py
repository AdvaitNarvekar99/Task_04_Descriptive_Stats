# Importing relevant libraries
import pandas as pd
import os

# Creating a dict to easily handle data paths
DATASETS = {
    "Facebook Posts": "./2024_fb_posts_president_scored_anon.csv",
    "Twitter Posts": "./2024_tw_posts_president_scored_anon.csv",
    "Facebook Ads": "./2024_fb_ads_president_scored_anon.csv"
}

# Function to display stats after group by
def display_grouped_stats(grouped):
    try:
        print(grouped.describe().T.head(10))
    except:
        print("Unable to compute descriptive stats for this group.")

# Creating the run function to load data and generate descriptive stats
def run(name, path):
    print(f"\n{name}")
    df = pd.read_csv(path)

    print("\nOverall Descriptive Stats:")
    print(df.describe(include='all').T)

    # Showing top 2 most frequent values
    print("\nTop Frequent (first 2 string fields):")
    for col in df.select_dtypes(include='object').columns:
        print(f"{col} → Unique: {df[col].nunique()}, Top 2: {df[col].value_counts().head(2).to_dict()}")

    # Grouping based on specific files
    if name == "Facebook Posts" and "Type" in df.columns:
        grouped = df.groupby("Type")
        print("\nGrouped by 'Type' (descriptive stats):")
        display_grouped_stats(grouped)

    if name == "Twitter Posts" and "lang" in df.columns:
        grouped = df.groupby("lang")
        print("\nGrouped by 'lang' (descriptive stats):")
        display_grouped_stats(grouped)

# Main for loop for running everything
for name, path in DATASETS.items():
    if os.path.exists(path):
        run(name, path)