# Scripts

This directory contains utility scripts for the USDiseaseTracker-Docs repository.

## generate_json_schema.py

This script generates `data_reporting_schema.json` from the Pydantic model definitions in `examples-and-templates/data_reporting_schema.py`.

**The Pydantic model (`data_reporting_schema.py`) is the source of truth.** This script ensures that the JSON schema stays synchronized with the Pydantic model.

### Usage

**Generate the JSON schema:**
```bash
python3 scripts/generate_json_schema.py
```

This will:
1. Import the Pydantic `DiseaseReport` model
2. Extract field definitions, types, and validation rules
3. Generate a JSON Schema file in the same format as the existing schema
4. Write the output to `examples-and-templates/data_reporting_schema.json`

### What it generates

The script generates a complete JSON Schema including:
- **Field definitions**: All field types and descriptions
- **Enum constraints**: For fields like `disease_name`, `state`, `age_group`, etc.
- **Validation rules**: Cross-field validations (e.g., disease-specific time_unit constraints)
- **Required fields**: Based on the Pydantic model configuration
- **Type constraints**: Date formats, integer ranges, etc.

### Automated generation

This script runs automatically via GitHub Actions when:
- `examples-and-templates/data_reporting_schema.py` is modified
- Changes are pushed to the `main` branch
- A pull request modifies the Pydantic schema file

The workflow will automatically:
1. Run the generation script
2. Commit the updated JSON schema if changes are detected
3. Validate the generated schema against documentation

## validate_schema_specs.py

This script validates that the technical specifications in `guides/data-technical-specs.md` and the data dictionary in `examples-and-templates/disease_tracking_data_dictionary.csv` match the JSON schema in `examples-and-templates/data_reporting_schema.json`.

**The JSON schema is the source of truth.** The script ensures that documentation and the data dictionary stay synchronized with the schema.

### Usage

**Check for mismatches:**
```bash
python3 scripts/validate_schema_specs.py
```

**Auto-update markdown and data dictionary from schema:**
```bash
python3 scripts/validate_schema_specs.py --update
```

### What it checks

**Markdown specifications:**
- **Age groups**: Validates that age group enumerations match between schema and markdown
- **Disease subtype values**: Checks that disease subtype values (meningococcal serogroups) are consistent
- **Geographic unit values**: Ensures geo_unit enumerations match
- **Required fields**: Verifies that required fields are consistent

**Data dictionary:**
- **Age groups**: Validates age_group values match the schema
- **Disease subtype values**: Checks disease_subtype values match the schema
- **Geographic unit values**: Ensures geo_unit values match the schema

### Automated checks

This script runs automatically via GitHub Actions on:
- Every push to the `main` branch
- Every pull request to `main`

If mismatches are detected, the workflow will automatically update the markdown file and data dictionary to match the schema and commit the changes.

### Exit codes

- `0`: All checks passed
- `1`: One or more checks failed (without `--update` flag)
- `0`: Checks failed but files were updated successfully (with `--update` flag)
