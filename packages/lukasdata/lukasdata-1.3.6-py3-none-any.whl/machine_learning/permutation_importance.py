import numpy as np


def reduce_dimension(predictions):
    new_list=[]
    for companies in predictions:
        label_lst=[]
        for years in companies:
            for label in years:
                label_lst.append(label)
        new_list.append(label_lst)
    predictions=np.array(new_list)
    return predictions


def permutation_importance(model, X, y, n_iterations=100):
    """
    Compute permutation importance for each feature in the given model.
    
    Parameters:
        model: Trained tf.keras model.
        X: Input features.
        y: True labels.
        metric: Function to evaluate model performance (e.g., accuracy, loss).
        n_iterations: Number of permutation iterations.
        
    Returns:
        importance_scores: Importance scores for each feature.
    """
    # Get baseline performance
    predictions=model.predict(X)

    new_list=[]

    

    predictions=reduce_dimension(predictions)
    
    #print(f"predictions: {model.predict(X)}")
    predicted_labels_binary = (predictions > 0.5).astype(int) #brauchen wir wahrscheinlich gar nicht
    #print(predicted_labels_binary)
    baseline_score =  accuracy_score(predicted_labels_binary, y)
    print(baseline_score)
    importance_scores = np.zeros(X.shape[2])
    
    for i in range(X.shape[2]):  # Iterate over features
        shuffled_X = X.copy()
        np.random.shuffle(shuffled_X[:,:,i])  # Shuffle the ith feature
        # Compute performance with shuffled feature
        shuffled_score = 0
        for _ in range(n_iterations):
            shuffled_prediction=model.predict(shuffled_X)
            shuffled_prediction=reduce_dimension(shuffled_prediction)
            shuffled_prediction_binary = (shuffled_prediction > 0.5).astype(int) #brauchen wir wahrscheinlich gar nicht
            shuffled_score += accuracy_score(shuffled_prediction_binary, y)
        shuffled_score /= n_iterations
        
        # Compute importance score for the ith feature
        importance_scores[i] = baseline_score - shuffled_score
    
    return importance_scores

# Example usage:
# Assuming model, X, y, and metric function are defined

from sklearn.metrics import accuracy_score

importance_scores = permutation_importance(model, padded_sequences, subsidized_array,)
print("Permutation importance scores:", importance_scores)