# Machine learning tools
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.base import clone



class DefaultModels():
    @classmethod
    def random_forest(cls):
        """
        Initializes a RandomForestClassifier with default parameters.
        
        Returns:
            RandomForestClassifier: An instance of RandomForestClassifier with preset parameters.
        """
        rf_model = RandomForestClassifier(
        n_estimators=500,                                 # matches the R code provided
        criterion='gini',                                 # matches the R code provided, default for classification 
        max_depth=None,                 # no equivalent in the R code provided
        min_samples_split=2,            # no equivalent in the R code provided
        min_samples_leaf=1,                               # no equivalent in the R code provided -- set to 1 so it is irrelivent 
        min_weight_fraction_leaf=0.0,   # no equivalent in the R code provided
        max_features='sqrt',                              # same as "mtry" in R, "sqrt(p)" is default in R 
        max_leaf_nodes=None,                              # same as "maxnode" default in R is NULL eq to None in python
        min_impurity_decrease=0.0,                        # no equivalent in the R, set to 0 to match R (I assume since there is no param for this)
        bootstrap=True,                                   # consistant with R when set to True: when R code "replace" is set to True
        oob_score=False,                                  # for Python it is default accuracy (but can be customized, for R param "err.rate" is kinda the same but not sure which metric
        n_jobs=None,                     # num jobs run in parallel
        random_state=42,                 # equivalent is set.seed -- not set in R code provided 
        verbose=0,                       # 
        warm_start=False,                # no equivalent in the R, default in python is False
        class_weight=None,               # no equivalent in the R, it would be wise to use this for our data
        ccp_alpha=0.0,                   # no equivalent in the R, default in python is 0 
        max_samples=None                 # no equivalent in the R, realted to "sampsize", instead of fraction it is a count and can be stratified per class
        )
        return rf_model
        
    @classmethod    
    def calibration_model(cls, base_model, cv, method='sigmoid', ensemble=True):
        """
        Initializes a CalibratedClassifierCV with LogisticRegression as the base estimator.
        base_model is the model you need to pass in for calibration 
        cv is the cross validation class, to ensure the sample splits are used for optuna and this class 

        ensemble is set to Fasle 
        
        Returns:
            CalibratedClassifierCV: An instance of CalibratedClassifierCV using Logistic Regression for probability calibration.
        """
        # we need to pass in an unfit model so that the CV steps work properly
        base_model = clone(base_model)
        
        # Set up CalibratedClassifierCV with settings matching the original GLM calibration model
        glm_calibrated = CalibratedClassifierCV(
            estimator=base_model,
            method=method,  # sigmoid == Platt scaling
            ensemble=ensemble,
            cv=cv  # Same cross-validation split as optuna model
        )
        return glm_calibrated


