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
import uuid
from appbuilder.core.agent import AgentRuntime
from appbuilder.core.context import init_context
from appbuilder.core.user_session import UserSession
from appbuilder.core.message import Message
from appbuilder.core._client import HTTPClient

from appbuilder.core.function_call.base import FunctionCallEventType
from appbuilder.core.function_call.base import FunctionCallResponse


class FunctionCall(AgentRuntime):
    integrated_url = "/dte/api/v2/function_call/integrated"

    def __init__(self):
        super().__init__()
        self._http_client = None
        self._user_session = None

    @property
    def http_client(self):
        if self._http_client is None:
            self._http_client = HTTPClient()
        return self._http_client

    @property
    def user_session(self):
        if self._user_session is None:
            self._user_session = UserSession()
        return self._user_session

    def chat(self, message: Message,
             instruction: str = "", tools: list(str) = [], conversation_id: str = "", stream: bool = False, **args) -> Message:

        if conversation_id == "":
            conversation_id = str(uuid.uuid4())

        chat_res = Message()
        used_tool = []

        # while True:
        if True:
            request_id = str(uuid.uuid4())
            init_context(session_id=conversation_id, request_id=request_id)

            events = self.run(message, instruction=instruction, tools=tools,
                              conversation_id=conversation_id, stream=stream)
            
            self.user_session.append({})

            for event in events:
                if event.type == FunctionCallEventType.LOCAL_FUNCTION_CALL:  # 本地调用的FuncCall
                    tool_result = eval(event.content["func"])(
                        event.content["arguments"])
                elif event.type == FunctionCallEventType.REMOTE_FUNCTION_CALL_RESULTS:
                    used_tool.append(event.content)
                else:
                    print(event.content)  # user visible results

            # if tool_result == "" and used_tool == []:
            #     break

            # Todo(chengmo): 根据tool_result和used_tool，组装新的message

        return chat_res

    def run(self, message: Message, instruction: str = "", tools: list(str) = [], conversation_id: str = "", stream: bool = False):
        # Todo(chengmo): 创建并处理 used_tools
        request_message = self._request_message_encoder(
            message, instruction=instruction, tools=tools, conversation_id=conversation_id, stream=stream)
        payload = json.dumps(request_message.content)

        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"
        # url='http://10.45.86.8/dte/api/v2/function_call/integrated'

        response = self.http_client.session.post(
            url=self.http_client.service_url(self.integrated_url),
            headers=headers,
            data=payload)
        response = FunctionCallResponse(response, stream)
    
        return response.to_message()

    def _request_message_encoder(self, message: Message, instruction: str = "", tools: list(str) = [], conversation_id: str = "", stream: bool = False) -> dict[str, str]:
        query = message.content
        response_mode = "streaming" if stream else "blocking"
        conversation_id = conversation_id
        # Todo(chengmo): 获取或者新建user_id
        user_id = "80c5bbee-931d-4ed9-a4ff-63e1971bd079"
        inputs = {
            "function_call.user_instruction": "",
            "function_call.builtin_tool_list": []
        }
        inputs["function_call.user_instruction"] = instruction

        for tool in tools:
            inputs["function_call.builtin_tool_list"].append({
                "agent_name": tool,
                "agent_config": {}
            })

        model_configs = {}

        return Message({
            "query": query,
            "response_mode": response_mode,
            "conversation_id": conversation_id,
            "user": user_id,
            "inputs": inputs,
            "model_configs": model_configs
        })



if __name__ == "__main__":
    function_call = FunctionCall(instruction="", tools_set=[])
    message = Message("秦始皇是谁？")
    function_call.chat(message)
