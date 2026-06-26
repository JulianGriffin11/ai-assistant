from pathlib import Path

from pydantic import Field

from launchpad.core.nodes.agent import AgentNode, AgentConfig, ModelProvider
from launchpad.core.task import TaskContext
from launchpad.services.prompt_loader import PromptManager

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


class GenerateResponseNode(AgentNode):
    class OutputType(AgentNode.OutputType):
        reasoning: str = Field(description="The reasoning for the response")
        response: str = Field(description="The response to the ticket")
        confidence: float = Field(
            ge=0, le=1, description="Confidence score for how helpful the response is"
        )

    def get_agent_config(self) -> AgentConfig:
        return AgentConfig(
            instructions=PromptManager.get_prompt(
                "customer_ticket_response", prompts_dir=PROMPTS_DIR
            ),
            output_type=self.OutputType,
            deps_type=None,
            model_provider=ModelProvider.OPENAI,
            model_name="gpt-5.4-mini",
        )

    async def process(self, task_context: TaskContext) -> TaskContext:
        event = task_context.event
        result = await self.agent.run(
            user_prompt=event.model_dump_json(),
        )
        self.save_output(result.output)
        return task_context
