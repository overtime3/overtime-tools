from constant import Constant
from csv_handler import CSV_Handler
from json_handler import Json, DisplayJson
import pandas as pd
import glob, csv

class TFL_Timetable_Converter():
    def __init__(self, dataset_path=Constant.DATASET_TIMETABLE_DIR):
        self.dataset_path = dataset_path

    # Remove space from string, we do not want space in file names
    def replace_space_by_delimiter(self, string: str) -> str:
        return "".join([Constant.FILE_NAME_DELIMITER if string[i].isspace() else string[i] for i in range(len(string))])

    def get_underground_timetable(self):
        csv_root = CSV_Handler()
        csv_timetable = CSV_Handler("api_dataset/timetable")
        csv_line = CSV_Handler(Constant.DATASET_LINE_DIR)
        json_timetable = Json(Constant.DATASET_TIMETABLE_DIR)
        tube_line = csv_root.get_single_field_from_csv('tfl_tube_mode.csv', "id") 

        for line in tube_line:
            if line == "district":
                stop_point_id_list = csv_line.get_single_field_from_csv(f'{line}_stop_points.csv', "id")
                line_stop_point_full_name_list = csv_line.get_single_field_from_csv(f'{line}_stop_points.csv', "commonName")
                line_stop_point_name_list = csv_line.get_single_field_from_csv(f'{line}_stop_points.csv', "commonName")

                # Remove the Underground Station from the name
                for i in range(len(line_stop_point_name_list)):
                    line_stop_point_name_list[i] = line_stop_point_name_list[i].replace(' Underground Station', '')
                
                # Dictionary containing each stop point id and corresponding stop point name (commonName)
                line_stations = {stop_point_id_list[i]: line_stop_point_name_list[i] for i in range(len(stop_point_id_list))}

                # Iterate through all the stations in the current line
                for i in range(len(line_stop_point_full_name_list)):
                    stop_point_no_space = self.replace_space_by_delimiter(line_stop_point_full_name_list[i])

                    inbound = json_timetable.read_json_file(f'{line}/{stop_point_no_space}_{line}_inbound_timetable.json')
                    outbound = json_timetable.read_json_file(f'{line}/{stop_point_no_space}_{line}_outbound_timetable.json')
                    
                    current = None
                    for direction in ['inbound', 'outbound']:
                        if direction == 'inbound':
                            current = inbound
                        else:
                            current = outbound

                        if "httpStatusCode" in current:
                            if current["httpStatusCode"] == 500:
                                print("File has errors")
                        else:
                            if "statusErrorMessage" in current:
                                if current == 'The stop you selected has now been removed from the route, and therefore we cannot show you a timetable. The route page will be updated shortly to reflect these changes.':
                                    print("There is no timetable availble for this station")
                            else:
                                print(f"Converting {line_stop_point_full_name_list[i]} {direction}")
                                line_id = current['lineId']
                                line_name = current['lineName']
                                if current['timetable']['departureStopId'] in line_stations:
                                    curr_station = line_stations[current['timetable']['departureStopId']]
                                    next_station = line_stations[current['timetable']['routes'][0]['stationIntervals'][0]['intervals'][0]['stopId']] #Grab first station from current
                                    next_station_distance = current['timetable']['routes'][0]['stationIntervals'][0]['intervals'][0]['timeToArrival'] # Distance from current station to the next

                                    journey_time = current['timetable']['routes'][0]['schedules'][0]['knownJourneys']
                                    data = []
                                    for time in journey_time:
                                        hour, minute = int(time['hour']), int(time['minute'])
                                        tstart = int((hour*100) + minute)
                                        tend = int(tstart + next_station_distance)
                                        data.append({'node1': curr_station, 'node2': next_station, 'tstart': tstart, 'tend': tend, 'line': f'{line_name} line to {next_station}'})
                                    csv_timetable.create_csv_file(data, f'{line_id}/csv/{curr_station}-{line_id}_{direction}.csv', 'node1', 'node2', 'tstart', 'tend', 'line')


t = TFL_Timetable_Converter()
t.get_underground_timetable()
