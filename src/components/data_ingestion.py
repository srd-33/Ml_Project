import os,sys,pandas as pd

from src.exception import CustonException
from src.logger import logging
from dataclasses import dataclass

from sklearn.model_selection import train_test_split

from src.components.data_tranform import DataTranformation


@dataclass
class DataIngestionConfig:
    train_data_path:str = os.path.join('artifacts','train.csv')
    test_data_path:str = os.path.join('artifacts','test.csv')
    raw_data_path:str = os.path.join('artifacts','data.csv')

class DataIngestion:
    def __init__(self):
        self.data_ing_config = DataIngestionConfig()

    def init_data_ing(self):

        logging.info("Entered the data ingestion method ")

        try:
            df = pd.read_csv('notebook/data/stud.csv')
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.data_ing_config.train_data_path),exist_ok=True)

            df.to_csv(self.data_ing_config.raw_data_path,index=False,header=True)

            logging.info("Train test split initiated")
            train_data, test_data = train_test_split(df,train_size=0.25,random_state=42)

            train_data.to_csv(self.data_ing_config.train_data_path,index=False,header=True)
            test_data.to_csv(self.data_ing_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of the data iss completed")

            return (
                self.data_ing_config.train_data_path,
                self.data_ing_config.test_data_path
            )
        
        except Exception as e:
            raise CustonException(e,sys)

if __name__ =="__main__":

    obj = DataIngestion()
    train_data,test_data=obj.init_data_ing()

    data_transformation=DataTranformation()
    train_arr,test_arr,_=data_transformation.init_data_transform(train_data,test_data)