# PGVector RAG — retrieval-augmented generation

Two-node retrieval-and-generation workflow on top of the PostgreSQL + `pgvector` that already ships with the Launchpad's Docker stack.

## What it demonstrates

- A plain `Node` (`RetrievalNode`) orchestrating a non-LLM side service (`PgvectorRAGService` in `services.py`) — no agent involved on the retrieval step.
- `AgentNode.DepsType` + `@self.agent.instructions` used to inject retrieved documents into the generation prompt at call time.
- `vecs` for vector storage and OpenAI embeddings (`text-embedding-3-small`, 1536 dims) for query encoding — easy to swap.

## Workflow graph

```
RetrievalNode (Node) → embeds query, returns RetrievalResults
        ↓
GenerationNode (AgentNode) → uses retrieved context to answer, returns
                             {answer, sources, confidence}
```

## Event schema

```python
class RagExampleEventSchema(BaseModel):
    query: str
```

## Run it

1. Bring the Docker stack up so Postgres + pgvector are available (`cd docker && ./start.sh`), and apply migrations from `app/launchpad/` (`./migrate.sh`).

2. Seed the collection with something to retrieve:

   ```python
   from launchpad.workflows.examples.pgvector_rag.services import PgvectorRAGService

   service = PgvectorRAGService()
   text = "Vector search enables semantic retrieval."
   embedding = service.get_embedding(text)
   service.upsert([("doc-1", embedding, {"source": "handbook", "text": text})])
   service.disconnect()
   ```

3. Run the workflow:

   ```bash
   uv run playground/pgvector_rag.py
   ```

   Loads [`request_examples/query.json`](./request_examples/) and prints the answer with sources and confidence.

Registered as `WorkflowRegistry.PGVECTOR_RAG`.

## Customize

- Swap the embedding model by passing a different `embedding_model` to `PgvectorRAGService` (or replace it with a non-OpenAI embedding client altogether).
- Adjust retrieval: change `limit`, `measure`, or add metadata filters in `RetrievalNode.process()`.
- Chain additional nodes between `RetrievalNode` and `GenerationNode` (reranking, source filtering, etc.) — they just read the retrieval output via `self.get_output(RetrievalNode)`.
