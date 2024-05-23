# Data handling
import numpy as np

# Machine learning tools
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier

# Optimization
import optuna
from optuna.samplers import TPESampler


class DefaultOptunaStudies():
    
    @staticmethod
    def create_cv(cv_folds=3, seed=42):
        """
        Static method to create a StratifiedKFold cross-validator.
        """
        return StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=seed)

    @staticmethod
    def create_sampler(seed=42):
        """
        Static method to create a sampler with a fixed seed for reproducibility.
        """
        return TPESampler(seed=seed)

    @classmethod
    def models_KNN(cls, trial, y, cv_folds):

        # Calculate the valid range of n_neighbors
        max_n_neighbors = cls._get_upper_range_for_k(y, cv_folds)
        max_n_neighbors = np.max([2, max_n_neighbors])
        n_neighbors = trial.suggest_int('n_neighbors', 1, max_n_neighbors)
        weights = trial.suggest_categorical('weights', ['uniform', 'distance'])
        p = trial.suggest_int('p', 1, 2)

        # Model initialization
        model = KNeighborsClassifier(n_neighbors=n_neighbors, 
                                     weights=weights, 
                                     p=p,
                                     algorithm='auto')
        return model

    @staticmethod
    def model_RF(trial):
        n_estimators = trial.suggest_int('n_estimators', 100, 1000)
        max_depth = trial.suggest_int('max_depth', 2, 128, log=True)
        min_samples_split = trial.suggest_int('min_samples_split', 2, 12)

        # Model initialization with a fixed random_state
        model = RandomForestClassifier(n_estimators=n_estimators, 
                                       max_depth=max_depth,
                                       min_samples_split=min_samples_split, 
                                       criterion='gini',
                                       random_state=42)
        return model

    @classmethod
    def build_model(cls, model_type_string, trial, y, cv_folds):
        """
        note that cv_folds is only used here to help set upper limit for KNN K value. it isnt used to setup the folds


        """
        if model_type_string.upper() == 'KNN':
            return cls.models_KNN(trial, y, cv_folds) 
        elif model_type_string.upper() == 'RF':
            return cls.model_RF(trial)
        else:
            raise ValueError(f"Unsupported model type: {model_type_string}. Only 'KNN' and 'RF' are accepted.")

    @classmethod
    def optuna_model_runner(cls, model_type_string, X, y,
                            binary_metric_fn='roc_auc', 
                            multiclass_metric_fn='roc_auc_ovr', 
                            direction='maximize', 
                            n_trials=60,
                            cv_folds=3):
        
        # optuna.logging.set_verbosity(optuna.logging.WARNING)

        # Utilize the static method to create StratifiedKFold
        cv = cls.create_cv(cv_folds)
        # Utilize the static method to create a sampler with a fixed seed
        sampler = cls.create_sampler()

        # select metric based on binary vs multiclass 
        metric_fn = multiclass_metric_fn if len(np.unique(y))>2 else binary_metric_fn

        def objective(trial):
            model = cls.build_model(model_type_string, trial, y, cv_folds)
            # Cross-validation
            score = cross_val_score(model, X, y, scoring=metric_fn, cv=cv, n_jobs=-1)
            return score.mean()

        study = optuna.create_study(direction=direction, sampler=sampler)
        study.optimize(objective, n_trials=n_trials, show_progress_bar=False)
        study.metadata = {'metric_to_optimize':metric_fn,
                          'direction_to_optimize':direction,
                          'n_trials':n_trials,
                          'cv_folds':cv_folds,
                          'is_multi_class':metric_fn==multiclass_metric_fn,
                          'binary_and_multi_class_metrics_list': [binary_metric_fn, multiclass_metric_fn],
                         }

        study.StratifiedKFold_CV_class = cv
        
        return study

    @classmethod
    def _get_upper_range_for_k(cls, y, cv_folds):
        """
        set an upper range for K based on the amount fo data in each training fold. 

        """
        samples_in_cv = np.floor(len(y)/cv_folds)*(cv_folds-1)
        max_k_value = np.floor(np.sqrt(samples_in_cv)*2)
        if samples_in_cv<=4:
            max_k_value = samples_in_cv-1
        return int(max_k_value)

