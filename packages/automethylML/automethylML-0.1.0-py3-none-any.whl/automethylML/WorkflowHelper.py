# Standard libraries
import os

# Data handling
import pandas as pd

# Custom classes from your package
from automethylML.FeatureSelection import FeatureSelection
from automethylML.RandomForestFeatureSelection import RandomForestFeatureSelection
from automethylML.TrainingData import TrainingData
from automethylML.OptunaHyperparameterTuning import OptunaHyperparameterTuning
from automethylML.TrainModels import TrainModels
from automethylML.PredictModule import PredictModule
from automethylML.EvaluatePredictions import EvaluatePredictions
import automethylML.utils as utils


def predict_and_save(pipeline_data, df, inference_dir, overwrite=False, save_name='prediction_module_object'):
    # Predict and save the predictions module
    PM = get_predictions(pipeline_data, df, inference_dir, save_name, overwrite=overwrite)

    utils.save_hierarchy_level_predictions(PM, inference_dir, overwrite=overwrite)
    # Save predictions DataFrame to CSV
    predictions_csv_path = os.path.join(inference_dir, 'predictions_df.csv')
    PM.predictions_df.to_csv(predictions_csv_path, index=True)

    return PM

def evaluate_and_save(pipeline_data, df, PM, metrics_dir, overwrite=False, save_name='evaluation_module_object'):
    # Get evaluation metrics and save the module
    EP = evaluate_predictions(pipeline_data, df, PM, metrics_dir, save_name, overwrite=overwrite)

    # Save metrics for each level
    utils.save_model_level_metrics(EP, metrics_dir, overwrite=overwrite)
    utils.save_hierarchical_level_metrics(EP, metrics_dir, overwrite=overwrite)

    return EP


def create_model_directory(save_dir, model_name_string, prepend_datetime=True):

    save_dir += os.sep # make sure there is a trailing slash

    if prepend_datetime:
        date_string = utils.get_formatted_datetime()
        model_name_string = date_string + '_' + model_name_string
    else:
        date_string = ''
        model_name_string = date_string + '_' + model_name_string

    dir_paths = {
        'save_dir': save_dir,
        'date_string': date_string,
        'data_idat_dir': os.path.join(save_dir, 'Data', 'IDAT'),
        'data_samplesheet_dir': os.path.join(save_dir, 'Data', 'Samplesheet'),
        'data_derived_dir': os.path.join(save_dir, 'Data', 'Derived'),
        
        'model_dir': os.path.join(save_dir, 'Model'),

        'inference_dir': os.path.join(save_dir, 'Inference', model_name_string),

        'metrics_dir': os.path.join(save_dir, 'Metrics', model_name_string),

        'model_name_string': model_name_string,
    }

    dir_paths['pipeline_data'] = os.path.join(dir_paths['model_dir'], dir_paths['model_name_string'] + '_pipeline_data.pkl')
    dir_paths['selected_features_csv_file'] = os.path.join(dir_paths['model_dir'], dir_paths['model_name_string'] + '_selected_features.csv')


    if os.path.exists(dir_paths['pipeline_data']):
        raise FileExistsError(f"The save name '{dir_paths['pipeline_data']}' already exists and will not be overwritten. Select a different name or delete ALL prefix data sarting witt {model_name_string}")
    
    if os.path.exists(dir_paths['metrics_dir']):
        raise FileExistsError(f"The folder '{dir_paths['metrics_dir']}' already exists and will not be overwritten. Select a different name or delete ALL prefix data sarting witt {model_name_string}")
    
    if os.path.exists(dir_paths['inference_dir']):
        raise FileExistsError(f"The folder '{dir_paths['inference_dir']}' already exists and will not be overwritten. Select a different name or delete ALL prefix data sarting witt {model_name_string}")
    
    
    full_dirs = [
        dir_paths['data_idat_dir'],
        dir_paths['data_samplesheet_dir'],
        dir_paths['data_derived_dir'],
        dir_paths['model_dir'],
        dir_paths['inference_dir'],
        dir_paths['metrics_dir'],
    ]


    utils.create_directory_structure('', full_dirs)

    return dir_paths  # Return the updated save_dir to be used in further processing

