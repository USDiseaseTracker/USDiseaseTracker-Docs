# Data Technical Specifications

**Version:** 1.0.0  
**Last Updated:** 2026-01-06  
**Status:** Draft

## Overview

This document provides detailed technical specifications for all data fields required in the US Disease Tracker system. For a high-level overview of data submission requirements, see the [Data Submission Guide](Data-Submission-Guide.md).

## Purpose

These technical specifications define:
- Exact field names and data types
- Validation rules and constraints
- Allowed values and formats
- Field-level requirements (required vs. optional)

## General Data Standards

### Data Types

The following data types are used throughout the system:

- **String**: Text data, UTF-8 encoded
- **Integer**: Whole numbers (no decimal places)
- **Date**: ISO 8601 format (YYYY-MM-DD)
- **Boolean**: Logical values (true/false)

### Common Validation Rules

1. **Uniqueness**: Certain fields must be unique within the dataset
2. **Format Compliance**: All data must match specified formats
3. **Range Validation**: Numeric fields must fall within acceptable ranges
4. **Code Validation**: Coded fields must use approved code lists
5. **Referential Integrity**: Related fields must maintain consistency

### Character Encoding

All text data must be UTF-8 encoded to support international characters and special symbols.

## Disease Tracking Report Fields

### Required Fields

The following fields are **required** for all disease tracking reports:

#### case_id

- **Data Type**: String
- **Description**: Unique identifier for the case
- **Validation Rules**: 
  - Must be unique across all submissions
  - Alphanumeric characters and hyphens allowed (A-Z, a-z, 0-9, -)
  - Maximum length: 50 characters
  - No spaces allowed
- **Example**: `CASE2026001234`, `CASE-2026-001-TX`

#### report_date

- **Data Type**: Date
- **Description**: Date the case was reported to the surveillance system
- **Validation Rules**: 
  - Must be in ISO 8601 format (YYYY-MM-DD)
  - Cannot be a future date
  - Must be within the current surveillance year or previous 2 years
- **Example**: `2026-01-15`

#### disease_code

- **Data Type**: String
- **Description**: Standard disease classification code
- **Validation Rules**: 
  - Must match an entry in the approved disease list
  - May contain alphanumeric characters and hyphens
  - Valid codes are maintained in the reference data system
- **Example**: `COVID-19`, `FLU-A`, `MEASLES`
- **Notes**: Contact the system administrator for the current approved disease list

#### jurisdiction

- **Data Type**: String
- **Description**: Two-letter code for the reporting jurisdiction (state)
- **Validation Rules**: 
  - Must be a valid two-letter US state or territory code
  - Uppercase letters only
  - Must be one of the 50 US states, DC, or US territories
- **Example**: `CA`, `NY`, `TX`, `DC`
- **Valid Values**: All US state codes (AL, AK, AZ, AR, CA, CO, CT, DE, FL, GA, HI, ID, IL, IN, IA, KS, KY, LA, ME, MD, MA, MI, MN, MS, MO, MT, NE, NV, NH, NJ, NM, NY, NC, ND, OH, OK, OR, PA, RI, SC, SD, TN, TX, UT, VT, VA, WA, WV, WI, WY, DC, AS, GU, MP, PR, VI)

#### age

- **Data Type**: Integer
- **Description**: Patient age in complete years at time of report
- **Validation Rules**: 
  - Must be an integer between 0 and 120 (inclusive)
  - No decimal values
  - For infants under 1 year, use 0
- **Example**: `45`, `0`, `78`

#### sex

- **Data Type**: String
- **Description**: Patient biological sex
- **Validation Rules**: 
  - Must be one of the allowed values
  - Single character
  - Uppercase
- **Allowed Values**:
  - `M` - Male
  - `F` - Female
  - `U` - Unknown (when sex cannot be determined or is not reported)
  - `O` - Other (for individuals who do not fit binary categories)
- **Example**: `F`

### Optional Fields

The following fields are **optional** but recommended for enhanced data quality:

#### race

- **Data Type**: String
- **Description**: Patient race using standard categories
- **Validation Rules**: 
  - Must use one of the standard race categories
  - Multiple races can be separated by semicolons
  - Case-insensitive matching
- **Allowed Values**:
  - `White` - White
  - `Black or African American` - Black or African American
  - `American Indian or Alaska Native` - American Indian or Alaska Native
  - `Asian` - Asian
  - `Native Hawaiian or Other Pacific Islander` - Native Hawaiian or Other Pacific Islander
  - `Other` - Other race
  - `Unknown` - Unknown or not reported
- **Example**: `White`, `Asian`, `White;Asian` (for multiple races)
- **Notes**: Use semicolons (;) to separate multiple race categories

