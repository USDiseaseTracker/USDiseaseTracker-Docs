# Example and Template Data Files

This directory contains example data files that demonstrate compliance with the data standards and template data files for data submission.

## Available Examples

### Disease Tracking Report Example
- `disease_tracking_report_WA-EXAMPLE_2026-02-09.csv` - Sample data file with measles and pertussis data from Washington state, demonstrating proper format and structure

## Using Examples

These examples can be used to:
1. Understand the structure of compliant data
2. Test data validation scripts
3. Develop data integration tools
4. Train users on data standards
<br>

## Available Templates

### Disease Tracking Report Template
- `disease_tracking_report_{jurisdiction}_{report_date}.csv` - Empty template file with correct field structure for data submission

**File naming convention:**
When using this template, rename the file following the pattern:
```
disease_tracking_report_{jurisdiction}_{report_date}.csv
```

### Jurisdiction Reporting Metadata Template
- `disease-tracking-metadata-{jurisdiction}.yaml` - Template for jurisdictions to provide required metadata about their data submission

**File naming convention:**
When using this template, rename the file following the pattern:
```
disease-tracking-metadata-{jurisdiction}.yaml
```
Replace `{jurisdiction}` with your jurisdiction's two-letter abbreviation (e.g., `disease-tracking-metadata-WA.yaml`).

## Using Templates

1. Download the template file
2. Fill in your jurisdiction's data following the field specifications
3. Rename the file using the naming convention above
4. Submit the file using one of the transfer methods described in the [Data Transfer Guide](../guides/data-transfer-guide.md)

**For the metadata template:**
1. Download `disease-tracking-metadata-{jurisdiction}.yaml`
2. Complete all required fields with your jurisdiction's information:
   - Date classification method (CCCD or custom hierarchy)
   - List of geographic units and their relationships
   - Data suppression policies
   - Contact information for technical and data quality questions
3. Rename the file with your jurisdiction abbreviation
4. Submit along with your data files
<br>


## Related Files

- [Data Submission Guide](../guides/data-submission-guide.md) - High-level guidance on what and when to submit
- [Data Technical Specifications](../guides/data-technical-specs.md) - Complete field definitions and requirements
- [Data dictionary (CSV)](disease_tracking_data_dictionary.csv) - Reference table of all fields and valid values