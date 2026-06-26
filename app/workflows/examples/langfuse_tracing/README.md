# Langfuse tracing — traced moderation pipeline

Smallest possible demo of enabling Langfuse observability on a real workflow. Use it as a reference when instrumenting your own workflows.

## What it demonstrates

- `Workflow(enable_tracing=True)` bootstrapping a Langfuse client at construction time.
- Automatic spans for the whole workflow and each node, with inputs and outputs captured.
- `LangfuseAuthenticationError` raised at init if credentials are missing or invalid — fail fast instead of silently dropping traces.
- `@self.agent.instructions` used to inject per-run context into the system prompt.

## Workflow graph

```
ViolationDetectionNode (AgentNode)
        ↓
ContextSummaryResult (AgentNode)
        ↓
RemoveCommentNode (Node)
```

`ViolationDetectionNode` classifies a comment, `ContextSummaryResult` writes an audit summary, and `RemoveCommentNode` deletes the comment when the first step flagged it.

## Event schema

```python
class LangfuseTracingEventSchema(BaseModel):
    event: str
    timestamp: datetime
    comment_id: str
    thread_id: str
    user_id: str
    content: str
```

## Run it

1. Add Langfuse credentials to the repo-root `.env`:

   ```bash
   LANGFUSE_PUBLIC_KEY=pk-lf-...
   LANGFUSE_SECRET_KEY=sk-lf-...
   LANGFUSE_BASE_URL=https://cloud.langfuse.com
   ```

2. Enable tracing in the playground by instantiating the workflow with `enable_tracing=True` (the shipped script leaves it off by default to keep local runs free of network calls). Then:

   ```bash
   uv run playground/langfuse_tracing.py
   ```

3. Open the Langfuse dashboard. You'll see a trace named after the workflow class with child spans for each node and the underlying LLM generations.

Registered as `WorkflowRegistry.LANGFUSE_TRACING`.

## Customize

- Opt individual nodes out of tracing by setting `instrument=False` on their `AgentConfig`.
- Capture the trace ID from `task_context.trace_id` after the workflow runs and return it to the caller so they can deep-link into Langfuse.
