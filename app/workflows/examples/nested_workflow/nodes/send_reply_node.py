from pydantic import BaseModel

from launchpad.core.nodes.base import Node
from launchpad.core.task import TaskContext
from launchpad.workflows.examples.nested_workflow.nodes.reply.draft_reply_node import (
    DraftReplyNode,
)


class SendReplyNode(Node):
    class OutputType(BaseModel):
        status: str
        message: str

    async def process(self, task_context: TaskContext) -> TaskContext:
        draft: DraftReplyNode.OutputType = self.get_output(DraftReplyNode)
        self.save_output(self.OutputType(status="sent", message=draft.reply))
        return task_context
