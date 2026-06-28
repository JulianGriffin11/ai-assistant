from core.schema import WorkflowSchema, NodeConfig
from core.workflow import Workflow
from schemas.nylas_webhook_schema import WebhookEvent
from workflows.email_workflow_nodes.email_filter_node import EmailFilterNode


class EmailWorkflow(Workflow):
    workflow_schema = WorkflowSchema(
        description="",
        event_schema=WebhookEvent,
        start=EmailFilterNode,
        nodes=[
            NodeConfig(
                node=EmailFilterNode,
                connections=[],
                description="",
                parallel_nodes=[],
            ),
        ],
    )