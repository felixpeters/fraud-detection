import random
from typing import Sequence

import numpy as np
import pandas as pd


def generate_customer_profiles_table(n_customers: int, random_state=0) -> pd.DataFrame:
    """Generates customer profiles.

    Args:
        n_customers (int): Number of desired customers.
        random_state (int, optional): Random state. Defaults to 0.

    Returns:
       pd.DataFrame: Dataframe containing customer profiles.
    """
    np.random.seed(random_state)

    customer_id_properties = []

    # Generate customer properties from random distributions
    for customer_id in range(n_customers):
        longitude = np.random.uniform(0, 100)
        latitude = np.random.uniform(0, 100)

        mean_amount = np.random.uniform(5, 100)  # Arbitrary (but sensible) value
        std_amount = mean_amount / 2  # Arbitrary (but sensible) value

        mean_nb_tx_per_day = np.random.uniform(0, 4)  # Arbitrary (but sensible) value

        customer_id_properties.append([customer_id, longitude, latitude, mean_amount, std_amount, mean_nb_tx_per_day])

    customer_profiles_table = pd.DataFrame(
        customer_id_properties,
        columns=["customer_id", "loc_long_coord", "loc_lat_coord", "mean_amount", "std_amount", "mean_nb_tx_per_day"],
    )

    return customer_profiles_table


def generate_terminal_profiles_table(n_terminals: int, random_state=0) -> pd.DataFrame:
    """Generates terminal profiles.

    Args:
        n_terminals (int): Desired number of terminals.
        random_state (int, optional): Random state. Defaults to 0.

    Returns:
        pd.DataFrame: Dataframe containing terminal profiles.
    """
    np.random.seed(random_state)

    terminal_id_properties = []

    # Generate terminal properties from random distributions
    for terminal_id in range(n_terminals):
        longitude = np.random.uniform(0, 100)
        latitude = np.random.uniform(0, 100)

        terminal_id_properties.append([terminal_id, longitude, latitude])

    terminal_profiles_table = pd.DataFrame(
        terminal_id_properties, columns=["terminal_id", "loc_long_coord", "loc_lat_coord"]
    )

    return terminal_profiles_table


def get_list_terminals_within_radius(customer_profile: pd.Series, x_y_terminals: np.ndarray, r: int) -> Sequence[int]:
    """Derives list of terminals within the radius of a given customer.

    Args:
        customer_profile (pd.Series): Row from the customer profiles table.
        x_y_terminals (np.ndarray): Longitude and latitude coordinates of terminals.
        r (int): Radius.

    Returns:
        Sequence[int]: List of terminal IDs in the radius.
    """
    # Use numpy arrays in the following to speed up computations

    # Location (x,y) of customer as numpy array
    x_y_customer = customer_profile[["loc_long_coord", "loc_lat_coord"]].values.astype(float)

    # Squared difference in coordinates between customer and terminal locations
    squared_diff_x_y = np.square(x_y_customer - x_y_terminals)

    # Sum along rows and compute suared root to get distance
    dist_x_y = np.sqrt(np.sum(squared_diff_x_y, axis=1))

    # Get the indices of terminals which are at a distance less than r
    available_terminals = list(np.where(dist_x_y < r)[0])

    # Return the list of terminal IDs
    return available_terminals


def generate_transactions_table(
    customer_profile: pd.Series, start_date: str = "2018-04-01", nb_days: int = 10
) -> pd.DataFrame:
    """Generates transactions for a given customer.

    Args:
        customer_profile (pd.Series): Customer profile row from the customer profiles table.
        start_date (str, optional): Start date for transaction data. Defaults to "2018-04-01".
        nb_days (int, optional): Number of days to generate transactions for. Defaults to 10.

    Returns:
        pd.DataFrame: Transactions table.
    """
    customer_transactions = []

    random.seed(int(customer_profile.customer_id))
    np.random.seed(int(customer_profile.customer_id))

    # For all days
    for day in range(nb_days):
        # Random number of transactions for that day
        nb_tx = np.random.poisson(customer_profile.mean_nb_tx_per_day)

        # If nb_tx positive, let us generate transactions
        if nb_tx > 0:
            for tx in range(nb_tx):
                # Time of transaction: Around noon, std 20000 seconds. This choice aims at simulating the fact that
                # most transactions occur during the day.
                time_tx = int(np.random.normal(86400 / 2, 20000))

                # If transaction time between 0 and 86400, let us keep it, otherwise, let us discard it
                if (time_tx > 0) and (time_tx < 86400):
                    # Amount is drawn from a normal distribution
                    amount = np.random.normal(customer_profile.mean_amount, customer_profile.std_amount)

                    # If amount negative, draw from a uniform distribution
                    if amount < 0:
                        amount = np.random.uniform(0, customer_profile.mean_amount * 2)

                    amount = np.round(amount, decimals=2)

                    if len(customer_profile.available_terminals) > 0:
                        terminal_id = random.choice(customer_profile.available_terminals)

                        customer_transactions.append(
                            [time_tx + day * 86400, day, customer_profile.customer_id, terminal_id, amount]
                        )

    customer_transactions = pd.DataFrame(
        customer_transactions, columns=["tx_time_seconds", "tx_time_days", "customer_id", "terminal_id", "tx_amount"]
    )

    if len(customer_transactions) > 0:
        customer_transactions["tx_datetime"] = pd.to_datetime(
            customer_transactions["tx_time_seconds"], unit="s", origin=start_date
        )
        customer_transactions = customer_transactions[
            ["tx_datetime", "customer_id", "terminal_id", "tx_amount", "tx_time_seconds", "tx_time_days"]
        ]

    return customer_transactions
