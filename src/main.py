import os
from history import SpotifyHistory
from report import SpotifyReport
from debugger import SpotifyHistoryDebugger

if __name__ == "__main__":
    debugMode = False
    # Path to the data directory
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    
    # Collect all JSON file paths in the directory
    file_paths = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.json')]

    if not file_paths:
        print("No JSON files found in the data directory.")
    else:
        if debugMode:
            debugger = SpotifyHistoryDebugger(file_paths)
            debugger.display_debug_info()
        else:
            # Process and report on the Spotify history
            history = SpotifyHistory(file_paths)
            SpotifyReport.display_results(history)
