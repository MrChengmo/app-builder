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

from typing import Tuple
from typing import Union
from typing import Optional
from pydantic import Field
from uuid import UUID
from enum import Enum
from appbuilder.core.component import Component, Message
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace


class Table(Message):
    """
    Table object, for storing the content of a table which is a part of a page.
    """
    table_id: UUID = Field(..., description="Table ID")
    table_offset: Tuple[int, int] = Field(...,
        description="A tuple representing the start and end indices based on text offset")
    body: Optional[list[list[str]]] = Field(None, description="Table body")
    meta: Optional[dict] = Field(
        dict, description="An extensible dictionary field")


class Image(Message):
    """
    Image object, for storing the content of an image which is a part of a page.
    """
    image_id: UUID = Field(..., description="Image ID")
    image_offset: Optional[Tuple[int, int]] = Field(None,
        description="A tuple representing the start and end indices based on text offset")
    caption: Optional[str] = Field(None, description="Image caption")
    meta: Optional[dict] = Field(
        None, description="An extensible dictionary field")


class Page(Message):
    """
    Page object, for storing the content of a page which is a part of a document.
    """
    page_id: UUID = Field(..., description="Page ID")
    page_offset: Optional[Tuple[int, int]] = Field(...,
        description="A tuple representing the start and end indices based on text offset")
    tables: Optional[list[Table]] = Field(
        [], description="List of tables in the page")
    images: Optional[list[Image]] = Field(
        [], description="List of images in the page")
    formulas: Optional[str] = Field(
        [], description="List of formulas in the page")
    title: Optional[str] = Field(None, description="Page title")
    header: Optional[list[str]] = Field([], description="Page header")
    footer: Optional[list[str]] = Field([], description="Page footer")
    meta: Optional[dict] = Field(
        None, description="An extensible dictionary field")


class ChunkType(Enum):
    """
    ChunkType
    """
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
    TEXT = "text"
    IMAGE = "image"
    TABLE = "table"
    # add more chunk types as needed


class Chunk(Message):
    """
    Chunk
    """
    chunk_id: UUID = Field(..., description="Chunk ID")
    content: Optional[str] = Field("", description="Chunk content")
    chunk_type: ChunkType = Field(..., description="Chunk type")
    meta: Optional[dict] = Field(
        None, description="An extensible dictionary field")


class Document(Message):
    """
    Document
    """
    file_id: UUID = Field(..., description="File ID")
    text: Optional[int] = Field("", description="Text")
    pages: Optional[list[Page]] = Field(
        None, description="List of pages in the document")
    filename: Optional[str] = Field("", description="Filename")
    url: Optional[str] = Field("", description="URL")
    mime: Optional[str] = Field("", description="MIME type")
    chunks: Optional[list[Chunk]] = Field(
        None, description="List of chunks in the document")
    meta: Optional[dict] = Field(
        None, description="An extensible dictionary field")
