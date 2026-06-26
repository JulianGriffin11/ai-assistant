from launchpad.core.schema import WorkflowSchema, NodeConfig
from launchpad.core.workflow import Workflow
from launchpad.workflows.examples.pgvector_rag.schema import RagExampleEventSchema
from launchpad.workflows.examples.pgvector_rag.nodes.retrieval_node import RetrievalNode
from launchpad.workflows.examples.pgvector_rag.nodes.generation_node import GenerationNode


class RagExampleWorkflow(Workflow):
    workflow_schema = WorkflowSchema(
        description="Simple RAG example workflow",
        event_schema=RagExampleEventSchema,
        start=RetrievalNode,
        nodes=[
            NodeConfig(
                node=RetrievalNode,
                connections=[GenerationNode],
                description="",
            ),
            NodeConfig(
                node=GenerationNode,
                connections=[],
                description="",
            ),
        ],
    )
