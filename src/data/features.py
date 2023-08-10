import datetime
from typing import Sequence, Union

import pandas as pd


def is_weekend(tx_datetime: Union[str, datetime.datetime]) -> int:
    """Determines whether the given datetime is a weekend day or not.

    Args:
        tx_datetime (Union[str, datetime.datetime]): Input datetime.

    Returns:
        int: 1 if weekend, 0 if weekday.
    """
    if isinstance(tx_datetime, str):
        tx_datetime = datetime.datetime.strptime(tx_datetime, "%Y-%m-%d %H:%M:%S")
    # Transform date into weekday (0 is Monday, 6 is Sunday)
    weekday = tx_datetime.weekday()
    # Binary value: 0 if weekday, 1 if weekend
    is_weekend = weekday >= 5

    return int(is_weekend)


def is_night(tx_datetime: Union[str, datetime.datetime]) -> int:
    """Determines whether the given datetime is a night time (0-6 AM) or not.

    Args:
        tx_datetime (Union[str, datetime.datetime]): Input datetime.

    Returns:
        int: 1 if night, 0 if day.
    """
    if isinstance(tx_datetime, str):
        tx_datetime = datetime.datetime.strptime(tx_datetime, "%Y-%m-%d %H:%M:%S")
    # Get the hour of the transaction
    tx_hour = tx_datetime.hour
    # Binary value: 1 if hour less than 6, and 0 otherwise
    is_night = tx_hour <= 6

    return int(is_night)


def get_customer_spending_features(customer_tx: pd.DataFrame, window_sizes: Sequence[int] = [1, 7, 30]) -> pd.DataFrame:
    """Derives recency, frequency and monetary features from the given customer transactions.

    Args:
        customer_tx (pd.DataFrame): Transactions to calculate features from and for.
        window_sizes (Sequence[int], optional): Window sizes in days. Defaults to [1, 7, 30].

    Returns:
        pd.DataFrame: Given customer transactions with the derived features.
    """
    # sort transactions by datetime
    customer_tx = customer_tx.sort_values(by="tx_datetime")

    # set index to tx_datetime to enable rolling functions
    customer_tx.index = customer_tx.tx_datetime

    for ws in window_sizes:
        # compute sum and number of transactions for this window size
        sum_amount_tx_window = customer_tx.tx_amount.rolling(f"{ws}D").sum()
        nb_tx_window = customer_tx.tx_amount.rolling(f"{ws}D").count()

        # compute the average transaction amount for this window size
        avg_amount_tx_window = sum_amount_tx_window / nb_tx_window

        # save feature values
        customer_tx[f"customer_id_nb_tx_{ws}_day_window"] = nb_tx_window
        customer_tx[f"customer_id_avg_amount_{ws}_day_window"] = avg_amount_tx_window

    # reindex according to transaction ID
    customer_tx.index = customer_tx.transaction_id

    return customer_tx


def get_terminal_risk_features(
    terminal_tx: pd.DataFrame, delay_period: int = 7, window_sizes: Sequence[int] = [1, 7, 30]
) -> pd.DataFrame:
    """Derives risk-related features for the given transactions from a terminal.

    Args:
        terminal_tx (pd.DataFrame): Transactions from a terminal.
        delay_period (int, optional): Period after which risk indicator (e.g., fraud label) is available. Defaults to 7.
        window_sizes (Sequence[int], optional): Window sizes. Defaults to [1, 7, 30].

    Returns:
        pd.DataFrame: Given transactions with the derived features.
    """
    # sort transactions by datetime
    terminal_tx = terminal_tx.sort_values(by="tx_datetime")

    # set index to tx_datetime to enable rolling functions
    terminal_tx.index = terminal_tx.tx_datetime

    # calculate number of total and fraudulent transactions for delay period
    nb_tx_delay_period = terminal_tx.tx_fraud.rolling(f"{delay_period}D").count()
    nb_fraud_delay_period = terminal_tx.tx_fraud.rolling(f"{delay_period}D").sum()

    for ws in window_sizes:
        # compute number of total and fraudulent transactions for this window size + delay period
        nb_fraud_delay_window = terminal_tx.tx_fraud.rolling(f"{ws + delay_period}D").sum()
        nb_tx_delay_window = terminal_tx.tx_fraud.rolling(f"{ws + delay_period}D").count()

        # compute number of total and fraudulent transactions for this window size
        nb_fraud_window = nb_fraud_delay_window - nb_fraud_delay_period
        nb_tx_window = nb_tx_delay_window - nb_tx_delay_period

        # compute the fraud rate for this window size
        risk_window = nb_fraud_window / nb_tx_window

        terminal_tx[f"terminal_id_nb_tx_{ws}_day_window"] = nb_tx_window
        terminal_tx[f"terminal_id_risk_{ws}_day_window"] = risk_window

    # reindex according to transaction ID
    terminal_tx.index = terminal_tx.transaction_id

    # replace NA values with 0 (all undefined risk scores where nb_tx_window is 0)
    terminal_tx.fillna(0, inplace=True)

    return terminal_tx
