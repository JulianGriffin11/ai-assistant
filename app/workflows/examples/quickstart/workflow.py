from launchpad.core.schema import WorkflowSchema, NodeConfig
from launchpad.core.workflow import Workflow
from launchpad.workflows.examples.quickstart.schema import CustomerCareEventSchema
from launchpad.workflows.examples.quickstart.nodes.analyze_ticket_node import AnalyzeTicketNode
from launchpad.workflows.examples.quickstart.nodes.close_ticket_node import CloseTicketNode
from launchpad.workflows.examples.quickstart.nodes.determine_intent_ticket_node import (
    DetermineTicketIntentNode,
)
from launchpad.workflows.examples.quickstart.nodes.escalate_ticket_node import EscalateTicketNode
from launchpad.workflows.examples.quickstart.nodes.filter_spam import FilterSpamNode
from launchpad.workflows.examples.quickstart.nodes.generate_response_node import GenerateResponseNode
from launchpad.workflows.examples.quickstart.nodes.process_invoice_node import ProcessInvoiceNode
from launchpad.workflows.examples.quickstart.nodes.send_reply_node import SendReplyNode
from launchpad.workflows.examples.quickstart.nodes.ticket_router_node import TicketRouterNode
from launchpad.workflows.examples.quickstart.nodes.validate_ticket_node import ValidateTicketNode


class CustomerCareWorkflow(Workflow):
    workflow_schema = WorkflowSchema(
        description="",
        event_schema=CustomerCareEventSchema,
        start=AnalyzeTicketNode,
        nodes=[
            NodeConfig(
                node=AnalyzeTicketNode,
                connections=[TicketRouterNode],
                description="",
                concurrent_nodes=[
                    DetermineTicketIntentNode,
                    FilterSpamNode,
                    ValidateTicketNode,
                ],
            ),
            NodeConfig(
                node=TicketRouterNode,
                connections=[
                    CloseTicketNode,
                    EscalateTicketNode,
                    GenerateResponseNode,
                    ProcessInvoiceNode,
                ],
                description="",
                is_router=True,
            ),
            NodeConfig(
                node=GenerateResponseNode,
                connections=[SendReplyNode],
                description="",
            ),
        ],
    )
