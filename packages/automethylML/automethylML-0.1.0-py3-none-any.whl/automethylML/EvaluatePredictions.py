# Data handling
import pandas as pd
import numpy as np
# from methyl_chla import utils
from automethylML.utils import *

"""

calculate_metrics

"""


class EvaluatePredictions:
    def __init__(self, pipeline_data, predict_module_class):
        self.PM = predict_module_class  # Reference to the PredictModule instance
        self.pipeline_data = pipeline_data
        self.hierarchy_level_targets = {}
        self.hierarchical_level_metrics = {}
        self.model_level_y_actual_dict = {}
        self.model_level_metrics = {}

    def get_hierarchy_level_targets(self, df_in):
        """
        Stores hierarchy level targets from the DataFrame for evaluation purposes.
        """
        self.hierarchy_level_targets = {}
        for hierarchy_key in self.pipeline_data['hierarchy_key_to_level_map'].keys():
            self.hierarchy_level_targets[hierarchy_key] = df_in.loc[:, hierarchy_key]

    def get_all_hierarchical_level_metrics(self, df_in):
        """
        Calculates and stores hierarchical level metrics based on predictions and true values.
        """
        self.get_hierarchy_level_targets(df_in)
        
        self.hierarchical_level_metrics = {}
        for hierarchy_key in self.pipeline_data['hierarchy_key_to_level_map'].keys():
            y_pred_proba = self.PM.hierarchy_level_predictions[hierarchy_key]
            y_true = self.hierarchy_level_targets[hierarchy_key]
            y_pred = y_pred_proba.idxmax(axis=1)
            ordered_labels = self.pipeline_data['hierarchical_every_outcome_dict'][hierarchy_key]
            results = calculate_metrics(y_true, y_pred, y_pred_proba, ordered_labels)
            self.hierarchical_level_metrics[hierarchy_key] = results

    def get_model_level_formated_pred_and_true(self, df_in):
        """
        Formats and stores model-level predictions and true values for further evaluation.
        """
        self.model_level_y_actual_dict = {}
        self.model_level_y_pred_proba_dict = {}
        self.model_level_y_pred_dict = {}
        self.model_level_y_pred_proba_dict_if_sorted_into_this_model = {}
        self.model_level_y_pred_dict_if_sorted_into_this_model = {}
        
        for global_key in self.pipeline_data['ALL_global_keys']:
            row_idx, col_idx, model_level, hierarchy_key = self.get_model_level_index_for_input_df(df_in, global_key)

            self.model_level_y_actual_dict[global_key] = df_in.loc[:, hierarchy_key].loc[row_idx]
            self.model_level_y_pred_proba_dict[global_key] = self.PM.hierarchy_level_predictions[hierarchy_key].loc[row_idx, col_idx]
            self.model_level_y_pred_dict[global_key] = self.PM.hierarchy_level_predictions[hierarchy_key].idxmax(axis=1).loc[row_idx]
            self.model_level_y_pred_proba_dict_if_sorted_into_this_model[global_key] = self.PM.y_hat_proba_dict[global_key].loc[row_idx, col_idx]
            self.model_level_y_pred_dict_if_sorted_into_this_model[global_key] = self.PM.y_hat_proba_dict[global_key].idxmax(axis=1).loc[row_idx]

    def get_model_level_index_for_input_df(self, df_in, global_key):
        """
        Returns indices for sorting data into model levels based on the global key.
        """
        level_to_hierarchy_key_map = {value: key for key, value in self.pipeline_data['hierarchy_key_to_level_map'].items()}
        col_idx = self.pipeline_data['classification_tree_classes'][global_key]
        model_level = global_key if global_key == 'Full_model' else global_key[0]
        hierarchy_key = level_to_hierarchy_key_map[model_level]
        row_idx = [k in col_idx for k in df_in.loc[:, hierarchy_key]]

        return row_idx, col_idx, model_level, hierarchy_key

    def get_all_model_level_metrics(self, df_in, use_propegated_predictions_for_model_level_eval=False):
        """
        Calculates and stores all model-level metrics, optionally using propagated predictions.
        """
        self.get_model_level_formated_pred_and_true(df_in)
        model_level_metrics = {}
        if use_propegated_predictions_for_model_level_eval:
            y_pred_proba_all = self.model_level_y_pred_proba_dict
            y_pred_all = self.model_level_y_pred_dict
        else:
            y_pred_proba_all = self.model_level_y_pred_proba_dict_if_sorted_into_this_model
            y_pred_all = self.model_level_y_pred_dict_if_sorted_into_this_model
        
        for global_key in self.pipeline_data['ALL_global_keys']:
            y_true = self.model_level_y_actual_dict[global_key]
            ordered_labels = self.pipeline_data['classification_tree_classes'][global_key]
            y_pred_proba = y_pred_proba_all[global_key]
            y_pred = y_pred_all[global_key]
            results = calculate_metrics(y_true, y_pred, y_pred_proba, ordered_labels)
            model_level_metrics[global_key] = results
        self.model_level_metrics = model_level_metrics
