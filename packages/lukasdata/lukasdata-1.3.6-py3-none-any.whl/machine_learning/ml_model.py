import os
#from machine_learning.keras_input import keras_input
from matplotlib import pyplot as plt
import tensorflow as tf

class ml_model():
    def __init__(self,model,keras_input) -> None:
        self.model=model
        self.input=keras_input
        self.history=None
        self.validation_history=[]
    def compile(self,lr=0.001):
        self.model.compile(optimizer=tf.keras.optimizers.Adam(lr),metrics=["accuracy"],loss="categorical_crossentropy")
    def fit(self,epochs,batch_size):
        self.history=self.model.fit(self.input.x_train, self.input.y_train, epochs=epochs, batch_size=batch_size, validation_data=(self.input.x_test, self.input.y_test))
    def save(self,file_name):
        os.chdir("C:/Users/lukas/Desktop/bachelor/models")
        self.model.save(file_name)
    def plot_metric(self,metrics_list):
        metrics_values_list=[]
        for metric in metrics_list:
            metrics_values_list.append(self.history.history[metric])
        for index,metric in enumerate(metrics_values_list):
            print(index)
            plt.subplot(1,2,1+index)
            plt.plot(metric,label=metrics_list[index])
            plt.title(metrics_list[index])
        plt.tight_layout()
        plt.show()   
    def validation_curve(self,learning_rates):
        for lr in learning_rates:
            self.compile(lr)
            self.fit()
            self.validation_curve.append(self.history.history['val_accuracy'][-1])
        plt.plot(learning_rates, self.validation_curve, marker='o')
        plt.xscale('log')
        plt.xlabel('Learning Rate')
        plt.ylabel('Validation Accuracy')
        plt.title('Validation Curve')
        plt.grid(True)
        plt.show()