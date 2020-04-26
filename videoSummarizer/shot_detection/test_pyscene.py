from SplitVideo import SplitVideo

def start_video_splits(video_path, output_folder):
    ob = SplitVideo(no_of_bytes = 32, threshold = 20, output_path = './video_scenes', video_format = '.mp4')
    ob.video_splits(video_path)
