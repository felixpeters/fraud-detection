import datetime
from typing import Tuple

import pandas as pd


def get_train_test_set(
    tx_df: pd.DataFrame,
    start_date_training: datetime.datetime,
    delta_train: int = 7,
    delta_delay: int = 7,
    delta_test: int = 7,
) -> Tuple[pd.DataFrame]:
    """Create train and test sets from the transaction data.

    Args:
        tx_df (pd.DataFrame): Transaction data
        start_date_training (datetime.datetime): Datetime to start training
        delta_train (int, optional): Number of days of training data. Defaults to 7.
        delta_delay (int, optional): Delay period for identifying frauds. Defaults to 7.
        delta_test (int, optional): Number of days of test data. Defaults to 7.

    Returns:
        Tuple[pd.DataFrame]: Training and test sets
    """
    train_df = tx_df[
        (tx_df.tx_datetime >= start_date_training)
        & (tx_df.tx_datetime < start_date_training + datetime.timedelta(delta_train))
    ]

    test_df = []

    # Note: cards known to be defrauded after the delay period are removed from the test set
    # First, get known defrauded customers from the training set
    known_defrauded_customers = set(train_df[train_df.tx_fraud == 1].customer_id)

    start_tx_time_days_training = train_df.tx_time_days.min()

    for day in range(delta_test):
        # Get test data for the day
        test_df_day = tx_df[tx_df.tx_time_days == start_tx_time_days_training + delta_train + delta_delay + day]

        # Compromised cards from that test day, minus delay period, are added to pool of known defrauded customers
        test_df_day_delay_period = tx_df[tx_df.tx_time_days == start_tx_time_days_training + delta_train * day - 1]

        new_defrauded_customers = set(test_df_day_delay_period[test_df_day_delay_period.tx_fraud == 1].customer_id)
        known_defrauded_customers = known_defrauded_customers.union(new_defrauded_customers)

        test_df_day = test_df_day[~test_df_day.customer_id.isin(known_defrauded_customers)]

        test_df.append(test_df_day)

    test_df = pd.concat(test_df)

    train_df = train_df.sort_values("transaction_id")
    test_df = test_df.sort_values("transaction_id")

    return train_df, test_df
