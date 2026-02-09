#!/usr/bin/env python3
"""
Update data standards tool and documentation from validation schema.

This script orchestrates the complete update process:
1. Generates JSON schema from Pydantic model (data_reporting_schema.py)
2. Updates data dictionary CSV from JSON schema
3. Updates markdown documentation from JSON schema
4. Validates consistency across all files

This ensures that the data standards tool (data_dictionary.csv) and
documentation always reflect the current validation schema.
"""

import sys
import subprocess
from pathlib import Path


def run_command(cmd: list, description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    
    try:
        subprocess.run(cmd, capture_output=False, check=True)
        print(f"✓ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} - FAILED (exit code: {e.returncode})")
        return False
    except OSError as e:
        print(f"✗ {description} - FAILED to start command: {e}")
        return False


def main():
    """Main function to update data standards."""
    script_dir = Path(__file__).parent
    
    print("="*60)
    print("Data Standards Update Process")
    print("="*60)
    print("\nThis script will:")
    print("  1. Generate JSON schema from Pydantic model")
    print("  2. Update data dictionary CSV from JSON schema")
    print("  3. Update markdown documentation from JSON schema")
    print("  4. Validate consistency across all files")
    
    # Step 1: Generate JSON schema from Pydantic model
    if not run_command(
        [sys.executable, str(script_dir / "generate_json_schema.py")],
        "Step 1: Generate JSON schema from Pydantic model"
    ):
        print("\n✗ Failed to generate JSON schema")
        sys.exit(1)
    
    # Step 2: Update data dictionary and markdown from JSON schema
    if not run_command(
        [sys.executable, str(script_dir / "validate_schema_specs.py"), "--update"],
        "Step 2: Update data dictionary and markdown from JSON schema"
    ):
        print("\n✗ Failed to update data dictionary and markdown")
        sys.exit(1)
    
    # Step 3: Validate final consistency
    if not run_command(
        [sys.executable, str(script_dir / "validate_schema_specs.py")],
        "Step 3: Validate final consistency"
    ):
        print("\n✗ Final validation failed")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✓ Data standards update completed successfully!")
    print("="*60)
    print("\nUpdated files:")
    print("  - examples-and-templates/data_reporting_schema.json")
    print("  - examples-and-templates/disease_tracking_data_dictionary.csv")
    print("  - guides/DATA-TECHNICAL-SPECS.md")
    print("\nThe data standards tool now reflects the current validation schema.")


if __name__ == '__main__':
    main()
