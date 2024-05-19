import pandas as pd

def drop_column_with_na(df : pd.DataFrame,min_not_na: int=0):
    #should I copy here?
    bool_df=df.notna()
    print(bool_df.columns)
    print(df.columns)
    for column_name in df.columns:
        if bool_df[column_name].sum() <= min_not_na:
            df=df.drop(columns=column_name,axis=1)
            print(f"dropped {column_name}")
    return df