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

from base_class import RetrieverBase
from appbuilder.core.components.doc_parser.base import ParseResult
from appbuilder import BESVectorStoreIndex
from appbuilder import TagExtraction
from appbuilder import Embedding
from collections import Counter, defaultdict


class SimpleBesRetriever(RetrieverBase):
    def __init__(self, cluster_id, user_name, password, embedding,
                 index_name=None, index_type="hnsw", prefix="/rpc/2.0/cloud_hub"):
        """
            初始化BESVectorStoreIndexRetriever对象。

        Args:
            cluster_id (str): Elasticsearch集群ID。
            user_name (str): Elasticsearch用户名。
            password (str): Elasticsearch密码。
            embedding (Union[List[int], List[float]]): 向量表示，可以是整数或浮点数列表。
            index_name (Optional[str], optional): Elasticsearch索引名称，默认为None。如果未指定，则使用默认的索引名称。
            index_type (str, optional): Elasticsearch索引类型，默认为"hnsw"。
            prefix (str, optional): REST API前缀，默认为"/rpc/2.0/cloud_hub"。

        Raises:
            ValueError: 当`embedding`不是整数或浮点数列表时会引发ValueError异常。
        """
        self.index_name = index_name
        self.index_type = index_type
        self.vector_dims = None
        self.bes_index = BESVectorStoreIndex(
            cluster_id=cluster_id,
            user_name=user_name,
            password=password,
            index_name=index_name,
            index_type=index_type,
            prefix=prefix,
            embedding=embedding
        )
        self.bes_retrier = self.bes_index.as_retriever()
        self.tagger = TagExtraction(model="ERNIE Speed-AppBuilder")

    @components_run_trace
    def run(self, message: Message, document=None, top_k: int = 3) -> Message:
        """
            根据消息中的标签，查找相关简历并返回前top_k个。
        如果没有找到足够多的相关简历，则会引发一个异常。

        Args:
            message (Message): 包含标签信息的消息对象。
            document (Message, optional): 不使用此参数。默认值为 None。
            top_k (int, optional): 要返回的相关简历的数量。默认值为 3。

        Raises:
            Exception: 如果没有找到足够多的相关简历。

        Returns:
            Message: 包含前top_k个相关简历信息的消息对象，格式为 {"chunk_id": str, "chunk_text": str}。
        """
        tags = self.tagger.run(message)
        tag_list = [tag.split(".")[1] for tag in tags.content.split("\n")]

        resume_count = Counter()
        resume_content = dict()

        for tag in tag_list:
            relevant_resumes = self.bes_retrier(
                query=Message(tag), top_k=top_k)
            for idx, res in enumerate(relevant_resumes.content):
                name = res["meta"]
                resume_count[name] += 1
                resume_content[name] = res.get("text", "")

        sorted_resumes = sorted(resume_count.items(),
                                key=lambda x: x[1], reverse=True)
        if len(sorted_resumes) < top_k:
            raise Exception("Not enough relevant resumes found")

        result = []
        for idx, item in enumerate(sorted_resumes[:top_k]):
            result.append({
                "chunk_id": item[0],
                "chunk_text": resume_content[item[0]],
            })

        return Message(result)


if __name__ == '__main__':
    os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-lBMDbhSjBl9kQyAByKY6H/d95cc204b24917b9a2792217d332a6d6f9480aa4"

    retriever = SimpleBesRetriever(
        cluster_id="940959010151075840",
        user_name="superuser",
        password="Appbuilder123",
        index_name="test_index_2024_08_06_21",
        embedding=Embedding(),
    )

    retriever_res = retriever.run(Message("刘备、关羽和张飞分别打造了什么兵器？"))
    print(retriever_res.model_dump_json(indent=4))
