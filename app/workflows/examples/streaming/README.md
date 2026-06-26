# Streaming — Server-Sent Events via `run_stream_async`

Reference for wiring an LLM workflow to an OpenAI-compatible `/v1/chat/completions` endpoint that streams tokens back to the client using Server-Sent Events.

## What it demonstrates

- `AgentStreamingNode` — an `AgentNode` variant whose `process()` is an async generator.
- `stream_text_deltas()` for plain-text output and `stream_structured_deltas()` for structured (Pydantic) output.
- `Workflow.run_stream_async()` driving the node chain and forwarding chunks up to the HTTP layer.
- OpenAI-compatible chunk format, so existing OpenAI client libraries work out of the box.

## Workflow graph

```
TextStreamingNode (str output)
        ↓
StructuredStreamingNode (pydantic OutputType: thinking + reply)
```

Both nodes call the same model; the first demonstrates raw text streaming and the second streams incrementally built structured objects.

## Event schema

`schema.py` defines `OpenAIChatSchema` — a Pydantic model of the OpenAI chat-completion request body. Key helpers:

- `get_message()` returns the latest user message.
- `get_message_history()` converts the `messages` array to pydantic-ai `ModelRequest` / `ModelResponse` objects.

## Run it

**Playground (in-process streaming):**

```bash
uv run playground/streaming.py
```

Prints each chunk the workflow yields.

**HTTP endpoint (SSE):** the streaming workflow backs `POST /v1/chat/completions` (see `app/launchpad/api/openai.py`). With the stack up:

```bash
curl -N -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "default", "messages": [{"role": "user", "content": "Hello"}]}'
```

Registered as `WorkflowRegistry.STREAMING`.

## Customize

- Change the model on either streaming node via its `AgentConfig`.
- Add a new structured field by extending `StructuredStreamingNode.OutputType` — pydantic-ai will stream partial objects as they fill in.
- Tune chunk cadence with the `debounce_by` argument on `stream_text_deltas` / `stream_structured_deltas`.
