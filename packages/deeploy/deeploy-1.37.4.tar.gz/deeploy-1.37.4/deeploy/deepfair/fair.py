from typing import Union

import numpy as np
import pandas as pd
from fairlearn.metrics import (
    demographic_parity_difference,
    demographic_parity_ratio,
    equalized_odds_difference,
    equalized_odds_ratio,
)

import deeploy.fairsd as fsd
from deeploy.enums import QualityFactor, SearchAlgorithm
from deeploy.fairsd.algorithms import ResultSet
from deeploy.fairsd.sgdescription import Description


class DeeployFairLab:
    def __init__(
        self,
        X: Union[pd.DataFrame, np.array],
        y_true: Union[pd.DataFrame, np.array],
        y_pred: Union[pd.DataFrame, np.array],
        feature_names: list[str] = None,
        sensitive_features: list[str] = None,
        nominal_features: list[str] = None,
        numeric_features: list[str] = None,
        ignore_features: list[str] = None,
    ):
        """
        X : pandas dataframe or numpy array
        y_true : numpy array, pandas dataframe, or pandas Series
            represent the ground truth
        y_pred : numpy array, pandas dataframe, or pandas Series
            contain the predicted values
        feature_names : list of string
            this parameter is necessary if the user supply X in a numpy array
        sensitive_features: list of string
            this list contains the names of the sensitive features
        nominal_features : optional, list of strings
            list of nominal features
        numeric_features : optional, list of strings
            list of numeric features
        """
        self.X = X
        self.y_true = y_true
        self.y_pred = y_pred
        self.feature_names = feature_names
        self.sensitive_features = sensitive_features
        self.nominal_features = nominal_features
        self.numeric_features = numeric_features
        if ignore_features:
            if sensitive_features:
                self.ignore_features = list(set(ignore_features) ^ set(sensitive_features))
            else:
                self.ignore_features = ignore_features
            if len(ignore_features) > len(self.ignore_features):
                raise Exception(
                    "Sensitive features found in ignore features list. Cannot ignore provided sensitive features"
                )
            if self.ignore_features:
                self.X = self.X.drop(self.ignore_features, axis=1)
                if self.nominal_features:
                    self.nominal_features = list(
                        set(self.nominal_features) ^ set(self.ignore_features)
                    )
                if self.numeric_features:
                    self.numeric_features = list(
                        set(self.numeric_features) ^ set(self.ignore_features)
                    )

    def find_sub_groups(
        self,
        quality_factor: QualityFactor,
        algorithm: SearchAlgorithm = SearchAlgorithm.dssd,
        beam_width: int = 20,
        a: float = 0.9,
        result_set_size: int = 5,
        **kwargs,
    ) -> ResultSet:
        """
        :param quality_factor: QualityFactor this parameter corresponds to the choice of quality factor
        :param algorithm: SearchAlgorithm this parameter corresponds to the choice of search algorithm to utilize to obtain sub groups
        :param beam_width: int
        :param a: float this parameter correspond to the alpha parameter. the more a is high, the less the subgroups redundancy is taken into account.
        """

        task = fsd.SubgroupDiscoveryTask(
            self.X,
            self.y_true,
            self.y_pred,
            qf=str(quality_factor),
            feature_names=self.feature_names,
            sensitive_features=self.sensitive_features,
            nominal_features=self.nominal_features,
            numeric_features=self.numeric_features,
            result_set_size=result_set_size,
        )

        if algorithm == SearchAlgorithm.beam_search:
            result_set = fsd.BeamSearch(beam_width=beam_width).execute(task)
        elif algorithm == SearchAlgorithm.dssd:
            result_set = fsd.DSSD(beam_width=beam_width, a=a).execute(task)

        self.result_set = result_set
        return result_set

    def get_subgroup_mask(self, index: int = 0) -> list[bool]:
        """
        This method generate and return the feature of the subgroup with index = sg_index in the current object.
            The result is indeed a boolean array of the same length of the dataset X.
            Each i-th element of this array is true iff the i-th tuple of X belong to the subgroup with index sg_index.
        :param index: int subgroup_index
        :return boolean: mapping for subgroup wrt to original dataset
        """
        sg_feature = self.result_set.sg_feature(sg_index=index, X=self.X)
        return sg_feature

    def get_subgroup_description(self, index: int = 0) -> Description:
        """
        This method returns description of subgroup at provided index from resultset
        :param index: int subgroup_index
        """
        return self.result_set.get_description(index)

    def get_user_defined_subgroup(self, multi_condition_func) -> pd.DataFrame:
        return self.X.apply(multi_condition_func, axis=1).astype("bool")

    def get_all_metrics_for_user_defined_subgroup(self, multi_condition_func):
        """
        multi_condition_func: lambda function condition on row for defining subgroup.
            eg. lambda row: ((row['age'] > 35) & (row['sex'] in ['Male', 'Nonbinary']) )
        """
        defined_subgroup = self.get_user_defined_subgroup(multi_condition_func)
        demographic_parity_difference_val = demographic_parity_difference(
            y_true=self.y_true, y_pred=self.y_pred, sensitive_features=defined_subgroup
        )
        demographic_parity_ratio_val = demographic_parity_ratio(
            y_true=self.y_true, y_pred=self.y_pred, sensitive_features=defined_subgroup
        )
        equalized_odds_difference_val = equalized_odds_difference(
            y_true=self.y_true, y_pred=self.y_pred, sensitive_features=defined_subgroup
        )
        equalized_odds_ratio_val = equalized_odds_ratio(
            y_true=self.y_true, y_pred=self.y_pred, sensitive_features=defined_subgroup
        )
        return (
            ("demographic_parity_difference", demographic_parity_difference_val),
            ("demographic_parity_ratio", demographic_parity_ratio_val),
            ("equalized_odds_difference", equalized_odds_difference_val),
            ("equalized_odds_ratio", equalized_odds_ratio_val),
        )
