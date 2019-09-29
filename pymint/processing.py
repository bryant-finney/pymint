import pandas as pd


def set_sign_from_type(data: pd.DataFrame, inplace=False) -> pd.DataFrame:
    """Set the sign of the field 'amount'.
    
    Debits have a sign < 0, and credits have a sign > 0.
    """
    if not inplace:
        data = data.copy()

    # flip the sign of all debit transactions that have a sign > 0
    idx = (data.transaction_type == "debit") & (data.amount > 0)
    data.loc[idx, "amount"] = data.loc[idx, "amount"].mul(-1)

    # flip the sign of all credit transactions that have a sign < 0
    idx = (data.transaction_type == "crebit") & (data.amount < 0)
    data.loc[idx, "amount"] = data.loc[idx, "amount"].mul(-1)

    return data