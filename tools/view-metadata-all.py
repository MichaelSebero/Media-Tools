import os
import subprocess
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from mutagen.oggvorbis import OggVorbis
from mutagen.oggopus import OggOpus
from moviepy.editor import VideoFileClip
from pydub.utils import mediainfo

# ANSI escape codes for bold and reset
BOLD = '\033[1m'
RESET = '\033[0m'

def format_duration(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def get_audio_metadata(file_path):
    audio_info = None
    audio = None  # Initialize audio variable

    if file_path.lower().endswith('.flac'):
        audio = FLAC(file_path)
    elif file_path.lower().endswith(('.mp3', '.aac', '.m4a')):
        audio_info = mediainfo(file_path)
        # Assign a dummy value to 'audio' for consistency
        audio = EasyID3(file_path)
    elif file_path.lower().endswith(('.ogg', '.oga')):
        audio = OggVorbis(file_path)
    elif file_path.lower().endswith('.opus'):
        audio = OggOpus(file_path)
    else:
        raise ValueError("Unsupported audio file format.")

    if audio_info:
        bitrate = audio_info.get('bit_rate', None)
        duration = audio_info.get('duration', None)
        sample_rate = audio_info.get('sample_rate', None)
    else:
        bitrate = getattr(audio.info, 'bitrate', None) if hasattr(audio, 'info') else None
        duration = getattr(audio.info, 'length', None) if hasattr(audio, 'info') else None
        sample_rate = getattr(audio.info, 'sample_rate', None) if hasattr(audio, 'info') else None

    # Return metadata as a sorted list of tuples
    return sorted([
        ("Artist", audio.get("artist", [""])[0] if audio else None),
        ("Album", audio.get("album", [""])[0] if audio else None),
        ("Bitrate", str(bitrate)),
        ("Duration", format_duration(float(duration)) if duration else None),
        ("Sample Rate", str(sample_rate) if sample_rate else None),
    ])

def get_video_metadata(file_path):
    video = VideoFileClip(file_path)

    # Use ffprobe to get detailed information
    ffprobe_cmd = ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", file_path]
    audio_codec = subprocess.check_output(ffprobe_cmd, universal_newlines=True).strip()

    # Return metadata as a sorted list of tuples
    return sorted([
        ("Duration", format_duration(video.duration)),
        ("Resolution", str(video.size)),
        ("FPS", str(video.fps)),
        ("Audio Codec", audio_codec if audio_codec else None),
        ("Sample Rate", str(video.audio.fps) if video.audio else None),
    ])

def main():
    # Ask user for directory location
    dir_path = input("Enter the path to the directory containing media files: ")

    if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
        print("Directory not found. Please provide a valid directory path.")
        return

    # Get a sorted list of filenames
    filenames = sorted(os.listdir(dir_path))

    # Iterate through all sorted files in the directory
    for filename in filenames:
        file_path = os.path.join(dir_path, filename)

        # Check if it's an audio or video file
        if file_path.lower().endswith(('.mp3', '.flac', '.wav', '.aac', '.m4a', '.ogg', '.oga', '.opus')):
            print(f"\n{BOLD}File:{RESET} {filename}")
            metadata = get_audio_metadata(file_path)
            for key, value in metadata:
                print(f"{BOLD}{key}{RESET}: {value}")
        elif file_path.lower().endswith(('.mp4', '.mkv', '.avi')):
            print(f"\n{BOLD}File:{RESET} {filename}")
            metadata = get_video_metadata(file_path)
            for key, value in metadata:
                print(f"{BOLD}{key}{RESET}: {value}")

    print("\nMetadata extraction complete.")

if __name__ == "__main__":
    main()
