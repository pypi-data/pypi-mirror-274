"""

DefaultOptunaStudies
TrainingData


"""
import warnings
from automethylML.DefaultOptunaStudies import DefaultOptunaStudies
from automethylML.TrainingData import TrainingData


# Other libraries
import optuna


class OptunaHyperparameterTuning():
    def __init__(self, pipeline_data, training_data_class):
        """
        optuna_model_info
        |------model_name (eg full model, etc)
               |------ML-model type (eg RF KNN)
                      |------full study
                      |------best model params
                      |------best model performance on metric optamized on 
                      |------target actual
                      |------prediction (proba)


        """
        self.pipeline_data = pipeline_data
        self.training_data_class = training_data_class
        self.each_type_model_type_strings = ['KNN', 'RF']

        self.optuna_model_info = {}
        self.ALL_global_keys = training_data_class.target_dict.keys()

    def _get_important_information(self):
        """
        Retrieves Optuna related information for the pipeline.
        
        Returns:
            dict: A dictionary containing Optuna trials and the best Optuna model information.
        """
        return {
            'optuna_model_info': self.optuna_model_info,
            'best_optuna_model_info': self.best_optuna_model_info,
            'each_type_model_type_strings': self.each_type_model_type_strings,
            'metric_fn_binary': self.metric_fn_binary,
            'metric_fn_binary_multiclass': self.metric_fn_binary_multiclass
        }
    
    def update_pipeline_data(self, pipeline_data):
        """
        Updates the given pipeline data with additional Optuna related information.
        
        Args:
            pipeline_data (dict): The current data of the pipeline to be updated.
        
        Returns:
            dict: The updated pipeline data including Optuna trials and the best Optuna model information.
        """
        new_pipeline_data = self._get_important_information()
        pipeline_data.update(new_pipeline_data)
        return pipeline_data
        
    
        
    def train_all_models(self, df, binary_metric_fn='roc_auc', multiclass_metric_fn='roc_auc_ovr', direction='maximize', n_trials=60, cv_folds=3):
        self.metric_fn_binary = binary_metric_fn
        self.metric_fn_binary_multiclass = multiclass_metric_fn

        # create a loading bar to estimate this 
        

        cnt=0
        total_model = len(self.ALL_global_keys)*len(self.each_type_model_type_strings)
        for global_key in self.ALL_global_keys:
            

            
            # init keys for saving optuna runs
            self.optuna_model_info[global_key] = {model_type: {} for model_type in self.each_type_model_type_strings}
            
            # get training data
            X, y = self.training_data_class.get_training_data(df, global_key)

            #run optuna studies 
            """
            ideally change the settings of these so that they all have a standard name and key they can be 
            executed regardless of model type

            """
            for model_type in self.each_type_model_type_strings:
                cnt+=1
                print(f"Running model: {global_key}\nModel type: {model_type}\nModel number {cnt}/{total_model}")    

                if cv_folds > self.pipeline_data['max_cross_validation_splits'][global_key]:
                    warnings.warn(f"The training data has at least one class where the number of samples for that class are less than the number of cross-validation folds of: {cv_folds}. Setting cv_folds to : {self.pipeline_data['max_cross_validation_splits'][global_key]}, to match the minimum of that class to allow the model to run.")
                    cv_folds = self.pipeline_data['max_cross_validation_splits'][global_key]

                model_study = DefaultOptunaStudies.optuna_model_runner(model_type,
                                                                       X, 
                                                                       y, 
                                                                       binary_metric_fn=binary_metric_fn, 
                                                                       multiclass_metric_fn=multiclass_metric_fn, 
                                                                       direction=direction, 
                                                                       n_trials=n_trials, 
                                                                       cv_folds=cv_folds)
                # save optuna studies 
                self.optuna_model_info[global_key][model_type]['study'] = model_study

                 # for easy access add these values up front
                self.optuna_model_info[global_key][model_type]['best_params'] = model_study.best_params
                self.optuna_model_info[global_key][model_type]['best_value'] = model_study.best_value

                self.optuna_model_info[global_key][model_type]['StratifiedKFold_CV_class'] = model_study.StratifiedKFold_CV_class
        
        self._get_best_model_key()
            

    def _get_best_model_key(self):
        # get the directions of the metric to optamize. this will be universally the same accross all of the 
        # optuna dictionary, but is set in each model to allow for easier iterating through model types etc. 
        # here we grab the first one which will be the same for every single model. 
        self.best_optuna_model_info = {}
        for global_key, model_groups in self.optuna_model_info.items():
        
            direction = model_groups[list(model_groups.keys())[0]]['study'].metadata['direction_to_optimize']
    
            if direction.lower() == 'maximize':
                best_model_key = max(model_groups, key=lambda mod_key: model_groups[mod_key]['study'].best_value)
            elif direction.lower() == 'minimize':
                best_model_key = min(model_groups, key=lambda mod_key: model_groups[mod_key]['study'].best_value)

            # only one model can be the best to ensure this turn all to False then set it . 
            for mod_key in model_groups:
                model_groups[mod_key]['IS_BEST_BASE_MODEL'] = False
            model_groups[best_model_key]['IS_BEST_BASE_MODEL'] = True


            # this is optional but is a easy way to access some of the importnat information for the selected best 
            # model based on Optuna. all this is accessible in the Optuna dict but this is organzied as a dict to 
            # be used 99% time since we only care about the best model unless digging int it for issues later. 
            best_model = model_groups[best_model_key]
            
            self.best_optuna_model_info[global_key] = {
                'model_type_string':                best_model_key,  # Assuming best_model_key is the key for the best model
                'params':                   best_model['best_params'],
                'metric_performance':       best_model['best_value'],
                'is_multi_class':           best_model['study'].metadata['is_multi_class'],
                'n_trials':                 best_model['study'].metadata['n_trials'],
                'cv_folds':                 best_model['study'].metadata['cv_folds'],
                'metric_to_optimize':       best_model['study'].metadata['metric_to_optimize'],
                'direction_to_optimize':    best_model['study'].metadata['direction_to_optimize'],
                'StratifiedKFold_CV_class':    best_model['study'].StratifiedKFold_CV_class,
            }
