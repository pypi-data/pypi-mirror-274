import numpy as np

def drop_columns_permutation_score(x,permutation_scores,threshold=0):
    x=x.copy()
    column_indices=[]
    for i in range(len(permutation_scores)):
        if permutation_scores[i]<=threshold:
            column_indices.append(i)
    x = np.delete(x, column_indices, axis=2)
    return x
