from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix
from sklearn.base import BaseEstimator,TransformerMixin
import numpy as np
import pandas as pd 


class CustomTransformer(BaseEstimator,TransformerMixin):
    def __init__(self,required_component) -> None:
        print(f"{'*'*5} init() call of Custom Transformer {'*'*5}")
        self.required_component = required_component

    def fit(self,X,y = None):
        print(f"{'*'*5} fit() call of Custom Transformer {'*'*5}")
        return self

    def transform(self,X,y = None):
        X_sparse = csr_matrix(X)
        tsvd = TruncatedSVD(n_components=X_sparse.shape[1]-1)
        X_tsvd = tsvd.fit(X)

        tsvd_var_ratios = tsvd.explained_variance_ratio_

        componets = self.select_n_components(tsvd_var_ratios, self.required_component)

        return componets
        

    def select_n_components(self,var_ratio, goal_var: float) -> int:
    # Set initial variance explained so far
        total_variance = 0.0
        
        # Set initial number of features
        n_components = 0
        
        # For the explained variance of each feature:
        for explained_variance in var_ratio:
            
            # Add the explained variance to the total
            total_variance += explained_variance
            
            # Add one to the number of components
            n_components += 1
            
            # If we reach our goal level of explained variance
            if total_variance >= goal_var:
                # End the loop
                break
                
        # Return the number of components
        return n_components


'''def n_componet_finder(X,required_varience):
    X_sparse = csr_matrix(X)
    tsvd = TruncatedSVD(n_components=X_sparse.shape[1]-1)
    X_tsvd = tsvd.fit(X)

    tsvd_var_ratios = tsvd.explained_variance_ratio_

    componets = select_n_components(tsvd_var_ratios, required_varience)

    return componets'''


