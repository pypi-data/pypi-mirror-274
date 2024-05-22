from abc import ABCMeta, abstractmethod
from io import BufferedReader, IOBase

class OutcomeValue:
    Probability = 0.0
    Value = None

    def __init__(self, value: any = '', probability: float = 0.0):
        self.Probability = probability
        self.Value = value

class InferenceContextData:
    StoredMeta: dict = {}

class InferenceRequest:
    InputValues: dict
    DesiredOutcomes: list
    Context: InferenceContextData = None 
    
class InferenceResponse:
    ErrorMessages: str = ''
    AdditionalInferenceCosts: float = 0.0
    Context: InferenceContextData = None
    OutcomeValues: dict = {}
    Outcomes: dict = {}

    def __init__(self):
        self.Context = InferenceContextData()

class ChainedInferenceRequest:
    ContextId: str = ''
    InputValues: dict
    DesiredOutcomes: list
    
class ChainedInferenceResponse:
    ContextId: str = ''
    RequestId: str = ''
    ErrorMessages: str = ''
    ComputeCost: float = 0.0
    OutcomeValues: dict = {}
    Outcomes: dict = {}

class FileTransmissionObj:
    FileName: str = ''
    FileHandle: IOBase = None

    def __init__(self, fileName, fileHandle):
        self.FileName = fileName
        self.FileHandle = fileHandle

class FileReceivedObj:
    FileName: str = ''
    LocalFilePath: str = ''

    def __init__(self, fileName, localFilePath):
        self.FileName = fileName
        self.LocalFilePath = localFilePath

class IPlatform:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def getModelsFolderPath(self) -> str: raise NotImplementedError

    @abstractmethod
    def getModelFile(self, modelFileName: str, mode: str = 'rb') -> IOBase: raise NotImplementedError

    @abstractmethod
    def getRequestFile(self, modelFileName: str, mode: str = 'rb') -> IOBase: raise NotImplementedError

    @abstractmethod
    def saveRequestFile(self, modelFileName: str, mode: str = 'wb') -> IOBase: raise NotImplementedError

    @abstractmethod
    def getLocalTempFolderPath(self) -> str: raise NotImplementedError

    @abstractmethod
    def logMsg(self, msg: str): raise NotImplementedError

    @abstractmethod
    def invokeUnityPredictModel(self, modelId: str, request: ChainedInferenceRequest) -> ChainedInferenceResponse: raise NotImplementedError