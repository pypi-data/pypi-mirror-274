import numpy as np
from manipulation.int_columns import filter_numeric_columns
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
import pandas as pd




class data():
    def __init__(self,df) -> None:
        self.df=df
        self.ndarray=np.array(self.df)
        self.numeric_df=filter_numeric_columns(self.df)
        self.numeric_array=np.array(self.numeric_df)
        self.statistics=statistics(self.numeric_array,self.df)


class data_3d(data):
    def __init__(self,array_3d) -> None:
        super().__init__()
        self.array_3d=array_3d
        self.ndarray=self.array_3d.flatten()
        
def identify_anamolies(self,kde,i,threshold=0.01):
    densities = np.exp(kde.score_samples(self.ndarray[:, [i]]))
    anomalies = self.ndarray[densities < threshold]
    print(anomalies)

class statistics():
    def __init__(self,ndarray,df) -> None:
        self.ndarray=ndarray
        self.df=df
        self.mean=np.mean(ndarray)
        self.median=np.median(ndarray)
        self.std=np.std(ndarray)
        #self.correlation=np.corrcoef()
        #self.covariance=self.covariance()
        self.hist,self.bins=np.histogram(ndarray,bins=10) #wir müssen sagen welche variable
    def plot_hist(self,max_hists):
        for i in range(max_hists):
            plt.figure(i+1)
            hist=np.histogram(self.ndarray[:,i])
            plt.hist(hist, bins=self.bins, edgecolor='black')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.title('Histogram')
        plt.grid(True)
        plt.show() 

    def plot_multiple_histograms(self,column_interval,bins_list=None, title_list=None, xlabel='', ylabel='', colors=None,):
        num_plots = len(self.ndarray)

        if not bins_list:
            bins_list = [20] * num_plots

        if not title_list:
            title_list = [''] * num_plots

        if not colors:
            colors = ['blue'] * num_plots

        for i in range(column_interval[0],column_interval[1]):

            plt.figure(i+1)
            plt.hist(np.abs(self.ndarray[:,i]), bins=bins_list[i], color=colors[i])
            print(self.ndarray[:,i])
            plt.title(self.df.columns[i])
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.grid(True)
            plt.tight_layout()

        plt.show()
    def kde(self,column_interval):
        for i in range(column_interval[0],column_interval[1]):
            kde = KernelDensity(kernel='gaussian', bandwidth=0.5).fit(self.ndarray[:,[i]])
            x = np.linspace(min(self.ndarray[:,i]), max(self.ndarray[:,i]), 1000)
            log_dens = kde.score_samples(x[:, None])
            identify_anamolies(self,kde,i)
            # Plot the results
            plt.plot(x, np.exp(log_dens), label='KDE')
            plt.hist(self.ndarray[:,[i]], bins=30, density=True, alpha=0.5, label='Histogram')
            plt.legend()
            plt.show()





imputed_csv=pd.read_csv("C:/Users/lukas/Desktop/bachelor/data/rf_imputed.csv")
imputed_actual_data=imputed_csv.iloc[:,5:] #ich schmeiß die ersten raus
imputed_data=data(imputed_actual_data)

print(imputed_data.statistics.mean)
#imputed_data.statistics.plot_multiple_histograms([25,35])
imputed_data.statistics.kde([20,30])




# Compute the density at specific points


# Identify anomalies (points with low density)
threshold = 0.01  # Example threshold for low density



