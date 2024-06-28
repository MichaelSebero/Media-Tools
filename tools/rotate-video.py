import os
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import rotate

# Dictionary mapping rotation choices to degrees
rotation_choices = {
    "1": 90,
    "2": 180,
    "3": 270
}

def rotate_video(input_file, output_file, angle):
    # Load the video clip
    clip = VideoFileClip(input_file)
    
    # Check if the video is vertical
    is_vertical = clip.size[0] < clip.size[1]  # Width is less than height
    
    # Adjust rotation angle if video is vertical
    if is_vertical:
        if angle in [90, 270]:
            angle += 180
    
    # Rotate the video clip by the adjusted angle
    rotated_clip = rotate(clip, angle)
    
    # Ensure same video quality
    rotated_clip.write_videofile(output_file, codec='libx264', bitrate='5000k', fps=clip.fps)

if __name__ == "__main__":
    input_file = input("Enter path of the video file to rotate: ")
    while not os.path.exists(input_file):
        print("File not found. Please enter a valid file path.")
        input_file = input("Enter the full path of the video file to rotate: ")
    
    # Display rotation choices
    print("Choose a rotation angle:")
    for choice, degrees in rotation_choices.items():
        print(f"{choice}: Rotate {degrees} degrees clockwise")
    
    user_choice = input("Enter your choice (1, 2, 3): ").strip()
    
    while user_choice not in rotation_choices:
        print("Invalid choice. Please choose from the available options.")
        user_choice = input("Enter your choice (1, 2, 3): ").strip()
    
    angle = rotation_choices[user_choice]
    
    # Set the output file path to the desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    output_file = os.path.join(desktop_path, "rotated_video.mp4")
    
    rotate_video(input_file, output_file, angle)
    
    print(f"Video rotated successfully and saved as {output_file}")
