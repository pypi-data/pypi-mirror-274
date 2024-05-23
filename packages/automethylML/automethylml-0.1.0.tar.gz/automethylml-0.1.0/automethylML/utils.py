

# Standard libraries
import copy
import os
import pickle
import warnings
from datetime import datetime
import shutil

# Data handling
import numpy as np
import pandas as pd

# Machine learning tools
# log_loss
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, confusion_matrix,
                             f1_score, matthews_corrcoef, precision_score,
                             recall_score, roc_auc_score)
import os




def _save_predictions(prediction_dict, inferece_dir, subdir, overwrite=False):
    """
    General function to save predictions to CSV files.
    """
    overwrite_mode = 'w' if overwrite else 'x'
    for global_key, predictions in prediction_dict.items():
        model_name = '_'.join(global_key) if isinstance(global_key, tuple) else global_key
        save_path = os.path.join(inferece_dir, subdir)
        os.makedirs(save_path, exist_ok=True)
        save_name = os.path.join(save_path, model_name + '.csv')
        predictions.to_csv(save_name, index=True, mode=overwrite_mode)

def save_hierarchy_level_predictions(PM, inferece_dir, overwrite=False):
    """
    Save hierarchy level predictions.
    """
    _save_predictions(PM.hierarchy_level_predictions, inferece_dir, 'hierarchy_level_predictions', overwrite)

def save_y_hat_proba(PM, inferece_dir, overwrite=False):
    """
    Save probability predictions (y_hat_proba).
    """
    _save_predictions(PM.y_hat_proba_dict, inferece_dir, 'y_hat_proba_dict', overwrite)


def _save_metrics(metric_dict, metrics_dir, subdir, overwrite=False):
    """
    General function to save metrics to CSV files.
    """
    overwrite_mode = 'w' if overwrite else 'x'
    for global_key, metrics in metric_dict.items():
        model_name = '_'.join(global_key) if isinstance(global_key, tuple) else global_key
        save_path = os.path.join(metrics_dir, subdir, model_name)
        os.makedirs(save_path, exist_ok=True)
        for metric_name, metric in metrics.items():
            save_name = os.path.join(save_path, metric_name + '.csv')
            metric.to_csv(save_name, index=True, mode=overwrite_mode)

def save_model_level_metrics(evaluate_predictions_class, metrics_dir, overwrite=False):
    """
    Save model-level metrics.

    """
    _save_metrics(evaluate_predictions_class.model_level_metrics, metrics_dir, 'model_level_metrics', overwrite)

def save_hierarchical_level_metrics(evaluate_predictions_class, metrics_dir, overwrite=False):
    """
    Save hierarchical-level metrics.
    """
    _save_metrics(evaluate_predictions_class.hierarchical_level_metrics, metrics_dir, 'hierarchical_level_metrics', overwrite)


# def check_cv_feasibility(counts_dict, cv_folds, raise_error=False):
#     """
#     Checks each entry in a dictionary of counts to see if cv_folds is feasible.
#     Issues a warning for each model where the minimum class count is less than cv_folds.
    
#     :param counts_dict: Dictionary of pandas Series with class counts.
#     :param cv_folds: Desired number of cross-validation folds.
#     :return: List of targets where class count is less than cv_folds.
#     """
#     error_trigger = False
#     # insufficient_samples = []
#     for global_key, counts in counts_dict.items():
#         min_count = counts.min()
#         if cv_folds > min_count:
#             error_trigger = True
#             warning_msg = (f"Model key'{global_key}', has class counts of {counts} where at least one is less than the"
#                            f"desired {cv_folds} CV folds.")
#             warnings.warn(warning_msg, category=UserWarning)
#             # insufficient_samples.append((global_key, counts))

#     if raise_error and error_trigger:
#         raise ValueError("One or more models have insufficient samples for the desired number of CV folds.")
#     # return insufficient_samples


def delete_model_directory(save_dir, model_name_string):
    # Append a trailing slash to save_dir if not already present
    save_dir = os.path.join(save_dir, '')

    # Define paths to directories and files that need to be deleted
    paths = {
        'inference_dir': os.path.join(save_dir, 'Inference', model_name_string),
        'metrics_dir': os.path.join(save_dir, 'Metrics', model_name_string),
        'pipeline_data_file': os.path.join(save_dir, 'Model', model_name_string + '_pipeline_data.pkl')
    }

    # Delete directories and files
    for path in paths.values():
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)  # Remove directory and all its contents
            else:
                os.remove(path)  # Remove a file
            print(f"Deleted: {path}")
        else:
            print(f"No such path: {path}")

    print("Deletion completed.")




