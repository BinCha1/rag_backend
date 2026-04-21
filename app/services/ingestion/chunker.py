from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)


class TextChunker:
    """
    Handles chunking using LangChain-supported strategies.
    """

    @staticmethod
    def chunk(text: str, strategy: str):

        if strategy == "recursive":
            """
            Best production-ready splitter for RAG systems.
            Preserves structure using recursive breakdown.
            """
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            return splitter.split_text(text)

        elif strategy == "sentence":
            """
            Simple paragraph/sentence-based splitting.
            """
            return [t.strip() for t in text.split("\n\n") if t.strip()]

        else:
            raise ValueError("Invalid chunk strategy")
