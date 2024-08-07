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
from base_class import EmbeddingBase
from appbuilder.core.components.doc_parser.base import ParseResult
from appbuilder import Embedding


class SimpleEmbedding(EmbeddingBase):
    def __init__(self):
        """
            Initializes the instance of the class.

        Args:
            None.

        Returns:
            None.
        """
        self.embedding = Embedding()

    @components_run_trace
    def run(self, message: Message) -> Message:
        """
            运行函数，将文档的每个chunk的内容转换为其对应的词向量，并存储在chunk的meta中。
        如果出现任何错误，则抛出RuntimeError异常。

        Args:
            message (Message): 包含要处理的文档的Message实例。文档由Document类表示，每个chunk由Chunk类表示。

        Returns:
            Message: 返回一个包含已经处理过的文档的Message实例。文档由Document类表示，每个chunk由Chunk类表示，chunk的meta字典中包含了对应chunk的词向量。

        Raises:
            RuntimeError: 当发生任何错误时，会抛出RuntimeError异常，提供错误信息。
        """
        document = message.content
        content_list = [
            chunk.content for chunk in document.chunks
        ]

        try:
            embedding_list = self.embedding.batch(
                content_list
            )
        except Exception as e:
            raise RuntimeError("Failed to embed document: {}".format(e))

        for i, chunk in enumerate(document.chunks):
            chunk.meta["embedding"] = embedding_list.content[i]

        return Message(content=document)


if __name__ == '__main__':
    from step1_xmind_parser import SimpleXmindParser
    os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-RPJR9XSOVFl6mb5GxHbfU/072be74731e368d8bbb628a8941ec50aaeba01cd"
    xmind_parser = SimpleXmindParser()
    parse_res = xmind_parser.run(
        Message(content="./demo.txt"), return_raw=True)

    from step2_doc_split_chunker import SimpleDocSplitter
    doc_splitter = SimpleDocSplitter()
    split_res = doc_splitter.run(parse_res)

    embedding = SimpleEmbedding()
    embedding_res = embedding.run(split_res)
    print(embedding_res.model_dump_json(indent=4))
