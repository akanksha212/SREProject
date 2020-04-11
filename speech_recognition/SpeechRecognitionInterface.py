import abc

class SpeechRecognitionInterface(abc.ABC):
    @abc.abstractmethod
    def transcribe(audio):
        pass

    @abc.abstractclassmethod
    def get_audio_config(local_file_path):
        pass
