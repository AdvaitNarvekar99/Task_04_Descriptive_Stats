# Importing relevant libraries
import polars as pl
import os

# Creating a dict to easily handle data paths
DATASETS = {
    "Facebook Posts": "./2024_fb_posts_president_scored_anon.csv",
    "Twitter Posts": "./2024_tw_posts_president_scored_anon.csv",
    "Facebook Ads": "./2024_fb_ads_president_scored_anon.csv"
}

# Creating the function to describe stats after group by
def display_grouped_stats(df, group_cols):
    try:
        numeric_cols = [col for col in df.columns if df[col].dtype in [pl.Float64, pl.Int64]]
        group = df.group_by(group_cols).agg([
            pl.len().alias("count"),
            *[pl.mean(col).alias(f"mean_{col}") for col in numeric_cols],
            *[pl.min(col).alias(f"min_{col}") for col in numeric_cols],
            *[pl.max(col).alias(f"max_{col}") for col in numeric_cols],
            *[pl.std(col).alias(f"std_{col}") for col in numeric_cols]
        ])
        print(group.head(10))
    except Exception as e:
        print("Unable to compute descriptive stats for this group:", e)

# Creating the run function to load data and generate descriptive stats
def run(name, path):
    print(f"\n{name}")
    df = pl.read_csv(path)

    print("\nOverall Descriptive Stats:")
    print(df.describe().head(10))

    # Displaying the unique values and most frequent values for the string columns
    print("\nTop Frequent (first 2 string fields):")
    for col in df.columns:
        if df[col].dtype == pl.Utf8:
            print(f"{col} → Unique: {df[col].n_unique()}, Top 2:")
            top = df.group_by(col).agg(pl.len().alias("count")).sort("count", descending=True).head(2)
            print(top)

    # Grouping based on specific files
    if name == "Facebook Ads" and 'page_id' in df.columns and 'ad_id' in df.columns:
        print("\nGrouped by ['page_id', 'ad_id'] (descriptive stats):")
        display_grouped_stats(df, ["page_id", "ad_id"])

    if name == "Facebook Posts" and "Type" in df.columns:
        print("\nGrouped by 'Type' (descriptive stats):")
        display_grouped_stats(df, ["Type"])

    if name == "Twitter Posts" and "lang" in df.columns:
        print("\nGrouped by 'lang' (descriptive stats):")
        display_grouped_stats(df, ["lang"])

# Main for loop for running everything
for name, path in DATASETS.items():
    if os.path.exists(path):
        run(name, path)