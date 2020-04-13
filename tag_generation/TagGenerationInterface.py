import abc

class TagGenerationInterface(abc.ABC):
    @abc.abstractmethod
    def generate_tags(filePath):
        pass