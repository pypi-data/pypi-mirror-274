from typing import List

import pandas as pd
import anndata
from ._preprocess_utils import *


def df_to_adata(
    df: pd.DataFrame,
    metadata_cols: List[str] = [],
    imputer_strategy: str = "knn",
) -> anndata.AnnData:

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input df must be a pandas DataFrame.")

    adata = create_anndata_object(df)

    log_data_statistics(adata.X)

    impute_missing_values(adata, imputer_strategy)

    if "X_imputed" in adata.layers:
        add_unstructured_data(adata, imputer_strategy)

    return adata
