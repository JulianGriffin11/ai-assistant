import logging

from launchpad.core.nodes.base import Node
from launchpad.core.task import TaskContext
from launchpad.workflows.examples.quickstart.nodes.generate_response_node import GenerateResponseNode


class SendReplyNode(Node):
    async def process(self, task_context: TaskContext) -> TaskContext:
        logging.info("Sending reply:")
        generate_response_node: GenerateResponseNode.OutputType = self.get_output(
            GenerateResponseNode
        )
        logging.info(generate_response_node.response)
        return task_context
