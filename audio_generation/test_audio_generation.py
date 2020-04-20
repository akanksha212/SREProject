import os
from AudioGeneration import AudioGeneration

ob = AudioGeneration()
ob.convert_audio(input_path=os.path.join("../../test/real_estate.mp4"), output_path="test.wav")
