#!/usr/bin/env python3
"""
Validate that DATA-TECHNICAL-SPECS.md and data dictionary match data_reporting_schema.json.
The JSON schema is the source of truth. Can optionally update markdown and data dictionary
from the schema.
"""

import csv
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any, Set


def load_schema(schema_path: Path) -> Dict[str, Any]:
    """Load the JSON schema file."""
    with open(schema_path, 'r') as f:
        return json.load(f)


def load_markdown(md_path: Path) -> str:
    """Load the markdown specifications file."""
    with open(md_path, 'r') as f:
        return f.read()


def load_data_dictionary(csv_path: Path) -> Dict[str, Dict[str, str]]:
    """Load the data dictionary CSV file."""
    data_dict = {}
    # Try different encodings
    for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
        try:
            with open(csv_path, 'r', encoding=encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Field Name'):
                        data_dict[row['Field Name']] = {
                            'data_type': row.get('Data Type', ''),
                            'values': row.get('Values/Format', ''),
                            'validated': row.get('Validated (format sensitive)*', ''),
                            'description': row.get('Description', '')
                        }
            break
        except UnicodeDecodeError:
            if encoding == 'iso-8859-1':
                raise
            continue
    return data_dict


def parse_csv_values(values_str: str) -> Set[str]:
    """Parse comma-separated values from CSV, handling quoted values."""
    if not values_str or values_str.strip() == 'n':
        return set()
    
    values_str = values_str.strip()
    values = []
    
    # Use regex to find all quoted values (handles both regular and smart quotes)
    # Pattern: any opening quote, capture content, any closing quote
    quoted_pattern = r'[""\"]([^""\"]+)[""\"]'
    quoted_matches = re.findall(quoted_pattern, values_str)
    
    # Also look for unquoted NA (not preceded or followed by quotes)
    if 'NA' in values_str:
        # Check if NA is not inside any kind of quotes
        if re.search(r'(?<!["""])NA(?!["""])', values_str):
            quoted_matches.append('NA')
    
    if quoted_matches:
        values = quoted_matches
    else:
        # Fallback to simple comma split
        values = [v.strip().strip('"').strip('"').strip('"') for v in values_str.split(',')]
    
    return set(v for v in values if v and v.strip())


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
    
    # Parse the valid values from markdown (e.g., `A`, `B`, `C`, etc.)
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


def check_data_dict_age_groups(schema: Dict, data_dict: Dict) -> Tuple[bool, str]:
    """Check if age group values in data dictionary match schema."""
    schema_age_groups = set(extract_enum_from_schema(schema, 'age_group'))
    
    age_group_entry = data_dict.get('age_group', {})
    dict_values_str = age_group_entry.get('values', '')
    dict_age_groups = parse_csv_values(dict_values_str)
    
    if schema_age_groups != dict_age_groups:
        missing_in_dict = schema_age_groups - dict_age_groups
        missing_in_schema = dict_age_groups - schema_age_groups
        msg = "Data dictionary age groups mismatch:\n"
        if missing_in_dict:
            msg += f"  In schema but not in data dictionary: {sorted(missing_in_dict)}\n"
        if missing_in_schema:
            msg += f"  In data dictionary but not in schema: {sorted(missing_in_schema)}\n"
        return False, msg
    
    return True, "Data dictionary age groups match"


def check_data_dict_disease_subtype(schema: Dict, data_dict: Dict) -> Tuple[bool, str]:
    """Check disease subtype values in data dictionary."""
    allOf = schema.get('items', {}).get('allOf', [])
    schema_subtypes = set()
    
    for condition in allOf:
        if 'oneOf' in condition:
            for option in condition['oneOf']:
                props = option.get('properties', {})
                if 'disease_subtype' in props:
                    subtype_enum = props['disease_subtype'].get('enum', [])
                    schema_subtypes.update(subtype_enum)
    
    disease_subtype_entry = data_dict.get('disease_subtype', {})
    dict_values_str = disease_subtype_entry.get('values', '')
    dict_subtypes = parse_csv_values(dict_values_str)
    
    if schema_subtypes != dict_subtypes:
        missing_in_dict = schema_subtypes - dict_subtypes
        missing_in_schema = dict_subtypes - schema_subtypes
        msg = "Data dictionary disease subtype values mismatch:\n"
        if missing_in_dict:
            msg += f"  In schema but not in data dictionary: {sorted(missing_in_dict)}\n"
        if missing_in_schema:
            msg += f"  In data dictionary but not in schema: {sorted(missing_in_schema)}\n"
        return False, msg
    
    return True, "Data dictionary disease subtype values match"


def check_data_dict_geo_unit(schema: Dict, data_dict: Dict) -> Tuple[bool, str]:
    """Check geo_unit values in data dictionary."""
    schema_geo_units = set(extract_enum_from_schema(schema, 'geo_unit'))
    
    geo_unit_entry = data_dict.get('geo_unit', {})
    dict_values_str = geo_unit_entry.get('values', '')
    dict_geo_units = parse_csv_values(dict_values_str)
    
    if schema_geo_units != dict_geo_units:
        missing_in_dict = schema_geo_units - dict_geo_units
        missing_in_schema = dict_geo_units - schema_geo_units
        msg = "Data dictionary geo_unit values mismatch:\n"
        if missing_in_dict:
            msg += f"  In schema but not in data dictionary: {sorted(missing_in_dict)}\n"
        if missing_in_schema:
            msg += f"  In data dictionary but not in schema: {sorted(missing_in_schema)}\n"
        return False, msg
    
    return True, "Data dictionary geo_unit values match"


def check_enum_field(schema: Dict, markdown: str, field_name: str) -> Tuple[bool, str]:
    """Check if enum values for a field match between schema and markdown."""
    schema_values = set(extract_enum_from_schema(schema, field_name))
    
    # Extract from markdown field summary table
    field_summary = extract_field_summary_table(markdown)
    field_info = field_summary.get(field_name, {})
    valid_values = field_info.get('valid_values', '')
    
    # Parse the valid values from markdown (e.g., `value1`, `value2`, etc.)
    md_values = set()
    for match in re.findall(r'`([^`]+)`', valid_values):
        md_values.add(match)
    
    if schema_values != md_values:
        missing_in_md = schema_values - md_values
        missing_in_schema = md_values - schema_values
        msg = f"{field_name} values mismatch:\n"
        if missing_in_md:
            msg += f"  In schema but not in markdown: {sorted(missing_in_md)}\n"
        if missing_in_schema:
            msg += f"  In markdown but not in schema: {sorted(missing_in_schema)}\n"
        return False, msg
    
    return True, f"{field_name} values match"


def check_data_dict_enum_field(schema: Dict, data_dict: Dict, field_name: str) -> Tuple[bool, str]:
    """Check if enum values for a field match between schema and data dictionary."""
    schema_values = set(extract_enum_from_schema(schema, field_name))
    
    field_entry = data_dict.get(field_name, {})
    dict_values_str = field_entry.get('values', '')
    dict_values = parse_csv_values(dict_values_str)
    
    if schema_values != dict_values:
        missing_in_dict = schema_values - dict_values
        missing_in_schema = dict_values - schema_values
        msg = f"Data dictionary {field_name} values mismatch:\n"
        if missing_in_dict:
            msg += f"  In schema but not in data dictionary: {sorted(missing_in_dict)}\n"
        if missing_in_schema:
            msg += f"  In data dictionary but not in schema: {sorted(missing_in_schema)}\n"
        return False, msg
    
    return True, f"Data dictionary {field_name} values match"


def update_markdown_from_schema(schema: Dict, markdown: str, schema_path: Path) -> str:
    """Update markdown to match schema."""
    updated = markdown
    
    # Update age groups table
    schema_age_groups = extract_enum_from_schema(schema, 'age_group')
    
    # Build age groups table with descriptions
    age_descriptions = {
        '<1 y': 'From birth up to but not including 1 year birthday',
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
    
    # Update outcome in field summary table
    schema_outcomes = extract_enum_from_schema(schema, 'outcome')
    outcome_values = ', '.join([f'`{v}`' for v in schema_outcomes])
    
    # Update the field summary table
    def replace_field_value(field_name: str, new_values: str) -> None:
        nonlocal updated
        # Match the table row for the field
        pattern = r'(\| ' + re.escape(field_name) + r' \| [^|]+ \| [^|]+ \| )([^|]+)( \| [^|]+ \|)'
        updated = re.sub(pattern, r'\1' + new_values + r'\3', updated)
    
    replace_field_value('disease_subtype', subtype_values)
    replace_field_value('geo_unit', geo_unit_values)
    replace_field_value('outcome', outcome_values)
    
    # Update the detailed field tables as well
    # Update disease_subtype in Disease-Specific Fields table
    detailed_subtype_pattern = r'(\| disease_subtype \| String \| Disease subtype \(meningococcal serogroup\) \| )([^|]+)( \|)'
    updated = re.sub(detailed_subtype_pattern, r'\1' + subtype_values + r'\3', updated)
    
    # Update geo_unit in Geographic Fields table
    detailed_geo_pattern = r'(\| geo_unit \| String \| Type of geographic unit \| )([^|]+)( \|)'
    updated = re.sub(detailed_geo_pattern, r'\1' + geo_unit_values + r'\3', updated)
    
    # Update outcome in Disease Fields table
    detailed_outcome_pattern = r'(\| outcome \| String \| Type of outcome being reported \| )([^|]+)( \|)'
    updated = re.sub(detailed_outcome_pattern, r'\1' + outcome_values + r'\3', updated)
    
    return updated


def format_csv_values(values: List[str]) -> str:
    """Format values for CSV with proper quoting (quote all except NA)."""
    return ', '.join([f'"{v}"' if v != 'NA' else v for v in values])


def update_data_dictionary_from_schema(schema: Dict, dict_path: Path) -> None:
    """Update data dictionary CSV file to match schema."""
    # Read the CSV file with proper encoding
    rows = []
    encoding = None
    for enc in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
        try:
            with open(dict_path, 'r', encoding=enc, newline='') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                encoding = enc
                break
        except UnicodeDecodeError:
            if enc == 'iso-8859-1':
                raise
            continue
    
    if not rows:
        print(f"Warning: No rows found in {dict_path}")
        return
    
    # Get schema values
    schema_age_groups = extract_enum_from_schema(schema, 'age_group')
    schema_geo_units = extract_enum_from_schema(schema, 'geo_unit')
    
    # Get disease subtypes from schema
    allOf = schema.get('items', {}).get('allOf', [])
    schema_subtypes = set()
    for condition in allOf:
        if 'oneOf' in condition:
            for option in condition['oneOf']:
                props = option.get('properties', {})
                if 'disease_subtype' in props:
                    subtype_enum = props['disease_subtype'].get('enum', [])
                    schema_subtypes.update(subtype_enum)
    
    # Update rows
    for row in rows:
        field_name = row.get('Field Name', '')
        
        if field_name == 'age_group':
            row['Values/Format'] = format_csv_values(schema_age_groups)
        
        elif field_name == 'geo_unit':
            row['Values/Format'] = format_csv_values(schema_geo_units)
        
        elif field_name == 'disease_subtype':
            row['Values/Format'] = format_csv_values(sorted(schema_subtypes))
    
    # Write back to CSV in UTF-8 encoding
    with open(dict_path, 'w', encoding='utf-8', newline='') as f:
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    """Main validation function."""
    repo_root = Path(__file__).parent.parent
    schema_path = repo_root / 'examples-and-templates' / 'data_reporting_schema.json'
    md_path = repo_root / 'guides' / 'DATA-TECHNICAL-SPECS.md'
    dict_path = repo_root / 'examples-and-templates' / 'disease_tracking_data_dictionary.csv'
    
    if not schema_path.exists():
        print(f"Error: Schema file not found at {schema_path}")
        sys.exit(1)
    
    if not md_path.exists():
        print(f"Error: Markdown file not found at {md_path}")
        sys.exit(1)
    
    if not dict_path.exists():
        print(f"Error: Data dictionary file not found at {dict_path}")
        sys.exit(1)
    
    schema = load_schema(schema_path)
    markdown = load_markdown(md_path)
    data_dict = load_data_dictionary(dict_path)
    
    print("Validating that markdown and data dictionary match schema (schema is source of truth)...\n")
    
    markdown_checks = [
        ("Markdown: Age groups", lambda s, m: check_age_groups(s, m)),
        ("Markdown: Disease subtype values", lambda s, m: check_disease_subtype(s, m)),
        ("Markdown: Geo unit values", lambda s, m: check_geo_unit(s, m)),
        ("Markdown: Required fields", lambda s, m: check_required_fields(s, m)),
        ("Markdown: outcome values", lambda s, m: check_enum_field(s, m, 'outcome')),
        ("Markdown: date_type values", lambda s, m: check_enum_field(s, m, 'date_type')),
        ("Markdown: time_unit values", lambda s, m: check_enum_field(s, m, 'time_unit')),
        ("Markdown: disease_name values", lambda s, m: check_enum_field(s, m, 'disease_name')),
        ("Markdown: confirmation_status values", lambda s, m: check_enum_field(s, m, 'confirmation_status')),
        # Note: 'state' field is not validated in markdown as it's documented generically
        # as "Two-letter state/territory code" for readability rather than listing all 56 codes.
        # The data dictionary contains the full enumeration and is validated below.
    ]
    
    data_dict_checks = [
        ("Data Dictionary: Age groups", lambda s, d: check_data_dict_age_groups(s, d)),
        ("Data Dictionary: Disease subtype values", lambda s, d: check_data_dict_disease_subtype(s, d)),
        ("Data Dictionary: Geo unit values", lambda s, d: check_data_dict_geo_unit(s, d)),
        ("Data Dictionary: outcome values", lambda s, d: check_data_dict_enum_field(s, d, 'outcome')),
        ("Data Dictionary: date_type values", lambda s, d: check_data_dict_enum_field(s, d, 'date_type')),
        ("Data Dictionary: time_unit values", lambda s, d: check_data_dict_enum_field(s, d, 'time_unit')),
        ("Data Dictionary: disease_name values", lambda s, d: check_data_dict_enum_field(s, d, 'disease_name')),
        ("Data Dictionary: confirmation_status values", lambda s, d: check_data_dict_enum_field(s, d, 'confirmation_status')),
        ("Data Dictionary: state values", lambda s, d: check_data_dict_enum_field(s, d, 'state')),
    ]
    
    all_passed = True
    failed_checks = []
    
    for check_name, check_func in markdown_checks:
        passed, message = check_func(schema, markdown)
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check_name}")
        if not passed:
            print(f"  {message}")
            all_passed = False
            failed_checks.append(check_name)
    
    for check_name, check_func in data_dict_checks:
        passed, message = check_func(schema, data_dict)
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
        
        # Check if we should update the markdown and data dictionary
        if '--update' in sys.argv:
            print("\nUpdating markdown and data dictionary from schema...")
            updated_markdown = update_markdown_from_schema(schema, markdown, schema_path)
            with open(md_path, 'w') as f:
                f.write(updated_markdown)
            print(f"✓ Updated {md_path}")
            
            update_data_dictionary_from_schema(schema, dict_path)
            print(f"✓ Updated {dict_path}")
            sys.exit(0)
        else:
            print("\nRun with --update flag to automatically update markdown and data dictionary from schema")
            sys.exit(1)


if __name__ == '__main__':
    main()
