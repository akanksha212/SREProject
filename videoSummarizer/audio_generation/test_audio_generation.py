import os
from AudioGeneration import AudioGeneration

def start_audio_gen(input_file, output_file):
    ob = AudioGeneration()
    ob.convert_audio(input_path=input_file, output_path=output_file)
