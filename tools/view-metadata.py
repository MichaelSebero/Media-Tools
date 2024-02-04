import os
from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
from mutagen.oggopus import OggOpus
from moviepy.editor import VideoFileClip
from pydub.utils import mediainfo
import subprocess

# ANSI escape codes for bold and reset
BOLD = '\033[1m'
RESET = '\033[0m'

def format_duration(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def get_audio_metadata(file_path):
    try:
        audio_info = None
        audio = None

        if file_path.lower().endswith(('.mp3', '.aac', '.m4a')):
            audio_info = mediainfo(file_path)
            if file_path.lower().endswith('.m4a'):
                audio = MP4(file_path)
            else:
                audio = EasyID3(file_path)
        elif file_path.lower().endswith('.opus'):
            audio = OggOpus(file_path)
        elif file_path.lower().endswith('.flac'):
            audio = FLAC(file_path)
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

        return {
            "Album": audio.get("album", [""])[0] if audio and audio.get("album") else None,
            "Artist": audio.get("artist", [""])[0] if audio and audio.get("artist") else None,
            "Bitrate": str(bitrate),
            "Duration": format_duration(float(duration)) if duration else None,
            "Sample Rate": str(sample_rate) if sample_rate else None,
        }
    except Exception as e:
        print(f"Error while extracting audio metadata: {e}")
        return None

def get_video_metadata(file_path):
    try:
        video = VideoFileClip(file_path)

        audio_codec = None
        if video.audio:
            try:
                # Use FFmpeg to query audio codec
                cmd = ['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                audio_codec = result.stdout.strip() if result.returncode == 0 else None
            except Exception as e:
                print(f"Error while querying audio codec using FFmpeg: {e}")

        return {
            "Audio Codec": audio_codec,
            "Duration": format_duration(video.duration),
            "FPS": str(video.fps),
            "Resolution": str(video.size),
            "Sample Rate": str(video.audio.fps) if video.audio else None,
        }
    except Exception as e:
        print(f"Error while extracting video metadata: {e}")
        return None

def main():
    # Ask the user for file location
    file_path = input("Enter the path to the media file: ")

    if not os.path.exists(file_path):
        print("File not found. Please provide a valid file path.")
        return

    # Check if it's an audio or video file
    if file_path.lower().endswith(('.mp3', '.aac', '.m4a', '.opus', '.flac')):
        metadata = get_audio_metadata(file_path)
        if metadata:
            for key, value in sorted(metadata.items()):
                print(f"{BOLD}{key}{RESET}: {value if value is not None else 'None'}")
    elif file_path.lower().endswith(('.mp4', '.mkv', '.avi')):
        metadata = get_video_metadata(file_path)
        if metadata:
            for key, value in sorted(metadata.items()):
                print(f"{BOLD}{key}{RESET}: {value if value is not None else 'None'}")
    else:
        print("Unsupported file format. Please provide a valid audio or video file.")

if __name__ == "__main__":
    main()
