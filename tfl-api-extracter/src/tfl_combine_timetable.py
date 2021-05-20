from constant import Constant
from csv_handler import CSV_Handler
import pandas as pd
import glob, csv

class TFL_Combine_Underground_Timetable():
    def __init__(self, dataset_path=Constant.DATASET_COMBINED_TIMETABLE_DIR):
        self.dataset_path = dataset_path

    def merge_csv(self, lines):
        csv_handler = CSV_Handler(Constant.DATASET_COMBINED_TIMETABLE_DIR)

        # for line in lines:
        path = f"api_dataset/combined_timetable/"
        file_names = glob.glob(f"{path}/*.csv")
        combined_data = []
        for name in file_names:
            with open(name, mode="r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    combined_data.append(row)
        
        new_file = csv_handler.create_csv_file(combined_data, f"all.csv", "node1", "node2", "tstart", "tend", "line")
        df = pd.read_csv(open(new_file))
        sorted_df = df.sort_values("tstart", ascending=True)
        sorted_df.to_csv(f'{self.dataset_path}underground_all.csv', mode='a', header=True, index=False)


# s = TFL_Combine_Underground_Timetable()
# s.merge_csv(["circle"])
# s.merge_csv(["central", "hammersmith-city", "jubilee", "metropolitan", "northern", "piccadilly", "victoria", "waterloo-city"])