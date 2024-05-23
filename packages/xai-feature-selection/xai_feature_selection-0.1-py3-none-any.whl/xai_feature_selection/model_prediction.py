import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from lime.lime_tabular import LimeTabularExplainer
import shap
import traceback


class Model:
    li_reg_model = LinearRegression()
    log_reg_model = LogisticRegression()
    ranfor_reg_model = RandomForestRegressor(random_state=42)
    ranfor_cla_model = RandomForestClassifier(random_state=42)

    reg_model_list = [li_reg_model, ranfor_reg_model]
    cla_model_list = [log_reg_model, ranfor_cla_model]

    def __init__(
        self,
        model_type: int,
        model_choice: int,
        data_file_path: str,
        predict_columns: list[str],
        columns_to_remove: list[str] = None,
    ) -> None:
        self.model_type = "classification" if model_type else "regression"
        self.model_sub_type = "tree" if model_choice else "linear"
        self.model = (
            self.cla_model_list[model_choice]
            if model_type
            else self.reg_model_list[model_choice]
        )
        if self.read_file(data_file_path):
            if columns_to_remove:
                self.remove_unwanted_columns(columns_to_remove)
            if self.encode_text_data():
                if self.split_xy_data(predict_columns):
                    self.prepare_data_for_model()

    def train(self):
        self.model.fit(self.x_train, self.y_train)

    def predict(self):
        self.y_pred = self.model.predict(self.x_test)

    def explain(self):
        self.explain_lime()
        self.explain_shap()

        return self.lime_importances_df, self.shap_importance_df

    def explain_lime(self):
        lime_importances = []
        linear_explainer = LimeTabularExplainer(
            self.x_train.values,
            feature_names=self.x_train.columns,
            mode=self.model_type,
        )
        # Loop through each instance in the test set
        for i in range(len(self.x_test[:20])):
            exp = linear_explainer.explain_instance(
                self.x_test.iloc[i],
                self.model.predict_proba
                if self.model_type == "classification"
                else self.model.predict,
                num_features=len(self.x_train.columns),
            )

            # Initialize an array for current instance's importances
            row_importances = np.zeros(len(self.x_train.columns))

            # Get the explanation as a list of (feature, importance) tuples
            exp_list = exp.as_list()

            # Map the feature importances to the correct indices
            for feature, importance in exp_list:
                # Extract feature name
                feature_name = feature.split()[0]
                if feature_name in self.x_train.columns:
                    feature_index = self.x_train.columns.get_loc(feature_name)
                    row_importances[feature_index] = importance

            # Append the importances for the current instance to the list
            lime_importances.append(row_importances)

        self.lime_importances_df = pd.DataFrame(
            lime_importances, columns=self.x_train.columns
        )

    def explain_shap(self):
        explainer = (
            shap.TreeExplainer(self.model, self.x_train)
            if self.model_sub_type == "tree"
            else shap.LinearExplainer(self.model, self.x_train)
        )
        shap_values = explainer.shap_values(
            self.x_test[:150]
        )  # you can modify this size for time being
        shap_sum = np.abs(shap_values).mean(axis=0)
        self.shap_importance_df = pd.DataFrame(
            {
                "feature": self.x_train.columns,
                "shap_importance": shap_sum,
            }
        )

    def read_file(self, file_path):
        try:
            self.df = pd.read_csv(file_path)
            return True
        except Exception:
            traceback.print_exc()
            print("Error:", Exception)
            print("Unable to read file! Check with file path.")

    def encode_text_data(self):
        try:
            if self.model_type == "classification":
                self.df.dropna(axis=0, inplace=True)

            string_columns = self.df.select_dtypes(include=["object"]).columns.tolist()
            encoder = LabelEncoder()

            for column in string_columns:
                self.df[column] = encoder.fit_transform(self.df[column])

            if self.model_type == "regression":
                self.df.fillna(0, inplace=True)

            return True
        except Exception as e:
            print("Error:", type(e).__name__)
            print("Unable to encode text data")

    def split_xy_data(self, predict_columns):
        try:
            self.y_data = self.df[predict_columns]
            self.df.drop(predict_columns, axis=1, inplace=True)
            self.x_data = self.df
            return True
        except Exception:
            print("Error:", Exception)
            print("Not able to split x and y data")

    def prepare_data_for_model(self):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.x_data,
            self.y_data,
            train_size=0.7,
            test_size=0.3,
            random_state=100,
        )

    def remove_unwanted_columns(self, column_list):
        self.df = self.df.drop(column_list, axis=1)
