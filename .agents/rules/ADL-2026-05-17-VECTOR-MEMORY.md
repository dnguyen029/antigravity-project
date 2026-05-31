# DECISION-2026-05-17-VECTOR-MEMORY: Switch to Vector Search for Recall

## Status
Accepted

## Context
As the project grows, the volume of decision logs and session histories has exceeded the efficiency thresholds for standard text-based retrieval. To maintain performance and minimize token usage on developer workstations, a more scalable retrieval mechanism is required.

## Decision
We are transitioning the recall mechanism from local file-based indexing to **Supabase Vector Search** (`public.lessons_learned`).

### Key Implementation Details:
1.  **Storage**: Embeddings for all decision logs, findings, and knowledge tags are stored in Supabase.
2.  **Retrieval**: Pre-task setup performs a similarity search against the current task context.
3.  **Output**: Results are automatically loaded into `.swarm/L3_CONTEXT.md` during the pre-task validation check.

## Terminology Alignment
This change ensures that long-term memory remains performant as project complexity scales.

## Consequences
- **Positive**: Reduced token usage during pre-task setup; higher relevance in historical recall.
- **Negative**: Dependency on Supabase availability for full recall; requirement for embedding generation on new artifacts.

## Metadata
- **Date**: 2026-05-17
- **Role**: Technical Writer
- **Rigor Level**: Strict
