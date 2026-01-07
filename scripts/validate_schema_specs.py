#!/usr/bin/env python3
"""
Validate that DATA-TECHNICAL-SPECS.md matches data_reporting_schema.json
and optionally update the markdown from the schema.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any


def load_schema(schema_path: Path) -> Dict[str, Any]:
    """Load the JSON schema file."""
    with open(schema_path, 'r') as f:
        return json.load(f)


def load_markdown(md_path: Path) -> str:
    """Load the markdown specifications file."""
    with open(md_path, 'r') as f:
        return f.read()


def extract_enum_from_schema(schema: Dict, field_name: str) -> List[str]:
    """Extract enum values for a field from the schema."""
    properties = schema.get('items', {}).get('properties', {})
    field = properties.get(field_name, {})
    return field.get('enum', [])


def extract_field_summary_table(markdown: str) -> Dict[str, Dict[str, str]]:
    """Extract the field summary table from markdown."""
    # Find the Field Summary table
    pattern = r'\| Field Name \| Data Type \| Description \| Valid Values \| Required \|\n\|[-\s|]+\n((?:\|[^\n]+\n)+)'
    match = re.search(pattern, markdown)
    
    if not match:
        return {}
    
    table_rows = match.group(1).strip().split('\n')
    fields = {}
    
    for row in table_rows:
        parts = [p.strip() for p in row.split('|')[1:-1]]  # Skip first and last empty elements
        if len(parts) >= 5:
            field_name = parts[0]
            fields[field_name] = {
                'data_type': parts[1],
                'description': parts[2],
                'valid_values': parts[3],
                'required': parts[4]
            }
    
    return fields


def check_age_groups(schema: Dict, markdown: str) -> Tuple[bool, str]:
    """Check if age group values match."""
    schema_age_groups = extract_enum_from_schema(schema, 'age_group')
    
    # Extract age groups from markdown
    md_pattern = r'\*\*Valid Age Groups:\*\*.*?\n\n\| Value \| Description \|\n\|[-\s|]+\n((?:\|[^\n]+\n)+)'
    match = re.search(md_pattern, markdown, re.DOTALL)
    
    if not match:
        return False, "Could not find age groups table in markdown"
    
    md_age_groups = []
    for row in match.group(1).strip().split('\n'):
        parts = [p.strip() for p in row.split('|')]
        if len(parts) >= 2 and parts[1].startswith('`'):
            age_val = parts[1].strip('`').strip()
            md_age_groups.append(age_val)
    
    schema_set = set(schema_age_groups)
    md_set = set(md_age_groups)
    
    if schema_set != md_set:
        missing_in_md = schema_set - md_set
        missing_in_schema = md_set - schema_set
        msg = "Age groups mismatch:\n"
        if missing_in_md:
            msg += f"  In schema but not in markdown: {sorted(missing_in_md)}\n"
        if missing_in_schema:
            msg += f"  In markdown but not in schema: {sorted(missing_in_schema)}\n"
        return False, msg
    
    return True, "Age groups match"


def check_disease_subtype(schema: Dict, markdown: str) -> Tuple[bool, str]:
    """Check disease subtype values."""
    # Extract from schema - need to check the conditional logic
    allOf = schema.get('items', {}).get('allOf', [])
    schema_subtypes = set()
    
    for condition in allOf:
        if 'oneOf' in condition:
            for option in condition['oneOf']:
                props = option.get('properties', {})
                if 'disease_subtype' in props:
                    subtype_enum = props['disease_subtype'].get('enum', [])
                    schema_subtypes.update(subtype_enum)
    
    # Extract from markdown field summary table
    field_summary = extract_field_summary_table(markdown)
    disease_subtype_info = field_summary.get('disease_subtype', {})
    valid_values = disease_subtype_info.get('valid_values', '')
    
    # Parse the valid values: `A`, `B`, `C`, `W`, `X`, `Y`, `unknown`, `unspecified`, `NA`
    md_subtypes = set()
    for match in re.findall(r'`([^`]+)`', valid_values):
        md_subtypes.add(match)
    
    if schema_subtypes != md_subtypes:
        missing_in_md = schema_subtypes - md_subtypes
        missing_in_schema = md_subtypes - schema_subtypes
        msg = "Disease subtype values mismatch:\n"
        if missing_in_md:
            msg += f"  In schema but not in markdown: {sorted(missing_in_md)}\n"
        if missing_in_schema:
            msg += f"  In markdown but not in schema: {sorted(missing_in_schema)}\n"
        return False, msg
    
    return True, "Disease subtype values match"


def check_geo_unit(schema: Dict, markdown: str) -> Tuple[bool, str]:
    """Check geo_unit values."""
    schema_geo_units = set(extract_enum_from_schema(schema, 'geo_unit'))
    
    # Extract from markdown field summary table
    field_summary = extract_field_summary_table(markdown)
    geo_unit_info = field_summary.get('geo_unit', {})
    valid_values = geo_unit_info.get('valid_values', '')
    
    md_geo_units = set()
    for match in re.findall(r'`([^`]+)`', valid_values):
        md_geo_units.add(match)
    
    if schema_geo_units != md_geo_units:
        missing_in_md = schema_geo_units - md_geo_units
        missing_in_schema = md_geo_units - schema_geo_units
        msg = "Geo unit values mismatch:\n"
        if missing_in_md:
            msg += f"  In schema but not in markdown: {sorted(missing_in_md)}\n"
        if missing_in_schema:
            msg += f"  In markdown but not in schema: {sorted(missing_in_schema)}\n"
        return False, msg
    
    return True, "Geo unit values match"


def check_required_fields(schema: Dict, markdown: str) -> Tuple[bool, str]:
    """Check that required fields in schema match markdown."""
    schema_required = set(schema.get('items', {}).get('required', []))
    
    # Extract from field summary table
    field_summary = extract_field_summary_table(markdown)
    md_required = set()
    for field_name, info in field_summary.items():
        if info.get('required', '').lower() == 'yes':
            md_required.add(field_name)
    
    if schema_required != md_required:
        missing_in_md = schema_required - md_required
        missing_in_schema = md_required - schema_required
        msg = "Required fields mismatch:\n"
        if missing_in_md:
            msg += f"  Required in schema but not in markdown: {sorted(missing_in_md)}\n"
        if missing_in_schema:
            msg += f"  Required in markdown but not in schema: {sorted(missing_in_schema)}\n"
        return False, msg
    
    return True, "Required fields match"


def update_markdown_from_schema(schema: Dict, markdown: str, schema_path: Path) -> str:
    """Update markdown to match schema."""
    updated = markdown
    
    # Update age groups table
    schema_age_groups = extract_enum_from_schema(schema, 'age_group')
    
    # Build age groups table with descriptions
    age_descriptions = {
        '0-11 m': 'From birth up to but not including 1 year birthday',
        '0-5 m': 'From birth up to but not including 6 months',
        '6-11 m': 'From 6 months up to but not including 1 year birthday',
        '1-4 y': 'From 1 year birthday up to but not including 5 year birthday',
        '5-11 y': 'From 5 year birthday up to but not including 12 year birthday',
        '12-18 y': 'From 12 year birthday up to but not including 19 year birthday',
        '19-22 y': 'From 19 year birthday up to but not including 23 year birthday',
        '23-44 y': 'From 23 year birthday up to but not including 45 year birthday',
        '45-64 y': 'From 45 year birthday up to but not including 65 year birthday',
        '>=65 y': 'From 65 year birthday and older',
        'total': 'All ages combined',
        'unknown': 'Age unknown',
        'unspecified': 'Age known but suppressed'
    }
    
    age_table = "| Value | Description |\n|-------|-------------|\n"
    for age in schema_age_groups:
        desc = age_descriptions.get(age, 'Age group')
        age_table += f"| `{age}` | {desc} |\n"
    
    # Replace age groups table
    pattern = r'(\*\*Valid Age Groups:\*\*.*?\n\n)\| Value \| Description \|\n\|[-\s|]+\n(?:\|[^\n]+\n)+'
    updated = re.sub(pattern, r'\1' + age_table, updated, flags=re.DOTALL)
    
    # Update field summary table for disease_subtype
    allOf = schema.get('items', {}).get('allOf', [])
    schema_subtypes = set()
    for condition in allOf:
        if 'oneOf' in condition:
            for option in condition['oneOf']:
                props = option.get('properties', {})
                if 'disease_subtype' in props:
                    subtype_enum = props['disease_subtype'].get('enum', [])
                    schema_subtypes.update(subtype_enum)
    
    subtype_values = ', '.join([f'`{v}`' for v in sorted(schema_subtypes)])
    
    # Update geo_unit in field summary table
    schema_geo_units = extract_enum_from_schema(schema, 'geo_unit')
    geo_unit_values = ', '.join([f'`{v}`' for v in schema_geo_units])
    
    # Update the field summary table
    def replace_field_value(field_name: str, new_values: str) -> None:
        nonlocal updated
        # Match the table row for the field
        pattern = r'(\| ' + re.escape(field_name) + r' \| [^|]+ \| [^|]+ \| )([^|]+)( \| [^|]+ \|)'
        updated = re.sub(pattern, r'\1' + new_values + r'\3', updated)
    
    replace_field_value('disease_subtype', subtype_values)
    replace_field_value('geo_unit', geo_unit_values)
    
    # Update the detailed field tables as well
    # Update disease_subtype in Disease-Specific Fields table
    detailed_subtype_pattern = r'(\| disease_subtype \| String \| Disease subtype \(meningococcal serogroup\) \| )([^|]+)( \|)'
    updated = re.sub(detailed_subtype_pattern, r'\1' + subtype_values + r'\3', updated)
    
    # Update geo_unit in Geographic Fields table
    detailed_geo_pattern = r'(\| geo_unit \| String \| Type of geographic unit \| )([^|]+)( \|)'
    updated = re.sub(detailed_geo_pattern, r'\1' + geo_unit_values + r'\3', updated)
    
    return updated


def main():
    """Main validation function."""
    repo_root = Path(__file__).parent.parent
    schema_path = repo_root / 'examples-and-templates' / 'data_reporting_schema.json'
    md_path = repo_root / 'guides' / 'DATA-TECHNICAL-SPECS.md'
    
    if not schema_path.exists():
        print(f"Error: Schema file not found at {schema_path}")
        sys.exit(1)
    
    if not md_path.exists():
        print(f"Error: Markdown file not found at {md_path}")
        sys.exit(1)
    
    schema = load_schema(schema_path)
    markdown = load_markdown(md_path)
    
    print("Validating schema matches markdown specifications...\n")
    
    checks = [
        ("Age groups", check_age_groups),
        ("Disease subtype values", check_disease_subtype),
        ("Geo unit values", check_geo_unit),
        ("Required fields", check_required_fields),
    ]
    
    all_passed = True
    failed_checks = []
    
    for check_name, check_func in checks:
        passed, message = check_func(schema, markdown)
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check_name}")
        if not passed:
            print(f"  {message}")
            all_passed = False
            failed_checks.append(check_name)
    
    if all_passed:
        print("\n✓ All checks passed!")
        sys.exit(0)
    else:
        print(f"\n✗ {len(failed_checks)} check(s) failed")
        
        # Check if we should update the markdown
        if '--update' in sys.argv:
            print("\nUpdating markdown from schema...")
            updated_markdown = update_markdown_from_schema(schema, markdown, schema_path)
            with open(md_path, 'w') as f:
                f.write(updated_markdown)
            print(f"✓ Updated {md_path}")
            sys.exit(0)
        else:
            print("\nRun with --update flag to automatically update the markdown from schema")
            sys.exit(1)


if __name__ == '__main__':
    main()
