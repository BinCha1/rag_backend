import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader, TextLoader


class DocumentParser:
    """
    Extracts raw text from PDF or TXT.
    Output = plain string (IMPORTANT for pipeline stability)
    """

    async def extract_text(self, file) -> str:
        content = await file.read()

        _, ext = os.path.splitext(file.filename)

        tmp_file = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
        tmp_file.write(content)
        tmp_file.close()

        try:
            if file.filename.endswith(".pdf"):
                loader = PyPDFLoader(tmp_file.name)
            elif file.filename.endswith(".txt"):
                loader = TextLoader(tmp_file.name)
            else:
                raise ValueError("Only PDF and TXT supported")

            documents = loader.load()

            # combine all pages into single text
            text = " ".join([doc.page_content for doc in documents])

            return text

        finally:
            os.unlink(tmp_file.name)
