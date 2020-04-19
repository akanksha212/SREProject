import pandas as pd
import os
import math
import datetime
import secrets

from SplitVideoInterface import SplitVideoInterface
from PySceneDetection import PySceneDetection

class SplitVideo(SplitVideoInterface):
    def __init__(self, no_of_bytes = 32, threshold = 20):
        self.video_name = str()
        self.no_of_bytes = 32
        self.threshold = 20

    def video_splits(self, local_video_path):
        ob = PySceneDetection()
        ob.detect_scenes(local_video_path)
        self.video_name = local_video_path.split('/')[-1].split('.')[0]
        self.best_splits(self.video_name + '_split_times.csv', local_video_path)

    def best_splits(self, local_file_path, local_video_path):
        """Splits the given video as detected by Class PySceneDetection"""
        dataframe = pd.read_csv(local_file_path)
        video_name = local_file_path.split('_')[0]
        command = 'ffmpeg -i ' + local_video_path
        video_parameter = ' -vcodec copy -acodec copy -ss '
        end_time_parameter = ' -to '
        file_extension = '.mp4'
        command += video_parameter
        for index, rows in dataframe.iterrows():
            generate_command = command + rows['Start Timecode'] + end_time_parameter + rows['End Timecode']
            os.system(generate_command + ' ' + rows['filename'] + file_extension)
