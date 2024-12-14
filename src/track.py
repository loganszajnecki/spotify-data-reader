from datetime import datetime

class SpotifyTrack:
    def __init__(self, track_name, artist_name, album_name, playback_time, timestamp, skipped):
        self.track_name = track_name
        self.artist_name = artist_name
        self.album_name = album_name
        self.playback_time = playback_time
        self.timestamp = timestamp
        self.skipped = skipped
