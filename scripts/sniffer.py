import threading
import time
import datetime
from collections import deque, Counter
import scapy.all as scapy
from scapy.layers.inet import IP, TCP, UDP, ICMP

class OptimizedSniffer:
    def __init__(self, history_size=60, update_interval=0.5):
        # --- CONFIGURATION ---
        self.update_interval = update_interval
        self.running = False
        self.lock = threading.Lock()

        # --- LIVE DATA (Fast Access) ---
        # These are incremented rapidly by the packet capture
        self._current_packet_count = 0
        self._total_protocols = Counter()

        # --- HISTORY DATA (For Graphing) ---
        # Deques automatically pop the oldest item when full (Optimization)
        self._pps_history = deque(maxlen=history_size)
        self._time_history = deque(maxlen=history_size)

    def _packet_callback(self, packet):
        """
        OPTIMIZATION TIP: Keep this function as short as possible.
        Every microsecond here = missed packets during high load.
        """
        # 1. Cheap filtering (Don't process if no IP layer)
        if IP not in packet:
            return

        # 2. Identify Protocol (Fastest way)
        proto = "OTHER"
        if packet.haslayer(TCP):
            proto = "TCP"
        elif packet.haslayer(UDP):
            proto = "UDP"
        elif packet.haslayer(ICMP):
            proto = "ICMP"

        # 3. Thread-Safe Update
        with self.lock:
            self._current_packet_count += 1
            self._total_protocols[proto] += 1

    def _monitor_loop(self):
        """
        Background process that handles the 'Time Series' logic.
        It runs independently of the Flask server.
        """
        while self.running:
            time.sleep(self.update_interval)
            
            with self.lock:
                # Calculate PPS (Packets / Interval)
                # If interval is 0.5s, we multiply count by 2 to get 'Per Second' rate
                pps = self._current_packet_count * (1 / self.update_interval)
                
                # Reset the counter for the next window
                self._current_packet_count = 0
                
                # Snapshot the data
                self._pps_history.append(pps)
                self._time_history.append(datetime.datetime.now().strftime("%H:%M:%S"))

    def start(self):
        if self.running:
            return
        
        # --- 1. RESET LOGIC (Added) ---
        with self.lock:
            self._pps_history.clear()       # Clears the Line Graph history
            self._time_history.clear()      # Clears the Time axis
            self._current_packet_count = 0  # Resets the "Current Speed" to 0
            self._total_protocols.clear()   # Resets the Pie Chart & Total Packet count
        # ------------------------------

        self.running = True
        
        # 1. Start the Packet Sniffer Thread
        self.sniff_thread = threading.Thread(target=self._start_sniffing)
        self.sniff_thread.daemon = True
        self.sniff_thread.start()

        # 2. Start the Monitor/History Thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def _start_sniffing(self):
        # store=0 is the #1 Memory Optimization
        scapy.sniff(prn=self._packet_callback, store=0, stop_filter=lambda x: not self.running)

    def stop(self):
        self.running = False

    # --- PUBLIC API (What Flask Calls) ---

    def get_pps_data(self):
        """
        Returns two lists: [Time Stamps], [PPS Values]
        Perfect for Plotly's x and y axes.
        """
        with self.lock:
            return list(self._time_history), list(self._pps_history)

    def get_protocol_data(self):
        """
        Returns a dictionary of all protocols seen so far.
        Example: {'TCP': 1500, 'UDP': 400, 'ICMP': 20}
        """
        with self.lock:
            return dict(self._total_protocols)