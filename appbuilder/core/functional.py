# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import os
import requests
import appbuilder
from appbuilder.core.agent import AgentRuntime
from appbuilder.core.component import Component
from appbuilder.core.message import Message
from appbuilder.core._client import HTTPClient

class FunctionCall(AgentRuntime):
    component: list[Component] = []

    def __init__(self, instruction:str="", tools_set: list=[]):
        super().__init__()
        os.environ["APPBUILDER_TOKEN"] = "Bearer bce-v3/ALTAK-tpJqnbAvTivWEAclPibrT/4ac0ef025903f00e9252a0c41b803b41372a4862"
        os.environ["GATEWAY_URL"] = ""
        # self.instruction = instruction
        # self.component = tools_set
        self._http_client = None

    @property
    def http_client(self):
        if self._http_client is None:
            self._http_client = HTTPClient()
        return self._http_client


    def chat(self, message: Message, stream: bool=False, **args) -> Message:
        used_tool = []
        events = self.run(message)
        

    def run(self, message: Message ,stream: bool = False):
        # response_mode = "streaming" if stream else "blocking"
        message = Message({
            "query": "秦始皇是谁？",
            "response_mode": "streaming",
            "conversation_id": "80c5bbee-931d-4ed9-a4ff-63e1971bd079",
            "user": "80c5bbee-931d-4ed9-a4ff-63e1971bd079",
            "inputs": {
                "function_call.user_instruction": "",
                "function_call.builtin_tool_list": [
                    {
                        "agent_name": "BaiduSearch",
                        "agent_config": {}
                    }
                ]
            },
            "model_configs": {}
        })
        payload = json.dumps(message.content)
        print(payload)
        headers = {"X-Appbuilder-Authorization": "Bearer bce-v3/ALTAK-tpJqnbAvTivWEAclPibrT/4ac0ef025903f00e9252a0c41b803b41372a4862",
                   "Content-Type": "application/json"}
        response = self.http_client.session.post(url='http://10.45.86.8/dte/api/v2/function_call/integrated',headers=headers, data=payload)
        bytes_ = b''
        for chunk in response:
            bytes_ += chunk
        result = bytes_.decode('utf8')
        print(result)
        

if __name__ == "__main__":
    function_call = FunctionCall(instruction="", tools_set=[])
    message = Message("秦始皇是谁？")
    function_call.chat(message)