def run_full_pipeline(    df, 
                          feature_keys,
                          hierarchy_keys, 
                          hierarchy_levels, 
                          save_name,
                          index_key_name = None,
                        #   model_name_string = '',
                          select_top_n_features_IQR=None, 
                          select_top_n_features_RF=None,
                          n_optuna_trials=50,
                          n_optuna_cv_folds=3,
                          optuna_binary_metric_fn = 'roc_auc',
                          optuna_multiclass_metric_fn = 'roc_auc_ovr',
                          optuna_metric_optamize_direction = 'maximize',
                          calibration_model_method = 'sigmoid',
                          calibration_model_is_ensemble = True,
                         ):
   
    # save_dir+=os.sep
    # date_string = utils.get_formatted_datetime()


    """
    jsut make seperate funciton for creating directory
    model name string should be required and should be appended by a date string 
    all of this should be the main folder inside this we can use the below organization
    remove the model folder 
    add a predictions/inference 
    add a metrics folder 
    for each of those you can have select datasets in there. or folders named base don teh datasets 
    """   

    print('Running: FeatureSelection')
    fclass = FeatureSelection(feature_keys, hierarchy_keys, hierarchy_levels, index_key_name=index_key_name, select_top_n_features=select_top_n_features_IQR)
    fclass.make_feature_selection_dict(df)
    pipeline_data = fclass.create_pipeline_data()

    print('Random forrest feature selection')
    # RF feature selection
    RFFS = RandomForestFeatureSelection(pipeline_data, select_top_n_features=select_top_n_features_RF)
    RFFS.run_RF_feature_selection(df)
    pipeline_data = RFFS.update_pipeline_data(pipeline_data)

    # create training data class for easy data extraction
    target_dict = pipeline_data['target_key_dict']
    selected_feature_dict = pipeline_data['RF_selected_feature_dict']
    sample_index_dict = pipeline_data['sample_index_dict']
    training_data_class = TrainingData(target_dict, selected_feature_dict, sample_index_dict)

    # check if the cv folds are feasible absed on the data splits, not sure the best way to handle this yet
    # because we dont want to remove samples since that may be valid for 'Full_model' but not for 'sub_model'
    # it seems that this will have to be handled at the lvel of the FeatureSelection class, where we first remove samples
    # using the sampled index dict, if the cv folds are not feasible. #$%^&*

    print('OptunaHyperparameterTuning')

    # tune hyperparamters using Optuna
    OHT = OptunaHyperparameterTuning(pipeline_data, training_data_class)
    OHT.train_all_models(df,
                         binary_metric_fn=optuna_binary_metric_fn,
                         multiclass_metric_fn=optuna_multiclass_metric_fn,
                         direction=optuna_metric_optamize_direction,
                         n_trials=n_optuna_trials,
                         cv_folds=n_optuna_cv_folds)
    
    pipeline_data = OHT.update_pipeline_data(pipeline_data)

    print('train regular and calibration models')
    # train regular and calibration model
    calibration_model_params = {'calibration_method':calibration_model_method,
                                             'calibration_IS_ENSEMBLE':calibration_model_is_ensemble}
    TBM = TrainModels(pipeline_data)
    TBM.train_all_models(df, calibration_model_params)
    pipeline_data = TBM.update_pipeline_data(pipeline_data)


    print('save it')
    print(save_name)
    utils.PickleHelper.save(pipeline_data, save_name)
    return pipeline_data


def get_predictions(pipeline_data, input_data, save_dir, save_name, overwrite=False):

    pm_save_name = save_dir + os.sep + save_name
    if overwrite == False:
        if os.path.exists(pm_save_name) or os.path.exists(pm_save_name+'.pkl'):
            raise FileExistsError(f"The predictions file '{pm_save_name}' already exists and will not be overwritten.")
    
    PM = PredictModule(pipeline_data)
    PM.predict_all(input_data) # predict on validation or inference data
    predictions_df = PM.get_all_hierarchical_predictions(input_data) # organize and extract hearchical predictions

    PM.pipeline_data = None # delete pipeline data since we dont need that for this module after saving. 
    
    utils.PickleHelper.save(PM, pm_save_name, overwrite=overwrite)
    return PM

def evaluate_predictions(pipeline_data, input_data, predict_module_class, save_dir, save_name, overwrite=False):

    ep_save_name = save_dir + os.sep + save_name
    if overwrite == False:
        if os.path.exists(ep_save_name) or os.path.exists(ep_save_name+'.pkl'):
            raise FileExistsError(f"The evaluation file '{ep_save_name}' already exists and will not be overwritten.")
    
    EP = EvaluatePredictions(pipeline_data, predict_module_class)
    EP.get_hierarchy_level_targets(input_data)  # EVAL # hierarchy_level_targets
    EP.get_all_hierarchical_level_metrics(input_data) # EVAL # PM.hierarchical_level_metrics (relies on above to be run "get_hierarchy_level_targets")
    EP.get_all_model_level_metrics(input_data) #EVAL
    
    EP.pipeline_data = None # delete pipeline data since we dont need that for this module after saving.
    EP.PM = None # delete predict module since we dont need that for this module after saving.

    utils.PickleHelper.save(EP, ep_save_name, overwrite=overwrite)

    return EP


    


def valdidate_dataset(pipeline_data, val_data, base_save_name):
    PM = PredictModule(pipeline_data) 
    PM.predict_all(val_data) # PRED
    predictions_df = PM.get_all_hierarchical_predictions(val_data) # PRED
    EP = EvaluatePredictions(pipeline_data, PM)
    EP.get_hierarchy_level_targets(val_data)  # EVAL # hierarchy_level_targets
    EP.get_all_hierarchical_level_metrics() # EVAL # PM.hierarchical_level_metrics (relies on above to be run "get_hierarchy_level_targets")
    EP.get_all_model_level_metrics(val_data) #EVAL

    PM.pipeline_data = None
    
    EP.pipeline_data = None
    EP.PM = None
    
    
    utils.PickleHelper.save(PM, base_save_name+'_PREDICTIONS')
    utils.PickleHelper.save(EP, base_save_name+'_EVALUATION')

# PD_name = '/Users/pmaire/Users/pmaire/Documents/DATA/cpmpublic/MethyArray/training/GSE90496_beta_values_annotations_PIPELINE_DATA.pkl'
# base_save_name = PD_name.split('_PIPELINE_DATA.pkl')[0]
# pipeline_data = utils.PickleHelper.load(PD_name)
# valdidate_dataset_2(pipeline_data, val_data, base_save_name)


