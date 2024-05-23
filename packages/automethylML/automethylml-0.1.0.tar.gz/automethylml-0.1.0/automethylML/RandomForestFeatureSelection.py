"""

DefaultModels




"""
from automethylML.DefaultModels import DefaultModels

# Data handling
import numpy as np
import pandas as pd

# Machine learning tools
from sklearn.ensemble import RandomForestClassifier


class RandomForestFeatureSelection():
    def __init__(self, pipeline_data, select_top_n_features=10000):
        
        self.select_top_n_features = select_top_n_features
        
        # Initialize dictionaries to store RF models and feature importances
        self.RF_feature_selection_model_dict = {}
        self.RF_feature_importance_dict = {}
        self.RF_selected_features = {}
        self.RF_selected_features_importance = {}

        self.pipeline_data = pipeline_data

    def _get_important_information(self):
        """
        Retrieves important information for the pipeline.
        
        Returns:
            dict: A dictionary containing RandomForest feature importances, model information, and selected feature indices.
   
        """
        return {
            'RF_feature_importance_dict': self.RF_feature_importance_dict,
            # 'RF_feature_selection_model_dict': self.RF_feature_selection_model_dict, # RF models, dont need to keep these 
            'RF_selected_feature_dict': self.RF_selected_features,
            'RF_selected_features_importance_dict': self.RF_selected_features_importance
        }
        
    def update_pipeline_data(self, pipeline_data):
        """
        Updates the given pipeline data with additional important information.
        
        Args:
            pipeline_data (dict): The current data of the pipeline to be updated.
        
        Returns:
            dict: The updated or newly created dictionary containing comprehensive data for versioning the ML pipeline,
              including feature importances, model information, and selected feature indices.
        """
        new_pipeline_data = self._get_important_information()
        pipeline_data.update(new_pipeline_data)
        return pipeline_data


    def run_RF_feature_selection(self, df, rf=None):
        """
        Runs feature selection using a RandomForestClassifier.

        Iterates over features and samples, subsets the DataFrame based on these features and samples, 
        and uses a provided or a default RandomForestClassifier to fit the data, updating class 
        attributes with models and feature importances.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing the features and target variables.
        - rf (RandomForestClassifier, optional): A pre-initialized RandomForestClassifier instance. 
                                                  If None, a new classifier with predefined settings is created.

        Returns:
        - tuple: A tuple containing two dictionaries, `RF_feature_selection_model_dict` and `RF_feature_importance_dict`,
                 mapping feature selection scenarios to fitted RandomForestClassifier instances and feature importances, respectively.
        """
        for global_key in self.pipeline_data['ALL_global_keys']:
            print(global_key)
            
            feature_col_idx = self.pipeline_data['IQR_selected_feature_dict'][global_key]                        
            sample_row_idx = self.pipeline_data['sample_index_dict'][global_key]            
            target_key = self.pipeline_data['target_key_dict'][global_key]
            
            combined_columns = target_key + feature_col_idx.tolist()
            selected_df = df.loc[sample_row_idx, combined_columns]

            if rf is None: #if user doesnt pass in RF model use the default
                rf = DefaultModels.random_forest()

            X = selected_df[feature_col_idx]  # Feature matrix
            y = selected_df[target_key].iloc[:, 0]  # Target variable, [:, 0] is to flatten it to 1D

            if self.select_top_n_features > len(X.columns):
                raise ValueError("selects_top_n_features cannot be greater than the number of elements the DataFrame.")

            rf.fit(X, y)
            
            self.RF_feature_selection_model_dict[global_key] = rf
            self.RF_feature_importance_dict[global_key] = rf.feature_importances_
    
            # grab top N features 
            selected_features_idx = np.argsort(rf.feature_importances_)[::-1][:self.select_top_n_features] # [::-1] to flip so largest to smallest
            # save them to a dictionary for later
            self.RF_selected_features[global_key] = [feature_col_idx[f_idx] for f_idx in selected_features_idx]

            self.RF_selected_features_importance[global_key] = [rf.feature_importances_[f_idx] for f_idx in selected_features_idx]
            

# RFFS = RandomForestFeatureSelection(fclass, select_top_n_features=3)
# RFFS.run_RF_feature_selection(df)

# RF_feature_selection_model_dict, RF_feature_importance_dict = run_RF_feature_selection(df, fclass, rf=None)
# Feature importances from the model
# feature_importances = rf.feature_importances_
