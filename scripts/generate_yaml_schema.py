#!/usr/bin/env python3
"""
Generate data_reporting_schema.yaml from data_reporting_schema.py and disease_metadata.csv.

This script reads the Pydantic model definitions in data_reporting_schema.py
for field-level constraints (age groups, geo units, states, etc.) and reads
disease_metadata.csv for disease-specific configuration (disease names,
time units, confirmation statuses, and subtype rules). Both sources are
combined to produce the YAML Schema.
"""

import csv
import sys
from pathlib import Path
from pydantic_core import PydanticUndefined
import yaml

# Add the examples-and-templates directory to the path so we can import the schema
sys.path.insert(0, str(Path(__file__).parent.parent / 'examples-and-templates'))

from data_reporting_schema import DiseaseReport


def read_disease_metadata(csv_path: Path) -> list[dict]:
    """Read and parse disease metadata from disease_metadata.csv.

    Returns a list of dicts with keys:
        disease, disease_long, time_unit, confirmation_status, disease_subtype (list)
    """
    required_columns = {
        'disease',
        'disease_long',
        'time_unit',
        'confirmation_status',
        'disease_subtype',
        'age_group',
        'aggregation_agegroups',
        'aggregations_diseasesubtype',
    }

    def _clean_required(row: dict, column: str, row_number: int) -> str:
        value = row.get(column)
        cleaned = value.strip() if isinstance(value, str) else ''
        if not cleaned:
            raise ValueError(
                f"Malformed row {row_number} in {csv_path}: required column '{column}' is blank"
            )
        return cleaned

    diseases = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        missing_columns = sorted(required_columns - set(fieldnames))
        if missing_columns:
            raise ValueError(
                f"Missing required columns in {csv_path}: {', '.join(missing_columns)}"
            )

        for row_number, row in enumerate(reader, start=2):
            if not row or not any(
                value.strip() for value in row.values() if isinstance(value, str)
            ):
                continue

            subtypes_value = row.get('disease_subtype')
            subtypes_raw = (
                subtypes_value.strip()
                if isinstance(subtypes_value, str) and subtypes_value.strip()
                else 'total'
            )
            subtypes = [s.strip() for s in subtypes_raw.split(',') if s.strip()]
            age_groups_value = row.get('age_group')
            age_groups_raw = (
                age_groups_value.strip()
                if isinstance(age_groups_value, str) and age_groups_value.strip()
                else 'total'
            )
            age_groups = [a.strip() for a in age_groups_raw.split(',') if a.strip()]
            def _parse_bool_flag(column: str, default: str) -> str:
                raw = row.get(column, default)
                normalized = raw.strip().upper() if isinstance(raw, str) else default
                if normalized not in ('TRUE', 'FALSE'):
                    disease_id = row.get('disease', f'row {row_number}')
                    raise ValueError(
                        f"Invalid value {raw!r} for column '{column}' in {csv_path} "
                        f"(disease={disease_id!r}). Expected 'TRUE' or 'FALSE'."
                    )
                return normalized

            diseases.append({
                'disease': _clean_required(row, 'disease', row_number),
                'disease_long': _clean_required(row, 'disease_long', row_number),
                'time_unit': _clean_required(row, 'time_unit', row_number),
                'confirmation_status': _clean_required(row, 'confirmation_status', row_number),
                'disease_subtype': subtypes,
                'age_group': age_groups,
                'aggregation_agegroups': _parse_bool_flag('aggregation_agegroups', 'TRUE'),
                'aggregations_diseasesubtype': _parse_bool_flag('aggregations_diseasesubtype', 'FALSE'),
            })
    return diseases


def _unique_ordered(values: list) -> list:
    """Return a de-duplicated list preserving first-occurrence order."""
    seen: set = set()
    result = []
    for v in values:
        if v not in seen:
            seen.add(v)
            result.append(v)
    return result


