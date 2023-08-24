from typing import Sequence, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score


def evaluate_predictions(
    predictions_df: pd.DataFrame,
    output_feature: str,
    prediction_feature: str,
    top_k_list: Sequence[int],
    rounded: bool = True,
) -> dict:
    """Evaluate predictions using AUC-ROC, average precision and card precision@k.

    Args:
        predictions_df (pd.DataFrame): Predictions dataframe.
        output_feature (str): Name of the output feature.
        prediction_feature (str): Name of the prediction feature.
        top_k_list (Sequence[int]): Top k values to compute card precision@k.
        rounded (bool, optional): Whether to round to three decimals. Defaults to True.

    Returns:
        dict: Dictionary containing the evaluation results.
    """
    auc_roc = roc_auc_score(predictions_df[output_feature], predictions_df[prediction_feature])
    ap = average_precision_score(predictions_df[output_feature], predictions_df[prediction_feature])

    results = {
        "auc_roc": auc_roc,
        "average_precision": ap,
    }

    for top_k in top_k_list:
        _, _, mean_card_precision_top_k = card_precision_top_k(predictions_df, top_k)
        results[f"card_precision@{top_k}"] = mean_card_precision_top_k

    if rounded:
        results = {k: round(v, 3) for k, v in results.items()}

    return results


def card_precision_top_k(
    predictions_df: pd.DataFrame, top_k: int, remove_detected_compromised_cards: bool = True
) -> Tuple[list, float]:
    """Calculate card precision top k.

    Args:
        predictions_df (pd.DataFrame): Predictions dataframe.
        top_k (int): Top k value.
        remove_detected_compromised_cards (bool, optional): Remove cards from consideration once they are compromised.
            Defaults to True.

    Returns:
        Tuple[list, float]: Number of compromised cards per day, card precision top k per day, mean card precision top k
    """
    # sort days by increasing order
    list_days = list(predictions_df.tx_time_days.unique())
    list_days.sort()

    # initialize list of detected compromised cards
    list_detected_compromised_cards = []

    card_precision_top_k_per_day_list = []
    nb_compromised_cards_per_day_list = []

    # for each day, compute precision top k
    for day in list_days:
        df_day = predictions_df[predictions_df.tx_time_days == day]

        # remove already detected compromised cards
        df_day = df_day[~df_day.customer_id.isin(list_detected_compromised_cards)]

        nb_compromised_cards_per_day_list.append(len(df_day[df_day.tx_fraud == 1].customer_id.unique()))

        # compute precision top k
        compromised_cards_day, card_precision_top_k = card_precision_top_k_day(df_day, top_k)

        # append results
        card_precision_top_k_per_day_list.append(card_precision_top_k)

        # update list of detected compromised cards
        if remove_detected_compromised_cards:
            list_detected_compromised_cards.extend(compromised_cards_day)

    # compute the mean
    mean_card_precision_top_k = np.array(card_precision_top_k_per_day_list).mean()

    return nb_compromised_cards_per_day_list, card_precision_top_k_per_day_list, mean_card_precision_top_k


def card_precision_top_k_day(df_day: pd.DataFrame, top_k: int) -> Tuple[Sequence[int], float]:
    """Calculate card precision top k for a given day.

    Args:
        df_day (pd.DataFrame): Predictions dataframe for a given day.
        top_k (int): Top k value.

    Returns:
        Tuple[Sequence[int], float]: List of compromised cards, card precision top k.
    """
    # take max of predictions and label tx_fraud for each customer
    # sort by decreasing order of fraudulent prediction
    df_day = df_day.groupby("customer_id").max().sort_values(by="predictions", ascending=False).reset_index(drop=False)

    # get the top k most suspicious cards
    df_day_top_k = df_day.head(top_k)
    list_detected_compromised_cards = list(df_day_top_k[df_day_top_k.tx_fraud == 1].customer_id)

    # compute precision top k
    card_precision_top_k = len(list_detected_compromised_cards) / top_k

    return list_detected_compromised_cards, card_precision_top_k
