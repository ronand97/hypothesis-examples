import pandas as pd
from pandas.testing import assert_series_equal
from typing import Optional

def df_column_assertions(
        df_old: pd.DataFrame,
        df_new: pd.DataFrame,
        new_cols: dict[str, type],
        check_rows_change: bool = True,
        check_old_cols: bool = True,
        old_cols_to_check: Optional[list[str]] = None):
    """
    Perform multiple assertions about new dataframe vs old dataframe.
    When processing/generating/creating a new dataframe it's worth checking that:
    * The new columns are added as expected
    * The new columns have the correct type
    * Cols that should survive have survived and not changed type
    * Number of rows hasn't changed (if applicable)

    -> Only checks columns, not indexes. use .reset_index() if needed
    **DOESN'T WORK FOR DATES -
    separately use pandas.api.types.is_datetime64_any_dtype**

    :param df_old: the starting dataframe
    :param df_new: the changed dataframe
    :param new_cols: dict of new cols with associated type
    :param check_rows_change: does the number of rows change by design
    :param check_old_cols: check cols in old_df exist unchanged in new df
    :param old_cols_to_check: check only subset of df_old[old_cols]. For example,
                              if some cols in df_old were renamed/removed
    """
    for col, col_type in new_cols.items():
        assert col in df_new.columns
        row_dtypes_are_expected_type: pd.Series = (df_new[[col]].applymap(type) == col_type).all()
        assert_series_equal(row_dtypes_are_expected_type, pd.Series([True], index=[col]))
    if check_old_cols:
        old_cols = df_old.columns if old_cols_to_check is None else old_cols_to_check
        for col in old_cols:
            assert col in df_new.columns
            assert df_new[col].dtype == df_old[col].dtype
    if check_rows_change:
        assert len(df_new) == len(df_old)
