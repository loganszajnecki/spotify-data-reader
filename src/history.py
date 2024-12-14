import json
from collections import Counter
from datetime import datetime
from track import SpotifyTrack

class SpotifyHistory:
    def __init__(self, file_paths, avg_track_length_ms=180000, min_play_percentage=0.1):
        self.file_paths = file_paths
        self.tracks = []
        self.failed_files = []
        self.avg_track_length_ms = avg_track_length_ms  # Average length of track in milliseconds (3 minutes)
        self.min_play_percentage = min_play_percentage  # 10% of track length to count as a valid play
        self._load_data()

    def _load_data(self):
        for file_path in self.file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for entry in data:
                        if self._validate_entry(entry, file_path):
                            # Calculate dynamic threshold (10% of estimated track length)
                            dynamic_threshold = self.avg_track_length_ms * self.min_play_percentage
                            
                            # Only add the track if it was played for long enough (compared to dynamic threshold)
                            if entry['ms_played'] >= dynamic_threshold or not entry['skipped']:
                                track = SpotifyTrack(
                                    track_name=entry['master_metadata_track_name'],
                                    artist_name=entry['master_metadata_album_artist_name'],
                                    album_name=entry['master_metadata_album_album_name'],
                                    playback_time=entry['ms_played'],
                                    timestamp=datetime.strptime(entry['ts'], '%Y-%m-%dT%H:%M:%SZ'),
                                    skipped=entry['skipped']
                                )
                                self.tracks.append(track)
                        else:
                            self.failed_files.append(file_path)
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")
                self.failed_files.append(file_path)

    def _validate_entry(self, entry, file_path):
        # Validate required fields
        required_fields = ['master_metadata_track_name', 'master_metadata_album_artist_name',
                           'master_metadata_album_album_name', 'ms_played', 'ts', 'skipped']
        
        missing_fields = [field for field in required_fields if field not in entry]
        if missing_fields:
            print(f"Skipping entry from {file_path}: Missing fields {missing_fields}")
            return False
        
        # Additional checks (e.g., valid data types)
        if not isinstance(entry['ms_played'], int) or not isinstance(entry['ts'], str):
            print(f"Skipping entry from {file_path}: Invalid data types")
            return False
        
        return True

    def get_total_tracks(self):
        return len(self.tracks)

    def get_failed_files(self):
        return len(self.failed_files)

    def get_total_playback_time(self):
        return sum(track.playback_time for track in self.tracks) / (1000 * 60 * 60)

    def get_skipped_tracks_count(self):
        return sum(1 for track in self.tracks if track.skipped)

    def get_track_summary(self):
        # Return summary by artist, track name, and album
        artist_summary = {}
        track_summary = {}
        album_summary = {}

        for track in self.tracks:
            artist_summary[track.artist_name] = artist_summary.get(track.artist_name, 0) + 1
            track_summary[track.track_name] = track_summary.get(track.track_name, 0) + 1
            album_summary[track.album_name] = album_summary.get(track.album_name, 0) + 1

        return artist_summary, track_summary, album_summary

    def get_top_entities(self, attribute, top_n=10):
        # Get the top entities (artists, tracks, albums) from the attribute
        summary = {}
        for track in self.tracks:
            value = getattr(track, attribute)
            if value:
                summary[value] = summary.get(value, 0) + 1
        
        # Sort by the count and return the top n
        sorted_entities = sorted(summary.items(), key=lambda x: x[1], reverse=True)
        return sorted_entities[:top_n]


