import pandas as pd

def concat_dfs(dataframes):
    concat_frames=[dataframe.reset_index(drop=True, inplace=True) for dataframe in dataframes]
    df=pd.concat(concat_frames,ignore_index=True)
    df.reset_index(drop=True,inplace=True)
    return df

