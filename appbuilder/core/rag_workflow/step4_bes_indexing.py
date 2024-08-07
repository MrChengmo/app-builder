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
from base_class import IndexingBase
from appbuilder.core.components.doc_parser.base import ParseResult
from appbuilder import BESVectorStoreIndex


class SimpleBesSimpleIndex(IndexingBase):
    def __init__(self, cluster_id, user_name, password,
                 index_name=None, index_type="hnsw", prefix="/rpc/2.0/cloud_hub"):
        """
            初始化BESVectorStoreIndex类的一个实例。

        Args:
            cluster_id (str): Elasticsearch集群ID。
            user_name (str): Elasticsearch用户名。
            password (str): Elasticsearch密码。
            index_name (str, optional): Elasticsearch索引名称，默认为None。如果不指定，则使用默认的索引名称。
            index_type (str, optional): Elasticsearch索引类型，默认为"hnsw"。可选值包括"hnsw"和"ivf"。
            prefix (str, optional): RPC请求的前缀，默认为"/rpc/2.0/cloud_hub"。

        Returns:
            None.

        Raises:
            无.
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
            prefix=prefix
        )

    def _create_index_object(self, chunk: Chunk) -> dict:
        """
            创建索引对象，包含文本、向量、元数据和ID等信息。
        如果向量维度为None，则将其设置为chunk的维度；否则，需要保证所有chunk的向量维度一致。

        Args:
            chunk (Chunk): 待处理的chunk对象，包含文本、向量、元数据和ID等信息。

        Returns:
            dict: 返回一个字典，包含以下键值对：
                - "_index" (str): 索引名称，默认为self.index_name。
                - "_source" (dict): 包含以下键值对：
                    - "text" (str): 待处理chunk的文本内容。
                    - "vector" (list[float]): 待处理chunk的向量，可能为None。
                    - "metadata" (str): 待处理chunk的元数据，可能为None。
                    - "id" (str): 待处理chunk的ID，类型为str。
        """
        text = chunk.content
        vector = chunk.meta.get("embedding", None)
        if self.vector_dims is None:
            self.vector_dims = len(vector)
        else:
            assert len(vector) == self.vector_dims, "vector dims not match"
        metadata = str(chunk.chunk_id)
        id = str(chunk.chunk_id)
        return {
            "_index": self.index_name,
            "_source": {
                "text": text,
                "vector": vector,
                "metadata": metadata,
                "id": id
            }
        }

    @components_run_trace
    def run(self, message: Message) -> Message:
        """
            将消息的内容转换为索引对象，并将其批量写入到BES Vector Store Index中。

        Args:
            message (Message): 包含要转换和写入索引的文本内容的消息对象。

        Returns:
            Message: 返回一个空的消息对象，表示成功处理了该消息。

        Raises:
            无。
        """
        document = message.content

        index_pre_list = []
        for chunk in document.chunks:
            index_pre_list.append(self._create_index_object(chunk))

        mappings = BESVectorStoreIndex.create_index_mappings(
            self.index_type, self.vector_dims)
        self.bes_index.bes_client.indices.create(index=self.index_name,
                                                 body={"settings": {"index": {"knn": True}}, "mappings": mappings})

        self.bes_index.helpers.bulk(self.bes_index.bes_client, index_pre_list)


if __name__ == '__main__':
    from step1_xmind_parser import SimpleXmindParser
    os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-RPJR9XSOVFl6mb5GxHbfU/072be74731e368d8bbb628a8941ec50aaeba01cd"
    xmind_parser = SimpleXmindParser()
    parse_res = xmind_parser.run(
        Message(content="./demo.txt"), return_raw=True)

    from step2_doc_split_chunker import SimpleDocSplitter
    doc_splitter = SimpleDocSplitter()
    split_res = doc_splitter.run(parse_res)

    from step3_ernie_embedding import SimpleEmbedding
    embedding = SimpleEmbedding()
    embedding_res = embedding.run(split_res)

    os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-lBMDbhSjBl9kQyAByKY6H/d95cc204b24917b9a2792217d332a6d6f9480aa4"
    bes_index = SimpleBesSimpleIndex(
        cluster_id="940959010151075840",
        user_name="superuser",
        password="Appbuilder123",
        index_name="test_index_2024_08_06_21"
    )
    bes_index.run(embedding_res)
    print('done')
