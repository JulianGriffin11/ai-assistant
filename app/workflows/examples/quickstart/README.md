# Quickstart — customer-care ticket workflow

End-to-end reference for the patterns you'll reach for most: run a few analyses concurrently, route on their results, then take an action. Good starting point when cloning this workflow for your own use case.

## What it demonstrates

- `ConcurrentNode` fanning three `AgentNode`s out in parallel (`DetermineTicketIntentNode`, `FilterSpamNode`, `ValidateTicketNode`).
- `BaseRouter` + multiple `RouterNode` rules deciding the next step based on the fan-out outputs.
- Jinja2 prompts colocated with the workflow in [`prompts/`](./prompts/), loaded via `PromptManager.get_prompt(..., prompts_dir=PROMPTS_DIR)`.
- Structured agent outputs validated against per-node `OutputType` Pydantic models.

## Workflow graph

```
AnalyzeTicketNode (ConcurrentNode)
 ├─ DetermineTicketIntentNode
 ├─ FilterSpamNode
 └─ ValidateTicketNode
       ↓
TicketRouterNode (BaseRouter)
 ├─ CloseTicketRouter  → CloseTicketNode       (spam with confidence > 0.8)
 ├─ EscalationRouter   → EscalateTicketNode    (intent flags escalate)
 ├─ InvoiceRouter      → ProcessInvoiceNode    (intent = BILLING_INVOICE)
 └─ fallback           → GenerateResponseNode → SendReplyNode
```

## Event schema

`schema.py` defines `CustomerCareEventSchema`:

```python
class CustomerCareEventSchema(BaseModel):
    ticket_id: UUID
    timestamp: datetime
    from_email: str
    to_email: str
    sender: str
    subject: str
    body: str
```

## Run it

```bash
uv run playground/quickstart.py
```

The script loads [`request_examples/invoice.json`](./request_examples/) by default. Swap to any of the other fixtures — `policy_question`, `product`, `prompt_injection`, `refund`, `service_desk`, `spam` — to exercise the different router branches.

Registered as `WorkflowRegistry.QUICKSTART`, so `POST /events/` (which defaults to `QUICKSTART`) runs the same pipeline via the Celery worker.

## Customize

- Swap the LLM provider on any node by changing `model_provider` / `model_name` in its `get_agent_config()`.
- Add a new router rule by writing another `RouterNode` subclass and prepending it to `TicketRouterNode.routes`.
- Edit the Jinja2 templates in [`prompts/`](./prompts/) to change tone or add fields without touching Python.
