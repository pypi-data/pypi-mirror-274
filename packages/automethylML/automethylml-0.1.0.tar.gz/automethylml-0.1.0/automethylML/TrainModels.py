"""

DefaultModels
TrainingData

"""

from automethylML.DefaultModels import DefaultModels
from automethylML.TrainingData import TrainingData

# Data handling
import pandas as pd
import numpy as np

# Machine learning tools
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

# Other libraries
import warnings


class TrainModels():

    def __init__(self, pipeline_data, training_data_class=None):
        
        self.best_model_of_each_type = {}     
        self.pipeline_data = pipeline_data
        if training_data_class is None: #allow pass in training_data_class but otherwise default pipeline
            self.training_data_class = TrainingData(pipeline_data['target_key_dict'], 
                                                    pipeline_data['RF_selected_feature_dict'], 
                                                    pipeline_data['sample_index_dict'])

    def _setup_final_inference_models(self):
        # default best models 
        self.final_inference_models_dict = {}
        for global_key in self.pipeline_data['ALL_global_keys']:
            # string model name from best optuna CV model
            model_type_string = self.pipeline_data['best_optuna_model_info'][global_key]['model_type_string']
            # we only want calibrates models for inference so add the appending string name 
            model_name_string  = model_type_string + '_CALIBRATED'
            # grab that model for the final model at that model level node
            self.final_inference_models_dict[global_key] = self.best_model_of_each_type[global_key][model_name_string]
            
    def build_model(self, model_info):
        
        if model_info['model_type_string'].upper() == 'KNN':
            return KNeighborsClassifier(**model_info['params'])
            
        elif model_info['model_type_string'].upper() == 'RF':
            return RandomForestClassifier(**model_info['params'])
            
        elif model_info['model_type_string'].upper() == 'KNN_CALIBRATED':
            base_model = KNeighborsClassifier(**model_info['params'])
            
        elif model_info['model_type_string'].upper() == 'RF_CALIBRATED':
            base_model = RandomForestClassifier(**model_info['params'])
                        
        else:
            print(model_info['model_type_string'].upper())
            raise ValueError(f"Unsupported model type string: {model_info['model_type_string']}. Check build_model function to see accepted strings")

        calibrated_model = DefaultModels.calibration_model(base_model, 
                                                           cv = model_info['StratifiedKFold_CV_class'],
                                                           method=model_info['calibration_method'],
                                                           ensemble = model_info['calibration_IS_ENSEMBLE'])
        return calibrated_model
        
    def train_all_models(self, df, calibration_model_params=None):
        for global_key in self.pipeline_data['ALL_global_keys']:
            self.train_best_model_of_each_type(df, global_key, calibration_model_params)

        self._setup_final_inference_models() # creates self.final_inference_models_dict
            
    def train_best_model_of_each_type(self, df, global_key, calibration_model_params=None):
        # set settings for calibration models 
        if calibration_model_params is None:
            calibration_model_params = {'calibration_method':'sigmoid', 
                                         'calibration_IS_ENSEMBLE':True}
        
        # init for saving models 
        self.best_model_of_each_type[global_key] = {}
        # model info form optuna save
        optuna_model_info = self.pipeline_data['optuna_model_info'][global_key]

        # first remove any keys that say calibrated in case we rerun multiple time. 
        optuna_model_info = {k: v for k, v in optuna_model_info.items() if '_CALIBRATED' not in k}
        
        # for each model_key_string, make a calibrated version and attach the settings to it
        optuna_model_info_calibrated = {k + '_CALIBRATED': {**v, **calibration_model_params} 
                                for k, v in optuna_model_info.items()}
        
        # add on the calibrated version which is just a copy for now. When calling biuld_model, only the params are kept
        optuna_model_info.update(optuna_model_info_calibrated)

        for model_type_string, model_info in optuna_model_info.items():
            #update these dictionaries so they work with the build_model function
            model_info['model_type_string'] = model_type_string
            model_info['params'] = model_info['best_params']

            model = self.train_model(df, global_key, model_info)

            self.best_model_of_each_type[global_key][model_type_string] = model

    def train_model(self, df, global_key, model_info):
        """
        need to add a check here in case a model uses different termonology besides "model.fit(X, y)

        """
        X, y = self.training_data_class.get_training_data(df, global_key)
        
        model = self.build_model(model_info)
        model.fit(X, y)

        return model
    

    def _get_important_information(self):
        """
        Retrieves important information for the pipeline.
        
        
        """
        return {'final_inference_models_dict': self.final_inference_models_dict,
                'required_features_for_final_inference': self.training_data_class.required_features_for_final_inference,
                'best_model_of_each_type': self.best_model_of_each_type,
                'training_data_class': self.training_data_class,
                # we use model.feature_names_in_ to get the feature for prediction so below is for for easy access only but is the same  
                'final_inference_selected_feature_dict': self.training_data_class.selected_feature_dict, 
                'ALL_model_type_strings': list(self.best_model_of_each_type['Full_model'].keys()) # list of model strings e.g. ['KNN', 'RF', 'RF_CALIBRATED' etc...
               }
      
    def update_pipeline_data(self, pipeline_data):
        """
        Updates the given pipeline data with additional important information.
        
        Args:
            pipeline_data (dict): The current data of the pipeline to be updated.
        
        Returns:
            dict: The updated pipeline data including the final inference models.
        """
        new_pipeline_data = self._get_important_information()
        pipeline_data.update(new_pipeline_data)
        return pipeline_data


