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
from appbuilder.core.component import Component
from appbuilder.core.context import init_context
from appbuilder.core.user_session import UserSession
from appbuilder.core.message import Message
from appbuilder.core._client import HTTPClient
from appbuilder.core.components.llms.base import CompletionResponse, LLMMessage


class FunctionCallEventType(object):
    """
    FunctionCallEventType, 函数调用事件类型
    """
    LOCAL_FUNCTION_CALL = "local_function_call" # 调用本地的函数实现
    LOCAL_FUNCTION_CALL_RESULTS = "local_function_call_results" # 本地调用函数的实现结果

    REMOTE_FUNCTION_CALL = "remote_function_call" # 调用远程的函数实现
    REMOTE_FUNCTION_CALL_RESULTS = "remote_function_call" # 远程调用函数的实现结果


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
        
        chat_res = Message()
        used_tool = []
        while True:       
            events = self.run(message, instruction=instruction, tools=tools,
                                conversation_id=conversation_id, stream=stream)

            for event in events:
                # Todo(chengmo): 定义event.type
                if event.type == FunctionCallEventType.LOCAL_FUNCTION_CALL: #本地调用的FuncCall
                    tool_result = eval(event.content["func"])(event.content["arguments"])
                elif event.type == FunctionCallEventType.REMOTE_FUNCTION_CALL_RESULTS:
                    used_tool.append(event.content)
                else:
                    print(event.content) # user visible results
            
            if tool_result == "" and used_tool == []:
                break

        return chat_res

    def run(self, message: Message, instruction: str = "", tools: list(str) = [], conversation_id: str = "", stream: bool = False):     
        if conversation_id == "":
            conversation_id = str(uuid.uuid4())
        request_id = str(uuid.uuid4())
        init_context(session_id=conversation_id, request_id=request_id)
        
        # Todo(chengmo): 创建并处理 used_tools
        request_message = self._request_message_encoder(
            message, instruction=instruction, stream=stream)
        payload = json.dumps(request_message.content)

        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"
        # url='http://10.45.86.8/dte/api/v2/function_call/integrated'

        response = self.http_client.session.post(
            url=self.http_client.service_url(self.integrated_url),
            headers=headers,
            data=payload)
        response_message = self._response_message_decoder(response, stream)


        self.user_session.append({})
        return response_message

    def _request_message_encoder(self, message: Message, instruction: str = "", stream: bool = False) -> dict[str, str]:
        query = message.content  # 用户输入
        response_mode = "streaming" if stream else "blocking"
        # Todo(chengmo): 获取或者新建conversation_id
        conversation_id = ""
        # Todo(chengmo): 获取或者新建user_id
        user_id = ""

        inputs = {
            "function_call.user_instruction": "",
            "function_call.builtin_tool_list": []
        }
        inputs["function_call.user_instruction"] = instruction

        # Todo(chengmo): 获取或者新建builtin_tool_list
        model_configs = {}

        return Message({
            "query": query,
            "response_mode": response_mode,
            "conversation_id": conversation_id,
            "user": user_id,
            "inputs": inputs,
            "model_configs": model_configs
        })

    def _response_message_decoder(self, response: dict[str, str]) -> Message:
        pass


class FunctionCallMessage(LLMMessage):
    converstation_id: str = ""

    def __str__(self):
        pass


class FunctionCallResponse(CompletionResponse):
    converstation_id: str = ""

    def __init__(self, response, stream: bool = False):
        """初始化客户端状态。"""
        super().__init__(response, stream)
        pass


class FunctionCollector(object):
    _instance = None
    _initialized = False

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._enable_function = {}

    def __new__(cls, *args, **kwargs):
        """
        单例模式
        """
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def register_builtin_function(self, function: Component):
        """
        注册内置函数
        """
        if not isinstance(function, Component):
            raise TypeError("Function must be a subclass of Component")
        pass

    def register_custom_function(self, function: Component):
        """
        注册自定义函数
        """
        if not isinstance(function, Component):
            raise TypeError("Function must be a subclass of Component")

    def get_function_impl_by_name(self, func_name: str) -> Component:
        """
        根据函数名获取函数实现
        """
        pass

    def get_total_function(self) -> list[str]:
        """
        获取已注册的函数名列表
        """
        pass

    def get_enable_function(self) -> list[str]:
        """
        获取当前用户可用的func列表
        """
        pass


if __name__ == "__main__":
    function_call = FunctionCall(instruction="", tools_set=[])
    message = Message("秦始皇是谁？")
    function_call.chat(message)
