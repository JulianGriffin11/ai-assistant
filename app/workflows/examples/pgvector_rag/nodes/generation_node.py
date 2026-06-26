from pydantic import Field
from pydantic_ai import RunContext

from launchpad.core.nodes.agent import AgentNode, AgentConfig, ModelProvider
from launchpad.core.task import TaskContext
from launchpad.workflows.examples.pgvector_rag.services import RetrievalResults
from launchpad.workflows.examples.pgvector_rag.nodes.retrieval_node import RetrievalNode


class GenerationNode(AgentNode):
    class DepsType(AgentNode.DepsType):
        context: RetrievalResults

    class OutputType(AgentNode.OutputType):
        answer: str = Field(description="The answer to the query")
        sources: list[str] = Field(description="The sources used to answer the query")
        confidence: float = Field(
            description="The confidence in the answer", ge=0, le=1
        )

    def get_agent_config(self) -> AgentConfig:
        return AgentConfig(
            instructions="You are a helpful assistant that can answer questions and provide information based on the retrieved documents.",
            output_type=GenerationNode.OutputType,
            deps_type=GenerationNode.DepsType,
            model_provider=ModelProvider.OPENAI,
            model_name="gpt-5.4-mini",
        )

    async def process(self, task_context: TaskContext) -> TaskContext:
        retrieval_results: RetrievalNode.OutputType = self.get_output(RetrievalNode)
        deps = GenerationNode.DepsType(
            context=retrieval_results.results,
        )

        @self.agent.instructions
        def add_rag_context(ctx: RunContext[GenerationNode.DepsType]) -> str:
            return f"Here are the documents I found for your query:\n{ctx.deps.context.model_dump_json(indent=2)}"

        result = await self.agent.run(
            user_prompt=task_context.event.query,
            deps=deps,
        )

        self.save_output(result.output)

        return task_context
