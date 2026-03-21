import pandas as pd
from typing import List, Dict

# -----------------------------------------------------------------
# 2️⃣ Helper – apply the selected transformations to a DataFrame
# -----------------------------------------------------------------
def apply_transformations(
    df: pd.DataFrame,
    transforms: List[str],
    rename_info: Dict[str, str] | None = None,
) -> pd.DataFrame:
    """Apply a list of transformation identifiers to ``df``."""
    for t in transforms:
        if t == "drop_duplicate_rows":
            df = df.drop_duplicates()
        elif t == "drop_duplicate_columns":
            df = df.loc[:, ~df.columns.duplicated()]
        elif t == "fill_nulls_zero":
            df = df.fillna(0)
        elif t == "drop_rows_with_nulls":
            df = df.dropna()
        elif t == "rename_column" and rename_info:
            old = rename_info.get("old_name")
            new = rename_info.get("new_name")
            if old in df.columns:
                df = df.rename(columns={old: new})
    return df
