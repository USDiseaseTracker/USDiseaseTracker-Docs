# Disease Tracking Report Data Standard

**Version:** 1.0.0  
**Last Updated:** 2026-01-06  
**Status:** Draft

## Overview

This document defines the data standard for disease tracking reports in the US Disease Tracker system. This standard specifies the required and optional fields for submitting aggregate disease case counts during the pilot phase.

**Important:** This standard is for aggregate data only. No line-level (individual case) data should be submitted.

## Data Structure

Data should be submitted in CSV format with one row per unique combination of:
- Time period (week, month, or year-to-date)
- Geographic unit
- Disease
- Age group (when applicable)
- Disease subtype (when applicable)

### No Zero Reporting

Only include rows with non-zero counts. The system will automatically infer zeros for missing combinations at higher aggregation levels.

## Required Fields

### Time Period Fields

| Field Name | Data Type | Description | Valid Values |
|------------|-----------|-------------|--------------|
| time_unit | String | Time aggregation unit | `week`, `month`, `ytd` |
| report_period_start | Date | Start date of reporting period (MMWR-aligned) | ISO 8601 format (YYYY-MM-DD) |
| report_period_end | Date | End date of reporting period (MMWR-aligned) | ISO 8601 format (YYYY-MM-DD) |
| date_type | String | Method used to assign cases to time periods | `cccd`, `jurisdiction date hierarchy` |

**Notes:**
- Use MMWR week boundaries for weekly reporting
- Use MMWR week-to-month crosswalk for monthly reporting
- For `ytd`, use MMWR week 1 start (2024-12-29) through end of last complete week
- Provide metadata describing custom date hierarchies if not using CCCD

### Disease Fields

| Field Name | Data Type | Description | Valid Values |
|------------|-----------|-------------|--------------|
| disease_name | String | Name of disease being reported | `measles`, `pertussis`, `meningococcus` |
| outcome | String | Type of outcome being reported | `cases` |
| confirmation_status | String | Case confirmation level | `confirmed`, `confirmed and probable` |

**Notes:**
- Measles: Use `confirmed` only
- Pertussis and Meningococcus: Use `confirmed and probable`
- Additional outcomes (hospitalizations, deaths) planned for future

### Geographic Fields

| Field Name | Data Type | Description | Valid Values |
|------------|-----------|-------------|--------------|
| reporting_jurisdiction | String | Jurisdiction submitting the data | Two-letter state/territory code or `NYC` |
| state | String | State/territory containing the geographic unit | Two-letter state/territory code |
| geo_unit | String | Type of geographic unit | `state`, `county`, `hsa`, `planning area`, `region`, `other`, `NA` |
| geo_name | String | Name of the geographic unit | Name string or `international resident`, `unspecified` |

**Notes:**
- Use standard two-letter abbreviations (AL, AK, ..., WY, DC, PR, etc.)
- For international residents: use `geo_name = "international resident"` and `geo_unit = "NA"`
- For suppressed small counts: use `geo_name = "unspecified"`
- Provide metadata listing all geographic unit names used

### Count Field

| Field Name | Data Type | Description | Valid Values |
|------------|-----------|-------------|--------------|
| count | Integer | Number of cases for this combination | Positive integers |

**Notes:**
- Only include non-zero counts
- Apply jurisdiction data suppression policies before submission
- Use `geo_name = "unspecified"` for suppressed counts to maintain totals

## Optional Fields

### Demographic Fields

| Field Name | Data Type | Description | Valid Values |
|------------|-----------|-------------|--------------|
| age_group | String | Age group of cases | See age group table below |

**Valid Age Groups:**

| Value | Description |
|-------|-------------|
| `0-11 m` | From birth up to but not including 1 year birthday |
| `1-4 y` | From 1 year birthday up to but not including 5 year birthday |
| `5-11 y` | From 5 year birthday up to but not including 12 year birthday |
| `12-18 y` | From 12 year birthday up to but not including 19 year birthday |
| `19-22 y` | From 19 year birthday up to but not including 23 year birthday |
| `23-44 y` | From 23 year birthday up to but not including 45 year birthday |
| `45-64 y` | From 45 year birthday up to but not including 65 year birthday |
| `>=65 y` | From 65 year birthday and older |
| `total` | All ages combined |
| `unknown` | Age unknown |

