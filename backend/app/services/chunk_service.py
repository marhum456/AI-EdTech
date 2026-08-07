from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(text: str):
    """
    Split lesson text into overlapping chunks for RAG.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = splitter.split_text(text)

    return chunks