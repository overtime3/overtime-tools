from flask import Flask, render_template
import overtime as ot
from graph_network_parser import Temporal_DiGraph_Network_Parser
app = Flask(__name__)

@app.route("/")
def home():
    return "This is Flask server hosting Overtime dataset."

@app.route("/temporal")
def temporal_network():
    return render_template("dir-temporal-graph-network.html")

@app.route("/dataset")
def dataset():      # This is hardcode example of dataset, in the future the user can select their own file 
    underground = ot.TemporalDiGraph('UndergroundLine', data=ot.CsvInput('./data/mini_jubilee.csv'))
    visual = Temporal_DiGraph_Network_Parser(underground)
    res = visual.parse_graph_to_json()
    return res

app.run()
