from typing import List

import pandas as pd
import numpy as np
import anndata
from sklearn.impute import SimpleImputer, KNNImputer


def create_anndata_object(df: pd.DataFrame) -> anndata.AnnData:
    na_column_mask = df.isna().all()

    if na_column_mask.sum() > 0:
        columns_with_nas = df.columns[na_column_mask]
        df = df.drop(columns=columns_with_nas)

    X = df.values
    obs_names = df.index.astype(str)
    var_names = df.columns.astype(str)

    if len(np.unique(var_names)) != len(var_names):
        raise ValueError

    obs = pd.DataFrame(index=obs_names)
    var = pd.DataFrame(index=var_names)
    adata = anndata.AnnData(X=X, obs=obs, var=var, layers={"X_original": X})

    return adata


def log_data_statistics(X: np.ndarray) -> None:
    n_obs, n_features = X.shape
    total_nas = np.isnan(X).sum()
    percent_nas = 100 * total_nas / (n_obs * n_features)


def impute_missing_values(adata: anndata.AnnData, strategy: str) -> None:
    adata.var["percent_na"] = np.isnan(adata.X).sum(axis=0) / adata.X.shape[0]

    if adata.var["percent_na"].sum() != 0:
        imputers = {
            "mean": SimpleImputer(strategy="mean", keep_empty_features=True),
            "median": SimpleImputer(strategy="median", keep_empty_features=True),
            "constant": SimpleImputer(strategy="constant", fill_value=0, keep_empty_features=True),
            "knn": KNNImputer(),
        }

        imputer = imputers.get(strategy)
        if not imputer:
            raise ValueError(f"Invalid imputer strategy: {strategy}")
        adata.X = imputer.fit_transform(adata.X)
        adata.layers["X_imputed"] = adata.X


def add_unstructured_data(adata: anndata.AnnData, imputer_strategy: str) -> None:
    adata.uns["imputer_strategy"] = imputer_strategy
