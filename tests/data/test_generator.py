import pytest

from src.data.generator import (
    generate_customer_profiles_table,
    generate_dataset,
    generate_terminal_profiles_table,
    generate_transactions_table,
    get_list_terminals_within_radius,
)


@pytest.fixture(scope="session")
def customer_df():
    return generate_customer_profiles_table(n_customers=5)


@pytest.fixture(scope="session")
def terminal_df():
    return generate_terminal_profiles_table(n_terminals=5)


@pytest.fixture(scope="session")
def dataset():
    return generate_dataset(n_customers=5, n_terminals=5, nb_days=5, start_date="2018-04-01", r=50)


@pytest.fixture(scope="session")
def transactions_df(customer_df, terminal_df):
    x_y_terminals = terminal_df[["loc_long_coord", "loc_lat_coord"]].values.astype(float)
    customer_df["available_terminals"] = customer_df.apply(
        lambda x: get_list_terminals_within_radius(x, x_y_terminals=x_y_terminals, r=50), axis=1
    )
    return (
        customer_df.groupby("customer_id")
        .apply(lambda x: generate_transactions_table(x.iloc[0], nb_days=5))
        .reset_index(drop=True)
    )


def test_generate_customer_profiles_table(customer_df):
    assert len(customer_df) == 5
    assert all(
        col in customer_df.columns
        for col in [
            "customer_id",
            "loc_long_coord",
            "loc_lat_coord",
            "mean_amount",
            "std_amount",
            "mean_nb_tx_per_day",
        ]
    )
    assert all(long >= 0 and long <= 100 for long in customer_df.loc_long_coord.values)
    assert all(lat >= 0 and lat <= 100 for lat in customer_df.loc_lat_coord.values)
    assert all(mean >= 5 and mean <= 100 for mean in customer_df.mean_amount.values)
    assert all(std >= 2.5 and std <= 50 for std in customer_df.std_amount.values)
    assert all(mean >= 0 and mean <= 4 for mean in customer_df.mean_nb_tx_per_day.values)


def test_generate_terminal_profiles_table(terminal_df):
    assert len(terminal_df) == 5
    assert all(col in terminal_df.columns for col in ["terminal_id", "loc_long_coord", "loc_lat_coord"])
    assert all(long >= 0 and long <= 100 for long in terminal_df["loc_long_coord"])
    assert all(lat >= 0 and lat <= 100 for lat in terminal_df["loc_lat_coord"])


def test_get_list_terminals_within_radius(customer_df, terminal_df):
    # We first get the geographical locations of all terminals as a numpy array
    x_y_terminals = terminal_df[["loc_long_coord", "loc_lat_coord"]].values.astype(float)
    # And get the list of terminals within radius of 50 for the last customer
    available_terminals = get_list_terminals_within_radius(customer_df.iloc[4], x_y_terminals=x_y_terminals, r=50)
    assert len(available_terminals) == 2
    assert all(term in available_terminals for term in [2, 3])


def test_generate_transactions_table(customer_df, terminal_df, transactions_df):
    assert len(transactions_df) > 0
    assert all(
        col in transactions_df.columns
        for col in ["tx_time_seconds", "tx_time_days", "customer_id", "terminal_id", "tx_amount"]
    )
    assert all(amount >= 0 for amount in transactions_df.tx_amount.values)


def test_generate_dataset(dataset):
    customer_table, terminal_table, transaction_table = dataset
    assert len(customer_table) == 5
    assert len(terminal_table) == 5
    assert len(transaction_table) > 0
