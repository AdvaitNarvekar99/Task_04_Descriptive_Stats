# 🧮 Task_04_Descriptive_Stats

Analyze 2024 US presidential election social media data using:
- ✅ Pure Python (no third-party libraries)
- ✅ Pandas
- ✅ Polars

---

## 📦 Datasets Used

⚠️ **Datasets are not included in the repository.**

This project uses:
- `2024_fb_ads_president_scored_anon.csv`
- `2024_fb_posts_president_scored_anon.csv`
- `2024_tw_posts_president_scored_anon.csv`

---

## 🎯 Objective

This task builds a descriptive statistics engine using three strategies to:
- Compute:
  - Count, Mean, Min, Max, Standard Deviation
  - Unique values & most frequent (for text)
- Perform the above **before and after grouping** by:
  - `page_id`
  - `page_id, ad_id` (only for Facebook Ads)
  - `Type` (for Facebook Posts)
  - `lang` (for Twitter Posts)

---

## 🧰 Scripts Overview

| Script                | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `pure_python_stats.py` | Uses `csv`, `math`, `collections` — no external libraries                  |
| `pandas_stats.py`      | Uses Pandas for `.describe()`, `.nunique()`, `.value_counts()`, `.agg()`   |
| `polars_stats.py`      | Uses Polars for high-performance `.describe()` and `group_by().agg()`      |

---

## ⚠️ Known Limitation (Pandas)

For `2024_fb_ads_president_scored_anon.csv`:
- `groupby(['page_id', 'ad_id']).describe()` is **slow or fails**
- ✅ Fixed by:
  - Selecting only numeric columns
  - Using `.agg(['mean', 'min', 'max', 'std'])`

---

## 🚀 How to Run

```bash
pip install pandas polars
