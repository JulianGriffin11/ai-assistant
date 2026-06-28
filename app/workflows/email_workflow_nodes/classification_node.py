import json
import sys
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_ai import RunContext
import nest_asyncio


sys.path.append(
    str(Path(__file__).parent.parent.parent)
)  # allow running this file directly

from core.nodes.agent import AgentConfig, AgentNode, ModelProvider
from core.task import TaskContext
from schemas.nylas_email_schema import EmailObject
from schemas.nylas_webhook_schema import WebhookEvent

load_dotenv()
nest_asyncio.apply()


class EmailCategory(str, Enum):
    SPAM = "spam"
    MESSAGE = "message"
    INVOICE = "invoice"
    OTHER = "other"


PROMPT = """
You are a helpful assistant that classifies emails into one of the following categories:
- SPAM
- MESSAGE
- INVOICE
- OTHER
"""


class ClassificationNode(AgentNode):
    class OutputType(AgentNode.OutputType):
        category: EmailCategory
        confidence: float = Field(
            ge=0, le=1, description="Confidence score for the category"
        )

    class DepsType(AgentNode.DepsType):
        from_email: str = Field(..., description="Email address of the sender")
        sender: str = Field(..., description="Name or identifier of the sender")
        subject: str = Field(..., description="Subject of the ticket")
        body: str = Field(..., description="The body of the ticket")

    def get_agent_config(self) -> AgentConfig:
        return AgentConfig(
            system_prompt=PROMPT,
            output_type=self.OutputType,
            deps_type=self.DepsType,
            model_provider=ModelProvider.OPENAI,
            model_name="gpt-4o-mini",
        )

    def process(self, task_context: TaskContext) -> TaskContext:
        email_object = EmailObject(**task_context.event.data["object"])
        deps = self.DepsType(
            from_email=email_object.from_[0].email,
            sender=email_object.from_[0].name,
            subject=email_object.subject,
            body=email_object.body,
        )

        @self.agent.system_prompt  # type: ignore
        def add_ticket_context(
            ctx: RunContext[ClassificationNode.DepsType],
        ) -> str:
            return ctx.deps.model_dump_json(indent=2)

        result = self.agent.run_sync(user_prompt="Classify this email", deps=deps)  # type: ignore

        task_context.update_node(node_name=self.node_name, result=result)
        return task_context


if __name__ == "__main__":
    """
    Run this file directly to test the node.
    """
    node = ClassificationNode()

    raw_event = json.load(
        open(
            "../../../requests/events/182c31c2-b499-11f0-afbf-391e827e2ece.json"
        )  # Replace with your event file
    )

    event = WebhookEvent(**raw_event)
    result = node.process(TaskContext(event=event))
    print(result.model_dump_json(indent=4))