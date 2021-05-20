import overtime as ot
from csv_handler import CSV_Handler

Line = "=====" * 15 + "\n"

##########################################################################
# London Underground dataset extraction
##########################################################################

root_csv = CSV_Handler("api_dataset")
line_csv = CSV_Handler("api_dataset/line")
timetable_csv = CSV_Handler("api_dataset/timetable")
combined_timetable_csv = CSV_Handler("api_dataset/combined_timetable")

tube_mode = root_csv.read_csv("tfl_tube_mode.csv")
northern_line = line_csv.read_csv("northern_stop_points.csv")
london_bridge_timetable = timetable_csv.read_csv("/northern/csv/London Bridge-northern_outbound.csv")
combined_northern_timetable = combined_timetable_csv.read_csv("/underground_northern.csv")

print(f'{Line}{tube_mode}')
print(f'{Line}{northern_line}')
print(f'{Line}{london_bridge_timetable}')
print(f'{Line}{combined_northern_timetable}')

##########################################################################
# Visualise the constructed graph
##########################################################################

underground_network = ot.TemporalDiGraph('London Underground', data=ot.CsvInput('./api_dataset/combined_timetable/mini_underground_all.csv'))
underground_nodes = underground_network.nodes.labels() 

ot.Circle(underground_network, ordered=True)
ot.Slice(underground_network)
ot.NodeScatter(underground_network)

sub_underground_network = underground_network.get_temporal_subgraph((920, 930))

ot.Circle(sub_underground_network, ordered=True)
ot.Slice(sub_underground_network)
ot.NodeScatter(sub_underground_network)


input("Press enter key to exit...")