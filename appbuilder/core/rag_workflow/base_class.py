# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
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
from appbuilder.core.component import Component, Message
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace
from data_class import Document


class ParserBase(Component):
    """
    ParserBase class
    """

    def __init__(self):
        """
            Initializes the ParserBase object. This method should not be called directly. It is intended
        to be used as a base class for other parser classes.

        Raises:
            NotImplementedError: Always raised because ParserBase is a base class and cannot be
                instantiated directly.
        """
        raise NotImplementedError(
            "ParserBase is a base class and cannot be instantiated directly")

    def __call__(self, *inputs, **kwargs):
        """
            调用函数，检查输入类型并运行函数。
        如果第一个参数不是Message类型，则引发TypeError异常。
        如果message.content不是字符串或列表，则引发TypeError异常。
        如果message.content是列表且不是所有元素都是字符串，则引发TypeError异常。

        Args:
            *inputs (Any, optional): 可变长度的输入，默认为空。如果提供了message参数，则应该是单个Message对象。
            **kwargs (dict, optional): 关键字参数，默认为空。如果提供了message参数，则应该包含一个名为'message'的键，其值为Message对象。

        Raises:
            TypeError: 如果第一个参数不是Message类型。
            TypeError: 如果message.content不是字符串或列表。
            TypeError: 如果message.content是列表且不是所有元素都是字符串。

        Returns:
            Any: 由run方法返回的任何内容。
        """
        message = inputs[0] if inputs else kwargs.get('message')
        if not isinstance(message, Message):
            raise TypeError("Expected argument of type Message")
        if not isinstance(message.content, (str, list)):
            raise TypeError("message.content must be of type str or List[str]")
        if isinstance(message.content, list) and not all(isinstance(i, str) for i in message.content):
            raise TypeError(
                "All elements in message.content list must be of type str")
        return self.run(*inputs, **kwargs)

    @components_run_trace
    def run(self, message: Message):
        """
            运行组件，处理消息。

        Args:
            message (Message): 待处理的消息对象，包括消息内容和其他相关信息。

        Returns:
            Message: 返回一个修改后的消息对象，包括可能的新的消息内容和其他相关信息。
        """
        return message


class ChunkerBase(Component):
    """
    ChunkerBase
    """

    def __init__(self):
        """
            Initializes the ChunkerBase object. This method should not be called as it raises a NotImplementedError.

        Raises:
            NotImplementedError: Always, since ChunkerBase is a base class and cannot be instantiated directly.
        """
        raise NotImplementedError(
            "ChunkerBase is a base class and cannot be instantiated directly")

    def __call__(self, *inputs, **kwargs):
        """
            调用函数，将输入的消息转换为Document类型。如果不是Message类型或者message.content不是Document类型，则抛出TypeError异常。
        参数（可选）:
            - inputs (tuple, optional): 包含单个元素的元组，该元素应该是一个Message对象。默认值：None。
            - kwargs (dict, optional): 包含键'message'和相应的值的字典，该值应该是一个Message对象。默认值：{}.
        返回值 (Any): 函数的返回值取决于实现细节。
        异常 (TypeError): 当输入不是Message类型或者message.content不是Document类型时抛出。
        """
        message = inputs[0] if inputs else kwargs.get('message')
        if not isinstance(message, Message):
            raise TypeError("Expected argument of type Message")
        if not isinstance(message.content, Document):
            raise TypeError("message.content must be of type Document")
        return self.run(*inputs, **kwargs)

    @components_run_trace
    def run(self, message: Message):
        """
            处理消息，返回新的Message对象。

        Args:
            message (Message): 包含要处理的消息内容的Message对象。
                content (Union[str, dict]): 消息内容，可以是字符串或者字典类型。如果是字典类型，则应该包含一个"type"键，其值为"message"。

        Returns:
            Message: 包含处理后的消息内容的Message对象。
            content (dict): 处理后的消息内容，格式与传入的message.content相同。

        Raises:
            无。
        """
        document_obj = message.content

        return Message(document_obj)
    pass


