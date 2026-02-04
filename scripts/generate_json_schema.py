#!/usr/bin/env python3
"""
Generate data_reporting_schema.json from data_reporting_schema.py.

This script reads the Pydantic model definitions in data_reporting_schema.py
and converts them to a JSON Schema format that matches the existing
data_reporting_schema.json structure.
"""

import json
import sys
from pathlib import Path
from pydantic_core import PydanticUndefined

# Add the examples-and-templates directory to the path so we can import the schema
sys.path.insert(0, str(Path(__file__).parent.parent / 'examples-and-templates'))

from data_reporting_schema import DiseaseReport


def generate_json_schema():
    """Generate JSON Schema from the Pydantic DiseaseReport model."""
    
    # Extract field information from the Pydantic model
    fields = DiseaseReport.model_fields
    
    # Build the properties dictionary
    properties = {}
    
    # Helper function to get enum values from Literal types
    def get_enum_values(field):
        """Extract enum values from a field's annotation."""
        annotation = field.annotation
        # Handle Literal types
        if hasattr(annotation, '__args__'):
            return list(annotation.__args__)
        return None
    
    # Map fields to JSON Schema properties
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
    
    # date_type
    properties["date_type"] = {
        "type": "string",
        "enum": get_enum_values(fields["date_type"]),
        "description": "Calculated Case Counting Date (cccd) or jurisdiction-defined date hierarchy. Details of jurisdiction date hierarchy should be provided in metadata."
    }
    
    # time_unit
    properties["time_unit"] = {
        "type": "string",
        "enum": get_enum_values(fields["time_unit"]),
        "description": "Time aggregation unit"
    }
    
    # disease_name
    properties["disease_name"] = {
        "type": "string",
        "enum": get_enum_values(fields["disease_name"]),
        "description": "Name of the disease"
    }
    
    # disease_subtype
    properties["disease_subtype"] = {
        "type": "string",
        "description": "Disease subtype (meningococcal serogroup). Use 'total' for non-subtype-stratified aggregations or diseases without subtype reporting (measles, pertussis). Use 'unknown' when subtyping was not performed. Use 'unspecified' when subtype is known but suppressed."
    }
    
    # reporting_jurisdiction
    properties["reporting_jurisdiction"] = {
        "type": "string",
        "description": "Abbreviation for the reporting state, city, or territory"
    }
    
    # state
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
    
    # geo_unit
    properties["geo_unit"] = {
        "type": "string",
        "enum": get_enum_values(fields["geo_unit"]),
        "description": "Geographic unit"
    }
    
    # age_group
    properties["age_group"] = {
        "type": "string",
        "enum": get_enum_values(fields["age_group"]),
        "description": "Standardized age group"
    }
    
    # confirmation_status
    properties["confirmation_status"] = {
        "type": "string",
        "enum": get_enum_values(fields["confirmation_status"]),
        "description": "Case classification status"
    }
    
    # outcome
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
    
    # Validation 1: disease_name and time_unit constraints
    all_of.append({
        "oneOf": [
            {
                "properties": {
                    "disease_name": {"const": "measles"},
                    "time_unit": {"const": "week"}
                }
            },
            {
                "properties": {
                    "disease_name": {"const": "pertussis"},
                    "time_unit": {"const": "week"}
                }
            },
            {
                "properties": {
                    "disease_name": {"const": "meningococcus"},
                    "time_unit": {"const": "week"}
                }
            }
        ]
    })
    
    # Validation 2: time_unit = week description
    all_of.append({
        "if": {"properties": {"time_unit": {"const": "week"}}},
        "then": {
            "properties": {
                "report_period_start": {
                    "description": "When time_unit='week', report_period_start must be an MMWR week ending (Saturday). JSON Schema cannot natively validate weekday; must be enforced in ETL or via custom validator."
                }
            }
        }
    })
    
    # Validation 3: disease_name and disease_subtype constraints
    # These values are extracted from the validate_disease_subtype validator in the Pydantic model
    all_of.append({
        "oneOf": [
            {
                "properties": {
                    "disease_name": {"const": "meningococcus"},
                    "disease_subtype": {"enum": ["A", "B", "C", "W", "X", "Y", "Z", "unknown", "unspecified", "total"]}
                }
            },
            {
                "properties": {
                    "disease_name": {"const": "measles"},
                    "disease_subtype": {"enum": ["total", "unknown", "unspecified"]}
                }
            },
            {
                "properties": {
                    "disease_name": {"const": "pertussis"},
                    "disease_subtype": {"enum": ["total", "unknown", "unspecified"]}
                }
            }
        ]
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
    """Main function to generate and write the JSON schema."""
    # Define paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    output_path = repo_root / 'examples-and-templates' / 'data_reporting_schema.json'
    
    # Generate the schema
    schema = generate_json_schema()
    
    # Write to file with nice formatting
    with open(output_path, 'w') as f:
        json.dump(schema, f, indent=4)
    
    print(f"✓ Generated {output_path}")
    print(f"  Schema contains {len(schema['items']['properties'])} properties")
    print(f"  {len(schema['items']['required'])} required fields")
    print(f"  {len(schema['items']['allOf'])} conditional validations")


if __name__ == '__main__':
    main()
