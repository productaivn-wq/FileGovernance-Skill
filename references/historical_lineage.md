# Historical Lineage & Theoretical Foundations

> **Academic and historical foundations referenced in the formulation of the FileGovernance Framework.**

When designing an autonomous document governance model for modern AI agents and knowledge graphs, we conducted extensive research across library science, records archival standards, engineering information management, and software architecture.

Below is the structured breakdown of the historical frameworks synthesized into this skill:

---

## 1. Library Science & Faceted Classification
* **Origins**: S.R. Ranganathan (1933) — *Colon Classification & PMEST*. Melvil Dewey (1876) — *Dewey Decimal Classification (DDC)*. Paul Otlet & Henri La Fontaine (1905) — *Universal Decimal Classification (UDC)*.
* **Core Insight**: Knowledge is multidimensional. Rather than forcing a single rigid tree, faceted classification assigns metadata across independent facets: Personality (Entity), Matter (Asset), Energy (Activity/Stage), Space (Domain/Area), and Time (Date).
* **Application in FileGovernance**: The naming format `{PROJECT}.{STAGE}.{SEQ} - {YYYYMMDD} - {Title}` is a lightweight faceted classification string that preserves project context, lifecycle stage, sequence, and chronology without requiring deep directory nesting.

---

## 2. Archival Science & Records Lifecycle Management
* **Origins**: Theodore Schellenberg (1956) — *Modern Archives: Principles and Techniques*. International Standard **ISO 15489-1** (*Information and documentation — Records management*).
* **Core Insight**: The Records Continuum Model. Documents transition through distinct lifecycle stages:
  1. *Current / Active*: High transactional activity, frequent updates.
  2. *Semi-Current / Continuous*: Maintained policies, active SOPs, continuous governance.
  3. *Reference / Secondary*: Non-record guidance materials used for consultation.
  4. *Non-Current / Inactive*: Permanent historical retention or archival disposition (immutable).
* **Application in FileGovernance**: Mapped directly to the 5 MECE zones (`00_INBOX`, `10_ACTIVE_TIMEBOUND`, `20_ACTIVE_CONTINUOUS`, `30_REFERENCE`, `40_ARCHIVE`), eliminating the "Outdated Truth" problem in RAG and AI search.

---

## 3. Engineering Information Management (ISO 19650)
* **Origins**: International Standard **ISO 19650-2** (*Organization and digitization of information about buildings and civil engineering works, including building information modelling (BIM)*).
* **Core Insight**: Multi-team engineering projects collapse if documents lack a deterministic naming container. ISO 19650 defines a strict delimiter-separated container: `Project-Originator-Volume-Level-Type-Role-Classification-Number`.
* **Application in FileGovernance**: Adopted the delimiter standard (`.` and `-`) and controlled 2-letter stage tags to guarantee deterministic regular-expression parsing.

---

## 4. Decimal Indexing Systems (Johnny.Decimal)
* **Origins**: John Noble (2018) — *Johnny.Decimal System*.
* **Core Insight**: Cognitive load increases exponentially beyond depth 2. Johnny.Decimal restricts top-level areas to 10-99 and sub-categories to 10.01-10.99.
* **Application in FileGovernance**: Flat depth invariant (depth = 2) and deterministic 2-digit project IDs (`PP`) coupled with sequential indices (`SEQ`).

---

## 5. Personal Knowledge Management (P.A.R.A)
* **Origins**: Tiago Forte (2017) — *Building a Second Brain (BASB)*.
* **Core Insight**: Organizing by *actionability* rather than by static topic. Projects (deadline), Areas (standard), Resources (interest), Archives (inactive).
* **Application in FileGovernance**: Reframed through mathematical MECE criteria:
  - Active vs. Inactive (Mutually Exclusive)
  - Time-bound vs. Continuous (Mutually Exclusive)
  - Reference vs. Archive (Mutually Exclusive)
  - Inbox (Collectively Exhaustive triage)

---

## 6. Continuous Quality Cycles (Deming / Shewhart PDCA)
* **Origins**: Walter A. Shewhart (1939) & W. Edwards Deming (1950) — *Plan-Do-Check-Act*.
* **Core Insight**: Work processes advance in a closed feedback loop: Planning defines goals, Doing executes them, Checking evaluates evidence, and Acting standardizes improvements.
* **Application in FileGovernance**: Replaced proprietary purpose codes with universal PDCA tags (`PL`, `DO`, `CK`, `AC`), instantly creating an automatic directed acyclic graph (DAG) of project lineage.
