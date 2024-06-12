import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

def combine_videos(video1_path, video2_path, output_path):
    # Load the two video clips
    clip1 = VideoFileClip(video1_path)
    clip2 = VideoFileClip(video2_path)

    # Combine the video clips
    combined_clip = concatenate_videoclips([clip1, clip2])

    # Save the combined video
    combined_clip.write_videofile(output_path, codec="libx264")

    # Close the clips
    clip1.close()
    clip2.close()
    combined_clip.close()

    # Delete the original videos
    os.remove(video1_path)
    os.remove(video2_path)

def process_videos_in_folder(folder_path):
    # Get list of video files in the folder
    video_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]

    # Check if there are at least two video files
    if len(video_files) < 2:
        print("Not enough video files to combine.")
        return

    # Take the first two video files
    video1_path = os.path.join(folder_path, video_files[0])
    video2_path = os.path.join(folder_path, video_files[1])

    # Create output path
    output_path = os.path.join(folder_path, "combined_video.mp4")

    # Combine the videos
    combine_videos(video1_path, video2_path, output_path)
    print(f"Combined video saved as {output_path}")

# Example usage
scenes_folder = 'path_to_scenes_folder'
process_videos_in_folder(scenes_folder)
