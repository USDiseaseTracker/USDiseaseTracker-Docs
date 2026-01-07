# Scripts

This directory contains utility scripts for the USDiseaseTracker-Docs repository.

## validate_schema_specs.py

This script validates that the technical specifications in `guides/DATA-TECHNICAL-SPECS.md` match the JSON schema in `examples-and-templates/data_reporting_schema.json`.

### Usage

**Check for mismatches:**
```bash
python3 scripts/validate_schema_specs.py
```

**Auto-update markdown from schema:**
```bash
python3 scripts/validate_schema_specs.py --update
```

### What it checks

- **Age groups**: Validates that age group enumerations match between schema and markdown
- **Disease subtype values**: Checks that disease subtype values (meningococcal serogroups) are consistent
- **Geographic unit values**: Ensures geo_unit enumerations match
- **Required fields**: Verifies that required fields are consistent

### Automated checks

This script runs automatically via GitHub Actions on:
- Every push to the `main` branch
- Every pull request to `main`

If mismatches are detected, the workflow will automatically update the markdown file to match the schema and commit the changes.

### Exit codes

- `0`: All checks passed
- `1`: One or more checks failed (without `--update` flag)
- `0`: Checks failed but markdown was updated successfully (with `--update` flag)
