# FileGovernance: Governance-Driven Workspace Organization & Knowledge Graph Integration

> **A standardized, open framework bridging operational file lifecycle states with Knowledge Graphs, Obsidian Vaults, and GraphRAG architectures.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()
[![Type](https://img.shields.io/badge/Skill-FileGovernance-orange.svg)]()

---

## 📌 Executive Summary

Modern knowledge workers and software engineers suffer from two symmetrical problems:
1. **Unorganized Files & Code**: Messy file naming (`test_final_v2.py`, `notes.md`) buried across arbitrary nested folders where neither humans nor AI agents can distinguish between active truth, work-in-progress drafts, and dead experiments.
2. **The Obsidian "Pretty Graph" Illusion**: Amassing thousands of bi-directionally linked notes that look like a breathtaking galaxy in Graph View, but provide zero structured discoverability or actionable operational utility.

**The Foundational Law**:
> **A Knowledge Graph cannot fix file chaos. Files require GOVERNANCE before they can become NODES.**

This repository packages the **FileGovernance** skill: an open standard designed to structure files into a flat, predictable MECE lifecycle model while deterministically exposing **Primary Keys**, **Artifact Lineage DAGs**, and **Temporal Lifecycle Boundaries** to Knowledge Graphs and GraphRAG search engines.

---

## 🏛️ Historical Lineage & "Steal With Pride" Origins

*Note: This framework was formulated out of necessity when building autonomous agent harnesses and GraphRAG pipelines because no single open-source blueprint existed that bridged file-system hygiene directly to knowledge graph indexing.*

However, every component in this framework deliberately draws from established, century-tested disciplines:

1. **Library Classification Systems**:
   - **Ranganathan's Colon Classification (PMEST)** & **Universal Decimal Classification (UDC)**: Faceted classification concepts ensuring multidimensional attributes (Project, Stage, Sequence, Date) are preserved in a flat syntax.
2. **Archival Science & Records Management (ISO 15489)**:
   - The foundational separation between *Active Records* (transactional), *Continuous/Maintenance Records* (guidelines), *Reference Resources* (non-records), and *Permanent Inactive Archives*.
3. **Information Management in Engineering (ISO 19650)**:
   - Construction & BIM document naming principles requiring structured fields (`Project-Originator-Volume-Level-Type-Role-Number`) to prevent asset collision.
4. **Johnny.Decimal (John Noble)**:
   - The discipline of restricting top-level categories and using structured numeric identifiers for instantaneous human recognition.
5. **Tiago Forte's P.A.R.A Method**:
   - Projects, Areas, Resources, and Archives, re-architected with strict mathematical MECE boundaries (Actionable vs Non-Actionable, Timebound vs Continuous).
6. **W. Edwards Deming’s PDCA Cycle**:
   - Plan-Do-Check-Act for modeling artifact lineage (Requirements $\to$ Implementation $\to$ QA Audit $\to$ Standardization/Handoff).

---

## 📐 The Two-Axis Architecture

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

- **Lifecycle Axis**: Answers *"Where is this file in its operational workflow right now?"* (Managed by 5 MECE folders).
- **Knowledge Axis**: Answers *"What does this file mean and what real-world systems does it affect?"* (Managed by the Knowledge Graph).

---

## 📁 The 5 MECE Lifecycle Folders (Depth = 2)

All managed files reside directly in one of 5 zones (relative depth = 2: `Zone/File.ext`):

```text
Workspace/
├── 00_INBOX/             # Landing area for raw, unclassified files
├── 10_ACTIVE_TIMEBOUND/  # Sprints, milestones, deliverables with clear deadlines
├── 20_ACTIVE_CONTINUOUS/ # Living SOPs, ongoing operations, recurring checklists
├── 30_REFERENCE/         # Reusable guidelines, playbooks, frameworks
└── 40_ARCHIVE/           # Completed milestones, superseded drafts (Read-Only)
```

---

## 🏷️ The Universal PDCA Naming Convention

Format:
```text
{PROJECT_ID}.{STAGE}.{SEQ} - {YYYYMMDD} - {Semantic_Title}.{ext}
```

- `PL` (Plan)  : Research, requirements, architecture, specs, proposals.
- `DO` (Do)    : Source code, prototypes, drafts, working implementation.
- `CK` (Check) : QA test reports, audits, peer reviews, benchmark results.
- `AC` (Act)   : Handoff decks, retrospectives, release notes, updated standards.

---

## 🤝 Community Feedback & Open Invitation

This framework is shared for reference, discussion, and collective refinement:
- If you know of any existing open-source repositories, academic papers, or industry battle-tested frameworks tackling this exact problem, please let us know!
- Pull requests, discussions, and critiques are warmly welcomed.
