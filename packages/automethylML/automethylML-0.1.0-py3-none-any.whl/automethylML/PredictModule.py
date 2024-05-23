"""
we want to make a seperate class for eval so this will use all above funciton that haev the EVAL in the 
description to operate on the data. for now we dont have time for this but will do this next. 

also for multiple modle type comparisons we can save the PM class WITH the eval class (or keep them combined)
this will allow easy comparison between them and ultimately the model selection step. 

"""

from automethylML.utils import PickleHelper



# Data handling
import pandas as pd
import numpy as np

# Other libraries
import warnings




class PredictModule:
    def __init__(self, pipeline_data, models_to_predict=None):
        self.pipeline_data = pipeline_data
        if models_to_predict is None:
            self.models_to_predict = pipeline_data['final_inference_models_dict']
        else:
            self.models_to_predict = models_to_predict
        
        self.y_hat_proba_dict = {}
        # Validate models_to_predict otherwise system will fail later
        self._validate_models_to_predict()

    def save_class(self, save_directory, remove_pipeline_data=True):#$%^&*

        self.pipeline_data = None
        PickleHelper.save()


    def _validate_models_to_predict(self):
        test_key_match = [key in self.models_to_predict.keys() for key in self.pipeline_data['ALL_global_keys']]
        missing_keys = [global_key for test_key, global_key in zip(test_key_match, self.pipeline_data['ALL_global_keys']) if not test_key]
        if missing_keys:
            raise KeyError(f"'models_to_predict' input is missing the global_keys: {missing_keys}")

    
    @staticmethod
    def _test_if_sum_to_one(df_to_check):
        # if True then it apsses and all are close to 1 (within available precision)
        return np.all(np.isclose(df_to_check.sum(axis=1), 1.0))
  
    def compile_hierarchy_level_predictions(self):
        """

        for each level of the hierachy after the first model (i.e. Full_model) there are multiple models that the level 
        of the hierarchy. given this in order to get evaluations at each fo these levels this funtion serves to combine als 
        of them in a standard order and get predictions for each. 
        note this is NOT for eval, this can be constructed during inference without any known targets


        """
        
        hierarchy_level_predictions = []

        # loop through hierarchy_key levels (e.g. ['Full_model', 'Superfamily_code', 'Family_code']) 
        for hierarchy_key in self.pipeline_data['hierarchy_key_to_level_map'].values(): 

            # compile all hierarchy_level prediciton 
            hierarchy_level_y_hat = [self.y_hat_proba_dict[global_key] for global_key in self.pipeline_data['classification_tree_classes'] if hierarchy_key in global_key]
            hierarchy_level_y_hat = pd.concat(hierarchy_level_y_hat, axis=1)
        
        
            if len(hierarchy_level_predictions)>0: # skip 'Full_model' b/c it's complete aready 
                each_class_previous_prediciton = hierarchy_level_predictions[-1].idxmax(axis=1) # we need the previous predictions to determine which predicitons to zero out
        
                # for predicted child target group, set all other children target groups to 0. all will sum to  now 
                for each_class in each_class_previous_prediciton.unique():
                    # indexs based on the predicted chold target group
                    row_idx = each_class==each_class_previous_prediciton
                    col_idx = self.pipeline_data['classification_tree_classes'][(hierarchy_key, each_class)]
                    keys_not_in_col_idx = list(hierarchy_level_y_hat.columns.difference(col_idx))
        
                    # set all non-predicted children target groups to 0 at relivent samples index (row_idx) 
                    hierarchy_level_y_hat.loc[row_idx, keys_not_in_col_idx] = 0
        
            hierarchy_level_predictions.append(hierarchy_level_y_hat)
        
        hierarchy_level_predictions = {key: val for key, val in zip(self.pipeline_data['ordered_hierarchy_keys'], hierarchy_level_predictions)}
        self.hierarchy_level_predictions = hierarchy_level_predictions

        

    
    def predict_all(self, df_to_predict):
        """
        predicts all and save

        """
        # Predict for all global keys in the pipeline data
        for global_key in self.pipeline_data['ALL_global_keys']:
            print(global_key)
            y_hat_proba_df = self.predict(df_to_predict, global_key)
            self.y_hat_proba_dict[global_key] = y_hat_proba_df
                
        # if only one possible outcome 
        for global_key, class_name in self.pipeline_data['one_outcome_mapping_dict'].items(): 
            class_name = class_name[-1] #class name is the end of the 2 part tuple for one outcmoe mapping
            
            fill_in_df = pd.DataFrame(np.ones(len(df_to_predict)), columns=[class_name], index=df_to_predict.index)
            # if upstream predictions predicts this class name, then fill in those samples with a float(1)
            self.y_hat_proba_dict[global_key] = fill_in_df
                        
        self.compile_hierarchy_level_predictions() # make dict "self.hierarchy_level_predictions"
                

    def predict(self, df_to_predict, global_key):
                
        # Predict only for the specified global key
        if global_key in self.pipeline_data['ALL_global_keys']:
            model = self.models_to_predict[global_key]
            X_df = df_to_predict.loc[:, model.feature_names_in_] 

            y_hat_proba = model.predict_proba(X_df)
            y_hat_proba_df = pd.DataFrame(y_hat_proba, columns=model.classes_, index=X_df.index)
            # self.y_hat_proba_dict[global_key] = y_hat_proba_df
            
            return y_hat_proba_df
        else:
            raise ValueError(f"Invalid key: {global_key}")

    
    def _get_prediction_data(self, global_key, sample_index):
        """
        Get the highest prediction for a given model, save the probability value, key name of the
        prediction, and then the next model key to predict again.
        #$%^ add check if sample_index is in the sample else returnn a clear error for the user, 

        sample_index here refers to a single index to get ONE SINGLE sample/row 
        
        """
        if global_key in self.pipeline_data['ALL_global_keys']:
            # Hierarchy key i.e. the first string in the tuple that defined the global_key
            hierarchy_key = self.pipeline_data['target_key_dict'][global_key][0]

            # Output class of classifier
            target_prediction_name = self.y_hat_proba_dict[global_key].loc[sample_index].idxmax()
            # Value of the probability for that class
            target_probability = self.y_hat_proba_dict[global_key].loc[sample_index].max()
        
            # Keys to index the next model in the hierarchy
            next_global_key = (hierarchy_key, target_prediction_name) # tuple key
            
        elif global_key in self.pipeline_data['one_outcome_mapping_dict'].keys():            
            target_prediction_name = self.pipeline_data['one_outcome_mapping_dict'][global_key][1] # d is a tuple with the column name and the value of that column (string) 
            # target_probability = float('inf')  # set inf for this special case
            target_probability = float(1)  # 
            next_global_key = self.pipeline_data['one_outcome_mapping_dict'][global_key]
            hierarchy_key = next_global_key[0]
            

        else:
            raise KeyError(f"Key {global_key} not found in 'ALL_global_keys' or 'one_outcome_mapping_dict'.")

        # compile a dict with the keys and data for predictins, will be used to compile a DF later
        column_levels = ['previous_hierarchy_key', 'global_key', 'target_prediction_name', 'target_probability', 'next_global_key']
        self.column_levels = column_levels

        previous_hierarchy_key = global_key[0]
        if global_key == 'Full_model':
            previous_hierarchy_key = None

        if next_global_key[0] == self.pipeline_data['ordered_hierarchy_keys'][-1]:
            next_global_key=None
        
            
        column_data = previous_hierarchy_key, global_key, target_prediction_name, target_probability, next_global_key
        prediction_dict = dict(zip(column_levels, column_data))
        
        return prediction_dict

    def get_hierarchical_prediction(self, sample_index):
        """
        if there is a hierarchy with nested classification then this function gets all predictions 
        for each level of the hierarchy for a single sample

        for a single sample/row this returns the each prediciton in the hierarchy. so first it gets 
        the highest level prediction. then gets the model that corresponds and predicts usign that model 
        and so on through the hierarchy
        


        """
        global_key = 'Full_model'
        prediction_data = []
        for k in range(self.pipeline_data['n_hierarchy_levels']):

            prediction_dict = self._get_prediction_data(global_key, sample_index)
            prediction_data.append([prediction_dict[k] for k in prediction_dict]) # make a list of lists            
            global_key = prediction_dict['next_global_key']
        
        return prediction_data
        
            

    def get_all_hierarchical_predictions(self, df_to_predict):
        """
        Iterates over df_to_predict getting prediction data for each level of the hierarchy for a single sample,
        and compiles the results into a single DataFrame at the end.
        """
        # Prepare to collect all rows in a list first
        all_rows = []
        
        # Iterate over each sample in the DataFrame
        for sample_index in df_to_predict.index:
            prediction_data  = self.get_hierarchical_prediction(sample_index)
            # Construct a row for the current predictions
            row_data = sum(prediction_data, []) # extend all lists together (works same as "+" operator with lists) 
    
            all_rows.append(row_data)
        
        # Define multi-level columns for the DataFrame
        columns = pd.MultiIndex.from_product([self.pipeline_data['ordered_hierarchy_keys'], self.column_levels],
                                             names=['Hierarchy', 'Attribute'])
        
        # Create the DataFrame from the collected rows
        predictions_df = pd.DataFrame(all_rows, columns=columns, index=df_to_predict.index)

        self.predictions_df = predictions_df
        
        return predictions_df
        
    def get_hierarchy_level_prediction_info(self, hierarchy_key):
        return self.predictions_df[hierarchy_key]
    
    def get_sample_level_prediction_info(self, sample_ID):
        return self.predictions_df.loc[sample_ID]

    # def get_hierarchy_and_sample_level_prediction_info(self, hierarchy_key, sample_ID):
    #     df_out = self.predictions_df[hierarchy_key].loc[sample_ID]
    #     return df_out
    
    def get_hierarchy_and_sample_level_prediction_info(self, hierarchy_key, sample_ID, return_model_info=True):
        df_out = self.predictions_df[hierarchy_key].loc[sample_ID]
        if return_model_info:
            model_info = self.get_model_level_data(df_out['global_key'])
            return df_out, model_info
        else:    
            return df_out

    def get_model_level_data(self, global_key):
        invalid_dicts = ['one_outcome_mapping_dict',
                        'classification_tree_classes',
                        'hierarchical_every_outcome_dict',
                        'hierarchy_key_to_level_map']
        if global_key in self.pipeline_data['ALL_global_keys']:
            # List of dictionary names that contain the global_key structure
            dictionary_names = [key for key, value in self.pipeline_data.items() if isinstance(value, dict) and key not in invalid_dicts]
            
            model_level_data = {''.join(d_name.split('_dict')): self.pipeline_data[d_name][global_key] for d_name in dictionary_names}
        elif global_key in list(self.pipeline_data['one_outcome_mapping_dict'].keys()):
            class_mapping = self.pipeline_data['one_outcome_mapping_dict'][global_key]
            return_msg = (
            f'RETURNING None: No model information for... {global_key[0]:20} {global_key[1]:20} '
            f'because it only has one {class_mapping[0]:20} {class_mapping[1]:20}'
            )
            print(return_msg)
            model_level_data = None
        else:
            raise ValueError(f"Invalid key: {global_key}")
    
        return model_level_data


