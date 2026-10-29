# RAG Starter: Learning Purposes

Oct 29, 2026 · @Casper

rag\_starter.py is a framework-free RAG pipeline of about 150 lines (Python, Ollama, numpy), built to teach the four mechanics the exam asks you to explain: chunking, embeddings, similarity retrieval and prompting.

## Pipeline steps and what each teaches

Each function in the script maps to one thing the exam wants you to explain or demonstrate.

| Step | Function | What it teaches | Exam requirement it supports |
| --- | --- | --- | --- |
| Chunking | `chunk_text` | Documents are cut into overlapping pieces (500 characters with 100 overlap by default), and chunk size decides what retrieval can find | How the RAG source material is prepared |
| Embedding | `embed` | Text becomes a vector so that similar meaning gives similar numbers (nomic-embed-text, served by Ollama) | Embeddings |
| Retrieval | `cosine_top_k` | The question vector is compared with every chunk vector by cosine similarity, and the top k chunks win | Similarity measures; showing how retrieval affects an answer |
| Prompting | `SYSTEM_PROMPT` | Traits, Task, Tone and Target written into one system prompt, with the retrieved chunks pasted into the user message | 4T's prompt engineering |
| Generation | `chat` | A local model (qwen3:4b) answers from the context, and `--compare` asks the same question without it | Local LLM; with versus without retrieval |

## What the first runs showed

Four things from the first runs are ready-made examples for the reflection and limitations part of the synopsis.

| Observation | Concept it illustrates | Where it fits in the synopsis |
| --- | --- | --- |
| With retrieval, the answer came from the exam file. Without it, the model guessed what "synopsis" means in general (plot summaries, academic abstracts). | Grounding: retrieval gives the model facts it was never trained on | Demonstrating how retrieval affects an answer |
| The answer to "What must the synopsis contain?" was incomplete, because the top chunk held only the end of the synopsis list. | Chunk boundaries can split an answer, so chunk size and k change what the model can see | A limitation you ran into, with a concrete example |
| A saved console output left in `docs/` was indexed and outranked the exam file (similarity 0.786 against 0.569 before). | Data quality: retrieval trusts similarity, not correctness, so a high score can point at the wrong text | Data preparation and the data-quality link to machine learning |
| Qwen3 printed its reasoning before the answer, even with thinking switched off in the request. | Model behaviour: outputs may need post-processing, and settings differ between model and Ollama versions | Model behaviour and the implementation notes |

## Experiments to run next

Change one thing per run and write down what happened, because those notes become evidence for the synopsis.

- [ ] Vary `--k` (1, 3, 8) and note how the retrieved chunks and the answer change
- [ ] Vary `--chunk-size` (200, 500, 1000) with the same question
- [ ] Ask something the documents do not cover and check whether the model says it cannot find it
- [ ] Add a short file that explains cosine similarity, and ask "What is cosine similarity?" before and after
- [ ] Add an irrelevant file and see whether it interferes with retrieval
- [ ] Remove one of the 4T's at a time from `SYSTEM_PROMPT` and compare the outputs
- [ ] Keep the notes file outside `docs/` so it is not indexed

## Limits of the toy version

The script is simple on purpose, and each shortcut is also a possible improvement for the team's real application.

| Shortcut in the script | Why it matters | Upgrade |
| --- | --- | --- |
| Chunks are cut by character count | Chunks can break mid-sentence or split a list | Split by paragraph or heading |
| Every document is re-embedded on every run | Slow, and wasteful as the collection grows | Cache vectors on disk, or use a vector store such as Chroma or pgvector |
| Cosine similarity runs against every chunk | Fine for a few dozen chunks, not for thousands | Let a vector store index the vectors |
| The top k chunks are always used, however low their score | Weak matches reach the model and can mislead it | Add a minimum similarity score |
| Only `.md` and `.txt` files are read | Limits what the collection can hold | Add loaders for the formats the team's data uses |
