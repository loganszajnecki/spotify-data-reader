import os
import json
from datetime import datetime
from track import SpotifyTrack

class SpotifyHistoryDebugger:
    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.tracks = []
        self.failed_files = []
        self._load_data()

    def _load_data(self):
        for file_path in self.file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for entry in data:
                        if self._validate_entry(entry):
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
                            print(f"Skipping malformed entry: {entry}")
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")
                self.failed_files.append(file_path)

    def _validate_entry(self, entry):
        # Check if all the necessary fields are present in the entry
        required_fields = ['master_metadata_track_name', 'master_metadata_album_artist_name',
                           'master_metadata_album_album_name', 'ms_played', 'ts', 'skipped']
        return all(field in entry for field in required_fields)

    def get_total_tracks(self):
        return len(self.tracks)

    def get_failed_files(self):
        return len(self.failed_files)

    def get_total_playback_time(self):
        return sum(track.playback_time for track in self.tracks) / (1000 * 60 * 60)

    def get_skipped_tracks_count(self):
        return sum(1 for track in self.tracks if track.skipped)

    def get_track_summary(self):
        # Return a summary of the tracks by artist, track name, and album
        artist_summary = {}
        track_summary = {}
        album_summary = {}

        for track in self.tracks:
            artist_summary[track.artist_name] = artist_summary.get(track.artist_name, 0) + 1
            track_summary[track.track_name] = track_summary.get(track.track_name, 0) + 1
            album_summary[track.album_name] = album_summary.get(track.album_name, 0) + 1

        return artist_summary, track_summary, album_summary

    def get_data_preview(self, num_samples=5):
        # Show a preview of a few track records
        return [(track.track_name, track.artist_name, track.album_name, track.playback_time) for track in self.tracks[:num_samples]]

    def display_debug_info(self):
        print(f"Total Files Processed: {len(self.file_paths) - len(self.failed_files)}")
        print(f"Failed Files: {len(self.failed_files)}")
        print(f"Total Tracks Extracted: {self.get_total_tracks()}")
        print(f"Total Playback Time: {self.get_total_playback_time():.2f} hours")
        print(f"Skipped Tracks: {self.get_skipped_tracks_count()}")
        print(f"\nTrack Summary:")
        artist_summary, track_summary, album_summary = self.get_track_summary()

        print(f"Top 5 Artists (by track count):")
        for artist, count in sorted(artist_summary.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {artist}: {count} tracks")

        print(f"\nTop 5 Tracks (by play count):")
        for track, count in sorted(track_summary.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {track}: {count} plays")

        print(f"\nTop 5 Albums (by play count):")
        for album, count in sorted(album_summary.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {album}: {count} plays")

        print(f"\nData Preview (first 5 records):")
        for track in self.get_data_preview():
            print(f"  {track}")
