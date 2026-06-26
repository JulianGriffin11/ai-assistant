from typing import Optional

from launchpad.core.nodes.agent import AgentNode, AgentConfig, ModelProvider
from launchpad.core.task import TaskContext
from launchpad.workflows.examples.langfuse_tracing.schema import LangfuseTracingEventSchema


class ViolationDetectionNode(AgentNode):
    class OutputType(AgentNode.OutputType):
        comment_id: str
        violation: bool
        reason: Optional[str] = None

    def get_agent_config(self) -> AgentConfig:
        return AgentConfig(
            instructions="Determine whether the comment is a violation or not. If it is a violation, provide a reason for violation. If it is not a violation, provide a reason for non-violation.",
            output_type=self.OutputType,
            deps_type=LangfuseTracingEventSchema,
            model_provider=ModelProvider.OPENAI,
            model_name="gpt-5.4-mini",
            instrument=True,
        )

    async def process(self, task_context: TaskContext) -> TaskContext:
        event: LangfuseTracingEventSchema = task_context.event

        @self.agent.instructions
        async def add_context() -> str:
            return event.model_dump_json()

        result = await self.agent.run(user_prompt=event.model_dump_json())

        self.save_output(result.output)

        return task_context
