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

import os
import uuid
from appbuilder.core.component import Component, Message
from appbuilder.utils.trace.tracer_wrapper import components_run_trace

from data_class import (
    Document,
    Chunk
)
from base_class import ChunkerBase
from appbuilder.core.components.doc_parser.base import ParseResult
from appbuilder import DocSplitter


class SimpleDocSplitter(ChunkerBase):
    def __init__(self, chunk_size=340):
        """
            Initializes the DocSplitter object with a default chunk size of 340 bytes.

        Args:
            chunk_size (int, optional): The maximum length of each segment in bytes. Defaults to 340.

        Returns:
            None: This function does not return anything. It initializes an instance variable doc_splitter.
        """
        self.doc_splitter = DocSplitter(
            splitter_type="split_by_chunk",
            max_segment_length=chunk_size
        )

    @components_run_trace
    def run(self, message: Message) -> Message:
        """
        将文档分割成单个段落，并返回一个新的消息对象。

        Args:
            message (Message): 包含要处理的文档内容的消息对象。消息中应该有一个名为 "parser_result" 的元数据项，其值是一个字典，包含了解析结果。

        Raises:
            ValueError: 如果文档分割失败时会引发此异常。

        Returns:
            Message: 包含已分割的文档内容和相关元数据的新消息对象。元数据项 "parser_result" 已被删除。
        """
        try:
            doc_parser_result = message.content.meta.get("parser_result", None)
            doc_splitter_result = self.doc_splitter.run(
                Message(doc_parser_result)
            )
        except Exception as e:
            raise ValueError(f"Failed to split document: {e}")

        res_document = self._split_res_to_document(
            message.content, doc_splitter_result.content)
        del (res_document.meta["parser_result"])
        return Message(res_document)

    def _split_res_to_document(self, origin_document, split_res):
        """
            将分词结果转换为文档对象，并设置到origin_document中。

        Args:
            origin_document (Document): 原始文档对象，需要包含chunks属性。
            split_res (dict): 分词结果字典，包含"paragraphs"键，值是一个列表，每个元素是一个字典，包含"text"键和其他可选的键值对。

        Returns:
            Document: 返回修改后的origin_document，其中chunks属性已经被更新。

        Raises:
            无。
        """
        chunk_list = []

        for para_idx, paragraph in enumerate(split_res.get("paragraphs", [])):
            chunk = {}
            chunk["chunk_id"] = uuid.uuid4()
            chunk["chunk_type"] = "text"
            chunk["content"] = paragraph.get("text", "")
            chunk["meta"] = {}
            chunk["meta"]["paragraph"] = paragraph
            chunk_list.append(Chunk(**chunk))

        origin_document.chunks = chunk_list
        return origin_document


if __name__ == '__main__':
    from a_xmind_parser import SimpleXmindParser
    os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-RPJR9XSOVFl6mb5GxHbfU/072be74731e368d8bbb628a8941ec50aaeba01cd"
    xmind_parser = SimpleXmindParser()
    parse_res = xmind_parser.run(
        Message(content="./demo.txt"), return_raw=True)

    doc_splitter = SimpleDocSplitter()
    split_res = doc_splitter.run(parse_res)
    print(split_res.model_dump_json(indent=4))
