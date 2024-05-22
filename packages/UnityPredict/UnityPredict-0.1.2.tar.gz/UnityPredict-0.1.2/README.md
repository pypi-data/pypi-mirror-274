# UnityPredict Local App Engine Creator

## Introduction

This library allows you to create App Engines in your local system and finetune the engines before updating it to the [ModelCentral](https://modelcentral.ai) repositories.

## Installation
* You can use pip to install the ```UnityPredict``` library.
```bash
pip install UnityPredict
```

## Usage
Use the following snippet to initialize the environment.


### main.py

```python

from UnityPredict import UnityPredictHost, Models
import sys
import uuid

import time

import os



if __name__ == "__main__":        
    platformInit = UnityPredictHost()

    configStat = platformInit.isConfigInitialized()

    if not configStat:
        print ("Config Initialization Unsuccessful!!")
        sys.exit(0)
    
    
    print ("Config Initialization Successful!!")

```

* This is the snippet to initialize the AppEngine environment.
* Run script using the following command:

```bash
python main.py
```

* If this script is run for the **first time**. The following Output will be shown

```bash

Config file not detected, creating templated config file: YourScriptPath/config.json
Config Initialization Unsuccessful!!

```
* A templated config file would be generated on the same directory as that of your main script.

```json
{
    "MODEL_DIR": "YourScriptPath/models",
    "REQUEST_DIR": "YourScriptPath/requests",
    "SAVE_CONTEXT": true,
    "TEMP_EXEC_DIR": "YourScriptPath",
    "UPT_API_KEY": ""
}

```

* Edit the JSON as per your requirements. The various keys represent:

    * **TEMP_EXEC_DIR**: Directory on which you wan the AppEngine to run
    
    * **REQUEST_DIR**: Files or Folders to be uploaded to AppEngine for using during the execution can be added under the specified **REQUEST_DIR**

    * **MODEL_DIR**: Local model files/binaries to be uploaded to AppEngine for using during the execution can be added under the specified **MODEL_DIR**

    * **SAVE_CONTEXT**: Retains context across multiple requests. Disable it using ```"SAVE_CONTEXT" : false```

    * **UPT_API_KEY**: API Key token generated from the ModelCentral profile of the user.

* Once configured, run the following script once again to get:

```bash
Config Initialization Successful!!
```

### EntryPoint.py

* In order to run your custom AppEngine, it is necessary to create a file named ```EntryPoint.py``` which is going to contain the inference logic.

This is an Example snippet of the `EntryPoint.py`:
```python
import json
from UnityPredict.Platform import IPlatform, InferenceRequest, InferenceResponse, OutcomeValue, InferenceContextData
from typing import List, Dict, Optional
from collections import deque
import sys
import datetime



def run_local_engine(request: InferenceRequest, platform: IPlatform) -> InferenceResponse:

    

    platform.logMsg("Running User Code...")
    response = InferenceResponse()
    
    context: Dict[str, str] = {}

    try:
        prompt = request.InputValues['InputMessage']

        
        # Saved context across requests
        # Use this variable to save new context in the dict format
        # request.Context.StoredMeta is of the format: Dict[str, str]
        context = request.Context.StoredMeta

        currentExecTime = datetime.datetime.now()
        currentExecTime = currentExecTime.strftime("%d-%m-%YT%H-%M-%S")
        resp_message = "Echo message: {} Time:: {}".format(prompt, currentExecTime)

        
        # platform.getRequestFile: Fetch Files specified under the "REQUEST_DIR" in config
        with platform.getRequestFile("myDetails.txt", "r") as reqFile:

            resp_message += "\n{}".format("\n".join(reqFile.readlines()))

        
        # Fill context according to your needs
        context[currentExecTime] = resp_message    
        
        
        # platform.saveRequestFile: Creates any file type Outputs
        # These files would be present under TEMP_EXEC_DIR/execTmp/outputs_<RequestLaunchTimeStamp>__<RequestId>
        # TEMP_EXEC_DIR: Configured under the config.json
        # execTmp: Creates enviroment for the AppEngine under the specified TEMP_EXEC_DIR
        with platform.saveRequestFile("final_resp_{}.txt".format(currentExecTime), "w+") as outFile:

            outFile.write(resp_message)

        
        cost = len(prompt)/1000 * 0.03 + len(resp_message)/1000 * 0.06
        response.AdditionalInferenceCosts = cost
        response.Outcomes['OutputMessage'] = [OutcomeValue(value=resp_message, probability=1.0)]
        
        # Set the updated context back to the response
        response.Context.StoredMeta = context
    except Exception as e:
        response.ErrorMessages = "Entrypoint Exception Occured: {}".format(str(e))

    print("Finished Running User Code...")
    return response


```

* Some APIs for using the AppEngine environment
    * **request.Context.StoredMeta**:
        * Saved context across requests
        * Use this variable to save new context in the dict format
        * request.Context.StoredMeta is of the format: Dict[str, str]

    * **platform.getRequestFile**: 
        * Fetch Files specified under the "**REQUEST_DIR**" in config

    * **platform.saveRequestFile**: 
        * Creates any file type Outputs
        * These files would be present under **TEMP_EXEC_DIR/execTmp/*outputs_RequestLaunchTimeStamp__RequestId***
        * **TEMP_EXEC_DIR**: Configured under the config.json
        * execTmp: Creates enviroment for the AppEngine under the specified TEMP_EXEC_DIR


* Go back to the `main.py` and add the following command to run your `EntryPoint.py`

```python
if __name__ == "__main__":        
    
    # Previous Snippet for initialization
    platformInit = UnityPredictHost()

    configStat = platformInit.isConfigInitialized()

    if not configStat:
        print ("Config Initialization Unsuccessful!!")
        sys.exit(0)
    
    
    print ("Config Initialization Successful!!")

    #### New Snippet to run EntryPoint.py via the AppEngine

    request = Models.AppEngineRequest(RequestId=str(uuid.uuid4()))
    request.EngineInputData = Models.EngineInputs(InputValues={"InputMessage": "Hi, this is the message to be echoed"}, DesiredOutcomes=[])
    
    response : Models.UnityPredictEngineResponse = platformInit.run_engine(request=request)

    # Print Outputs
    if (response.EngineOutputs != None):
        print ("Output: {}".format(response.EngineOutputs.toJSON()))
    
    # Print Error Messages (if any)
    print ("Error Messages: {}".format(response.ErrorMessages))
    
```


## Contributing

## License