class EmbeddingBase(Component):
    """
    EmbeddingBase
    """

    def __init__(self):
        """
            Initializes the EmbeddingBase object. This method should not be called directly. It is intended
        to be used as a base class for other embedding classes.

        Raises:
            NotImplementedError: Always raised, since EmbeddingBase is a base class and cannot be
                instantiated directly.
        """
        raise NotImplementedError(
            "EmbeddingBase is a base class and cannot be instantiated directly")

    def __call__(self, *inputs, **kwargs):
        """
            调用函数，将输入转换为Message类型并执行run方法。
        如果输入不是Message类型，则引发TypeError异常。
        如果message.content不是Document类型，则引发TypeError异常。

        Args:
            inputs (tuple, optional): 可选参数，包含单个元素，该元素应为str或None类型，默认为空元组。
                如果提供了message参数，则它将被忽略。
            默认值：()
            kwargs (dict, optional): 关键字参数，包含一个名为'message'的键，其值应为Message类型，默认为{}.
            默认值：{}

        Raises:
            TypeError: 如果输入不是Message类型。
            TypeError: 如果message.content不是Document类型。

        Returns:
            Any: run方法返回的结果。
        """
        message = inputs[0] if inputs else kwargs.get('message')
        if not isinstance(message, Message):
            raise TypeError("Expected argument of type Message")
        if not isinstance(message.content, Document):
            raise TypeError("message.content must be of type Document")
        return self.run(*inputs, **kwargs)

    @components_run_trace
    def run(self, message: Message):
        """
            运行组件，处理消息。

        Args:
            message (Message): 待处理的消息对象，包括消息内容和其他相关信息。

        Returns:
            Message: 返回一个处理后的消息对象，包括处理结果和其他相关信息。
        """
        return message
    pass


class IndexingBase(Component):
    """
    IndexingBase
    """

    def __init__(self):
        """
            Initializes the IndexingBase.

        Raises:
            NotImplementedError: Always, as IndexingBase is a base class and cannot be instantiated directly.
        """
        raise NotImplementedError(
            "IndexingBase is a base class and cannot be instantiated directly")

    def __call__(self, *inputs, **kwargs):
        """
            调用函数，将输入的消息转换为Document类型。
        如果输入不是Message类型或者message.content不是Document类型，则抛出TypeError异常。

        Args:
            inputs (tuple, optional): 包含单个元素的元组，该元素应该是一个Message对象（可选）。默认为空元组。
            如果提供了message参数，则它将被忽略。
            kwargs (dict, optional): 包含键值对的字典，其中键是'message'，值是一个Message对象（可选）。默认为空字典。
            如果提供了message参数，则它将被忽略。

        Raises:
            TypeError: 如果输入不是Message类型或者message.content不是Document类型。

        Returns:
            Any: 返回self.run()方法的返回值。
        """
        message = inputs[0] if inputs else kwargs.get('message')
        if not isinstance(message, Message):
            raise TypeError("Expected argument of type Message")
        if not isinstance(message.content, Document):
            raise TypeError("message.content must be of type Document")
        return self.run(*inputs, **kwargs)

    @components_run_trace
    def run(self, message: Message):
        """
            运行组件，处理消息。

        Args:
            message (Message): 待处理的消息对象，包括消息内容和其他相关信息。

        Returns:
            Message: 返回一个新的消息对象，包括处理后的消息内容和其他相关信息。如果没有进行任何处理，则直接返回输入的message对象。
        """
        return message
    pass


class RetrieverBase(Component):
    """
    RetrieverBase
    """

    def __init__(self):
        """
            Initializes the RetrieverBase object. This method should not be called directly. It is intended
        to be used as a base class for other retrievers.

        Raises:
            NotImplementedError: Always, since RetrieverBase is a base class and cannot be instantiated directly.
        """
        raise NotImplementedError(
            "RetrieverBase is a base class and cannot be instantiated directly")

    @components_run_trace
    def run(self, message: Message):
        """
            运行组件，处理消息。

        Args:
            message (Message): 待处理的消息对象。

        Returns:
            Message: 返回已经处理过的消息对象。
        """
        return message
    pass
