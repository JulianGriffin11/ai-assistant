# Nested Workflow

Deterministic customer-care example that shows one Launchpad workflow calling another workflow with the same `TaskContext`.

## What It Demonstrates

- A parent workflow that calls a child workflow from a node.
- A child `ReplyDraftWorkflow` that writes its output to the same `TaskContext`.
- Workflow composition with `await ReplyDraftWorkflow().run_async(context=task_context)`.
- A runnable example that does not require LLM, tracing, database, or vector-search credentials.

## Workflow Graph

```text
RunReplyWorkflowNode
  ↓ calls ReplyDraftWorkflow with shared context
DraftReplyNode
  ↓
SendReplyNode
```

## Run It

```bash
uv run playground/nested_workflow.py
```

The script loads `request_examples/billing_question.json` by default.

Registered as `WorkflowRegistry.NESTED_WORKFLOW`.
