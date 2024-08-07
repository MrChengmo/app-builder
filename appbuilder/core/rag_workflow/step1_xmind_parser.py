"""
parsers
"""
import os
import uuid
from appbuilder.core.component import Component, Message
from appbuilder.utils.trace.tracer_wrapper import components_run_trace

from data_class import (
    Document,
    Page,
    Table
)
from base_class import ParserBase

from appbuilder import DocParser


class SimpleXmindParser(ParserBase):
    """
    XMind parser class.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize XMind parser.
        """
        self.doc_parser_impl = DocParser()

    @components_run_trace
    def run(self, message: Message, return_raw=False) -> Message:
        """
        Run the XMind parser.
        """
        try:
            message_parser_result = self.doc_parser_impl.run(
                message, return_raw=return_raw)
        except Exception as e:
            raise ValueError(f"Xmind parser failed: {e}")

        try:
            document = self._parser_res_to_document(
                message_parser_result.content, file_name=message.content)
        except Exception as e:
            raise ValueError(f"Xmind Parser Result to Document failed: {e}")
        return Message(content=document)

    def _parser_res_to_document(self, parser_result, file_name) -> Document:
        """
            将解析结果转换为Document对象，包含文件名、页面信息和表格信息。

        Args:
            parser_result (ParseResult): ParseResult类型的解析结果，包含页面内容和表格信息等。
            file_name (str): 文件名，用于保存到Document中。

        Returns:
            Document (dict): Document对象，包含以下字段：
                    - file_id (str): 文件ID，UUID格式。
                    - file_name (str): 文件名，从file_name参数中获取。
                    - pages (list[dict]): 页面列表，每个元素是一个字典，包含以下字段：
                        - page_id (str): 页面ID，UUID格式。
                        - page_offset (tuple[int, int]): 页码范围，包含起始页码和结束页码。
                        - tables (list[dict]): 表格列表，每个元素是一个字典，包含以下字段：
                            - id (str): 表格ID，UUID格式。
                            - table_offset (tuple[int, int]): 表格范围，包含起始行号和结束行号。
                    - meta (dict): 额外信息，包含以下字段：
                        - parser_result (ParseResult): 原始的解析结果，ParseResult类型。

        """
        # parser_result：ParseResult
        # para_node_tree: Optional[List[ParaNode]] = []
        # page_contents: Optional[List[PageContent]] = []
        # pdf_data: Optional[str] = ""
        # raw: Optional[Dict] = {}
        document = {}
        # file_id
        document["file_id"] = uuid.uuid4()
        document["file_name"] = file_name.split("/").pop()
        document["pages"] = []
        total_page_num = len(parser_result.page_contents)
        for idx, page_content in enumerate(parser_result.page_contents):
            page = {}
            # page basic info
            page["page_id"] = uuid.uuid4()
            page["page_offset"] = (idx, idx + 1)

            # page table
            page["tables"] = []
            total_table_num = len(page_content.tables)
            for table_idx, element in enumerate(page_content.tables):
                table = {}
                table["id"] = uuid.uuid4()
                table["table_offset"] = (table_idx, table_idx + 1)
                # pass
                page["tables"].append(Table(**table))

            # page other info
            document["pages"].append(Page(**page))

        document["meta"] = {
            "parser_result": parser_result
        }
        return Document(**document)


if __name__ == "__main__":
    os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-RPJR9XSOVFl6mb5GxHbfU/072be74731e368d8bbb628a8941ec50aaeba01cd"
    xmind_parser = SimpleXmindParser()
    res = xmind_parser.run(Message(content="./demo.txt"), return_raw=True)
    print(res.model_dump_json(indent=4))
