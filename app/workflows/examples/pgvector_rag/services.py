from pydantic import BaseModel
import tiktoken
import vecs
from launchpad.database.database_utils import DatabaseUtils
from dotenv import load_dotenv
from openai import OpenAI
from vecs.collection import Collection


class Record(BaseModel):
    id: str
    metadata: dict


class RetrievalResults(BaseModel):
    results: list[Record]


class PgvectorRAGService:
    def __init__(
        self, collection_name="docs", embedding_model="text-embedding-3-small"
    ):
        """Initialize the RAG service with vector database connection and OpenAI client."""
        load_dotenv(".env")

        # Get database connection string
        db_connection = DatabaseUtils.get_connection_string()

        # Create vector store client
        self.__vx = vecs.create_client(db_connection)

        # Get or create collection
        self.__collection_name = collection_name
        self.__collection = self.__vx.get_or_create_collection(
            name=collection_name, dimension=1536
        )

        # Initialize OpenAI client
        self.client = OpenAI()
        self.embedding_model = embedding_model

    def get_embedding(self, text):
        """Generate embedding for the given text."""
        text = text.replace("\n", " ")
        return (
            self.client.embeddings.create(input=[text], model=self.embedding_model)
            .data[0]
            .embedding
        )

    def get_collection(self) -> Collection:
        """Get the collection."""
        return self.__collection

    def count_tokens(self, text, encoding_name="cl100k_base"):
        """Count the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        return len(encoding.encode(text))

    def upsert(self, records: list[tuple[str, list[float], dict]]):
        """Upsert a document into the vector database."""
        self.__collection.upsert(records=records)

    def parse_results(
        self, results: list[tuple[str, list[float], dict]]
    ) -> RetrievalResults:
        """Format the results from the vector database."""
        return RetrievalResults(
            results=[Record(id=result[0], metadata=result[1]) for result in results]
        )

    def disconnect(self):
        """Disconnect from the vector database."""
        self.__vx.disconnect()
