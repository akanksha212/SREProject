from SplitVideo import SplitVideo

ob = SplitVideo(no_of_bytes = 32, threshold = 20, output_path = 'video_scenes')
ob.video_splits('../../index1.mp4')