# Data Technical Specifications

| Version | Changes from previous version |   
|---------|---------|
|  1.1.0 (updated 2026-01-07) | - Initial version of documentation repository <br>- Fixed contradictions between files |


---

**Status:** Draft

## Overview

This document provides the complete technical specifications for disease tracking data submissions to the US Disease Tracker system. These specifications define the required and optional fields, data types, valid values, and formatting requirements for submitting aggregate disease case count data.

**Important:** This is for aggregate data only. No line-level (individual case) data should be submitted.

**Note:** For high-level submission guidance including what data to submit, when to submit it, and case classification rules, see the [Data Submission Guide](DATA-SUBMISSION-GUIDE.md).

### Contents

- [Data Structure](#data-structure) - Field summary and data organization requirements
- [Field Specifications](#field-specifications) - Detailed specifications for all required and optional fields
- [Validation](#validation) - Data validation requirements
- [Example Data](#example-data) - Sample files and templates
- [Metadata Requirements](#metadata-requirements) - Required accompanying metadata
- [Version History](#version-history) - Document version tracking
- [References](#references) - Related documentation and resources
<br>
<br>


## Data Structure

Data should be submitted in CSV format with one row per unique combination of:
- Time period (week, month, or year-to-date)
- Geographic unit
- Disease
- Age group (when applicable)
- Disease subtype (when applicable)
- Outcome (currently only cases)

### Field Summary

The following table provides a comprehensive overview of all data fields required for submission:

| Field Name | Data Type | Description | Valid Values | Required |
|------------|-----------|-------------|--------------|----------|
| time_unit | String | Time aggregation unit | `week`, `month`, `ytd` | Yes |
| report_period_start | Date | Start date of reporting period (MMWR week aligned) | ISO 8601 format (YYYY-MM-DD) | Yes |
| report_period_end | Date | End date of reporting period (MMWR week aligned) | ISO 8601 format (YYYY-MM-DD) | Yes |
| date_type | String | Method used to assign cases to reporting periods | `cccd`, `jurisdiction date hierarchy` | Yes |
| disease_name | String | Name of disease being reported | `measles`, `pertussis`, `meningococcus` | Yes |
| outcome | String | Type of outcome being reported | `cases`, `hospitalizations`, `deaths` | Yes |
| confirmation_status | String | Case confirmation level | `confirmed`, `confirmed and probable` | Yes |
| reporting_jurisdiction | String | Jurisdiction submitting the data | Two-letter state/territory code or `NYC` | Yes |
| state | String | State/territory containing the geographic unit | Two-letter state/territory code | Yes |
| geo_unit | String | Type of geographic unit | `county`, `state`, `region`, `planning area`, `hsa`, `NA` | Yes |
| geo_name | String | Name of the geographic unit | Name string or `international resident`, `unspecified` | Yes |
| count | Integer | Number of cases for this combination | Positive integers | Yes |
| age_group | String | Age group of cases | `0-5 m`, `6-11 m`, `1-4 y`, `5-11 y`, `12-18 y`, `19-22 y`, `23-44 y`, `45-64 y`, `>=65 y`, `total`, `unknown` | Yes |
| disease_subtype | String | Disease subtype (meningococcal serogroup) | `A`, `B`, `C`, `NA`, `W`, `X`, `Y`, `Z`, `unknown`, `unspecified` | No |

**Key Notes:**
- **Report Period:** Use MMWR week boundaries for weekly reporting and MMWR week 1 start (2024-12-29) through end of last complete week for `ytd`
- **Disease-Specific Rules:** Measles uses `confirmed` only; Pertussis and Meningococcus use `confirmed and probable`
- **Geographic Units:** Use standard two-letter abbreviations (AL, AK, ..., WY, DC, PR, etc.); for international residents use `geo_name = "international resident"` and `geo_unit = "NA"`; for suppressed small counts use `geo_name = "unspecified"`
- **Age Groups:** Age groups displayed at jurisdiction level only (not sub-jurisdiction); use `total` for non-age-stratified aggregations
- **Disease Subtype:** Use `NA` for diseases without subtype reporting (measles, pertussis); use `unknown` when subtyping was not performed; use `unspecified` when subtype is known but suppressed
- **Counts:** Only include non-zero counts; apply jurisdiction data suppression policies before submission

### No Zero Reporting

Only include rows with non-zero counts. The system will automatically infer zeros for missing combinations at higher aggregation levels.

## Fields Specifications

### Reporting Period Fields

| Field Name | Data Type | Description | Valid Values |
|------------|-----------|-------------|--------------|
| time_unit | String | Time aggregation unit | `week`, `ytd` |
| report_period_start | Date | Start date of reporting period (MMWR-aligned) | ISO 8601 format (YYYY-MM-DD) |
| report_period_end | Date | End date of reporting period (MMWR-aligned) | ISO 8601 format (YYYY-MM-DD) |
| date_type | String | Method used to assign cases to reporting time periods | `cccd`, `jurisdiction date hierarchy` |

**Notes:**
- Use MMWR week boundaries for weekly reporting
- For `ytd`, use MMWR week 1 start (2024-12-29) through end of last complete week
- Provide metadata describing custom date hierarchies if not using CCCD

### Disease Fields

| Field Name | Data Type | Description | Valid Values |
|------------|-----------|-------------|--------------|
| disease_name | String | Name of disease being reported | `measles`, `pertussis`, `meningococcus` |
| outcome | String | Type of outcome being reported | `cases`, `hospitalizations`, `deaths` |
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
| geo_unit | String | Type of geographic unit | `county`, `state`, `region`, `planning area`, `hsa`, `NA` |
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

### Demographic Fields

| Field Name | Data Type | Description | Valid Values |
|------------|-----------|-------------|--------------|
| age_group | String | Age group of cases | See age group table below |

**Valid Age Groups:**

| Value | Description |
|-------|-------------|
| `0-5 m` | From birth up to but not including 6 months |
| `6-11 m` | From 6 months up to but not including 1 year birthday |
| `1-4 y` | From 1 year birthday up to but not including 5 year birthday |
| `5-11 y` | From 5 year birthday up to but not including 12 year birthday |
| `12-18 y` | From 12 year birthday up to but not including 19 year birthday |
| `19-22 y` | From 19 year birthday up to but not including 23 year birthday |
| `23-44 y` | From 23 year birthday up to but not including 45 year birthday |
| `45-64 y` | From 45 year birthday up to but not including 65 year birthday |
| `>=65 y` | From 65 year birthday and older |
| `total` | All ages combined |
| `unknown` | Age unknown |
| `unspecified` | Age known but suppressed |

**Notes:**
- Age groups displayed at jurisdiction level only (not sub-jurisdiction)
- Same age groupings used for all diseases
- Use `total` for non-age-stratified aggregations

### Disease-Specific Fields

| Field Name | Data Type | Description | Valid Values |
|------------|-----------|-------------|--------------|
| disease_subtype | String | Disease subtype (meningococcal serogroup) | `A`, `B`, `C`, `NA`, `W`, `X`, `Y`, `Z`, `unknown`, `unspecified` |

**Notes:**
- Use for meningococcal disease serogroup reporting
- Use `NA` for diseases without subtype reporting (measles, pertussis)
- Use `unknown` when subtyping was not performed or is otherwise not known
- Use `unspecified` when subtype is known but suppressed

## Validation

See [Validation](VALIDATION.md) for details on file and data validation.


## Example Data

Example data files are available to help understand the required format:

**In this repository:**
- [Complete example](../examples-and-templates/disease_tracking_report_WA_2025-09-30.csv) - Sample data file with measles and pertussis data
- [Empty template](../examples-and-templates/disease_tracking_report_{jurisdiction}_{report_date}.csv) - Template file with correct structure
- [Data dictionary (CSV)](../examples-and-templates/disease_tracking_data_dictionary.csv) - Reference table of all fields and valid values

**File naming convention:**
Files should be named following the pattern:
```
disease_tracking_report_{jurisdiction}_{report_date}.csv
```

Examples:
- `disease_tracking_report_WA_2025-09-30.csv` (Washington state, submitted September 30, 2025)

## Metadata Requirements

Jurisdictions should provide accompanying metadata using the [Jurisdiction Reporting Metadata Template](../examples-and-templates/disease-tracking-metadata-{jurisdiction}.json) [*Coming Soon*]. Metadata required includes:

1. **Date Classification Method**
   - If using CCCD, indicate "cccd"
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


## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-01-06 | Initial draft for pilot phase |

## References

- [Data Submission Guide](DATA-SUBMISSION-GUIDE.md) - High-level guidance on what and when to submit
- [Data Transfer Guide](DATA-TRANSFER-GUIDE.md) - Technical details on how to transfer data
- [Data dictionary (CSV)](../examples-and-templates/disease_tracking_data_dictionary.csv) - Reference table of all fields and valid values
- [Validation Rules](VALIDATION.md) - Complete validation requirements
- [CSTE CCCD Guidelines](https://cdn.ymaws.com/www.cste.org/resource/resmgr/2015weston/DSWG_BestPracticeGuidelines_.pdf)
- [CSTE Residency Guidelines](https://learn.cste.org/images/dH42Qhmof6nEbdvwIIL6F4zvNjU1NzA0MjAxMTUy/Course_Content/Case_based_Surveillance_for_Syphilis/CSTE_Revised_Guidelines_for_Determining_Residency_for_Disease_Reporting_Purposes.pdf)
- [MMWR Week Calendar](https://health.maryland.gov/phpa/OIDEOR/CIDSOR/NEDSS/MMWR_Calendar.pdf)
- [MMWR Week-to-Month Crosswalk (CSV)](../examples-and-templates/MMWR_week_to_month_crosswalk.csv) - Reference table for crosswalk/aggregation of MMWR weeks into correct reporting months.
- [Data dictionary and examples (SharePoint)](https://cste.sharepoint.com/:x:/g/EYIPI-VSAaJAqJlUfPpwoagBrjHTQaM862FGjLfhoPjXsA?e=OtN9Ql)

## Questions

For questions about these technical specifications, see the [Data Submission Guide](DATA-SUBMISSION-GUIDE.md) or contact the project team.