**Notes:**
- Age groups displayed at jurisdiction level only (not sub-jurisdiction)
- Same age groupings used for all diseases
- Leave blank or use `total` for non-age-stratified aggregations

### Disease-Specific Fields

| Field Name | Data Type | Description | Valid Values |
|------------|-----------|-------------|--------------|
| disease_subtype | String | Disease subtype (meningococcal serogroup) | `A`, `B`, `C`, `W`, `X`, `Y`, `unknown`, `unspecified`, `NA` |

**Notes:**
- Use for meningococcal disease serogroup reporting
- Use `NA` for diseases without subtype reporting (measles, pertussis)
- Use `unknown` when subtyping was not performed
- Use `unspecified` when subtype is known but suppressed

## Data Validation Rules

### Format Validation

- File must be valid CSV format
- Required fields must be present in all rows
- Field names must match specification exactly (case-sensitive)

### Data Type Validation

- Dates must be in YYYY-MM-DD format
- Counts must be positive integers
- String fields must use exact valid values (case-sensitive)

### Logical Validation

- `report_period_end` must be after or equal to `report_period_start`
- Date ranges must align with MMWR week/month boundaries
- Geographic units must be consistent with reporting jurisdiction
- Age group required for age-stratified aggregations
- Disease subtype only valid for applicable diseases

### Cross-Field Validation

- Measles confirmation_status must be `confirmed`
- Pertussis and meningococcus confirmation_status must be `confirmed and probable`
- Measles requires both weekly and monthly time_unit submissions
- Pertussis and meningococcus require monthly time_unit submissions

## Example Data

See the following files in the `examples/` directory:

- `disease_tracking_report_example.csv` - Complete example with all field types
- `disease_tracking_report_minimal.csv` - Minimal valid submission

## Metadata Requirements

Jurisdictions should provide accompanying metadata including:

1. **Date Classification Method**
   - If using CCCD, indicate "CCCD"
   - If using custom hierarchy, provide detailed description

2. **Geographic Units**
   - List of all geographic unit names used
   - Mapping of units to parent jurisdictions (if applicable)

3. **Data Suppression Policies**
   - Rules for small count suppression
   - How suppressed counts are aggregated

4. **Contact Information**
   - Technical point of contact
   - Data quality contact

## Validation

Validation scripts are under development. The validation process will check:

- File format and structure
- Required field presence
- Data type compliance
- Valid value adherence
- Logical consistency
- Cross-field rules

Validation errors will be reported back to submitters with specific error descriptions.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-06 | Initial draft for pilot phase |

## References

- [CSTE CCCD Guidelines](https://cdn.ymaws.com/www.cste.org/resource/resmgr/2015weston/DSWG_BestPracticeGuidelines_.pdf)
- [CSTE Residency Guidelines](https://learn.cste.org/images/dH42Qhmof6nEbdvwIIL6F4zvNjU1NzA0MjAxMTUy/Course_Content/Case_based_Surveillance_for_Syphilis/CSTE_Revised_Guidelines_for_Determining_Residency_for_Disease_Reporting_Purposes.pdf)
- [MMWR Week Calendar](https://ndc.services.cdc.gov/wp-content/uploads/MMWR-Weeks-Calendar_2024-2025.pdf)
- [Data Submission Template](https://cste.sharepoint.com/:x:/g/EYIPI-VSAaJAqJlUfPpwoagBrjHTQaM862FGjLfhoPjXsA?e=2Xea8R)

## Questions

For questions about this data standard, see the [Data Submission Guide](../DATA-SUBMISSION-GUIDE.md) or contact the project team through your jurisdiction's liaison.
