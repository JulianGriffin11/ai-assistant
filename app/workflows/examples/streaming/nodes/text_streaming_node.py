from typing import AsyncIterator, Dict, Any

from launchpad.core.nodes.agent import AgentConfig, ModelProvider
from launchpad.core.nodes.agent_streaming_node import AgentStreamingNode
from launchpad.core.task import TaskContext
from launchpad.workflows.examples.streaming.schema import OpenAIChatSchema


class TextStreamingNode(AgentStreamingNode):
    def get_agent_config(self) -> AgentConfig:
        return AgentConfig(
            model_provider=ModelProvider.OPENAI,
            model_name="gpt-5.4-mini",
            output_type=str,
        )

    async def process(self, task_context: TaskContext) -> AsyncIterator[Dict[str, Any]]:
        event: OpenAIChatSchema = task_context.event
        async with self.agent.run_stream(user_prompt=event.get_message()) as result:
            async for chunk in self.stream_text_deltas(result):
                yield chunk
