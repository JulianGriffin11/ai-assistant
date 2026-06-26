from launchpad.core.schema import NodeConfig, WorkflowSchema
from launchpad.core.workflow import Workflow
from launchpad.workflows.examples.nested_workflow.nodes.reply.draft_reply_node import (
    DraftReplyNode,
)
from launchpad.workflows.examples.nested_workflow.schema import (
    NestedWorkflowEventSchema,
)


class ReplyDraftWorkflow(Workflow):
    workflow_schema = WorkflowSchema(
        description="Child workflow that drafts a customer-care reply.",
        event_schema=NestedWorkflowEventSchema,
        start=DraftReplyNode,
        nodes=[
            NodeConfig(
                node=DraftReplyNode,
                description="Drafts a deterministic reply for the customer.",
            ),
        ],
    )
