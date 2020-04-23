import os
import importlib
import shutil
import pandas as pd
#import modules here
from shot_detection import test_pyscene
from audio_generation import test_audio_generation

from summarize.models import *


def get_generated_audio(video_split_paths, target_folder):
    split_audio_paths = []
    for split_video in video_split_paths:
        split_name = split_video.split("/")[-1].split(".")[0]
        audio_file_name = target_folder +"/"+split_name+".wav"
        test_audio_generation.start_audio_gen(split_video, audio_file_name)
        split_audio_paths.append(audio_file_name)
    return split_audio_paths


def get_video_splits(video_path):
    video_path = "media/" + str(video_path)
    video_name = video_path.split('/')[-1]
    video_name = video_name.split(".")[0]
    
    shots_root_folder = "media/video_meta_data/" + video_name
    output_folder = "../shot_detection/video_scenes/"

    test_pyscene.start_video_splits(video_path, output_folder)
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
        sv_obj = VideoSplit(VideoID=video_id, SplitID=Split(split_id))
        sv_obj.save()

    split_audio_paths = get_generated_audio(video_split_paths, target_folder)
    #insert into Split Speech Table
    for split_id,audio_path in zip(split_ids,split_audio_paths):
        ss_obj = SplitSpeech(SplitID=Split(split_id),SpeechPath=audio_path)
        ss_obj.save()

