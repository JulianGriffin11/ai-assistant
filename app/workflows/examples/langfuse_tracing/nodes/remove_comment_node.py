import logging

from launchpad.core.nodes.base import Node
from launchpad.core.task import TaskContext
from launchpad.workflows.examples.langfuse_tracing.schema import LangfuseTracingEventSchema
from launchpad.workflows.examples.langfuse_tracing.nodes.violation_detection_node import (
    ViolationDetectionNode,
)


class RemoveCommentNode(Node):
    class OutputType(Node.OutputType):
        result: str

    def remove_comment(self, comment_id: str) -> OutputType:
        result = f"Removed comment with ID: {comment_id}"
        logging.info(result)
        return self.OutputType(result=result)

    async def process(self, task_context: TaskContext) -> TaskContext:
        event: LangfuseTracingEventSchema = task_context.event
        violation_detection: ViolationDetectionNode.OutputType = self.get_output(
            ViolationDetectionNode
        )

        if violation_detection.violation:
            result = self.remove_comment(event.comment_id)
        else:
            result = "No violation detected, skipping comment removal."
            logging.info(result)

        self.save_output(result)

        return task_context
