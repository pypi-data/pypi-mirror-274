from typing import Iterator, List, Union
from langchain_core.documents import Document
from langchain_community.document_loaders.base import BaseLoader
from ..config import get_textlong_folder, _DOCS_FOLDER_NAME
from .base import LocalFilesLoader

class QAMarkdownLoader(LocalFilesLoader):
    """
    指定引用源过滤，就可以实现QA对分离的知识查询：
      即根据问题的文本相似度查询文档中的Question部份，
      但根据Question结果的source部份查询匹配的Anwser，作为LLM的参考结果。
    """

    def __init__(
        self,
        *args, **kwargs
    ):
        super().__init__(documents_folder, **kwargs)
        self.extensions = ["md", "markdown"]
        self.documents_folder = os.path.join(get_textlong_folder(), self.user_id, _QA_FOLDER_NAME)


