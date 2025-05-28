
from .corpus_handler.create_corpus import create_corpus 
from .corpus_handler.list_corpora import list_corpora
from .corpus_handler.get_corpus_info import get_corpus_info
from .corpus_handler.delete_corpus import delete_corpus

from .documents_handler.add_document import add_data
from .documents_handler.delete_document import delete_document


__all__ = [
    "create_corpus",
    "list_corpora",
    "get_corpus_info",
    "delete_corpus",
    "add_data",
    "delete_document",
]
