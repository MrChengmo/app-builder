import os
import appbuilder
from appbuilder import Message
from step1_xmind_parser import SimpleXmindParser
from step2_doc_split_chunker import SimpleDocSplitter
from step3_ernie_embedding import SimpleEmbedding
from step4_bes_indexing import SimpleBesSimpleIndex
from step5_bes_search_retriever import SimpleBesRetriever


def runtime_main():
    """
    函数用于在运行时进行主程序的操作，包括设置环境变量、初始化模型、运行示例代码等。

    Args:
        无参数，函数不需要传入任何参数。

    Returns:
        无返回值，直接在函数内部对应的变量进行赋值操作。

    Raises:
        无异常抛出。
    """
    os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-RPJR9XSOVFl6mb5GxHbfU/072be74731e368d8bbb628a8941ec50aaeba01cd"

    xmind_parser = SimpleXmindParser()
    doc_splitter = SimpleDocSplitter()
    embedding = SimpleEmbedding()

    demo_file = "./demo.txt"

    parse_res = xmind_parser(Message(demo_file), return_raw=True)
    split_res = doc_splitter(parse_res)
    embedding_res = embedding(split_res)

    os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-lBMDbhSjBl9kQyAByKY6H/d95cc204b24917b9a2792217d332a6d6f9480aa4"
    # 运行前更改 index_name
    index_name = "test_index_2024_08_06_22"

    bes_config = {
        "cluster_id": "940959010151075840",
        "user_name": "superuser",
        "password": "Appbuilder123",
        "index_name": index_name
    }

    bes_index = SimpleBesSimpleIndex(
        cluster_id=bes_config["cluster_id"],
        user_name=bes_config["user_name"],
        password=bes_config["password"],
        index_name=bes_config["index_name"],
    )
    bes_index(embedding_res)

    retriever = SimpleBesRetriever(
        cluster_id=bes_config["cluster_id"],
        user_name=bes_config["user_name"],
        password=bes_config["password"],
        index_name=bes_config["index_name"],
        embedding=appbuilder.Embedding(),
    )

    retriever_res = retriever(Message("刘备、关羽和张飞分别打造了什么兵器？"), top_k=1)
    print(retriever_res.model_dump_json(indent=4))

    chunk_list = []
    for chunk in embedding_res.content.chunks:
        for retriever in retriever_res.content:
            if retriever["chunk_id"] == str(chunk.chunk_id):
                chunk_list.append(chunk)
                break

    for chunk in chunk_list:
        print(chunk.model_dump_json(indent=4))


if __name__ == '__main__':
    runtime_main()
