import os
import random
import string
import threading
import tempfile
import subprocess
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import rotate

# Dictionary mapping rotation choices to degrees
rotation_choices = {
    "1": 90,
    "2": 180,
    "3": 270
}

def reencode_video(input_file, temp_dir):
    """Re-encode the video to ensure proper format and metadata."""
    try:
        temp_file = os.path.join(temp_dir, get_random_filename())
        command = ["ffmpeg", "-i", input_file, "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", temp_file]
        subprocess.run(command, check=True)
        return temp_file
    except Exception as e:
        print(f"Failed to re-encode {input_file}: {e}")
        return None

def rotate_video(input_file, output_file, angle, timeout=60):
    def target(input_file, output_file, angle):
        try:
            # Load the video clip
            clip = VideoFileClip(input_file)
            
            # Check if the video is vertical
            is_vertical = clip.size[0] < clip.size[1]  # Width is less than height
            
            # Adjust rotation angle if video is vertical
            if is_vertical and angle in [90, 270]:
                angle += 180
            
            # Rotate the video clip by the adjusted angle
            rotated_clip = rotate(clip, angle)
            
            # Ensure same video quality
            rotated_clip.write_videofile(output_file, codec='libx264', bitrate='5000k', fps=clip.fps)
            
            print(f"Video rotated successfully and saved as {output_file}")
        except Exception as e:
            print(f"An error occurred while processing {input_file}: {e}")
    
    thread = threading.Thread(target=target, args=(input_file, output_file, angle))
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        print(f"Processing {input_file} took too long and was skipped.")
        thread.join()  # Ensure the thread is terminated properly

def get_random_filename(extension=".mp4"):
    # Create a filename with a mix of letters (uppercase and lowercase) and digits
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(8)) + extension

def create_rotated_directory(base_dir):
    rotated_dir = os.path.join(base_dir, "rotated")
    if not os.path.exists(rotated_dir):
        os.makedirs(rotated_dir)
    return rotated_dir

def rotate_videos_in_directory(directory, angle):
    rotated_dir = create_rotated_directory(directory)
    temp_dir = tempfile.mkdtemp()  # Create a temporary directory for re-encoded files

    try:
        # Add support for .mov and other video formats
        supported_formats = [".mp4", ".mov", ".webm"]  # Add more formats as needed
        for filename in os.listdir(directory):
            if any(filename.endswith(ext) for ext in supported_formats):
                input_file = os.path.join(directory, filename)
                reencoded_file = reencode_video(input_file, temp_dir)
                
                if reencoded_file:
                    output_file = os.path.join(rotated_dir, get_random_filename())
                    rotate_video(reencoded_file, output_file, angle)
    finally:
        # Clean up temporary directory
        for temp_file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, temp_file))
        os.rmdir(temp_dir)

def process_path(path, angle):
    if os.path.isdir(path):
        rotate_videos_in_directory(path, angle)
    elif os.path.isfile(path):
        rotated_dir = create_rotated_directory(os.path.dirname(path))
        temp_dir = tempfile.mkdtemp()  # Create a temporary directory for re-encoded files
        
        try:
            reencoded_file = reencode_video(path, temp_dir)
            
            if reencoded_file:
                output_file = os.path.join(rotated_dir, get_random_filename())
                rotate_video(reencoded_file, output_file, angle)
        finally:
            # Clean up temporary directory
            for temp_file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, temp_file))
            os.rmdir(temp_dir)
    else:
        print("Invalid path. Please enter a valid file or directory path.")

if __name__ == "__main__":
    input_path = input("Enter the path of the video file or directory to rotate: ")
    while not os.path.exists(input_path):
        print("Path not found. Please enter a valid file or directory path.")
        input_path = input("Enter the full path of the video file or directory to rotate: ")

    # Display rotation choices
    print("Choose a rotation angle:")
    for choice, degrees in rotation_choices.items():
        print(f"{choice}: Rotate {degrees} degrees clockwise")
    
    user_choice = input("Enter your choice (1, 2, 3): ").strip()
    
    while user_choice not in rotation_choices:
        print("Invalid choice. Please choose from the available options.")
        user_choice = input("Enter your choice (1, 2, 3): ").strip()
    
    angle = rotation_choices[user_choice]
    
    process_path(input_path, angle)
