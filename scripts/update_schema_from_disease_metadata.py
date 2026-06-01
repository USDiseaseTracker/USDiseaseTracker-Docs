#!/usr/bin/env python3
"""
Update data reporting schema when disease_metadata.csv changes.

This script is the entry point for keeping all schema-derived files in sync
with the disease catalog in disease_metadata.csv.  It runs the full update
pipeline:

  1. Regenerate data_reporting_schema.yaml from data_reporting_schema.py
     (Pydantic model) + disease_metadata.csv (disease catalog).
  2. Update disease_tracking_data_dictionary.csv from the YAML schema.
  3. Update guides/data-technical-specs.md from the YAML schema.
  4. Validate consistency across all three derived files.

Intended to be called by the 'update-schema-from-disease-metadata' GitHub
Actions workflow whenever disease_metadata.csv is pushed to any branch.
"""

import sys
import subprocess
from pathlib import Path

import yaml


def _run(cmd: list[str], description: str) -> None:
    """Run a subprocess command; exit with a non-zero code on failure."""
    print(f"\n{'='*60}")
    print(description)
    print('='*60)
    try:
        subprocess.run(cmd, check=True)
        print(f"✓ {description} — SUCCESS")
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} — FAILED (exit code: {e.returncode})")
        sys.exit(e.returncode)
    except OSError as e:
        print(f"✗ {description} — FAILED to start command: {e}")
        sys.exit(1)


def _read_disease_names(yaml_path: Path) -> list[str]:
    """Return the disease_name enum from the YAML schema."""
    with open(yaml_path) as f:
        schema = yaml.safe_load(f)
    return schema.get('items', {}).get('properties', {}).get('disease_name', {}).get('enum', [])


def main() -> None:
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    csv_path = repo_root / 'examples-and-templates' / 'disease_metadata.csv'
    yaml_path = repo_root / 'examples-and-templates' / 'data_reporting_schema.yaml'

    print('='*60)
    print('Update Schema from Disease Metadata')
    print('='*60)
    print(f'\nSource: {csv_path}')
    print('\nThis script will:')
    print('  1. Regenerate YAML schema from Pydantic model + disease_metadata.csv')
    print('  2. Update data dictionary CSV from YAML schema')
    print('  3. Update markdown documentation from YAML schema')
    print('  4. Validate consistency across all derived files')

    # Capture current disease list so we can report what changed.
    diseases_before: list[str] = []
    if yaml_path.exists():
        diseases_before = _read_disease_names(yaml_path)

    # Step 1: Regenerate YAML schema
    _run(
        [sys.executable, str(script_dir / 'generate_yaml_schema.py')],
        'Step 1: Regenerate YAML schema from Pydantic model + disease_metadata.csv',
    )

    diseases_after = _read_disease_names(yaml_path)
    added = sorted(set(diseases_after) - set(diseases_before))
    removed = sorted(set(diseases_before) - set(diseases_after))
    if added:
        print(f'  + Diseases added:   {added}')
    if removed:
        print(f'  - Diseases removed: {removed}')
    if not added and not removed:
        print('  No disease_name changes detected.')

    # Step 2 & 3: Update data dictionary and markdown from YAML schema
    _run(
        [sys.executable, str(script_dir / 'validate_schema_specs.py'), '--update'],
        'Step 2: Update data dictionary CSV and markdown documentation from YAML schema',
    )

    # Step 4: Validate final consistency
    _run(
        [sys.executable, str(script_dir / 'validate_schema_specs.py')],
        'Step 4: Validate consistency across all derived files',
    )

    print('\n' + '='*60)
    print('✓ Schema update from disease metadata completed successfully!')
    print('='*60)
    print('\nUpdated files:')
    print('  - examples-and-templates/data_reporting_schema.yaml')
    print('  - examples-and-templates/disease_tracking_data_dictionary.csv')
    print('  - guides/data-technical-specs.md')


if __name__ == '__main__':
    main()
