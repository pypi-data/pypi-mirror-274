import pandas as pd
import sklearn.metrics
import matplotlib.pyplot as plt
import seaborn as sns


def roc_curve(y_true, y_score) -> None:
    """
    Plot the ROC curve.

    :param y_true: An array of true binary labels.
    :param y_score: An array of predicted probabilities.
    """
    fpr, tpr, thresholds = sklearn.metrics.roc_curve(y_true = y_true, y_score = y_score)
    auc = sklearn.metrics.roc_auc_score(y_true = y_true, y_score = y_score)
    print(f'AUC: {auc:.5f}')

    plt.figure(figsize = (8, 6))
    plt.plot(fpr, tpr, label='ROC curve (AUC = {:.2f})'.format(auc))

    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.xlabel('False Positive Rate (FPR)')
    plt.ylabel('True Positive Rate (TPR)')
    plt.legend(loc="lower right")
    plt.grid(True, linestyle = 'dashed', alpha = 0.5)

    plt.show()


def confusion_matrix(y_true, y_label) -> None:
    """
    Generates and plots a confusion matrix of a classification model.

    :param y_true: An array of true binary labels.
    :param y_label: An array of labels predicted by the model.
    """
    cm = sklearn.metrics.confusion_matrix(y_true = y_true, y_pred = y_label)
    cm_matrix = pd.DataFrame(data = cm,
                             columns = ['Predict Negative:0', 'Predict Positive:1'], 
                             index = ['Actual Negative:0', 'Actual Positive:1'])
    sns.heatmap(cm_matrix, annot = True, fmt = 'd', cmap = 'YlGnBu')