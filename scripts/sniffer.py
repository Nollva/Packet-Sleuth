import threading
import time
import datetime
from collections import deque, Counter
import scapy.all as scapy
from scapy.layers.inet import IP, TCP, UDP, ICMP

class OptimizedSniffer:
    # UPDATED: Default interval set to 1.0 second for 1:1 timing
    def __init__(self, history_size=60, update_interval=1.0):
        # --- CONFIGURATION ---
        self.update_interval = update_interval
        self.running = False
        self.lock = threading.Lock()

        # --- LIVE DATA (Fast Access) ---
        self._current_packet_count = 0
        self._total_protocols = Counter()

        # --- HISTORY DATA (For Graphing) ---
        self._pps_history = deque(maxlen=history_size)
        self._time_history = deque(maxlen=history_size)

    def _packet_callback(self, packet):
        """
        OPTIMIZATION TIP: Keep this function as short as possible.
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
        """
        while self.running:
            time.sleep(self.update_interval)
            
            with self.lock:
                # Calculate PPS (Packets / Interval)
                # Since interval is 1.0, this is now a direct 1:1 count (e.g. 50 packets * 1 = 50 PPS)
                pps = self._current_packet_count * (1 / self.update_interval)
                
                # Reset the counter for the next window
                self._current_packet_count = 0
                
                # Snapshot the data
                self._pps_history.append(pps)
                self._time_history.append(datetime.datetime.now().strftime("%H:%M:%S"))

    def start(self):
        if self.running:
            return
        
        # --- RESET LOGIC ---
        with self.lock:
            self._pps_history.clear()       
            self._time_history.clear()      
            self._current_packet_count = 0  
            self._total_protocols.clear()   

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

    # --- PUBLIC API ---

    def get_pps_data(self):
        with self.lock:
            return list(self._time_history), list(self._pps_history)

    def get_protocol_data(self):
        with self.lock:
            return dict(self._total_protocols)