import time
from typing import Sequence

import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.preprocessing import MinMaxScaler


def fit_model(
    classifier: BaseEstimator,
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    input_features: Sequence[str],
    output_feature: str,
    scale: bool = True,
) -> dict:
    """Fit a classifier and return predictions.

    Args:
        classifier (BaseEstimator): Classifier to fit.
        train_df (pd.DataFrame): Training dataframe.
        test_df (pd.DataFrame): Test dataframe.
        input_features (Sequence[str]): List of input features.
        output_feature (str): Output feature.
        scale (bool, optional): Whether to scale using min-max scaler. Defaults to True.

    Returns:
        dict: Dictionary containing the classifier, predictions, training and prediction execution time.
    """
    if scale:
        # Scale data using min-max scaler
        scaler = MinMaxScaler()
        train_df[input_features] = scaler.fit_transform(train_df[input_features])
        test_df[input_features] = scaler.transform(test_df[input_features])

    start_time = time.time()
    classifier.fit(train_df[input_features], train_df[output_feature])
    training_time = time.time() - start_time

    start_time = time.time()
    predictions_test = classifier.predict_proba(test_df[input_features])[:, 1]
    prediction_time = time.time() - start_time

    predictions_train = classifier.predict_proba(train_df[input_features])[:, 1]

    return {
        "classifier": classifier,
        "predictions_train": predictions_train,
        "predictions_test": predictions_test,
        "training_execution_time": training_time,
        "prediction_execution_time": prediction_time,
    }
