import sys,os, pandas as pd,numpy as np

from src.exception import CustonException
from src.logger import logging

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.utils import save_object

from dataclasses import dataclass

@dataclass
class DataTransformConfig():
    preprocessor_path = os.path.join('artifacts','preprocessor.pkl')

class DataTranformation:
    def __init__(self):
        self.preprocessorconfig = DataTransformConfig()

    def get_data_transform(self):
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())

                ]
            )

            cat_pipeline=Pipeline(

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                ]

            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)

                ]


            )

            return preprocessor
        
        except Exception as e:
            raise CustonException(e,sys)
        
    def init_data_transform(self,train_path,test_path):

        try:
            
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info("Obtaining preprocessing object")

            pre_procc_obj = self.get_data_transform()

            target_column_name="math_score"

            ind_fea_train = train_df.drop(columns=[target_column_name],axis=1)
            tgt_fet_train = train_df[target_column_name]

            ind_fea_test = test_df.drop(columns=[target_column_name],axis=1)
            tgt_fet_test = test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            ind_tain_arr = pre_procc_obj.fit_transform(ind_fea_train)
            ind_test_arr = pre_procc_obj.transform(ind_fea_test)

            train_arr = np.c_[
                ind_tain_arr,np.array(tgt_fet_train)
            ]

            test_arr = np.c_[
               ind_test_arr,np.array(tgt_fet_test)
            ]

            save_object(

                file_path=self.preprocessorconfig.preprocessor_path,
                obj=pre_procc_obj

            )

            return (
                train_arr,
                test_arr,
                self.preprocessorconfig.preprocessor_path
            )


        except Exception as e:
            raise CustonException(e,sys)

        
