# Quality Checkpoints: File Governance Skill

## CP-001: Workspace MECE Zone Verification
- **Criteria**: Zero loose files in repository root or unclassified directories.
- **Enforcement**: Directory linter / Quality Gate StructureReviewer.

## CP-002: PDCA Naming Compliance
- **Criteria**: All production artifacts follow `{Domain}.{Cycle}.{Seq} - {Date} - {Title}` format.
- **Enforcement**: Regular expression schema validator.

## CP-003: High-Entropy Secrets Prevention
- **Criteria**: Zero API tokens or cookies stored in source files.
- **Enforcement**: Quality Gate SecretsScannerReviewer.
