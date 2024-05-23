import numpy as np
import pandas as pd
import sklearn.metrics
import lightgbm as lgb

from typing import Tuple, Optional, Any
from flameai.train import gen_threshold


def lgb_feature_importance(gbm: lgb.Booster) -> None:
    """
    Calculate the importance of features in a LightGBM model.

    :param gbm: The trained LightGBM model.
    """
    items = [(k, v) for k, v in zip(gbm.feature_name(), gbm.feature_importance())]
    sorted_items = sorted(items, key = lambda e: e[1], reverse = True)
    for i, (k, v) in enumerate(sorted_items):
        print(f'[rank {i+1}] {k}: {v}')


def eval_continuous(y_true, y_pred) -> None:
    """
    This function evaluates the performance of a regression model by calculating
    the Mean Absolute Error (MAE), Mean Squared Error (MSE), and R-squared (R2) score.

    :param y_true: An array of the true values.
    :param y_label: An array of the model's predictions.
    """
    mae = sklearn.metrics.mean_absolute_error(y_true, y_pred)
    mse = sklearn.metrics.mean_squared_error(y_true, y_pred)
    r2_score = sklearn.metrics.r2_score(y_true, y_pred)

    print(f'mae: {mae:.5f}')
    print(f'mse: {mse:.5f}')
    print(f'r2_score: {r2_score:.5f}')


def eval_binary(y_true,
                y_pred,
                threshold: Optional[float] = None,
                n_trials: int = 200,
                ret: bool = False
    ) -> Optional[Tuple[Any, float]]:
    """
    Evaluate a binary classification task.

    :param y_true: An array of the true values.
    :param y_pred: An array of the model's predictions.
    :param threshold: The threshold determines whether a case is positive or negative.
                      If the predicted probability is greater than the threshold,
                      it is classified as a positive case. If the threshold is None,
                      the optuna package will be used to calculate the optimal threshold.
    :param n_trials: The number of trials for threshold generation. Default is 200.
    :param ret: A flag to indicate if the function should return the predicted labels and threshold. Default is False.
    :return: If ret is True, the function returns the predicted labels and threshold.
    """

    # Metrics that can be directly calculated using y_pred
    auc = sklearn.metrics.roc_auc_score(y_true = y_true, y_score = y_pred)
    log_loss = sklearn.metrics.log_loss(y_true = y_true, y_pred = y_pred)

    # If the threshold does not exist, obtain it
    if threshold is None:
        threshold = gen_threshold(y_true, y_pred, n_trials)

    y_label = [1 if e > threshold else 0 for e in y_pred]

    # Metrics that require the predicted labels (y_label)
    acc = sklearn.metrics.accuracy_score(y_true = y_true, y_pred = y_label)
    precision = sklearn.metrics.precision_score(y_true = y_true, y_pred = y_label)
    recall = sklearn.metrics.recall_score(y_true = y_true, y_pred = y_label)
    f1 = sklearn.metrics.f1_score(y_true = y_true, y_pred = y_label)
    cm = sklearn.metrics.confusion_matrix(y_true = y_true, y_pred = y_label)
    tn, fp, fn, tp = cm.ravel()

    print(f'threshold: {threshold:.5f}')
    print(f'accuracy: {acc:.5f}')
    print(f'precision: {precision:.5f}')
    print(f'recall: {recall:.5f}')
    print(f'f1_score: {f1:.5f}')
    print(f'auc: {auc:.5f}')
    print(f'cross-entropy loss: {log_loss:.5f}')
    print(f'True Positive (TP): {tp}')
    print(f'True Negative (TN): {tn}')
    print(f'False Positive (FP): {fp}')
    print(f'False Negative (FN): {fn}')
    print(f'confusion matrix:\n{cm}')

    if ret:
        return y_label, threshold