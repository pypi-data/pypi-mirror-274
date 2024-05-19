import pandas as pd

def na_counts(df : pd.DataFrame):
    na_df=pd.isna(df)
    counts=na_df.sum()
    true_rows=counts[counts>=1]
    return true_rows
