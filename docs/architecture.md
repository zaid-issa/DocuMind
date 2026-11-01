# DocuMind Architecture

Status: planned design. Sections are updated as features are implemented.

## Pipeline

PDF upload -> text extraction -> cleaning -> chunking -> embeddings
-> vector store -> similarity search -> LLM -> answer with citations

## Project layout

- `app/config.py`   Settings loaded from environment variables (.env)
- `app/services/`   Business logic: PDF processing, chunking, embeddings,
                    vector store, retrieval, LLM
- `app/api/`        FastAPI routes (HTTP layer only, no business logic)
- `ui/`             Streamlit front end
- `tests/`          pytest tests, added together with each feature
- `docs/`           Documentation

## Design decisions

1. **Provider abstraction.** Embeddings and the LLM sit behind small
   interfaces so a provider can be replaced by changing one file.
2. **Separation of concerns.** Routes call services; services do not
   know about HTTP. Configuration lives in one place.
3. **Metadata from the start.** Every chunk stores its document name and
   page number so answers can cite sources.
4. **Secrets in environment variables.** API keys live in `.env`,
   which is git-ignored. `.env.example` documents required settings.
5. **Untrusted input.** Uploaded files are validated (type, size), and
   retrieved document text is treated as data, not instructions,
   when building prompts.
6. **Lightweight by design.** No local LLMs or model training; the
   project must run on a laptop with 8 GB RAM.

## Known limitations (planned)

- Scanned PDFs (images without a text layer) are not supported; the
  application should detect them and return a clear error.
