from launchpad.core.nodes.base import Node
from launchpad.core.task import TaskContext
from launchpad.workflows.examples.pgvector_rag.services import PgvectorRAGService, RetrievalResults
from launchpad.workflows.examples.pgvector_rag.schema import RagExampleEventSchema


class RetrievalNode(Node):
    class OutputType(Node.OutputType):
        results: RetrievalResults

    async def process(self, task_context: TaskContext) -> TaskContext:
        rag_service = PgvectorRAGService()
        collection = rag_service.get_collection()
        event: RagExampleEventSchema = task_context.event
        embedding = rag_service.get_embedding(event.query)

        results = collection.query(
            data=embedding,
            limit=3,
            measure="cosine_distance",
            include_value=False,
            include_metadata=True,
        )
        results: RetrievalResults = rag_service.parse_results(results)
        output = self.OutputType(results=results)

        self.save_output(output)
        rag_service.disconnect()

        return task_context
