from enum import Enum

from launchpad.workflows.examples.streaming.workflow import ExampleStreamingWorkflow
from launchpad.workflows.examples.quickstart.workflow import CustomerCareWorkflow
from launchpad.workflows.examples.langfuse_tracing.workflow import (
    LangfuseTracingWorkflow,
)
from launchpad.workflows.examples.nested_workflow.workflow import (
    NestedWorkflow,
)
from launchpad.workflows.examples.pgvector_rag.workflow import RagExampleWorkflow


class WorkflowRegistry(Enum):
    STREAMING = ExampleStreamingWorkflow
    QUICKSTART = CustomerCareWorkflow
    LANGFUSE_TRACING = LangfuseTracingWorkflow
    PGVECTOR_RAG = RagExampleWorkflow
    NESTED_WORKFLOW = NestedWorkflow
