import pandas as pd


def value_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Count the distinct values in each column.
    """
    val_cnt_list = []
    for col in df.columns:
        val_cnt_list.append(len(df[col].value_counts()))

    return pd.DataFrame({
        'col_name': df.columns,
        'val_cnt': val_cnt_list
    })