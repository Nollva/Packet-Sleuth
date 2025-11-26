from scripts.sniffer import OptimizedSniffer
from scripts.graph_update import update_json_data
from flask import Flask, render_template, jsonify
import json
import plotly.graph_objects as go

ATTACK_THRESHOLD = 5000 

app = Flask(__name__)
app.config['SECRET_KEY'] = "9876543210"

sniffer = OptimizedSniffer()

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/graph_data')
def json_data_update():
    # 1. Get raw data first to calculate DDoS status
    # FIX: Using 'get_pps_data' (Original Name)
    _, pps_history = sniffer.get_pps_data()
    current_pps = pps_history[-1] if pps_history else 0
    
    # 2. Logic: Calculate DDoS Chance
    ddos_chance = int((current_pps / ATTACK_THRESHOLD) * 100)
    if ddos_chance > 100: ddos_chance = 100
    
    # 3. Logic: Determine Color
    if ddos_chance > 80:
        graph_color = '#dc3545' # Red
    elif ddos_chance > 50:
        graph_color = '#ffc107' # Yellow
    else:
        graph_color = '#58A6FF' # Blue (Your original color)

    # 4. Generate Graphs (Passing the color we just chose)
    curr_pps, proto_data, line_chart, line_layout, pie_chart, pie_layout = update_json_data(sniffer=sniffer, line_color=graph_color)
    
    # 5. Logic: Calculate Total Packets & Top Protocol
    total_packets = sum(proto_data.values())
    if proto_data:
        top_protocol = max(proto_data, key=lambda k: proto_data[k])
    else:
        top_protocol = "N/A"

    return jsonify({
            # Data Cards
            "total_packets": total_packets,
            "top_protocol": top_protocol,
            "ddos_chance": ddos_chance,
            
            # Graphs
            "current_pps": curr_pps,
            "line_chart": line_chart,
            "line_layout": line_layout,
            "pie_chart": pie_chart,
            "pie_layout": pie_layout
        })

@app.route('/start_sniffer', methods=['POST'])
def start_sniffer():
    sniffer.start()
    return jsonify({"status": "Sniffer Started", "running": True})

@app.route('/stop_sniffer', methods=['POST'])
def stop_sniffer():
    sniffer.stop()
    return jsonify({"status": "Sniffer Stopped", "running": False})

@app.route('/status_sniffer', methods=['GET'])
def check_status():
    return jsonify({"running": sniffer.running})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)