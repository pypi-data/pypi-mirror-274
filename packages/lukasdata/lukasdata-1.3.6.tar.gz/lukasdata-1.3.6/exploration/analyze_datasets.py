def analyze_datasets(x_train,x_test,y_train,y_test):
    print(f"The Shape of x_train is {x_train.shape}")
    print(f"The Shape of x_test is {x_test.shape}")
    print(f"The Shape of y_train is {y_train.shape}")
    print(f"The Shape of y_test is {y_test.shape}")

    dimensions_train=len(x_train.shape)
    dimensions_test=len(y_train.shape)

    #checking if types are np
    #print out if the shapes correspond as they should