from launchpad.core.schema import WorkflowSchema, NodeConfig
from launchpad.core.workflow import Workflow
from launchpad.workflows.examples.streaming.schema import OpenAIChatSchema
from launchpad.workflows.examples.streaming.nodes.text_streaming_node import TextStreamingNode
from launchpad.workflows.examples.streaming.nodes.structured_streaming_node import (
    StructuredStreamingNode,
)


class ExampleStreamingWorkflow(Workflow):
    workflow_schema = WorkflowSchema(
        description="",
        event_schema=OpenAIChatSchema,
        start=TextStreamingNode,
        nodes=[
            NodeConfig(
                node=TextStreamingNode,
                connections=[StructuredStreamingNode],
                description="",
            ),
            NodeConfig(
                node=StructuredStreamingNode,
                connections=[],
                description="",
            ),
        ],
    )
