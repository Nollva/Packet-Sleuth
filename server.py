from scripts.sniffer import OptimizedSniffer
from flask import Flask, render_template, jsonify

# Set the DDOS Threshold for the percentages to be calculated later on.
ATTACK_THRESHOLD = 1000 

# Setup the flask web framework.
app = Flask(__name__)
app.config['SECRET_KEY'] = "9876543210"

# Enable the sniffer class.
sniffer = OptimizedSniffer()

# Flask WebApp Routes.
@app.route("/")
def home():
    '''Renders the index.html template for the homepage.'''
    return render_template("index.html")

# @app.route('/graph_data')
# def update_json_data():
    '''Takes the data from the sniffer, turns it into graphs and variable,
    and then returns it as a json when requested.'''
    # Xavier's Code Goes right here.

    # update the code to ensure certain variables are conducted and especially the return statement from https://gemini.google.com/share/4602bd1f9fc5


@app.route('/start_sniffer', methods=['POST'])
def start_sniffer():
    '''Starts the sniffer and updates the status when the button is pressed on the frontend.'''
    sniffer.start()
    return jsonify({"status": "Sniffer Started", "running": True})

@app.route('/stop_sniffer', methods=['POST'])
def stop_sniffer():
    '''Stops the sniffer and updates the status when the button is pressed on the frontend.'''
    sniffer.stop()
    return jsonify({"status": "Sniffer Stopped", "running": False})

@app.route('/status_sniffer', methods=['GET'])
def check_status():
    '''Gets the status of the sniffer to ensure it is running still even if the page reloads.'''
    return jsonify({"running": sniffer.running})


# If ran locally from the file, start the server, otherwise do nothing.
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)