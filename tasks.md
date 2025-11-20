Capstone Project Roadmap: Real-Time Network Traffic Visualizer

Project Name: Packet-Sleuth (Tentative)
Goal: Build a dashboard that visualizes network traffic in real-time and flags suspicious activity.
Tech Stack: Python, Scapy, Flask, SocketIO, HTML/CSS, JavaScript (Chart.js).

Phase 1: Environment Setup & "Hello World"

Focus: Getting the tools installed and ensuring everyone can run the code.

All Team Members

✅ Create GitHub Repository: Set up a shared repo and invite all members.

[ ] Create Virtual Environment: Set up a Python venv to keep libraries isolated.

[ ] Install Dependencies: Run pip install flask flask-socketio scapy.

[ ] Permission Check: Verify everyone knows how to run Python scripts as Administrator/Root (required for sniffing).

Backend Team (Python Focus)

[ ] Basic Scapy Script: Write a simple script that sniffs 10 packets and prints them to the console.

[ ] Filter Test: Modify the script to only capture TCP traffic (ignore UDP/ARP for now).

[ ] Data Extraction: Write a function to extract Source IP, Destination IP, and Destination Port from a packet.

Frontend Team (Web Focus)

[ ] Hello World Flask: Create app.py and templates/index.html to ensure a basic web page loads.

[ ] Layout Sketch: Draw a quick whiteboard sketch of where the Charts and the Alert Logs will go on the screen.

Phase 2: The Bridge (Connecting Python to Web)

Focus: Moving data from the terminal to the browser using WebSockets.

Backend Team

[ ] Implement Threading: specific task to run the Scapy sniffing loop in a background thread so it doesn't block the Flask server.

[ ] Socket Emission: Replace print() statements with socketio.emit() to send packet data to the frontend.

[ ] JSON Formatting: Ensure the data sent is a clean dictionary (e.g., {'src': '192.168.1.5', 'dst': '8.8.8.8', 'len': 500}).

Frontend Team

[ ] Socket Client Setup: specific task to include the socket.io.js client library in the HTML head.

[ ] Console Logger: Write a JavaScript function socket.on('packet_data', ...) that simply logs the incoming data to the browser developer console (F12).

[ ] Integration Test: Run the app, generate traffic, and confirm data appears in the browser console.

Phase 3: Visualization (The "Wow" Factor)

Focus: Turning raw numbers into graphs.

Frontend Team

[ ] Chart.js Setup: Implement a Line Chart (packets per second) or a Bar Chart (top IP addresses).

[ ] Live Updating: Write the JavaScript logic to push new data points into the chart array and remove old ones (to create a scrolling effect).

[ ] Styling: Apply CSS (Bootstrap or Tailwind) to make the dashboard look like a "Security Operations Center" (Dark mode recommended).

Backend Team

[ ] Traffic Volume Logic: Instead of sending every single packet, calculate "Packets Per Second" and emit that integer every 1 second (reduces browser lag).

[ ] Protocol Detection: Add logic to identify if traffic is HTTP, HTTPS, DNS, or SSH based on port numbers.

Phase 4: Blue Team Features (The Security Logic)

Focus: Adding the cybersecurity logic that makes this a capstone.

Team Collaboration

[ ] Port Scan Detector:

Logic: If one Source IP hits > 10 unique Destination Ports in < 2 seconds.

Action: Emit a special "ALERT" event to the frontend.

[ ] Cleartext Detector:

Logic: If packet payload contains "HTTP" and "POST" (indicating unencrypted form submission).

Action: Flag as "Insecure Data Transmission".

[ ] Blacklist Check:

Logic: Create a list of "Bad IPs" (mock data). If a packet matches, trigger a Red Alert.

[ ] The Alert Box: Create a scrolling table in the UI that lists these security alerts in red text.

Phase 5: Polish & Documentation

Focus: Getting ready for Demo Day.

Final Polish

[ ] Stop/Start Button: Add a button in the UI to pause the sniffer.

[ ] Error Handling: Ensure the app doesn't crash if it sees a malformed packet.

[ ] Cleanup: Remove console logs and unused code.

Documentation (Required for Grading)

[ ] Architecture Diagram: Create a visual map of how Scapy talks to Flask.

[ ] README.md: Write clear instructions on how to install and run the tool (especially the sudo part).

[ ] Presentation Deck: Prepare the slides explaining why you built this and how it helps Blue Teams.