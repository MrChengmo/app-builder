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
from appbuilder.utils.sse_util import SSEClient
from appbuilder.core.components.llms.base import CompletionResponse
from appbuilder.core.components.llms.base import LLMMessage
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


class FunctionCallEvent(object):
    event: str = None
    """
    event是当前事件，区分如下几类，枚举：
    意图类事件：
        * function_call：function_call调用，返回type为function_call

    富文本类事件，富文本类事件可能有其独立的逻辑，event也各不相同：
        * Text2Image：文生图，返回type为image
        * DocCropEnhance：文档增强，返回type为image
        * CodeInterpreter：代码解释器，返回type可以为files, code, text
        * BaiduSearch / RAGAgent：问答，返回type可以为references, text
        * AgentConfigGenerator / RAGConfigGenerator：自然语言转配置结果，当前用于App Builder Bot生成的应用，返回type为json
        * BingImageSearch：bing图片搜索，返回type为files
        * TTS：文本转语音，返回type为audio
    """

    event_status: str = None
    """
    event_status标志了当前event的状态，枚举：
        * running：当前事件运行中，内容流式输出的中间事件
        * done：当前事件完成，内容流式输出的终止事件
        * preparing：准备执行工具
        * error：当前工具执行错误
        * success：当前工具执行成功
    """

    event_id: str = None
    """
    当前事件的id。对于同一个事件，type不同event_id就不同
    例如：同个代码解释器应用中代码与文本穿插，这时候event_id是不同的
    """

    event_type: str = None
    """
    如下枚举类型：
        * text：大模型文本
        * function_call：模型调用指令
        * code：代码块
        * files：代码解释器生成的文件，不同类型需要特殊判断
        * urls：搜索得到的文件链接
        * references：引用
        * image: 图片
        * audio：语音
        * video：视频
        * json：定制化内容
        * status：执行状态，error或success，内容为报错信息
    """

    text: str = None
    """
    不同type对应的text类型不同：
        * text：string
        * function_call：json
        * code：string
        * files（文件URL）：list of string
        * urls：list of string
        * references：list of object
        * image: string of url
        * audio：string of url
        * video: string of url
        * json：json
        * status：string
    """

    def __init__(self, event: str = None):
        """初始化客户端状态。"""
        self.event = event

    def _status_trans(self, event_status:str ="") ->FunctionCallEventType:
        # if event_status == "local":
        #     return FunctionCallEventType.LOCAL_FUNCTION_CALL
        # elif event_status == "remote":
        #     return FunctionCallEventType.REMOTE_FUNCTION_CALL
        # else:
        #     raise ValueError("Unknown event type")
        return FunctionCallEventType.FUNCTION_CALL_COMPLETED

    def __str__(self) -> str:
        return f"Event: {self.event}, EventStatus: {self.event_status}, EventId: {self.event_id}\
        , EventType: {self.event_type}, Text: {self.text}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__} Event: {self.event}, EventStatus: {self.event_status}, EventId: {self.event_id}\
        , EventType: {self.event_type}, Text: {self.text}"


class FunctionCallMessage(LLMMessage):
    conversation_id: str = ""

    def __str__(self):
        return f"Message(name={self.name}, content={self.content}, mtype={self.mtype}, extra={self.extra}, conversation_id={self.conversation_id})"


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
            if "code" in data and data.get("code") != 0:
                raise AppBuilderServerException(self.log_id, data["code"], data["message"])

            if "code" in data and "message" in data and "requestId" in data:
                raise AppBuilderServerException(self.log_id, data["code"], data["message"])

            if "code" in data and "message" in data and "status" in data:
                raise AppBuilderServerException(self.log_id, data["code"], data["message"])

            self.id = data.get("id", "")

            self.answer = data.get("result").get("answer", None)
            self.conversation_id = data.get("result").get("conversation_id", "")
            self.events = self.parse_func_event_data( data.get("result").get("content", None))

    def message_iterable_wrapper(self, message):
        """
        对模型输出的 Message 对象进行包装。
        当 Message 是流式数据时，数据被迭代完后，将重新更新 content 为 blocking 的字符串。
        """

        class IterableWrapper:
            def __init__(self, stream_content):
                self._content = stream_content
                self._concat = ""
                self._extra = {}

            def __iter__(self):
                return self

            def __next__(self):
                try:
                    resp = next(self._content)
                    result_json = resp.get("result")
                    char = result_json.get("answer", "")
                    conversation_id = result_json.get("conversation_id", "")
                    content = result_json.get("content", None)
                    if content:
                        for item in content:
                            if item.get("content_type") == "references":
                                references = item.get("outputs").get("references")
                                if references:
                                    for ref in references:
                                        key = ref["from"]
                                        if key in self._extra.keys():
                                            self._extra[key].extend(ref)
                                        else:
                                            self._extra[key] = [ref]
                    message.extra = self._extra  # Update the original extra
                    message.conversation_id = conversation_id
                    self._concat += char
                    return char
                except StopIteration:
                    message.content = self._concat  # Update the original content
                    raise

        from collections.abc import Generator
        if isinstance(message.content, Generator):
            # Replace the original content with the custom iterable
            message.content = IterableWrapper(message.content)
        return message

        
    def parse_func_event_data(self, content:dict ={}):
        event_data = []

        if not content:
            return event_data
        
        for item in content:
            event = FunctionCallEvent()
            event.event = item.get("event", "")
            event.event_type = item.get("event_type", "")
            event.text = item.get("text", "")
            event.event_status = item.get("event_status", "")
            event.event_id = item.get("event_id", -1)

            event_data.append(event)
        
        return event_data
    
    def to_message(self):
        message = FunctionCallMessage()
        message.id = self.id
        message.content = self.answer
        message.extra = self.events
        message.conversation_id = self.conversation_id
        return self.message_iterable_wrapper(message)