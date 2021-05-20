import csv, collections
import pandas as pd
import glob
from constant import Constant

class CSV_Handler():
    def __init__(self, dataset_path=Constant.DATASET_DIR):
        self.dataset_path = dataset_path

    # Converts Json dataset to cvs, where *fields is the array of fields
    def create_csv_file(self, dataset, file_name: str, *fields):
        with open(f'{self.dataset_path}/{file_name}', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(fields)
            for i in range(len(dataset)):
                data_row = []
                for field in fields:
                    data_row.append(dataset[i][field])
                writer.writerow(data_row)
        return f'{self.dataset_path}{file_name}'


    def get_single_field_from_csv(self, file_name: str, field: str):
        result = []
        with open(f'{self.dataset_path}/{file_name}', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                result.append(row[field])
        return result
    
    # Converts selected fields from CSV - combine them and make dataframe
    def get_multiple_field_from_csv(self, file_name: str,  *fields):
        df = pd.read_csv(f'{self.dataset_path}/{file_name}')
        frames = []
        for field in fields:
            frames.append(df[field])
        result = pd.concat(frames, join="outer", axis=1)
        return result

    def read_csv(self, file_name: str):
        df = pd.read_csv(f'{self.dataset_path}/{file_name}')
        return df

csv_root = CSV_Handler()