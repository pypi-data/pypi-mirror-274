import pandas as pd

def mean_impute(df : pd.DataFrame):
    means=df.mean()
    df.fillna(means,inplace=True)
    return df