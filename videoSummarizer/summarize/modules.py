import os
import importlib
import shutil
import pandas as pd

#import modules here
from shot_detection.SplitVideo import SplitVideo
from audio_generation.AudioGeneration import AudioGeneration
from speech_recognition.GoogleSpeechRecognition import GoogleSpeechRecognition
from tag_generation.YakeSummarization import YakeSummarization
from summarization.WordFrequencySummarization import WordFrequencySummarization
from summarize.models import *


def get_summary(text):
    summ_obj = WordFrequencySummarization()
    summary = summ_obj.summarize(text)
    return summary


def get_tags(text):
    tags_obj = YakeSummarization()
    tags = tags_obj.generate_tags(text)
    return tags


def get_split_transcript(audio_file_path):
    speech_obj = GoogleSpeechRecognition(language="en-US", blob_length=32)
    transcript = speech_obj.transcribe(audio_file_path)
    return transcript


def get_generated_audio(video_split_paths, target_folder):
    split_audio_paths = []
    for split_video in video_split_paths:
        split_name = split_video.split("/")[-1].split(".")[0]
        audio_file_path = target_folder +"/"+split_name+".wav"
        audio_gen = AudioGeneration()
        audio_gen.convert_audio(split_video, audio_file_path)
        split_audio_paths.append(audio_file_path)
    return split_audio_paths


def get_video_splits(video_path):
    video_path = "media/" + str(video_path)
    video_name = video_path.split('/')[-1]
    video_name = video_name.split(".")[0]

    shots_root_folder = "media/video_meta_data/" + video_name
    output_folder = "./shot_detection/video_scenes/"

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

    print("\n\n============= Starting Video Split Generation ==========\n\n")
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

    print("\n\n============= Starting Audio Generation ==========\n\n")
    split_audio_paths = get_generated_audio(video_split_paths, target_folder)
    #insert into Split Speech Table
    for split_id,audio_path in zip(split_ids,split_audio_paths):
        ss_obj = SplitSpeech(SplitID=Split(split_id),SpeechPath=audio_path)
        ss_obj.save()

    
    print("\n\n============= Starting Audio To Text Generation ==========\n\n")
    transcript_files = []
    for audio_file in split_audio_paths:
        transcript = get_split_transcript(audio_file)
        transcript_file_name = audio_file.split(".")[0]+".txt"
        transcript_files.append(transcript_file_name)
        with open(transcript_file_name,'w') as f:
            f.write(transcript)
    #inset into SplitTranscript Table
    for split_id,transcript in zip(split_ids, transcript_files):
        st_obj = SplitTranscript(SplitID=Split(split_id), TranscriptPath=transcript)
        st_obj.save()
    
    print("\n\n============= Starting Tag and Summary Generation ==========\n\n") 
    split_tags = []  
    split_summary = [] 
    for transcript_file in transcript_files:
        with open(transcript_file, 'r') as f:
            text = f.read()
        tags = get_tags(text)
        split_tags.append(tags)
        #summary
        summary = get_summary(text)
        summary = "".join(summary)
        summary_file = transcript_file.split(".")[0]+"_summ.txt"
        with open(summary_file,"w") as f:
            f.write(summary)
        split_summary.append(summary_file)

    #insert into SplitTag Table
    for split_id,tags in zip(split_ids, split_tags):
        for tag in tags:
            stag_obj = SplitTag(SplitID=Split(split_id), Tag=tag)
            stag_obj.save()
    
    #insert into SplitSummary Table
    for split_id,summary_file in zip(split_ids, split_summary):
        ssum_obj = SplitSummary(SplitID=Split(split_id), Summary=summary_file)
        ssum_obj.save()


    print("\n\n ===================== FINISHED PROCESSING VIDEO ================= \n\n")


def tag_search(tag):
    tag = tag.lower()
    split_ids = []
    split_paths = []
    summary_paths = []
    #get split id for the given tag
    tag_obj = SplitTag.objects.filter(Tag=tag)
    for t in tag_obj:
        t = str(t).split(":")
        split_ids.append(t[0])
        split_paths.append(t[1])
    print("Split ids: ",split_ids)
    print("Split paths: ",split_paths)
    #get summary file path for each split id
    for split_id in split_ids:
        summary_paths.append(SplitSummary.objects.get(SplitID=Split(split_id)))
    print("Summary files: ",summary_paths)
    return split_paths, summary_paths




   





