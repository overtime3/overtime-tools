import json, requests
from constant import Constant
from tfl_default import TFL_Default
from csv_handler import CSV_Handler
from json_handler import Json
from tfl_json_to_csv_converter import TfL_Json_to_Csv_Converter

# Get information related to a given line. For example victoria line
class Tfl_Line_Stop_Points(TFL_Default):

    # Get all stations under a specific line
    def get_line_stations(self, line):
        url = f'{Constant.ROOT_URL}/Line/{line}/StopPoints?{Constant.API_KEY}'
        response = requests.get(url)
        self.response_status_code(response.status_code, url)
        dataset = response.json()
        return dataset
    
    def get_and_save_tfl_dataset(self, line, dataset_path=Constant.DATASET_LINE_DIR):
        file_name = f'{line}_line_stop_points.json'
        dataset = self.get_line_stations(line)
        file_path = self.save_as_json(dataset, file_name, dataset_path)
        return file_path


if __name__ == "__main__":

    filename = "tfl_tube_mode.csv"
    csv = CSV_Handler()
    tfl_tube_line = csv.get_single_field_from_csv(filename, "id")

    line_station = Tfl_Line_Stop_Points()

    # For each line call the TfL API to get stop points and save it as JSON
    for line in tfl_tube_line:
        respond = line_station.get_and_save_tfl_dataset(line)

    # Now use the converter to extract the field from JSON to CSV 
    converter = TfL_Json_to_Csv_Converter()
    converter.convert_stop_points(transport_line_csv_name=filename, mode="tube")
