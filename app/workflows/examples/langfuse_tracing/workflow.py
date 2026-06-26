from launchpad.core.schema import WorkflowSchema, NodeConfig
from launchpad.core.workflow import Workflow
from launchpad.workflows.examples.langfuse_tracing.schema import LangfuseTracingEventSchema
from launchpad.workflows.examples.langfuse_tracing.nodes.context_summary_result_node import (
    ContextSummaryResult,
)
from launchpad.workflows.examples.langfuse_tracing.nodes.remove_comment_node import RemoveCommentNode
from launchpad.workflows.examples.langfuse_tracing.nodes.violation_detection_node import (
    ViolationDetectionNode,
)


class LangfuseTracingWorkflow(Workflow):
    workflow_schema = WorkflowSchema(
        description="",
        event_schema=LangfuseTracingEventSchema,
        start=ViolationDetectionNode,
        nodes=[
            NodeConfig(
                node=ViolationDetectionNode,
                connections=[ContextSummaryResult],
                description="",
            ),
            NodeConfig(
                node=ContextSummaryResult,
                connections=[RemoveCommentNode],
                description="",
            ),
            NodeConfig(
                node=RemoveCommentNode,
                connections=[],
                description="",
            ),
        ],
    )
