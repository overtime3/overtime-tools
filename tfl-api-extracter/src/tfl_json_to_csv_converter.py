from csv_handler import CSV_Handler
from json_handler import Json, DisplayJson
from constant import Constant

# Extract all the stop points or stations for each given line
class TfL_Json_to_Csv_Converter:  
    def __init__(self, line_directory=Constant.DATASET_LINE_DIR):
        self.csv_handler = CSV_Handler() 
        self.csv_line_handler = CSV_Handler(line_directory)

    def convert_stop_points(self, transport_line_csv_name, mode):
        tube_transportation_line = self.csv_handler.get_single_field_from_csv(transport_line_csv_name, "id")
        json_handler = DisplayJson(Constant.DATASET_LINE_DIR)

        for line in tube_transportation_line:
            json_handler.read_json_file(f"{line}_line_stop_points.json")
            line_json = json_handler.get_readable_json()

            total_tube = 0
            # Check if all of the stop points within each entry contains the tube mode, hence it is underground
            # We do not want stop points that is available on for buses
            for _, stop_point in enumerate(line_json):
                if mode in stop_point["modes"]:
                    total_tube += 1
            accuracy = (total_tube/len(line_json)) * 100
            print(f'The accuracy for {line} is {accuracy}%')

            if int(accuracy) == 100:
                self.csv_line_handler.create_csv_file(line_json, f'{line}_stop_points.csv', "id", "commonName", "stopType", "lat", "lon")

converter = TfL_Json_to_Csv_Converter()
converter.convert_stop_points(transport_line_csv_name="tfl_tube_mode.csv", mode="tube")