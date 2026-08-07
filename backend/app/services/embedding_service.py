from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Generates embeddings for text using Sentence Transformers.
    """

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_text(self, text: str):
        """
        Generate embedding for a single text.
        """
        return self.model.encode(text).tolist()

    def embed_documents(self, documents: list[str]):
        """
        Generate embeddings for multiple documents.
        """
        return self.model.encode(documents).tolist()


embedding_service = EmbeddingService()