def generate_schema():
    """Generate Schema from the Pydantic DiseaseReport model and disease_metadata.csv."""

    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    csv_path = repo_root / 'examples-and-templates' / 'disease_metadata.csv'

    # Load disease metadata from CSV (authoritative source for disease-specific config)
    diseases = read_disease_metadata(csv_path)

    # Extract field information from the Pydantic model (authoritative for non-disease fields)
    fields = DiseaseReport.model_fields

    # Helper function to get enum values from Literal types
    def get_enum_values(field):
        """Extract enum values from a field's annotation."""
        annotation = field.annotation
        if hasattr(annotation, '__args__'):
            return list(annotation.__args__)
        return None

    # Build the properties dictionary
    properties = {}

    # report_period_start and report_period_end - date fields
    properties["report_period_start"] = {
        "type": "string",
        "format": "date",
        "description": "Date of report period start (YYYY-MM-DD)"
    }

    properties["report_period_end"] = {
        "type": "string",
        "format": "date",
        "description": "Date of report period end (YYYY-MM-DD)"
    }

    # date_type — from Pydantic model
    properties["date_type"] = {
        "type": "string",
        "enum": get_enum_values(fields["date_type"]),
        "description": "Calculated Case Counting Date (cccd) or jurisdiction-defined date hierarchy. Details of jurisdiction date hierarchy should be provided in metadata."
    }

    # time_unit — union of all time units in disease_metadata.csv
    properties["time_unit"] = {
        "type": "string",
        "enum": _unique_ordered([d['time_unit'] for d in diseases]),
        "description": "Time aggregation unit"
    }

    # disease_name — from disease_metadata.csv (authoritative disease catalog)
    properties["disease_name"] = {
        "type": "string",
        "enum": _unique_ordered([d['disease'] for d in diseases]),
        "description": "Name of the disease"
    }

    # disease_subtype — free string; valid values are disease-specific (see allOf)
    properties["disease_subtype"] = {
        "type": "string",
        "description": "Disease subtype (meningococcal serogroup). Use 'total' for non-subtype-stratified aggregations or diseases without subtype reporting (measles, pertussis). Use 'unknown' when subtyping was not performed. Use 'unspecified' when subtype is known but suppressed."
    }

    # reporting_jurisdiction
    properties["reporting_jurisdiction"] = {
        "type": "string",
        "description": "Abbreviation for the reporting state, city, or territory"
    }

    # state — from Pydantic model
    properties["state"] = {
        "type": "string",
        "enum": get_enum_values(fields["state"]),
        "description": "2-letter abbreviation for the state of the jurisdiction"
    }

    # geo_name
    properties["geo_name"] = {
        "type": "string",
        "description": "Name of the geographic unit"
    }

    # geo_unit — from Pydantic model
    properties["geo_unit"] = {
        "type": "string",
        "enum": get_enum_values(fields["geo_unit"]),
        "description": "Geographic unit"
    }

    # age_group — from Pydantic model
    properties["age_group"] = {
        "type": "string",
        "enum": get_enum_values(fields["age_group"]),
        "description": "Standardized age group"
    }

    # confirmation_status — union of all statuses in disease_metadata.csv
    properties["confirmation_status"] = {
        "type": "string",
        "enum": _unique_ordered([d['confirmation_status'] for d in diseases]),
        "description": "Case classification status"
    }

    # outcome — from Pydantic model
    properties["outcome"] = {
        "type": "string",
        "enum": get_enum_values(fields["outcome"]),
        "description": "Reported outcome type"
    }

    # count
    properties["count"] = {
        "type": "integer",
        "minimum": 0,
        "description": "Count of specified outcome for the specified group for this time period"
    }

    # Build the allOf section with conditional validations
    all_of = []

    # Validation 1: each disease_name must pair with its declared time_unit
    # Generated from disease_metadata.csv
    all_of.append({
        "oneOf": [
            {
                "properties": {
                    "disease_name": {"const": d['disease']},
                    "time_unit": {"const": d['time_unit']}
                }
            }
            for d in diseases
        ]
    })

    # Validation 2: time_unit = week description
    all_of.append({
        "if": {"properties": {"time_unit": {"const": "week"}}},
        "then": {
            "properties": {
                "report_period_start": {
                    "description": "When time_unit='week', report_period_start must be a Sunday (MMWR week start). JSON Schema cannot natively validate weekday; must be enforced in ETL or via custom validator."
                },
                "report_period_end": {
                    "description": "When time_unit='week', report_period_end must be a Saturday (MMWR week end). JSON Schema cannot natively validate weekday; must be enforced in ETL or via custom validator."
                }
            }
        }
    })

    # Validation 3: each disease_name must pair with its allowed disease_subtype values
    # Generated from disease_metadata.csv
    all_of.append({
        "oneOf": [
            {
                "properties": {
                    "disease_name": {"const": d['disease']},
                    "disease_subtype": {"enum": d['disease_subtype']}
                }
            }
            for d in diseases
        ]
    })

    # Validation 4: each disease_name must pair with its allowed age_group values
    # Generated from disease_metadata.csv
    all_of.append({
        "oneOf": [
            {
                "properties": {
                    "disease_name": {"const": d['disease']},
                    "age_group": {"enum": d['age_group']}
                }
            }
            for d in diseases
        ]
    })

    # Validation 5: state-level stratification rules, per disease category
    # (replaces the former blanket rule that incorrectly excluded no-age-breakdown diseases)
    #
    # 5a. Diseases with age breakdown only (no subtype breakdown):
    #     when geo_unit='state', age_group must not be 'total'.
    age_only_diseases = [
        d['disease'] for d in diseases
        if d['aggregation_agegroups'] == 'TRUE' and d['aggregations_diseasesubtype'] != 'TRUE'
    ]
    if age_only_diseases:
        all_of.append({
            "if": {
                "properties": {
                    "disease_name": {"enum": age_only_diseases},
                    "geo_unit": {"const": "state"},
                }
            },
            "then": {
                "properties": {
                    "age_group": {"not": {"const": "total"}}
                }
            }
        })

    # 5b. Diseases with subtype breakdown (e.g. meningococcus):
    #     when geo_unit='state', exactly one of age_group or disease_subtype must be 'total'
    #     (the other must not be 'total').
    subtype_diseases = [
        d['disease'] for d in diseases
        if d['aggregations_diseasesubtype'] == 'TRUE'
    ]
    if subtype_diseases:
        all_of.append({
            "if": {
                "properties": {
                    "disease_name": {"enum": subtype_diseases},
                    "geo_unit": {"const": "state"},
                }
            },
            "then": {
                "oneOf": [
                    {
                        "properties": {
                            "age_group": {"not": {"const": "total"}},
                            "disease_subtype": {"const": "total"}
                        }
                    },
                    {
                        "properties": {
                            "age_group": {"const": "total"},
                            "disease_subtype": {"not": {"const": "total"}}
                        }
                    }
                ]
            }
        })

    # 5c. Diseases with no age breakdown (e.g. perinatal hepatitis b):
    #     age_group must always be 'total' at all geo levels.
    no_age_diseases = [
        d['disease'] for d in diseases
        if d['aggregation_agegroups'] != 'TRUE'
    ]
    if no_age_diseases:
        all_of.append({
            "if": {
                "properties": {
                    "disease_name": {"enum": no_age_diseases},
                }
            },
            "then": {
                "properties": {
                    "age_group": {"const": "total"}
                }
            }
        })

    # Get required fields from the model
    required_fields = [
        field_name for field_name, field_info in fields.items()
        if field_info.is_required() or field_info.default is PydanticUndefined
    ]

    # Build the complete JSON schema
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Disease Report Dataset Schema",
        "type": "array",
        "items": {
            "type": "object",
            "properties": properties,
            "required": required_fields,
            "additionalProperties": False,
            "allOf": all_of
        }
    }

    return schema


def main():
    """Main function to generate and write the YAML schema."""
    # Define paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    csv_path = repo_root / 'examples-and-templates' / 'disease_metadata.csv'
    yaml_output_path = repo_root / 'examples-and-templates' / 'data_reporting_schema.yaml'

    # Generate the schema
    schema = generate_schema()

    # Write YAML schema
    with open(yaml_output_path, 'w') as f:
        yaml.dump(schema, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    disease_names = schema['items']['properties']['disease_name'].get('enum', [])
    print(f"✓ Generated {yaml_output_path}")
    print(f"  Diseases (from {csv_path.name}): {disease_names}")
    print(f"  Schema contains {len(schema['items']['properties'])} properties")
    print(f"  {len(schema['items']['required'])} required fields")
    print(f"  {len(schema['items']['allOf'])} conditional validations")


if __name__ == '__main__':
    main()
