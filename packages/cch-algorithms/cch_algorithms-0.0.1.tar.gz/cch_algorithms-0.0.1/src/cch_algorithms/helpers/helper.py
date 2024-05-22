from sklearn.model_selection import StratifiedKFold, StratifiedShuffleSplit


def get_cross_val_obj(cv_method=None, n_splits=None, random_state=None, test_size=None):

    if cv_method == "skf":        
        cv_split_obj = StratifiedKFold(
            n_splits=n_splits, 
            shuffle=True, 
            random_state=random_state)
    elif cv_method == "sss":
        cv_split_obj = StratifiedShuffleSplit(
            n_splits=n_splits, 
            test_size=test_size, 
            random_state=random_state)
    else:
        raise Exception("* Must select valid cv method")
    
    return cv_split_obj