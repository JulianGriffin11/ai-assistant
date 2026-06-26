from typing import Optional

from launchpad.core.nodes.base import Node
from launchpad.core.nodes.router import BaseRouter, RouterNode
from launchpad.core.task import TaskContext
from launchpad.workflows.examples.quickstart.nodes.close_ticket_node import CloseTicketNode
from launchpad.workflows.examples.quickstart.nodes.determine_intent_ticket_node import (
    CustomerIntent,
    DetermineTicketIntentNode,
)
from launchpad.workflows.examples.quickstart.nodes.escalate_ticket_node import EscalateTicketNode
from launchpad.workflows.examples.quickstart.nodes.filter_spam import FilterSpamNode
from launchpad.workflows.examples.quickstart.nodes.generate_response_node import GenerateResponseNode
from launchpad.workflows.examples.quickstart.nodes.process_invoice_node import ProcessInvoiceNode


class TicketRouterNode(BaseRouter):
    def __init__(self):
        self.routes = [
            CloseTicketRouter(),
            EscalationRouter(),
            InvoiceRouter(),
        ]
        self.fallback = GenerateResponseNode()


class CloseTicketRouter(RouterNode):
    def determine_next_node(self, task_context: TaskContext) -> Optional[Node]:
        filter_spam_node: FilterSpamNode.OutputType = self.get_output(FilterSpamNode)
        if not filter_spam_node.is_human and filter_spam_node.confidence > 0.8:
            return CloseTicketNode()
        return None


class EscalationRouter(RouterNode):
    def determine_next_node(self, task_context: TaskContext) -> Optional[Node]:
        intent_node: DetermineTicketIntentNode.OutputType = self.get_output(
            DetermineTicketIntentNode
        )
        if intent_node.intent.escalate or intent_node.escalate:
            return EscalateTicketNode()
        return None


class InvoiceRouter(RouterNode):
    def determine_next_node(self, task_context: TaskContext) -> Optional[Node]:
        intent_node: DetermineTicketIntentNode.OutputType = self.get_output(
            DetermineTicketIntentNode
        )
        if intent_node.intent == CustomerIntent.BILLING_INVOICE:
            return ProcessInvoiceNode()
        return None
