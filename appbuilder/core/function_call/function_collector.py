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
