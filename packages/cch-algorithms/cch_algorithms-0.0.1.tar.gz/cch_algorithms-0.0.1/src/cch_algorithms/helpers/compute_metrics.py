import logging
import matplotlib.pyplot as plt
from sklearn.calibration import calibration_curve
from sklearn.metrics import (accuracy_score, auc, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_curve, balanced_accuracy_score)

from cch_algorithms.helpers.plot_figues import (
    plot_calibration_curve,
    plot_confusion_matrix,
    plot_roc_curve
)


def compute_metrics(
        run_label=None, 
        run_id=None,
        y_test=None,
        y_pred=None, 
        y_prob=None,
        run_results_dir='results'):
    
    logging.info(f"* Computing classifier ({run_label}) performance metrics")
    
    result = {}
    result['acc'] = accuracy_score(y_test, y_pred)
    result["balanced_acc"] = balanced_accuracy_score(y_test, y_pred)
    result['precision'] = precision_score(y_test, y_pred)
    result['recall'] = recall_score(y_test, y_pred)
    result['f1'] = f1_score(y_test, y_pred)

    conf_matrix = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = map(int, conf_matrix.ravel())

    result['true_negative'] = tn
    result['false_positive'] = fp
    result['false_negative'] = fn
    result['true_positive'] = tp
    result['specificity'] = tn / (tn + fp)

    plot_confusion_matrix(
        run_label=run_label,
        run_id=run_id,
        y_true=y_test,
        y_pred=y_pred,
        normalize=False,
        cmap=plt.cm.Blues,
        run_results_dir=run_results_dir
    )

    if y_prob is not None:
        # Compute and store additional metrics
        fpr, tpr, thresholds = roc_curve(y_test, y_prob)
        result['roc_auc'] = auc(fpr, tpr)
        result['fpr'] = fpr.tolist()
        result['tpr'] = tpr.tolist()
        result['roc_thresholds'] = thresholds.tolist()
        prob_true, prob_pred = calibration_curve(y_test, y_prob, n_bins=10)
        result['calibration_curve_prob_true'] = prob_true.tolist()
        result['calibration_curve_prob_pred'] = prob_pred.tolist()

        plot_roc_curve(
            fpr,
            tpr,
            result['roc_auc'],
            run_label,
            run_id,
            result['acc'],
            result['precision'],
            result['recall'],
            result['specificity'],
            result['f1'],
            run_results_dir
        )

        plot_calibration_curve(run_label, run_id, prob_pred, prob_true,run_results_dir)

    return result

