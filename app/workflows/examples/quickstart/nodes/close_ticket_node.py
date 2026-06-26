import logging

from launchpad.core.nodes.base import Node
from launchpad.core.task import TaskContext


class CloseTicketNode(Node):
    async def process(self, task_context: TaskContext) -> TaskContext:
        logging.info("Closing ticket")
        return task_context
