"""
Minimal RAG pipeline for learning purposes (no frameworks).

Setup:
    uv init
    uv add requests numpy
    ollama pull qwen3:4b
    ollama pull nomic-embed-text
    mkdir docs   # put a few .md or .txt files in here

Usage:
    python rag_starter.py "Your question here"
    python rag_starter.py "Your question here" --k 5 --chunk-size 400 --compare
    python rag_starter.py "Your question here" --show-chunks
"""

import argparse
from pathlib import Path

import numpy as np
import requests

OLLAMA = "http://localhost:11434"
CHAT_MODEL = "qwen3:4b"
EMBED_MODEL = "nomic-embed-text"
DOCS_DIR = Path("docs")

# 4T's: Traits, Task, Tone, Target (rewrite these to practise the 4T's)
SYSTEM_PROMPT = """\
Traits: You are a careful assistant that only states what the provided context supports.
Task: Answer the user's question using ONLY the context below. If the context does not
contain the answer, say "I can't find that in the provided documents."
Tone: Clear, concise and neutral.
Target: A student developer who wants a short, direct answer (max 5 sentences).
"""


# ---------- 1. Chunking ----------
def chunk_text(text: str, size: int = 500, overlap: int = 100) -> list[str]:
    """Split text into overlapping character chunks (simple on purpose)."""
    chunks, start = [], 0
    while start < len(text):
        chunk = text[start:start + size].strip()
        if chunk:
            chunks.append(chunk)
        start += size - overlap
    return chunks


def load_chunks(size: int, overlap: int) -> list[dict]:
    """Load chunks from docs."""
    items = []
    files = sorted(list(DOCS_DIR.glob("**/*.md")) + list(DOCS_DIR.glob("**/*.txt")))
    if not files:
        raise SystemExit(f"No .md/.txt files found in {DOCS_DIR}/")
    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for i, chunk in enumerate(chunk_text(text, size, overlap)):
            items.append({"source": path.name, "index": i, "text": chunk})
    return items


# ---------- 2. Embeddings ----------
def embed(texts: list[str]) -> np.ndarray:
    """Embed the given texts using the specified model."""
    r = requests.post(
        f"{OLLAMA}/api/embed",
        json={"model": EMBED_MODEL, "input": texts},
        timeout=300,
    )
    r.raise_for_status()
    return np.array(r.json()["embeddings"], dtype=np.float32)


# ---------- 3. Retrieval (cosine similarity, by hand) ----------
def cosine_top_k(query_vec: np.ndarray, matrix: np.ndarray, k: int):
    """Compute the top-k cosine similarity between the query vector and the matrix."""
    q = query_vec / np.linalg.norm(query_vec)
    m = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
    scores = m @ q
    top = np.argsort(scores)[::-1][:k]
    return [(int(i), float(scores[i])) for i in top]


# ---------- 4. Generation ----------
def strip_thinking(text: str) -> str:
    """Remove leaked reasoning: Qwen3 sometimes prints its thinking followed by
    a closing </think> tag. Keep only what comes after the last one."""
    if "</think>" in text:
        text = text.split("</think>")[-1]
    return text.strip()


def chat(system: str, user: str) -> str:
    """Chat with a model."""
    # Qwen3 understands "/no_think" as an instruction to skip its reasoning phase.
    # Only add it for Qwen3 models, other models would just see it as extra text.
    if "qwen3" in CHAT_MODEL.lower():
        user = user + "\n\n/no_think"

    r = requests.post(
        f"{OLLAMA}/api/chat",
        json={
            "model": CHAT_MODEL,
            "stream": False,
            "think": False,  # newer Ollama versions: disable thinking mode
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        },
        timeout=600,
    )
    r.raise_for_status()
    return strip_thinking(r.json()["message"]["content"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("question")
    ap.add_argument("--k", type=int, default=3, help="number of chunks to retrieve")
    ap.add_argument("--chunk-size", type=int, default=500)
    ap.add_argument("--overlap", type=int, default=100)
    ap.add_argument("--compare", action="store_true", help="also answer WITHOUT retrieval")
    ap.add_argument("--show-chunks", action="store_true", help="print retrieved chunks and scores")
    args = ap.parse_args()

    items = load_chunks(args.chunk_size, args.overlap)
    print(f"Loaded {len(items)} chunks from {DOCS_DIR}/")

    # In a real app you'd cache these instead of re-embedding every run.
    matrix = embed([it["text"] for it in items])
    query_vec = embed([args.question])[0]

    hits = cosine_top_k(query_vec, matrix, args.k)

    if args.show_chunks:
        print("\n--- Retrieved chunks ---")
        for idx, score in hits:
            it = items[idx]
            print(f"[{score:.3f}] {it['source']} #{it['index']}\n{it['text']}\n")

    context = "\n\n---\n\n".join(items[i]["text"] for i, _ in hits)
    rag_user = f"Context:\n{context}\n\nQuestion: {args.question}"

    print("\n=== WITH retrieval ===")
    print(chat(SYSTEM_PROMPT, rag_user))

    if args.compare:
        print("\n=== WITHOUT retrieval ===")
        print(chat("You are a helpful assistant. Keep answers short.", args.question))


if __name__ == "__main__":
    main()