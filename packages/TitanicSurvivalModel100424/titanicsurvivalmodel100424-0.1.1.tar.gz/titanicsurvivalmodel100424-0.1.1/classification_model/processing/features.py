from typing import List
import pandas as pd
import numpy as np
import re

from sklearn.base import BaseEstimator, TransformerMixin


class ExtractLetterTransformer(BaseEstimator, TransformerMixin):
    
    def __init__(self, variables: List[str]):
        
        if not isinstance(variables, list):
            raise ValueError('variables should be a list')
        
        self.variables = variables

    def fit(self, X: pd.DataFrame, y=None):

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        X = X.copy()
        
        for feature in self.variables:
            X[feature] = X[feature].str[0]

        return X
    
# ================================================================
class ReplaceWithNan(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):

        return self

    def transform(self, X):
        
        return X.replace('?', np.nan)
    
# ================================================================
class DropColumns(BaseEstimator, TransformerMixin):
    
    def __init__(self, variables):
        
        if not isinstance(variables, list):
            raise ValueError('variables should be a list')
        
        self.variables = variables

    def fit(self, X, y=None):

        return self

    def transform(self, X):

        X = X.copy()
        
        return X.drop(labels=self.variables, axis=1)
# ================================================================
class DTypeTransformer_Float(BaseEstimator, TransformerMixin):
    
    def __init__(self, variables):
        
        if not isinstance(variables, list):
            raise ValueError('variables should be a list')
        
        self.variables = variables

    def fit(self, X, y=None):

        return self

    def transform(self, X):

        X = X.copy()
        
        for feature in self.variables:
            X[feature] = X[feature].astype('float')


        return X
# ================================================================
class GetFirstCabin(BaseEstimator, TransformerMixin):
    
    def __init__(self, variables):
        
        if not isinstance(variables, list):
            raise ValueError('variables should be a list')
        
        self.variables = variables

    def fit(self, X, y=None):

        return self

    def transform(self, X):

        X = X.copy()
        
        def get_first_cabin(row):
            try:
                return row.split()[0]
            except:
                return np.nan
        
        
        feature = self.variables[0]
        X[feature] = X[feature].apply(get_first_cabin)

        return X
# ================================================================
class GetTitle(BaseEstimator, TransformerMixin):
    
    def __init__(self, variables):
        
        if not isinstance(variables, list):
            raise ValueError('variables should be a list')
        
        self.variables = variables

    def fit(self, X, y=None):

        return self

    def transform(self, X):

        X = X.copy()
        
        def get_title(passenger):
            line = passenger
            if re.search('Mrs', line):
                return 'Mrs'
            elif re.search('Mr', line):
                return 'Mr'
            elif re.search('Miss', line):
                return 'Miss'
            elif re.search('Master', line):
                return 'Master'
            else:
                return 'Other'
        
        feature = self.variables[0]
        X['Title'] = X[feature].apply(get_title)

        return X