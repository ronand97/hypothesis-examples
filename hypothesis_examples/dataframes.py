import hypothesis.strategies as st
import hypothesis.extra.pandas as hpd

from datetime import datetime
import numpy as np


def simple_df() -> st.SearchStrategy:
    """
    Generates simple dataframe with 3 columns: one with datetime,
    one with strings and one with uuids.
    """
    return hpd.data_frames(
        columns=[
            hpd.column("datetime", elements=st.datetimes(
                min_value=datetime(year=2000, month=1, day=1),
                max_value=datetime(year=2100, month=1, day=1))),
            hpd.column("strings", elements=st.text(min_size=0, max_size=100)),
            hpd.column("uuids", elements=st.uuids())
        ]
    )


def df_with_lists_and_restricted_alphabet() -> st.SearchStrategy:
    """Generate a dataframe containing two columns. One with a column
    of strings where the allowed values are restricted, and one with
    a column of list entries where each list entry is a timedelta.
    Lists are forced to be at least length one and will appear as
    type "object" in pandas dtype.
    """
    return hpd.data_frames(
        columns=[
            hpd.column("strings_restricted", elements=st.text(alphabet=["a", "b", "c", "d"], max_size=79)),
            hpd.column("list_of_timedeltas", elements=st.lists(st.timedeltas(), min_size=1))
        ]
    )


@st.composite
def complex_df_with_same_length_non_null_cols(draw: st.DrawFn) -> st.SearchStrategy:
    """
    Create a dataframe containing columns of list elements where each
    list element is the same length. One of the list columns is a list of
    floats which has min/max constrains to avoid pandas memory overflow.
    Also have a column of integers bound by min/max defined as int64.

    Use this in your @given decorator, e.g.:

    ```
    @given(complex_df_with_same_length_non_null_cols())
    def test_my_complex_df(complex_df: pd.DataFrame):
        assert isinstance(complex_df, pd.DataFrame)
    ```

    Useful references:
    https://stackoverflow.com/a/51599429
    https://hypothesis.readthedocs.io/en/latest/data.html#composite-strategies
    """
    n = draw(st.integers(min_value=2, max_value=50))  # this is used to fix the length
    fixed_length_cols = [
        hpd.column(
            "list_of_floats",
            elements=st.lists(
                st.floats(min_value=-10 ** 5, max_value=10 ** 5),
                min_size=n, max_size=n),
            dtype=object),
        hpd.column("list_of_strings", elements=st.lists(st.text(), min_size=n, max_size=n), dtype=object),
        hpd.column("list_of_strings_2", elements=st.lists(st.text(), min_size=n, max_size=n), dtype=object),
        hpd.column("int64s", elements=st.integers(min_value=-10 ** 5, max_value=10 ** 5), dtype=np.dtype(np.int64))
    ]
    df = hpd.data_frames(fixed_length_cols)
    return draw(df)


def df_with_constrained_len(min_len: int, max_len: int) -> st.SearchStrategy:
    """Generate a df with constrained number of rows. We do this by
    leveraging the range index functionality.
    """
    return hpd.data_frames(
        index=hpd.range_indexes(min_size=min_len, max_size=max_len),
        columns=[
            hpd.column("a string column", st.text()),
            hpd.column("a datetime column", st.datetimes())
        ]
    )


def list_of_dfs_with_constrained_elements() -> st.SearchStrategy:
    """
    Generate a list of dataframes. Each dataframe has two columns.
    The first is a list of UUIDs, the second is a string column
    where the allowed strings are defined in a list.
    Both are marked as pandas dtype == 'object', but the UUIDs
    will still be UUID types when accessed.

    :return: _description_
    """
    return st.lists(
            hpd.data_frames(columns=[
                st.column("list_of_ids",
                       elements=st.lists(
                           st.uuids(),
                           min_size=1),
                       dtype="object"),
                st.column("people_names",
                       elements=st.sampled_from(
                           ["neil lennon", "ange postecoglou", "nicola sturgeon", "hasbullah"]),
                       dtype="object")
            ]), min_size=1
        )