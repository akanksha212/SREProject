from SplitVideo import SplitVideo

ob = SplitVideo(no_of_bytes = 32, threshold = 20, output_path = 'video_scenes/',video_format='.mkv')
ob.video_splits('../../The_Leaf_Part_1.mkv')