from SplitVideo import SplitVideo

ob = SplitVideo(no_of_bytes = 32, threshold = 20, output_path = 'video_scenes/',video_format='.mp4')
ob.video_splits('../../index.mp4')