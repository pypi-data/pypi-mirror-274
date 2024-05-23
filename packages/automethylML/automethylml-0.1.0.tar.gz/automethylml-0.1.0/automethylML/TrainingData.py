# This  needs to be tied into the train all models class this is pointly to be a class as is 
"""
this part int eh train all models class 

# get training data
df_for_training, target_key, selected_features_keys = self.training_data_class.get_training_data(df, global_key)
X, y = df_for_training[selected_features_keys], df_for_training[target_key].iloc[:, 0]

            

needs to be general sucht htat it can be run by itself to get the dats for visualizing and seeing 
what data was actually traine dthere


"""

# Data handling
import numpy as np
import pandas as pd

class TrainingData():
    def __init__(self, target_dict, selected_feature_dict, sample_index_dict=None):
        self.target_dict = target_dict
        self.selected_feature_dict = selected_feature_dict
        
        self.sample_index_dict = sample_index_dict

        self.required_features_for_final_inference = np.unique(sum([selected_feature_dict[k] for k in selected_feature_dict], []))
        self.required_features_for_final_inference = np.unique([feature for sublist in selected_feature_dict.values() for feature in sublist])


        self.classification_target_encoding = {}

    def _get_combined_training_dataframe(self, df, global_key, sample_row_idx=None, include_target=False):
        
        
        selected_features_keys = self.selected_feature_dict[global_key]
        target_key = self.target_dict[global_key]
        
        if include_target: 
            column_index = target_key + selected_features_keys
        else:
            column_index = selected_features_keys

        
        if sample_row_idx is None: # all data, for inference 
            df_out = df.loc[:, column_index]
            
        else: #for training data were we select subset of samples that apply to the training problem. 
            sample_row_idx = self.sample_index_dict[global_key]
            df_out = df.loc[sample_row_idx, column_index]

        

        return df_out, target_key, selected_features_keys
        
    def get_training_data(self, df, global_key):
        df_for_training, target_key, selected_features_keys = self._get_combined_training_dataframe(df, global_key, sample_row_idx=self.sample_index_dict[global_key], include_target=True)
        X = df_for_training[selected_features_keys]
        y_names = df_for_training[target_key].iloc[:, 0] # #$%^& test without using .iloc for trianing data since we want it to align in index
        
        return X, y_names
        
    def get_data(self, df, global_key):
        df_for_training, target_key, selected_features_keys = self._get_combined_training_dataframe(df, global_key, sample_row_idx=None, include_target=True)
        X = df_for_training[selected_features_keys]
        y_names = df_for_training[target_key].iloc[:, 0]
        
        return X, y_names
    
    def get_feature_data(self, df, global_key):
        df_for_training, target_key, selected_features_keys = self._get_combined_training_dataframe(df, global_key, sample_row_idx=None, include_target=False)
        X = df_for_training[selected_features_keys]
        return X 
    # def get_target_data(self, df, global_key):
    #     target_key = self.target_dict[global_key]
    #     y = df.loc[:, target_key]
    #     return y 


