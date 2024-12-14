import matplotlib.pyplot as plt
from history import SpotifyHistory

class SpotifyReport:
    @staticmethod
    def display_results(history):
        # Display general information
        print(f"Total Tracks Played: {history.get_total_tracks()}")
        print(f"Total Playback Time: {history.get_total_playback_time():.2f} hours")
        print(f"Skipped Tracks: {history.get_skipped_tracks_count()}")

        # Display top artists, tracks, and albums
        print("\nTop 10 Artists:")
        for artist, count in history.get_top_entities('artist_name'):
            print(f"  {artist}: {count} plays")

        print("\nTop 10 Tracks:")
        for track, count in history.get_top_entities('track_name'):
            print(f"  {track}: {count} plays")

        print("\nTop 10 Albums:")
        for album, count in history.get_top_entities('album_name'):
            print(f"  {album}: {count} plays")

        # Generate and display histograms for top 50 artists and top 50 tracks
        top_50_artists = history.get_top_entities('artist_name', 50)
        top_50_tracks = history.get_top_entities('track_name', 50)

        # Create and display histograms for artists and tracks
        SpotifyReport.plot_histogram(top_50_artists, "Top 50 Artists", "Artist", "Number of Plays")
        SpotifyReport.plot_histogram(top_50_tracks, "Top 50 Tracks", "Track", "Number of Plays")
        plt.show()
    @staticmethod
    def plot_histogram(top_entities, title, x_label, y_label):
        # Unzip the list of tuples into two lists (labels and values)
        labels, values = zip(*top_entities)

        # Create a new figure for each histogram
        fig, ax = plt.subplots(figsize=(10, 6))  # Create a new figure and axes

        # Plot a horizontal bar chart
        ax.barh(labels, values, color='skyblue')

        # Set labels and title
        ax.set_xlabel(y_label)
        ax.set_ylabel(x_label)
        ax.set_title(title)

        # Invert the y-axis to have the highest values at the top
        ax.invert_yaxis()
        # Add the value at the end of each bar
        bars = ax.barh(labels, values, color='skyblue')
        for bar in bars:
            width = bar.get_width()  # Get the width of the bar (the value)
            ax.text(width + 1, bar.get_y() + bar.get_height() / 2,  # Positioning text just after the bar
                    str(width), va='center', ha='left', color='black', fontsize=10)
