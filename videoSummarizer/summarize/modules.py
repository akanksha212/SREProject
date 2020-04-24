import os
import importlib
import shutil
import pandas as pd

#import modules here
from shot_detection.SplitVideo import SplitVideo
from audio_generation.AudioGeneration import AudioGeneration

from summarize.models import *

''' Changes:
    1. In settings.py file : added the path of folders after copying in videoSummarizer folder
    2. In views.py file : called pre_process in video_new function -> Done
    3. Updated the Model for Split -> Done
    4. Change the path of .cnf file in settings.py
'''

 ''' TODO
    1. call module for speech recognition on each video split 
    2. call module for summarization (word frequency summarization)
    3. call module for tag generation
    4. update respective tables
'''

def get_generated_audio(video_split_paths, target_folder):
    split_audio_paths = []
    for split_video in video_split_paths:
        split_name = split_video.split("/")[-1].split(".")[0]
        audio_file_name = target_folder +"/"+split_name+".wav"
        audio_gen = AudioGeneration()
        audio_gen.convert_audio(split_video, audio_file_name)
        split_audio_paths.append(audio_file_name)
    return split_audio_paths


def get_video_splits(video_path):
    video_path = "media/" + str(video_path)
    video_name = video_path.split('/')[-1]
    video_name = video_name.split(".")[0]

    shots_root_folder = "media/video_meta_data/" + video_name
    output_folder = "../shot_detection/video_scenes/"

    split_vid_obj = SplitVideo(no_of_bytes = 32, threshold = 20, output_path = output_folder, video_format = '.mp4')
    split_vid_obj.video_splits(video_path)
    shutil.copytree(output_folder, shots_root_folder)
    
    split_csv_file = shots_root_folder+"/"+video_name+"_split_times.csv"
    csv_reader = pd.read_csv(split_csv_file)
    split_files = csv_reader['filename'][:]
    video_split_file_paths = []
    for video in split_files:
        split_name = shots_root_folder +"/"+video+".mp4"
        video_split_file_paths.append(split_name)
    # removed the video_scenes folder for next video
    shutil.rmtree(output_folder)

    return video_split_file_paths, shots_root_folder


def pre_process(video_path, video_id):
    print("In modules.py file -----")
    video_split_paths, target_folder = get_video_splits(video_path)
    #insert into Split and VideoSplit Tables
    split_ids = []
    for split_path in video_split_paths:
        s_obj = Split(SplitPath = split_path)
        s_obj.save()
        split_ids.append(s_obj.id)
    
    for split_id in split_ids:
        sv_obj = VideoSplit(VideoID=Video(video_id), SplitID=Split(split_id))
        sv_obj.save()

    split_audio_paths = get_generated_audio(video_split_paths, target_folder)
    #insert into Split Speech Table
    for split_id,audio_path in zip(split_ids,split_audio_paths):
        ss_obj = SplitSpeech(SplitID=Split(split_id),SpeechPath=audio_path)
        ss_obj.save()

   