def calculate_metrics(y_true, y_pred, y_pred_proba, ordered_labels, average_type = 'micro'):
    results = {}
    # exception where no data or not enough data
    if len(y_true)==0:
        results['metrics'] = None
        results['confusion_matrix'] = None
        print('y_true has length of 0, returning None')
        return results

    if len(np.unique(y_true))==1:
        # results['metrics'] = None
        # results['confusion_matrix'] = None
        print('y_true has has only one class, all AUC values will be undefined')
        # return results

    # ensure correct order for confusion matrix to work 
    ordered_labels = sorted(ordered_labels) #$%^&* #$%^&* #$%^&* this should be implemented in the predict module stage so that data is already organized liek this
    y_pred_proba = y_pred_proba.reindex(columns=ordered_labels)
    
    # Calculating the confusion matrix
    conf_matrix = confusion_matrix(y_true, y_pred, labels=ordered_labels)
    results['confusion_matrix'] = pd.DataFrame(conf_matrix, columns=ordered_labels, index=ordered_labels)
        
    # # Collecting other metrics
    metrics_data = {
        'F1 Score': [f1_score(y_true, y_pred, average=average_type, zero_division = np.nan)],
        'Matthews Correlation Coefficient': [matthews_corrcoef(y_true, y_pred)],
        'Balanced Accuracy Score': [balanced_accuracy_score(y_true, y_pred)],
        'Accuracy': [accuracy_score(y_true, y_pred)],
        'Precision': [precision_score(y_true, y_pred, average=average_type, labels=ordered_labels, zero_division = np.nan)],
        'Sensitivity (Recall)': [recall_score(y_true, y_pred, average=average_type, labels=ordered_labels, zero_division = np.nan)],
    }

    # Define the parameter combinations for all AUC metrics, some methods work when y_true doesn't have all the 
    # classes that the model was trained on. (e.g. training data has a control class and the test set doesn't)
    # so defining all the types and let the user decide
    combinations = [
        ('micro', 'ovr'),
        # ('micro', 'ovo'), # never a valid combo
        ('macro', 'ovr'),
        ('macro', 'ovo'),
        ('weighted', 'ovr'),
        ('weighted', 'ovo'),    
    ]

    if len(ordered_labels)==2: # binary case 
        y_pred_proba = y_pred_proba.iloc[:, 1]# must be 1 NOT 0 index here as per the docs
        
    # Use each combination in a try-except block
    auc_results = {}
    for average, multi_class in combinations:
        key_name = '_'.join(['ROC_AUC', average, multi_class])
        try:
            auc = roc_auc_score(y_true, y_pred_proba, average=average, multi_class=multi_class, labels=ordered_labels)
        except Exception as e:
            auc = np.nan
            ### for not remove the printing of the issue since it becomes extreamly verbose. #$%^&
            # msg = f'\nROC_AUC average type: "{average}" and method: "{multi_class}" set to NAN due to: "{str(e)}"'
            # warnings.warn(msg)
            # print(msg)
        auc_results[key_name] = auc

    # update metrics dict and turn into dataframe 
    metrics_data.update(auc_results)
    results['metrics'] = pd.DataFrame(metrics_data)
    
    return results   



def get_formatted_datetime():
    return datetime.now().strftime("%Y-%m-%d")




def create_directory_structure(base_path, dirs):
    """
    example: list your directories and base directoyr and run it
    dirs = [
    "Data/IDAT/",
    "Data/Samplesheet",
    "Derived",
    "Model",
    "Metrics"
]


    base_directory = "/Users/pmaire/Downloads/test_data_dir"  
    create_directory_structure(base_directory, dirs)

    """
    
    base_path = base_path+os.sep # Ensure the base path ends with a separator
    # Create each directory in the list
    for dir_path in dirs:
        full_path = os.path.join(base_path, dir_path)
        os.makedirs(full_path, exist_ok=True)  # Create the directory if it doesn't exist
        print(f"Created directory: {full_path}")





class PickleHelper:
    DEFAULT_PROTOCOL = 5  # Default protocol set to 5

    @classmethod
    def _check_pkl(cls, name):
        """Ensure the file name has a .pkl extension."""
        if not name.endswith('.pkl'):
            return name + '.pkl'
        return name

    @classmethod
    def save(cls, obj, name, protocol=None, overwrite=False):
        """
        Save an object to a file using pickle.

        :param obj: Object to be saved.
        :param name: Filename for the saved object.
        :param protocol: Pickle protocol version.
        :param overwrite: Boolean indicating whether to overwrite existing files. Default is False.
        """
        filename = cls._check_pkl(name)
        if not overwrite and os.path.exists(filename):
            raise FileExistsError(f"The file '{filename}' already exists and will not be overwritten.")
        if protocol is None:
            protocol = cls.DEFAULT_PROTOCOL

        # Check if the highest protocol or the default protocol differs from the selected/default
        if pickle.HIGHEST_PROTOCOL != protocol:
            warnings.warn(f"pickle.HIGHEST_PROTOCOL ({pickle.HIGHEST_PROTOCOL}) is different from the selected/default protocol ({protocol}).")
        if pickle.DEFAULT_PROTOCOL != protocol:
            warnings.warn(f"pickle.DEFAULT_PROTOCOL ({pickle.DEFAULT_PROTOCOL}) is different from the selected/default protocol ({protocol}).")

        with open(filename, 'wb') as f:
            pickle.dump(obj, f, protocol=protocol)

    @classmethod
    def load(cls, name):
        """Load an object from a pickle file."""
        with open(cls._check_pkl(name), 'rb') as f:
            return pickle.load(f)





