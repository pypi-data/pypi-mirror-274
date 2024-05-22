import importlib
from io import BufferedReader, IOBase, StringIO
import json
import os, sys
import shutil
import datetime
import uuid
import filecmp

import requests
from .Models import AppEngineRequest, AppEngineConfig, EngineResults, InferenceContext, UnityPredictEngineResponse
from .Platform import ChainedInferenceRequest, ChainedInferenceResponse, FileReceivedObj, FileTransmissionObj, IPlatform, InferenceRequest,InferenceResponse, InferenceContextData

class UnityPredictHost(IPlatform):

    Initialized = False
    isConfigInit = False
    LoadedEngineId = None
    CurrentRequest: AppEngineRequest = None
    logMsgs: str = ''

    configFile = os.path.join(os.getcwd(), "config.json")
    appEngineConfig: AppEngineConfig = AppEngineConfig()


    execTempDir = "execTmp"
    execRequestFolder: str = "requests"
    execModelFolder: str = "models"
    execOutputFolder: str = "outputs"

    def __init__(self) -> None:
        
        config_dict : dict = {}
        if not os.path.exists(self.configFile):

            print ("Config file not detected, creating templated config file: {}".format(self.configFile))
            
            self.appEngineConfig.TEMP_EXEC_DIR = os.getcwd()

            with open(self.configFile, "w+") as confFile:
                confFile.write(self.appEngineConfig.toJSON())

            return None
        
        print ("Config file detected, loading data from: {}".format(self.configFile))
        with open (self.configFile, "r+") as confFile:
            config_dict = json.load(confFile)
            
        self.appEngineConfig = AppEngineConfig(**config_dict)
        self.CurrentRequest = AppEngineRequest()

        self.workingDir = os.path.join(self.appEngineConfig.TEMP_EXEC_DIR, self.execTempDir)
        self.CurrentRequest.EngineApiKey = self.appEngineConfig.UPT_API_KEY


        self.CurrentRequest.ModelFilesFolderPath = os.path.join(self.workingDir, self.execModelFolder)
        self.CurrentRequest.RequestFilesFolderPath = os.path.join(self.workingDir, self.execRequestFolder)
        
            
        self.isConfigInit = True

        return None
    
    def isConfigInitialized(self) -> bool:

        return self.isConfigInit
    
    def isPlatformInitialized(self) -> bool:

        return self.Initialized
    
    
    def getModelsFolderPath(self) -> str:
        # ToDo: return the correct path
        return self.CurrentRequest.ModelFilesFolderPath
    
    def getModelFile(self, modelFileName: str, mode: str = 'rb') -> IOBase:
        # ToDo: return the correct file handle
        absFilePath = os.path.join(self.getModelsFolderPath(), modelFileName)
        fileHandler = open(absFilePath, mode)

        return fileHandler
    

    def getLocalTempFolderPath(self) -> str: 
        # ToDo: return the correct path
        return self.workingDir
    
    def getRequestFolderPath(self) -> str:
        # ToDo: return the correct path
        return self.CurrentRequest.RequestFilesFolderPath

        
    def getRequestFile(self, requestFileName: str, mode: str = 'rb') -> IOBase: 
        # ToDo: return the correct file handle
        absFilePath = os.path.join(self.getRequestFolderPath(), requestFileName)
        fileHandler = open(absFilePath, mode)

        return fileHandler
    
    def saveRequestFile(self, requestFileName: str, mode: str = 'wb') -> IOBase: 
        # ToDo: return the correct file handle
        absFilePath = os.path.join(self.execOutputFolder, requestFileName)
        fileHandler = open(absFilePath, mode)

        return fileHandler
    
    
    def logMsg(self, msg: str):
        self.logMsgs += "\n{}\n".format(msg)

    def errorMsg(self, msg: str):
        self.errorMsgs += "\n{}\n".format(msg)


    def syncDirectories(self, source: str, destination: str, create_dest_if_not_present: bool = False):
        
        if not os.path.exists(source) or not os.path.isdir(source):
            print(f"Source directory '{source}' does not exist or is not a directory.")
            return

        if create_dest_if_not_present:
            if not os.path.exists(destination):
                os.makedirs(destination)
        else:
            if not os.path.exists(destination) or not os.path.isdir(source):
                print(f"Destination directory '{destination}' does not exist or is not a directory.")
                return

        # Copy or update files from source to destination
        for src_dir, _, files in os.walk(source):
            dst_dir = src_dir.replace(source, destination, 1)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            for file in files:
                src_file = os.path.join(src_dir, file)
                dst_file = os.path.join(dst_dir, file)

                if not os.path.exists(dst_file) or not filecmp.cmp(src_file, dst_file, shallow=False):
                    shutil.copy2(src_file, dst_file)  # Preserve metadata with copy2
                    print(f"Copied: {src_file} to {dst_file}")
                else:
                    print(f"Skipped: {src_file} is already up to date.")

        # Remove files and directories from destination that are not in source
        for dst_dir, _, files in os.walk(destination, topdown=False):
            src_dir = dst_dir.replace(destination, source, 1)

            if not os.path.exists(src_dir):
                shutil.rmtree(dst_dir)
                print(f"Removed directory: {dst_dir}")
            else:
                for file in files:
                    dst_file = os.path.join(dst_dir, file)
                    src_file = os.path.join(src_dir, file)

                    if not os.path.exists(src_file):
                        os.remove(dst_file)
                        print(f"Removed file: {dst_file}")

    def createPlatform(self, request: AppEngineRequest) -> bool:
        if not self.isConfigInit:
            return False
        
        # Creating output folder based on RequestID
        if (request.RequestId == ""):

            self.errorMsg("Please provide a proper request id\n")

            return False
         
        # Create the folders
        if not os.path.exists(self.workingDir):
            os.mkdir(self.workingDir)
        
        if not os.path.exists(self.CurrentRequest.ModelFilesFolderPath):
            os.mkdir(self.CurrentRequest.ModelFilesFolderPath)

        # Create request folder having the name of the current Timestamp
        currentExecTime = datetime.datetime.now()
        currentExecTime = currentExecTime.strftime("%d-%m-%YT%H-%M-%S")
        
        self.execRequestFolder = "{}_{}__{}".format(self.execRequestFolder, currentExecTime, request.RequestId)
        self.CurrentRequest.RequestFilesFolderPath = os.path.join(self.workingDir, self.execRequestFolder)

        if not os.path.exists(self.CurrentRequest.RequestFilesFolderPath):
            os.mkdir(self.CurrentRequest.RequestFilesFolderPath)
        
        
        # Create output folder based on the request Id
        self.execOutputFolder = "{}_{}__{}".format(self.execOutputFolder, currentExecTime, request.RequestId)
        self.execOutputFolder = os.path.join(self.workingDir, self.execOutputFolder)
        if not os.path.exists(self.execOutputFolder):
            os.mkdir(self.execOutputFolder)


        # TODO: Copy user configured folder contents to respective exec folders
        # Sync Request Files
        self.syncDirectories(self.appEngineConfig.REQUEST_DIR, self.CurrentRequest.RequestFilesFolderPath)
        # Sync Model Files
        self.syncDirectories(self.appEngineConfig.MODEL_DIR, self.CurrentRequest.ModelFilesFolderPath)

        self.Initialized = True

        return True
    
    def run_engine(self, request: AppEngineRequest) -> UnityPredictEngineResponse:

        self.logMsgs: str = ''
        self.MaxlogMsgBuffer: int = 3000
        self.NegMaxlogMsgBuffer: int = -1 * self.MaxlogMsgBuffer

        self.errorMsgs: str = ''
        self.MaxErrorMsgsBuffer: int = 3000
        self.NegMaxErrorMsgsBuffer: int = -1 * self.MaxErrorMsgsBuffer
        
        toreturn: UnityPredictEngineResponse = UnityPredictEngineResponse()
        try:  

            # Create the platform for execution
            # 1) Prepare temp folders on local directories for A) Request Files B) Model Files C) Temp Files
            # 2) Put the files into the right folders 
            if not self.createPlatform(request=request):

                self.errorMsg("Unable to create the platform")
                toreturn.ErrorMessages = self.errorMsgs[self.NegMaxErrorMsgsBuffer:] # limit length of the logs
                toreturn.LogMessages = self.logMsgs[self.NegMaxlogMsgBuffer:] # limit length of the logs

                return toreturn
            
            
            # 3) Store/Restore Context (probably using some local json file) if requested by user
            # Initialize context

            if (self.appEngineConfig.SAVE_CONTEXT):
                
                contextJson = os.path.join(self.getLocalTempFolderPath(), "context.json")
                
                context = {}
                if os.path.exists(contextJson):
                    with open(contextJson, "r+") as ctxtf:
                        context = json.load(ctxtf) 

                    request.Context = InferenceContext(**context)

            # 4) Convert the AppEngineRequest to the InferenceRequest that the model needs

            inferReq: InferenceRequest = InferenceRequest()
            inferReq.InputValues = request.EngineInputData.InputValues
            inferReq.DesiredOutcomes = request.EngineInputData.DesiredOutcomes

            inferReq.Context = InferenceContextData()

            if (request.Context != None):
                inferReq.Context.StoredMeta = request.Context.StoredMeta
            else:
                inferReq.Context.StoredMeta = {}
            

            # 5) Run EntryPoint.py
            entryPoint = importlib.import_module("EntryPoint")
            inferResp: InferenceResponse = entryPoint.run_local_engine(inferReq, self)

            # 6) Copy InferenceResponse to UnityPredictEngineResponse

            toreturn.AdditionalInferenceCosts = inferResp.AdditionalInferenceCosts
            toreturn.EngineOutputs = EngineResults()
            
            if (inferResp.Outcomes != None):
                toreturn.EngineOutputs.Outcomes = inferResp.Outcomes
            else:
                toreturn.EngineOutputs.Outcomes = {}

            if (inferResp.OutcomeValues != None):
                toreturn.EngineOutputs.OutcomeValues = inferResp.OutcomeValues
            else:
                toreturn.EngineOutputs.OutcomeValues = {}


            toreturn.EngineOutputs.OutcomeValues = inferResp.OutcomeValues
            toreturn.ErrorMessages = inferResp.ErrorMessages

            if (self.appEngineConfig.SAVE_CONTEXT):
            
                toreturn.Context = InferenceContext(ContextId="")
                if (request.Context  != None):
                    toreturn.Context.ContextId = request.Context.ContextId 
                if (inferResp.Context == None or inferResp.Context.StoredMeta == None or inferResp.Context.StoredMeta == {}):
                    
                    if (request.Context  != None):
                        toreturn.Context.StoredMeta = inferReq.Context.StoredMeta
                    else:
                        toreturn.Context.StoredMeta = {}
                    
                else:    
                    toreturn.Context.StoredMeta = inferResp.Context.StoredMeta

                if toreturn.Context.ContextId == "":
                    toreturn.Context.ContextId = str(uuid.uuid4())


                with open(contextJson, "w+") as ctxtf:
                    ctxtf.write(toreturn.Context.toJSON())


            toreturn.LogMessages = self.logMsgs[self.NegMaxlogMsgBuffer:] # limit length of the logs
            
        except Exception as e:

            print ("Error occured: {}".format(str(e)))
            self.errorMsg(str(e))
            toreturn.ErrorMessages += self.errorMsgs[self.NegMaxErrorMsgsBuffer:] # limit length of the logs
            toreturn.LogMessages = self.logMsgs[self.NegMaxlogMsgBuffer:] # limit length of the logs

        return toreturn
        

    def invokeUnityPredictModel(self, modelId: str, request: ChainedInferenceRequest) -> ChainedInferenceResponse:
        results = ChainedInferenceResponse()

        apiKey = self.CurrentRequest.EngineApiKey
        apiBaseUrl = self.CurrentRequest.PredictEndpoint.rstrip('/')

        needFileUpload: bool = False

        ##### 
        # The request can contain file objects so we need to change those to file names before sending out
        #####
        # first get a list of file that we'll need to upload later & update the POST obj
        filesToUpload = {}
        for xvarName in request.InputValues:
            if isinstance(request.InputValues.get(xvarName), FileTransmissionObj):
                needFileUpload = True
                break

        finalResponseJson: any = ''

        response: requests.Response = None
        if not needFileUpload:
            # serialize the POST obj
            jsonBody = json.dumps(request, default=vars)

            # there are no files to upload so just post normally
            response = requests.post(url = "{}/{}".format(apiBaseUrl, modelId), data=jsonBody, headers={"Authorization": "Bearer {}".format(apiKey)})

            if response.status_code != 200:
                results.ErrorMessages = 'Error from server: {}'.format(response.status_code)
                return results
            
            finalResponseJson = response.json()
        else:
            # we need to initialize first
            response = requests.post(url = "{}/initialize/{}".format(apiBaseUrl, modelId), data="", headers={"Authorization": "Bearer {}".format(apiKey)})

            requestId: str = response.json().get('requestId')

            if response.status_code != 200:
                results.ErrorMessages = 'Error from server: {}'.format(response.status_code)
                return results
            
            # upload the files
            for xvarName in request.InputValues: 
                if isinstance(request.InputValues.get(xvarName), FileTransmissionObj):
                    fileToUpload: FileTransmissionObj = request.InputValues.get(xvarName)
                    response = requests.get(url = "{}/upload/{}/{}".format(apiBaseUrl, requestId, fileToUpload.FileName), headers={"Authorization": "Bearer {}".format(apiKey)})
                    uploadLink = response.json().get('uploadLink')
                    fileName = response.json().get('fileName')
                    request.InputValues[xvarName] = fileName # make sure that only the filename is in the request that we are going to POST
                    requests.put(url = uploadLink, data=fileToUpload.FileHandle)
            
            jsonBody = json.dumps(request, default=vars)
            
            response = requests.post(url = "{}/{}/{}".format(apiBaseUrl, modelId, requestId), data=jsonBody, headers={"Authorization": "Bearer {}".format(apiKey)})

            finalResponseJson = response.json()

        
        print(finalResponseJson)

        while (finalResponseJson.get('status') == 'Processing'):
            statusUrl: str = finalResponseJson.get('statusUrl')

            response = requests.get(url = statusUrl, headers={"Authorization": "Bearer {}".format(apiKey)})
            finalResponseJson = response.json()


        finalResponseRequestId: str = finalResponseJson.get('requestId')

        tempOutputFolder: str = os.path.join(self.getLocalTempFolderPath(), "chainedResults", finalResponseRequestId)
        if not os.path.exists(tempOutputFolder):
            os.makedirs(tempOutputFolder)

        outcomeValues = finalResponseJson.get('outcomeValues')
        for outputVarName in outcomeValues: 
            outcome: dict = outcomeValues.get(outputVarName)
            if outcome.get('dataType') == 'File':
                fileName = outcome.get('value')

                tempFilePath = os.path.join(tempOutputFolder, fileName)
                response = requests.get(url = "{}/download/{}/{}".format(apiBaseUrl, finalResponseRequestId, fileName), headers={"Authorization": "Bearer {}".format(apiKey)})
                with open(tempFilePath, 'wb') as f:
                    f.write(response.content)

                fileReceived: FileReceivedObj = FileReceivedObj(fileName, tempFilePath)
                outcome['value'] = fileReceived

        outcomes = finalResponseJson.get('outcomes')
        for outputVarName in outcomes: 
            outcome: list = outcomes.get(outputVarName)
            for outcomeItem in outcome:
                if outcomeItem.get('dataType') == 'File':
                    fileName = outcomeItem.get('value')

                    tempFilePath = os.path.join(tempOutputFolder, fileName)
                    response = requests.get(url = "{}/download/{}/{}".format(apiBaseUrl, finalResponseRequestId, fileName), headers={"Authorization": "Bearer {}".format(apiKey)})
                    with open(tempFilePath, 'wb') as f:
                        f.write(response.content)

                    fileReceived: FileReceivedObj = FileReceivedObj(fileName, tempFilePath)
                    outcomeItem['value'] = fileReceived


        try:
            results.ComputeCost = finalResponseJson.get('computeCost')
            results.OutcomeValues = outcomeValues
            results.Outcomes = outcomes
            results.RequestId = finalResponseRequestId
            results.ContextId = finalResponseJson.get('contextId')
            results.ErrorMessages = finalResponseJson.get('errorMessages')

        except Exception as e:
            print(e)

        return results