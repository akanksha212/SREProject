from SplitVideo import SplitVideo

def start_video_splits(video_path, output_folder):
    ob = SplitVideo(output_folder, no_of_bytes = 32, threshold = 20,video_format='.mp4')
    ob.video_splits(video_path)