import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

class keras_input():
    def __init__(self,df) -> None:
        self.df=df
        self.grouped_df=self.create_grouped("idnr")
        self.array=None
        self.padded_sequences=None
        self.x_train=None
        self.x_test=None
        self.y_train=None
        self.y_test=None
    def create_grouped(self,group):
        self.grouped_df=self.df.groupby(group)
    def drop_column(self,dropped_columns):
        self.df.drop(columns=dropped_columns)
    def create_y(self,column_name,entry_len):
        series=self.df[column_name]
        outer_list=[]
        for group_name,group_data in self.grouped_df:
            series_data=series[group_name]
            if isinstance(series_data,(np.int64)):
                list=[series_data]*entry_len
            else: 
                list=[series_data.iloc[0]]*entry_len
            outer_list.append(list)
        array=np.array(outer_list)
        self.y=array
    def create_array_from_grouped_df(self):
        big_array=[]
        #big_array=np.array(big_array)
        for group_name,group_data in self.grouped_df:
            array=np.array(group_data) #ist das notwendig?
            array_list=array.tolist()
            big_array.append(array_list)
        self.array=big_array
    def padding(self,max_len):
        self.padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(self.array, maxlen=max_len, padding='post', truncating='post') 
    def train_test_split(self):
        self.x_train,self.x_test,self.y_train,self.y_test=train_test_split(self.padded_sequences,self.y,test_size=0.33)
    def init_input(self,group_name="idnr",entry_len=10,y_column_name="subsidized"):
        self.create_grouped(group_name)
        self.create_array_from_grouped_df()
        self.create_y(y_column_name,entry_len)
        self.padding(entry_len)
        self.train_test_split()





