# Example workflows

Reference workflows that ship with the Launchpad. They are meant to be read, run, copied, and then replaced by your own workflow packages at `app/launchpad/workflows/<your_workflow>/`.

Each subdirectory is self-contained (`schema.py`, `workflow.py`, `nodes/`, `request_examples/`, and — where relevant — `prompts/`) and is registered in [`workflow_registry.py`](../workflow_registry.py).

| Example | Demonstrates | Playground |
| --- | --- | --- |
| [`quickstart/`](./quickstart/) | Concurrent analysis + routing + Jinja2 prompts on a customer-care ticket | `uv run playground/quickstart.py` |
| [`nested_workflow/`](./nested_workflow/) | Minimal nested workflow composition with a parent node calling a child workflow | `uv run playground/nested_workflow.py` |
| [`streaming/`](./streaming/) | SSE streaming through `run_stream_async`, text + structured output | `uv run playground/streaming.py` |
| [`langfuse_tracing/`](./langfuse_tracing/) | Enabling Langfuse tracing on a multi-node moderation pipeline | `uv run playground/langfuse_tracing.py` |
| [`pgvector_rag/`](./pgvector_rag/) | Retrieval-augmented generation against `pgvector` | `uv run playground/pgvector_rag.py` |

Delete whichever examples you don't need and remove their entries from `WorkflowRegistry` — nothing else in the app depends on them.
