# Functional Requirements: File Governance & Knowledge Graph Integration

## FR-001: 5-Zone MECE Workspace Routing
The system shall route every incoming, active, reference, and historical file into one of 5 mutually exclusive, collectively exhaustive zones:
- `00_INBOX`: Ephemeral triage (retention: 24h)
- `10_ACTIVE_TIMEBOUND`: Sprint deliverables
- `20_ACTIVE_CONTINUOUS`: Core skills and persistent capabilities
- `30_REFERENCE`: Read-only specifications and schemas
- `40_ARCHIVE`: Immutable historical records

## FR-002: PDCA Delimited Artifact Naming
The system shall enforce deterministic artifact naming conforming to ISO 19650 / PDCA schema:
`{Domain}.{Cycle}.{Seq} - {YYYYMMDD} - {Descriptive_Title}.{ext}`

## FR-003: Knowledge Graph Ontology Mapping
The system shall decouple operational lifecycle state from semantic ontology nodes, ensuring clean entity-relationship mapping without folder nesting traps.
