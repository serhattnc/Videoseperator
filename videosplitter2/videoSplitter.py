from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
import os

class VideoProcessor:
    def __init__(self, url, output_path='video.mp4', output_folder='scenes'):
        self.url = url
        self.output_path = output_path
        self.output_folder = output_folder

    def download_video(self):
        yt = YouTube(self.url)
        stream = yt.streams.get_highest_resolution()
        stream.download(filename=self.output_path)
        print("Download complete.")

    def split_scenes(self):
        video_manager = VideoManager([self.output_path])
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector(threshold=55))
        video_manager.set_downscale_factor()
        video_manager.start()
        scene_manager.detect_scenes(frame_source=video_manager)
        scene_list = scene_manager.get_scene_list()
        print(f"Detected {len(scene_list)} scenes")
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        video = VideoFileClip(self.output_path)
        for i, (start, end) in enumerate(scene_list):
            start_time = start.get_seconds()
            end_time = end.get_seconds()
            scene_clip = video.subclip(start_time, end_time)
            output_file = os.path.join(self.output_folder, f"{i+1}.mp4")
            scene_clip.write_videofile(output_file, codec='libx264')
            print(f"Saved scene {i+1} to {output_file}")

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    video_processor = VideoProcessor(video_url)
    print("Downloading video...")
    video_processor.download_video()
    print("Splitting video into scenes...")
    video_processor.split_scenes()
