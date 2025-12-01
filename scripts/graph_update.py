import plotly.graph_objects as go

def update_json_data(sniffer, line_color="#58A6FF"):    
    # Get Raw Data
    time_data, pps_data = sniffer.get_pps_data()
    protocol_data = sniffer.get_protocol_data() if hasattr(sniffer, 'get_protocol_data') else {}    

    REQUIRED_POINTS = 60
    
    # --- PERSISTENT STATE MANAGEMENT ---
    if not hasattr(sniffer, 'frame_counter'):
        sniffer.frame_counter = 0
    if not hasattr(sniffer, 'max_seen_pps'):
        sniffer.max_seen_pps = 0

    # Increment the counter every time this function is called
    sniffer.frame_counter += 1
    
    # --- PADDING LOGIC ---
    current_len = len(pps_data)
    missing_count = max(0, REQUIRED_POINTS - current_len)

    # Pad Y-Values with 0
    pps_data = [0] * missing_count + list(pps_data)
    # Pad Time Labels with empty strings
    time_data = [""] * missing_count + list(time_data)
    
    # --- DYNAMIC SLIDING X-AXIS ---
    end_x = sniffer.frame_counter + REQUIRED_POINTS
    start_x = sniffer.frame_counter
    
    # Create the range of X values for this specific frame
    x_numeric_axis = list(range(start_x, end_x))
    
    # --- Y-AXIS HEIGHT ---
    current_window_max = max(pps_data) if pps_data else 0
    if current_window_max > sniffer.max_seen_pps:
        sniffer.max_seen_pps = current_window_max
    y_axis_max = max(sniffer.max_seen_pps * 1.2, 100) 

    # 3. Get latest value
    current_pps = pps_data[-1]

    # --- LINE CHART ---
    line_chart = [{
            'x': x_numeric_axis,   
            "y": pps_data,
            'type': "scatter",
            'mode': "lines",
            'lines': {
                "color": line_color,
                "width": 3,
                "shape": "spline", 
                "smoothing": 1.3
            },
            "fill": "tozeroy",
            "fillcolor": line_color, 
            "opacity": 0.2
    }]    
    
    line_layout = {
            "title": {
                'text': 'Live Traffic Speed',
                'font': {'size': 24, 'color': '#FFFFFF'} 
            },
            
            "uirevision": "true", 
            "transition": {"duration": 300, "easing": "quadratic-in-out"},
            
            "xaxis": {
                "title": {"text": "Time", "font": {"size": 18, "color": "#FFFFFF"}},
                "tickfont": {"size": 14, "color": "#CCCCCC"},
                "gridcolor": "rgba(255, 255, 255, 0.1)",
                "linecolor": "rgba(255, 255, 255, 0.2)",
                "tickangle": -45, 
                
                "tickmode": "array",
                # UPDATED: Removed [::2] slicing because 1 update now equals 1 second
                "tickvals": x_numeric_axis, 
                "ticktext": time_data,      
                
                "range": [start_x, end_x - 1], 
                "type": "linear" 
            },
            "yaxis": {
               "title": {"text": "Packets Per Second (PPS)", "font": {"size": 18, "color": "#FFFFFF"}},
               "color": "#FFFFFF",
               "tickfont": {"size": 14, "color": "#CCCCCC"},
               "gridcolor": "rgba(255, 255, 255, 0.1)",
               "linecolor": "rgba(255, 255, 255, 0.2)",
               "range": [0, y_axis_max] 
            },
            
            "margin": {"t": 50, "l": 80, "r": 30, "b": 80},
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)"
    }    

    # --- PIE CHART ---
    pie_chart = [{
            "labels": list(protocol_data.keys()),
            "values": list(protocol_data.values()),
            "type": "pie",
            "hole": 0.4,
            "marker": {
                "colors": ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"]
            },
            "textinfo": "label+percent",
            "textposition": "inside"
    }]
    
    pie_layout = {
            "title": {"text": "Protocol Distribution", "font": {"size": 24, "color": "#FFFFFF"}},
            "legend": {"font": {"size": 14, "color": "#CCCCCC"}}, 
            "margin": {"t": 50, "l": 30, "r": 30, "b": 50},
            "transition": {"duration": 300, "easing": "cubic-in-out"},
            "paper_bgcolor": "rgba(0,0,0,0)",
            "uirevision": "true",
            "hoverlabel": {
                "bgcolor": "#36454F",
                "font": {
                    "color": "#C9D1D9",
                    "size": 14
                }
            }
    }
    
    return current_pps, protocol_data, line_chart, line_layout, pie_chart, pie_layout