#### ethnicity

- **Data Type**: String
- **Description**: Patient ethnicity (Hispanic origin)
- **Validation Rules**: 
  - Must be one of the allowed values
  - Case-insensitive matching
- **Allowed Values**:
  - `Hispanic or Latino` - Hispanic or Latino
  - `Not Hispanic or Latino` or `Non-Hispanic` - Not Hispanic or Latino
  - `Unknown` - Unknown or not reported
- **Example**: `Non-Hispanic`, `Hispanic or Latino`

#### symptom_onset_date

- **Data Type**: Date
- **Description**: Date when symptoms first appeared
- **Validation Rules**: 
  - Must be in ISO 8601 format (YYYY-MM-DD)
  - Cannot be after the report_date
  - Should not be more than 60 days before report_date (warning only)
  - Cannot be a future date
- **Example**: `2026-01-10`
- **Notes**: This field is crucial for epidemiological analysis and outbreak detection

#### hospitalized

- **Data Type**: Boolean
- **Description**: Whether the patient was hospitalized due to this illness
- **Validation Rules**: 
  - Must be either true or false
  - Use lowercase in data files
- **Allowed Values**:
  - `true` - Patient was hospitalized
  - `false` - Patient was not hospitalized
- **Example**: `true`

## Data Submission Formats

### CSV Format

Data should be submitted in CSV (Comma-Separated Values) format with the following specifications:

- **Encoding**: UTF-8
- **Delimiter**: Comma (,)
- **Header Row**: First row must contain field names exactly as specified
- **Quoting**: Text fields containing commas must be enclosed in double quotes
- **Line Endings**: Unix-style (LF) or Windows-style (CRLF) are both acceptable
- **Empty Values**: Optional fields can be left empty (no value between commas)

### Field Order

Fields can appear in any order in the CSV file. The header row determines the field mapping.

### Example CSV Structure

```csv
case_id,report_date,disease_code,jurisdiction,age,sex,race,ethnicity,symptom_onset_date,hospitalized
CASE-2026-001-TX,2026-01-05,COVID-19,TX,42,F,White,Non-Hispanic,2026-01-02,false
CASE-2026-002-NY,2026-01-05,FLU-A,NY,67,M,Asian,Not Hispanic or Latino,2026-01-03,false
CASE-2026-003-CA,2026-01-06,MEASLES,CA,3,F,Black or African American,Hispanic or Latino,2026-01-04,true
```

## Validation

### Pre-Submission Validation

**Coming Soon**: Automated validation scripts will be provided to check data compliance before submission.

### Expected Validation Checks

The validation system will check for:

1. **Required Field Presence**: All required fields must be present
2. **Data Type Compliance**: All fields must match their specified data types
3. **Format Validation**: Dates, codes, and other formatted fields must follow rules
4. **Range Validation**: Numeric fields must be within acceptable ranges
5. **Code List Validation**: Coded fields must use approved values
6. **Referential Integrity**: Related fields must be consistent (e.g., symptom_onset_date before report_date)

### Validation Error Handling

When validation errors are detected:
- **Critical Errors**: Required field violations, data type mismatches - submission rejected
- **Warnings**: Optional field issues, unusual values - submission accepted with warnings
- **Information**: Best practice suggestions - submission accepted

## Examples

Complete example files are available in the `examples/` directory:

- **[disease_tracking_report_example.csv](examples/disease_tracking_report_example.csv)**: Complete example with all fields populated
- **[disease_tracking_report_minimal.csv](examples/disease_tracking_report_minimal.csv)**: Minimal valid submission with only required fields

## Reference Data

### Disease Code List

The approved disease code list is maintained separately and updated periodically. To request the current list or propose additions:

1. Check the reference data repository (link coming soon)
2. Open an issue in the [GitHub repository](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/issues)
3. Contact the data standards team

### Jurisdiction Codes

Standard two-letter US state and territory codes are used. See the `jurisdiction` field specification above for the complete list.

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2026-01-06 | Initial consolidated technical specifications | US Disease Tracker Team |

## Related Documentation

- **[Data Submission Guide](Data-Submission-Guide.md)**: High-level overview of data submission requirements
- **[Disease Tracking Report Standard](standards/disease-tracking-report-standard.md)**: Original standard definition
- **[Standard Definition Template](templates/standard-definition-template.md)**: Template for creating new standards
- **[Contributing Guide](CONTRIBUTING.md)**: How to contribute to the standards

## Contact

For technical questions about these specifications:
- Open an issue in the [GitHub repository](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/issues)
- Tag issues with the `data-standards` label