def load_and_check_sample_sheet(file_path,
                                sentrix_barcode='sentrix_barcode',
                                sample_type='sample_type',
                                idat_red='idat_red',
                                idat_grn='idat_grn',
                                array_type='arrayType',
                                id_column=None):
    """
    Load a CSV file and check for required columns.

    :param file_path: Path to the CSV file.
    :param sentrix_barcode: Column name for sentrix barcode, default is 'sentrix_barcode'.
    :param sample_type: Column name for sample type, default is 'sample_type'.
    :param idat_red: Column name for IDAT red channel file, default is 'idat_red'.
    :param idat_grn: Column name for IDAT green channel file, default is 'idat_grn'.
    :param array_type: Column name for array type, default is 'arrayType'.
    :param id_column: Optional column name for an ID, default is None.
    :return: Pandas DataFrame of the loaded file.
    :raises ValueError: If required columns are missing.
    """
    # Load the CSV file
    df = pd.read_csv(file_path)

    # List of required columns
    required_columns = [sentrix_barcode, sample_type, idat_red, idat_grn, array_type]
    
    # Add the optional ID column if provided
    if id_column:
        required_columns.append(id_column)
    
    # Check for missing columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    
    return df






def get_class_info(c, sort_by_type=True, include_underscore_vars=False, return_name_and_type=False, end_prev_len=40):
    def get_len_or_shape(x_in):
        which_one = None
        try:
            len_or_shape_out = str(len(x_in))
            which_one = 'length'
            if type(x_in).__module__ == np.__name__:
                len_or_shape_out = str(x_in.shape)
                which_one = 'shape '
        except:
            if which_one is None:
                len_or_shape_out = 'None'
                which_one = 'None  '
        return len_or_shape_out, which_one

    names = []
    len_or_shape = []
    len_or_shape_which_one = []
    type_to_print = []

    for k in dir(c):
        if include_underscore_vars is False and k[0] != '_':

            tmp1 = str(type(eval('c.' + k)))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(k)
            a, b = get_len_or_shape(eval('c.' + names[-1]))
            len_or_shape.append(a)
            len_or_shape_which_one.append(b)
        elif include_underscore_vars:
            tmp1 = str(type(eval('c.' + k)))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(k)
            a, b = get_len_or_shape(eval('c.' + names[-1]))
            len_or_shape.append(a)
            len_or_shape_which_one.append(b)
    len_space = ' ' * max(len(k) for k in names)
    len_space_type = ' ' * max(len(k) for k in type_to_print)
    len_space_shape = ' ' * max(len(k) for k in len_or_shape)
    if sort_by_type:
        ind_array = np.argsort(type_to_print)
    else:
        ind_array = np.argsort(names)

    for i in ind_array:
        k1 = names[i]
        k2 = type_to_print[i]
        k5 = len_or_shape[i]
        x = eval('c.' + names[i])
        k3 = str(x)
        k1 = (k1 + len_space)[:len(len_space)]
        k2 = (k2 + len_space_type)[:len(len_space_type)]
        k5 = (k5 + len_space_shape)[:len(len_space_shape)]
        if len(k3) > end_prev_len:
            k3 = '...' + k3[-end_prev_len:]
        else:
            k3 = '> ' + k3[-end_prev_len:]
        print(k1 + ' type->   ' + k2 + '  ' + len_or_shape_which_one[i] + '->   ' + k5 + '  ' + k3)
    if return_name_and_type:
        return names, type_to_print


