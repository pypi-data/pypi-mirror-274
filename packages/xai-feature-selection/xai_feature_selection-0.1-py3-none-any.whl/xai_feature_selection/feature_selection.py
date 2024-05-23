import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class FeatureSelect:
    def __init__(self, shap_data: pd.DataFrame, lime_data: pd.DataFrame) -> None:
        """constructor to initiate variables, shap and lime dataframes"""
        self.feature_data = []
        self.shap_data = shap_data
        self.lime_data = lime_data

    def prepare_weights(self) -> None:
        """preparing weights from the shap dataframe"""
        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(self.shap_data[["shap_importance"]])
        self.shap_data["weights"] = scaled.flatten()
        self.weight_data = self.shap_data[["feature", "weights"]].to_dict("tight")[
            "data"
        ]
        self.total_weight = np.sum(self.shap_data.weights)
        self.threshold_value = (self.total_weight / 100) * 80

        compare_threshold_value = 0
        for idx, row in (
            self.shap_data.sort_values(by="weights", ascending=False)
            .reset_index()
            .iterrows()
        ):
            if self.is_threshold_reached(compare_threshold_value):
                self.threshold_index = idx
                break
            compare_threshold_value += row["weights"]

    def is_threshold_reached(self, comparison_value):
        if comparison_value >= self.threshold_value:
            return True
        else:
            return False

    def calculate_feature_values(self) -> None:
        """Calculating total weighted average value for each record in the lime dataframe and calculating the column wise average and a record with highest weighted average
        and produces two dataframes by calculating average of column wise range and max row data and dividing both column wise range and max row data"""
        self.lime_weights_df = pd.DataFrame()
        self.final_average_dataframe = pd.DataFrame()
        self.final_division_dataframe = pd.DataFrame()

        for idx, row in self.lime_data.iterrows():
            for data in self.weight_data:
                self.lime_weights_df.loc[idx, data[0]] = row[data[0]] * data[1]
        self.column_wise_average = dict(self.lime_weights_df.mean())

        for idx, row in self.lime_weights_df.iterrows():
            self.lime_weights_df.loc[idx, "weighted_average"] = (
                np.sum(row) / self.total_weight
            )

        self.max_row = self.lime_weights_df[
            self.lime_weights_df["weighted_average"]
            == self.lime_weights_df["weighted_average"].max()
        ]
        self.max_row = self.max_row.reset_index(drop=True)
        self.column_total = pd.DataFrame(self.column_wise_average, index=[0])

        for idx, row in self.column_total.iterrows():
            for col in list(self.column_total.columns):
                self.final_average_dataframe.loc[idx, col] = (
                    row[col] + self.max_row.loc[idx, col]
                ) / 2
                # self.final_division_dataframe.loc[idx, col] = (
                #     self.max_row.loc[idx, col] / row[col] if row[col] > 0 else 1
                # )
        self.final_average_dataframe = self.final_average_dataframe.T
        self.final_average_dataframe = self.final_average_dataframe.reset_index()
        self.final_average_dataframe.columns = ["features", "ranking"]
        self.final_average_dataframe = self.final_average_dataframe.sort_values(
            by="ranking", ascending=False
        )

        self.best_features_df = self.final_average_dataframe[: self.threshold_index + 1]

    def get_best_feature_data(self) -> None:
        """Returning the two data with different calculated values for the features"""
        return {
            "data": self.best_features_df,
            "total_features": self.threshold_index + 1,
            "total_weight": self.total_weight,
            "threshold_value": self.threshold_value,
        }


"""Below is the code example for fetching the best feature data"""
# obj=FeatureSelect(shap_data=shap_importance_df,lime_data=lime_importances_df)
# obj.prepare_weights()
# obj.calculate_feature_values()
#
