import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from sklearn.metrics import confusion_matrix



def plot_roc_curve(
        fpr,
        tpr,
        roc_auc,
        run_label,
        run_id,
        acc,
        precision,
        recall,
        specificity,
        f1,
        run_results_dir):

    # Plot ROC Curve
    # plt.figure()
    plt.plot(
        fpr,
        tpr,
        color='darkorange',
        lw=2,
        label=f'ROC curve (AUC = {roc_auc:.2f})'
    )

    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f"{run_label} ROC Curve")

    # Annotate ROC plot with metric values
    metrics_text = f"""
        Accuracy: {acc:.2f}\n
        Precision: {precision:.2f}\n
        Sensitivity: {recall:.2f}\n
        Specificity: {specificity:.2f}\n
        F1 Score: {f1:.2f}
        """
    plt.annotate(
            metrics_text,
            xy=(0.6, 0.3),
            xycoords='axes fraction',
            bbox=dict(boxstyle="round, pad=0.5", fc="white", ec="black", lw=2)
        )

    plt.legend(loc="lower right")

    fig_path = os.path.join(run_results_dir, f"{run_label}_roc_curve.png")
    plt.savefig(fig_path, dpi=600)
    plt.clf()


def plot_calibration_curve(run_label, run_id, prob_pred, prob_true,run_results_dir):
    # plt.figure()
    plt.plot(prob_pred, prob_true, marker='o', linewidth=1, label='Model')
    plt.plot(
        [0, 1],
        [0, 1],
        linestyle='--',
        color='red',
        label='Perfectly calibrated'
    )
    plt.xlabel('Mean Predicted Probability')
    plt.ylabel('Fraction of Positives')
    plt.title(f'{run_label} Calibration Curve')
    plt.legend()

    fig_path = os.path.join(run_results_dir, f"{run_label}_calibration_curve.png")
    plt.savefig(
        fig_path,
        dpi=600)
    plt.clf()


def plot_confusion_matrix(
        run_label,
        run_id,
        y_true,
        y_pred,
        normalize=False,
        cmap=plt.cm.Blues,
        run_results_dir="results"):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    title = f'{run_label} Confusion Matrix'
    if normalize:
        title += ' (normalized)'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    classes = [0, 1]

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()

    fig_path = os.path.join(run_results_dir, f"{run_label}_confusion_matrix.png")
    fig.savefig(
        fig_path,
        dpi=600)
    fig.clear()
