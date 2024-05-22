from enum import Enum
from pydantic import BaseModel
import json
import os

class EngineResults:
    OutcomeValues: dict = {}
    Outcomes: dict = {}

    def __init__(self):
        self.OutcomeValues = dict()
        self.Outcomes = dict()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class OutcomePrediction:
    Probability = 0.0
    Value = None

    def __init__(self):
        self.Probability = 0.0
        self.Value = None

class DataTypes(str, Enum):
    Boolean = 'Boolean'
    Integer = 'Integer'
    Float = 'Float'
    String = 'String'
    File = 'File'
    Tensor = 'Tensor'

class InputInfo (BaseModel):
    Name: str = ''
    InputType: DataTypes = DataTypes.Integer

class OutcomeInfo (BaseModel):
    Name: str = ''
    OutcomeType: DataTypes = DataTypes.Integer
    
class BasePredictEngineConfig (BaseModel):    
    # Inputs: list[InputInfo] = None
    # Outcomes: list[OutcomeInfo] = None
    Inputs: list
    Outcomes: list

class InferenceContext (BaseModel):
    ContextId: str = ''
    StoredMeta: dict = {}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class EngineInputs (BaseModel):     
    InputValues: dict
    DesiredOutcomes: list    

class AppEngineConfig (BaseModel):
    TEMP_EXEC_DIR: str = os.getcwd()
    UPT_API_KEY: str = ""
    MODEL_DIR: str = os.path.join(os.getcwd(), "models")
    REQUEST_DIR: str = os.path.join(os.getcwd(), "requests")
    SAVE_CONTEXT: bool = True

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

# Note: these models will be different for every engine type
###############################################################################################################    
class AppEngineInferenceOptions (BaseModel):    
    pass

class AIEngineConfiguration (BasePredictEngineConfig):    
    InferenceOptions: AppEngineInferenceOptions = None

class AppEngineRequest (BaseModel):    
    RequestId: str = ''
    EngineId: str = ''
    RequestInputFiles: bool = False
    RequestOutputFiles: bool = False
    RequestFilesFolderPath: str = False
    PackagesFolderPath: str = ''
    PackagesFolderPath: str = ''
    SourcesFolderPath: str = ''
    ModelFilesFolderPath: str = ''
    EngineApiKey: str = ''
    PredictEndpoint: str = ''
    Context: InferenceContext = None
    CallbackQueue: str = ''
    EngineInputData: EngineInputs = None
    EngineConfig: AIEngineConfiguration = None

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

###############################################################################################################
    
class UnityPredictEngineResponse:
    RequestId: str = ''
    ErrorMessages: str = ''
    LogMessages: str = ''
    AdditionalInferenceCosts: float = 0.0
    EngineOutputs: EngineResults = None
    Context: InferenceContext = None

    def __init__(self):
        self.ErrorMessages = ''
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)



