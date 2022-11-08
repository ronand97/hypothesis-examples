import hypothesis.strategies as st
import hypothesis.extra.pandas as hpd
from hypothesis import given
import pandas as pd
from pandas.api.types import is_string_dtype


@given(hpd.data_frames(columns=[
        hpd.column("unique_strs", elements=st.uuids() , dtype="object")
    ],
    index=hpd.range_indexes(min_size=5))
)
def test_unique_cols(df: pd.DataFrame) -> None:
    df["unique_strs"] = df["unique_strs"].astype(str)
    assert is_string_dtype(df["unique_strs"])
    assert len(df) == df["unique_strs"].nunique()