def get_dict_info(c, sort_by_type=True, include_underscore_vars=False, return_name_and_type=False, end_prev_len=30):
    names = []
    type_to_print = []
    for k in c.keys():
        if include_underscore_vars is False and str(k)[0] != '_':
            tmp1 = str(type(c[k]))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(str(k))
        elif include_underscore_vars:
            tmp1 = str(type(c[k]))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(str(k))
    len_space = ' ' * max(len(k) for k in names)
    len_space_type = ' ' * max(len(k) for k in type_to_print)
    if sort_by_type:
        ind_array = np.argsort(type_to_print)
    else:
        ind_array = np.argsort(names)

    for i in ind_array:
        k1 = names[i]
        k2 = type_to_print[i]

        if names[i] not in list(c.keys()):
          names[i] = eval(names[i])
        try:
            k3 = str(c[names[i]])
        except:
            k3 = str(c[float(names[i])])


        k1 = (k1 + len_space)[:len(len_space)]
        k2 = (k2 + len_space_type)[:len(len_space_type)]

        if len(k3) > end_prev_len:
            k3 = '...' + k3[-end_prev_len:]
        else:
            k3 = '> ' + k3[-end_prev_len:]

        if 'numpy.ndarray' in k2:
            k4 = str(c[names[i]].shape)
            k4_str = '   shape-> '
        else:
            try:
                k4 = str(len(c[names[i]]))
                k4_str = '   len-> '
            except:
                k4_str = '   None->'
                k4 = 'None'

        print(k1 + ' type->   ' + k2 + k4_str + k4 + '  ' + k3)
    if return_name_and_type:
        return names, type_to_print

def get_class_info2(c, sort_by=None, include_underscore_vars=False, return_name_and_type=False, end_prev_len=30):
    def get_len_or_shape(x_in):
        which_one = None
        try:
            len_or_shape_out = str(len(x_in))
            which_one = 'length'
            if type(x_in).__module__ == np.__name__:
                len_or_shape_out = str(x_in.shape)
                which_one = 'shape '
        except:
            if which_one is None:
                len_or_shape_out = 'None'
                which_one = 'None  '
        return len_or_shape_out, which_one

    names = []
    len_or_shape = []
    len_or_shape_which_one = []
    type_to_print = []

    for k in dir(c):
        if include_underscore_vars is False and k[0] != '_':

            tmp1 = str(type(eval('c.' + k)))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(k)
            a, b = get_len_or_shape(eval('c.' + names[-1]))
            len_or_shape.append(a)
            len_or_shape_which_one.append(b)
        elif include_underscore_vars:
            tmp1 = str(type(eval('c.' + k)))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(k)
            a, b = get_len_or_shape(eval('c.' + names[-1]))
            len_or_shape.append(a)
            len_or_shape_which_one.append(b)
    len_space = ' ' * max(len(k) for k in names)
    len_space_type = ' ' * max(len(k) for k in type_to_print)
    len_space_shape = ' ' * max(len(k) for k in len_or_shape)
    if sort_by is None:
        ind_array = np.arange(len(names))
    elif 'type' in sort_by.lower():
        ind_array = np.argsort(type_to_print)
    elif 'len' in sort_by.lower() or 'shape' in sort_by.lower():
        np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
        tmp1 = np.asarray([eval(k) for k in len_or_shape])
        tmp1[tmp1 == None] = np.nan
        tmp1 = [np.max(iii) for iii in tmp1]
        ind_array = np.argsort(tmp1)
    elif 'name' in sort_by.lower():
        ind_array = np.argsort(names)
    else:
        ind_array = np.arange(len(names))

    for i in ind_array:
        k1 = names[i]
        k2 = type_to_print[i]
        k5 = len_or_shape[i]
        x = eval('c.' + names[i])
        k3 = str(x)
        k1 = (k1 + len_space)[:len(len_space)]
        k2 = (k2 + len_space_type)[:len(len_space_type)]
        k5 = (k5 + len_space_shape)[:len(len_space_shape)]
        if len(k3) > end_prev_len:
            k3 = '...' + k3[-end_prev_len:]
        else:
            k3 = '> ' + k3[-end_prev_len:]
        print(k1 + ' type->   ' + k2 + '  ' + len_or_shape_which_one[i] + '->   ' + k5 + '  ' + k3)
    if return_name_and_type:
        return names, type_to_print




def info(x):
    if isinstance(x, dict):
        print('type is dict')
        get_dict_info(x)
    elif isinstance(x, list):
        try:
            x = copy.deepcopy(np.asarray(x))
            print('type is list, converting a copy to numpy array to print this info')
            np_stats(x)
        except:
            print(
                "type is a list that can't be converted to a numpy array for printing info or maybe data format is not compatible")

    elif type(x).__module__ == np.__name__:
        print('type is np array')
        np_stats(x)
    else:
        try:
            print('type is ' + str(type(x)) + ' will try printing using "get_class_info2" ')
            get_class_info2(x)
        except:
            print('cant find out what to do with input of type')
            print(type(x))



def np_stats(in_arr):
    print('\nmin', np.min(in_arr))
    print('max', np.max(in_arr))
    print('mean', np.mean(in_arr))
    print('shape', in_arr.shape)
    print('len of unique', len(np.unique(in_arr)))
    print('type', type(in_arr))
    try:
        print('Dtype ', in_arr.dtype)
    except:
        pass



