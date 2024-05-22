from statistics import mean
from scipy import stats
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from cch_algorithms.helpers.compute_metrics import compute_metrics
from cch_algorithms.helpers.helper import get_cross_val_obj


def run_xgb_classifier_binary(
        run_label=None,
        run_id=None, 
        run_results_dir=None,
        X=None, 
        y=None, 
        random_state=42, 
        test_size=0.3,
        n_splits=5,
        cv_method="sss"):
    
    cv_results = None

    if n_splits is None or n_splits == 1:

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state)

        model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
        model.fit(X_train, y_train)

        # Predict class label and probabilities
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

        result = compute_metrics(
            run_label=run_label,
            run_id=run_id, 
            y_test=y_test, 
            y_pred=y_pred, 
            y_prob=y_prob,
            run_results_dir=run_results_dir)

        return result, cv_results

    elif n_splits > 1:
        # Get cross validation object
        cv_split_obj = get_cross_val_obj(cv_method=cv_method, n_splits=n_splits, test_size=test_size, random_state=random_state)

        cv_results = {}
        current_split = 0
        for train_index, test_index in tqdm(cv_split_obj.split(X, y), total=len(range(n_splits)), desc="Running CV"):  # noqa: E501

            current_split += 1
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]

            model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
            model.fit(X_train, y_train)

            # Predict class label and probabilities
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]

            # Compute metrics and plot graphs for current_split
            cv_result = compute_metrics(
                run_label=f"{run_label}_cv{current_split}", 
                run_id=run_id, 
                y_test=y_test, 
                y_pred=y_pred, 
                y_prob=y_prob,
                run_results_dir=run_results_dir)

            # Curate total cross-validation dictionary with each metric
            for k, v in cv_result.items():
                if k not in cv_results:
                    cv_results[k] = []
                cv_results[k].append(v)

        result = {}
        mlflow_metrics = ["acc","f1","precision","recall","roc_auc","specificity","balanced_acc"]
        for k,v in cv_results.items():
            if k in mlflow_metrics:
                result[f"cv_mean_{k}"] = np.mean(cv_results[k])
                result[f"cv_SD_{k}"] = np.std(cv_results[k])
                result[f"cv_median_{k}"] = np.median(cv_results[k])
                result[f"cv_025%_{k}"] = np.percentile(cv_results[k], 2.5)
                result[f"cv_975%_{k}"] = np.percentile(cv_results[k], 97.5)

        return result, cv_results
    
    else:
        raise Exception(f"Must specify valid positive integer for n_splits or None. n_splits currently: {n_splits}")
