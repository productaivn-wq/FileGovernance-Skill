---
name: FileGovernance
description: Governance-driven file and document organization for human-AI workflows. Bridges operational file lifecycle states with Knowledge Graphs and GraphRAG architectures.
version: 1.0.0
status: active
author: Antigravity Community
tags:
  - knowledge-management
  - file-organization
  - knowledge-graph
  - graphrag
  - obsidian
  - second-brain
---

# FileGovernance Skill

> **Philosophy**: A Knowledge Graph cannot fix file chaos. Files require **governance** before they can become **nodes**.

The `FileGovernance` skill establishes an open, standardized framework to classify, name, and maintain digital documents and codebases. It ensures that workspaces remain effortlessly understandable to humans while serving as deterministic, collision-free seeds for **Knowledge Graphs**, **Obsidian vaults**, and **GraphRAG pipelines**.

---

## 1. Core Architecture: The Two-Axis Model

This skill enforces a strict separation between two independent dimensions:

```text
       KNOWLEDGE AXIS (Domain Ontology & Semantic Meaning)
             ▲
             │      [Entities, Decisions, Architectures, APIs]
             │         • Authentication Gateway
             │         • Payment Infrastructure
             │         • DB Lockout Mitigation
             │
─────────────┼──────────────────────────────────────────► LIFECYCLE AXIS
             │   Inbox  ──►  Active  ──►  Archive          (Operational State)
             │   (Raw)       (In-Flight)  (Historical)
```

1. **The Lifecycle Axis (Operational State)**:
   - Manages *where* a file sits in its workflow.
   - Governed by 5 Mutually Exclusive, Collectively Exhaustive (MECE) zones.
   - Solves the **Outdated Truth Problem**: ensures AI agents distinguish between active production truth and historical/deprecated drafts.

2. **The Knowledge Axis (Domain Ontology)**:
   - Manages *what* a file means and how it connects conceptually to other entities.
   - Modeled via Knowledge Graphs (e.g., KùzuDB, Neo4j, GraphRAG, Obsidian Graph).

---

## 2. The 5 MECE Lifecycle Zones (Flat Depth = 2)

Workspaces are organized into exactly 5 top-level zones. Nested folder mazes are strictly prohibited (maximum depth = 2: `Zone/Document.ext`):

| Zone | Lifecycle Purpose | Actionability | Scope |
|:---|:---|:---:|:---|
| `00_INBOX/` | Raw triage area | Pending | Unsorted notes, incoming drafts, raw downloads |
| `10_ACTIVE_TIMEBOUND/` | Sprints & Milestones | Active | Time-boxed initiatives with defined completion criteria |
| `20_ACTIVE_CONTINUOUS/` | Evergreen Operations | Active | Living SOPs, operational runbooks, recurring checklists |
| `30_REFERENCE/` | Reusable Knowledge | Non-Active | Playbooks, templates, architecture specs, frameworks |
| `40_ARCHIVE/` | Historical Snapshots | Read-Only | Completed milestones, superseded drafts, immutable audit trails |

---

## 3. Universal PDCA Naming Standard

Every managed file must follow a predictable, machine-parseable naming convention:

```text
{PROJECT_ID}.{STAGE}.{SEQ} - {YYYYMMDD} - {Semantic_Title}.{ext}
```

- `{PROJECT_ID}`: 2-digit project or domain code (e.g., `10`, `42`, `PRJ`).
- `{STAGE}`: 2-letter Deming cycle (PDCA) stage:
  - `PL` (Plan)  : Research, requirements, architecture, specs, proposals.
  - `DO` (Do)    : Source drafts, implementation modules, prototypes.
  - `CK` (Check) : QA test reports, audits, peer reviews, benchmark results.
  - `AC` (Act)   : Handoff decks, retrospectives, release notes, updated standards.
- `{SEQ}`: 2-digit sequential index (`01`, `02`, `03`...) ensuring chronological sorting.
- `{YYYYMMDD}`: ISO creation or milestone date.
- `{Semantic_Title}`: 3 to 6 words in Title_Case or snake_case with underscores.

---

## 4. Knowledge Graph & GraphRAG Synergy

1. **Deterministic Primary Keys**: The prefix `{PROJECT_ID}.{STAGE}.{SEQ}` (e.g., `10.PL.01`) serves as a collision-free Node ID. Moving a file across zones or tweaking the title does not break graph references.
2. **Automatic Artifact DAG**: The progression `PL` $\to$ `DO` $\to$ `CK` $\to$ `AC` forms a natural Directed Acyclic Graph ($O(1)$ relationship parsing without LLM inference).
3. **Exact Relational Retrieval**: AI agents can execute precise graph queries (e.g., `MATCH (d:Doc {stage: 'CK'}) WHERE d.project = '10'`) instead of relying solely on probabilistic vector similarity.

---

## 5. Rules & Invariants

1. **Flat Depth Invariant**: Managed files sit directly inside a zone (`Zone/File.ext`). No intermediate nested category folders.
2. **Never Delete Ambiguous Content**: Unclassified or uncertain files route to `00_INBOX/`.
3. **Archive Read-Only**: Files inside `40_ARCHIVE/` are immutable snapshots.
4. **Zero Outdated Truth**: Deprecated or superseded files must transition to archive with status updated in the knowledge index.
