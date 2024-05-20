from feature_engine.encoding import OneHotEncoder, RareLabelEncoder
from feature_engine.imputation import AddMissingIndicator, CategoricalImputer, MeanMedianImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from classification_model.config.core import config
from classification_model.processing import features as pp

titanic_pipe = Pipeline(
    [   
        # ==== INITIAL PREPROCESSING ====  
        ('replace_?_w_nan', pp.ReplaceWithNan()),
        
        ('get_first_cabin', pp.GetFirstCabin(variables=config.model_config.cabin)),

        ('get_title', pp.GetTitle(variables=config.model_config.name_title)),
        
        ('convert_to_float', pp.DTypeTransformer_Float(variables=config.model_config.convert_to_float)),
        
        ('drop_cols', pp.DropColumns(variables=config.model_config.cols_to_drop)),

        # ===== IMPUTATION =====
        # impute categorical variables with string missing
        (
        'categorical_imputation', CategoricalImputer(
        imputation_method='missing', variables=config.model_config.categorical_vars)
        ),
        # add missing indicator to numerical variables
        (
        'missing_indicator', AddMissingIndicator(variables=config.model_config.numerical_vars)
        ),
        # impute numerical variables with the median
        (
        'median_imputation', MeanMedianImputer(
        imputation_method='median', variables=config.model_config.numerical_vars)
        ),
        # Extract letter from cabin
        (
        'extract_letter', pp.ExtractLetterTransformer(variables=config.model_config.cabin)
        ),
        # == CATEGORICAL ENCODING ======
        # remove categories present in less than 5% of the observations (0.05)
        # group them in one category called 'Rare'
        (
        'rare_label_encoder', RareLabelEncoder(
        tol=0.05, n_categories=1, variables=config.model_config.categorical_vars)
        ),
        # encode categorical variables using one hot encoding into k-1 variables
        (
        'categorical_encoder', OneHotEncoder(
        drop_last=True, variables=config.model_config.categorical_vars)
        ),
        (
        'scaler', StandardScaler()
        ),
        (
        'Logit', LogisticRegression(C=config.model_config.C, random_state=config.model_config.random_state)
        ),
    ]
)
