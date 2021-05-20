import overtime as ot
from abc import ABC, abstractmethod
import json

class Graph_Network_Parser(ABC):
    def __init__(self, graph):
        self.graph = graph
        self.node_labels = graph.nodes.labels()
        self.edge_labels = graph.edges.labels()

    @abstractmethod
    def parse_graph_to_json(self):
        pass

class Temporal_DiGraph_Network_Parser(Graph_Network_Parser):
    def __init__(self, graph):
        super().__init__(graph)
        self.start_time = graph.edges.start_times()
        self.end_time = graph.edges.end_times()

    def parse_graph_to_json(self):
        json_dataset = {}
        json_dataset['nodes'] = self.node_labels
        json_dataset['edges'] = []
        for i in range(len(self.edge_labels)):
            edge = {}
            source_and_target = self.edge_labels[i].split("-") 
            edge['source'] = source_and_target[0]
            edge['target'] = source_and_target[1]
            edge['start'] = self.start_time[i]
            edge['end'] = self.end_time[i]
            json_dataset['edges'].append(edge)
        return json.dumps(json_dataset)

underground = ot.TemporalDiGraph('UndergroundLine', data=ot.CsvInput('./data/mini_underground_all.csv'))
visual = Temporal_DiGraph_Network_Parser(underground)
result = visual.parse_graph_to_json()
print(result)


