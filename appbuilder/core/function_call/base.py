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
from appbuilder.utils.sse_util import SSEClient
from appbuilder.core.components.llms.base import CompletionResponse
from appbuilder.core._exception import AppBuilderServerException


class FunctionCallEventType(object):
    """
    FunctionCallEventType, 函数调用事件类型
    """
    LOCAL_FUNCTION_CALL = "local_function_call"  # 调用本地的函数实现
    LOCAL_FUNCTION_CALL_RESULTS = "local_function_call_results"  # 本地调用函数的实现结果
    REMOTE_FUNCTION_CALL = "remote_function_call"  # 调用远程的函数实现
    REMOTE_FUNCTION_CALL_RESULTS = "remote_function_call"  # 远程调用函数的实现结果
    FUNCTION_CALL_COMPLETED = "function_call_completed"  # 函数调用过程完成


class FunctionCallResponse(CompletionResponse):
    error_no = 0
    error_msg = ""
    result = None
    log_id = ""
    extra = None
    conversation_id = ""

    

    def __init__(self, response, stream: bool = False):
        """初始化客户端状态。"""
        super().__init__(response, stream)
        
        if stream:
            self.parse_stream_data(response)
        else:
            self.parse_block_data(response)
    
    def parse_stream_data(self, response):
        def stream_data():
            sse_client = SSEClient(response)
            for event in sse_client.events():
                if not event:
                    continue
                answer = self.parse_stream_data(event)
                if answer is not None:
                    yield answer

        self.result = stream_data()

    def parse_block_data(self, response):
        if response.status_code != 200:
            self.error_no = response.status_code
            self.error_msg = "error"
            self.result = response.text
        
            raise AppBuilderServerException(self.log_id, self.error_no, self.result)
        else:
            data = response.json()
            data = response.json()

            if "code" in data and data.get("code") != 0:
                raise AppBuilderServerException(self.log_id, data["code"], data["message"])

            if "code" in data and "message" in data and "requestId" in data:
                raise AppBuilderServerException(self.log_id, data["code"], data["message"])

            if "code" in data and "message" in data and "status" in data:
                raise AppBuilderServerException(self.log_id, data["code"], data["message"])

            self.result = data.get("result").get("answer", None)
            self.conversation_id = data.get("result").get("conversation_id", "")
            content = data.get("result").get("content", None)
            res = self.parse_func_event_data(content)
        
    def parse_func_event_data(self, content:dict ={}):
        if not content:
            return
        
        for item in content:
            event = item.get("event", "")
            event_type = item.get("event_type", "")
            text = item.get("text", "")
            event_status = item.get("event_status", "")
            evetn_message = item.get("event_message", "")
            event_id = item.get("event_id", -1)