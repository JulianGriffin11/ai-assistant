import logging

from launchpad.core.nodes.base import Node
from launchpad.core.task import TaskContext


class ProcessInvoiceNode(Node):
    async def process(self, task_context: TaskContext) -> TaskContext:
        logging.info("Processing invoice")
        return task_context
