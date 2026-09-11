Here's a walkthrough of the script [`rag_admission_langflow_watsonx.py`](rag_admission_langflow_watsonx.py):

---

## What it does

A full **Retrieval-Augmented Generation (RAG)** pipeline that:

1. **Loads** PDF and TXT admission documents from a local directory
2. **Chunks** them with overlapping windows for better recall
3. **Embeds** them using IBM's Slate retrieval model via the watsonx.ai API
4. **Indexes** them in an in-memory FAISS vector store
5. **Answers** questions using Granite via a LangChain `RetrievalQA` chain

---

## Key components

| Layer | Component | IBM Model / Class |
|---|---|---|
| LLM | [`WatsonxLLM`](rag_admission_langflow_watsonx.py:48) | `ibm/granite-3-3-8b-instruct` |
| Embeddings | [`WatsonxEmbeddings`](rag_admission_langflow_watsonx.py:63) | `ibm/slate-125m-english-rtrvr` |
| Vector store | [`FAISS.from_documents()`](rag_admission_langflow_watsonx.py:101) | In-memory, no server needed |
| RAG chain | [`RetrievalQA`](rag_admission_langflow_watsonx.py:120) | `stuff` chain type, top-4 passages |

---

## Setup

**1. Install dependencies:**
```bash
pip install ibm-watsonx-ai langchain langchain-ibm langchain-community faiss-cpu pypdf
```

**2. Set credentials** — either export environment variables:
```bash
export WATSONX_API_KEY="<your-ibm-cloud-api-key>"
export WATSONX_URL="https://us-south.ml.cloud.ibm.com"
export WATSONX_PROJECT_ID="<your-watsonx-project-id>"
```
…or edit the [`CREDENTIALS block`](rag_admission_langflow_watsonx.py:16) directly.

**3. Add your documents:**
```bash
mkdir admission_docs
cp your_admission_guide.pdf ./admission_docs/
```

**4. Run:**
```bash
python rag_admission_langflow_watsonx.py
```

---

## Customisation tips

- **Swap the LLM model** by changing [`GRANITE_LLM_ID`](rag_admission_langflow_watsonx.py:22) — e.g. `ibm/granite-3-3-2b-instruct` for a lighter model, or `ibm/granite-3-8b-instruct` for stronger reasoning.
- **Tune retrieval** by changing `k` in [`search_kwargs`](rag_admission_langflow_watsonx.py:117) or switching `search_type` to `"mmr"` for diversity.
- **Persist the index** by calling `store.save_local("faiss_index")` after building it, then `FAISS.load_local(...)` to skip re-embedding on the next run.
- **Custom prompt** — edit the [`RAG_PROMPT`](rag_admission_langflow_watsonx.py:107) template to tune tone or add system instructions.
