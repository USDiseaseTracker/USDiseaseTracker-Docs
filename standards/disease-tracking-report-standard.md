# Data Technical Specifications

**Version:** 1.0.0  
**Last Updated:** 2026-01-06  
**Status:** Draft

## Overview

This document provides the complete technical specifications for disease tracking data submissions to the US Disease Tracker system. These specifications define the required and optional fields, data types, valid values, and formatting requirements for submitting aggregate disease case count data.

**Important:** This is for aggregate data only. No line-level (individual case) data should be submitted.

**Note:** For high-level submission guidance including what data to submit, when to submit it, and case classification rules, see the [Data Submission Guide](../DATA-SUBMISSION-GUIDE.md).

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

## Validation

See [Validation](validation.md) for details on file and data validation.


## Example Data

Example data files are available to help understand the required format:

**In this repository:**
- [Complete example](../examples/disease_tracking_report_WA_2025-09-30.csv) - Sample data file with measles and pertussis data
- [Empty template](../templates/disease_tracking_report_{state}_{report_date}.csv) - Template file with correct structure
- [Data dictionary (CSV)](disease_tracking_data_dictionary.csv) - Reference table of all fields and valid values

**External resources:**
- [Data dictionary and additional examples (SharePoint)](https://cste.sharepoint.com/:x:/g/EYIPI-VSAaJAqJlUfPpwoagBrjHTQaM862FGjLfhoPjXsA?e=OtN9Ql) - Complete reference with field definitions and external resources

**File naming convention:**
Files should be named following the pattern:
```
disease_tracking_report_{state}_{report_date}.csv
```

Examples:
- `disease_tracking_report_WA_2025-09-30.csv` (Washington state, submitted September 30, 2025)
- `disease_tracking_report_CA_2025-10-15.csv` (California, submitted October 15, 2025)
- `disease_tracking_report_NYC_2025-11-01.csv` (New York City, submitted November 1, 2025)

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


## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-06 | Initial draft for pilot phase |

## References

- [Data Submission Guide](../DATA-SUBMISSION-GUIDE.md) - High-level guidance on what and when to submit
- [Data Transfer Guide](../DATA-TRANSFER-GUIDE.md) - Technical details on how to transfer data
- [Data dictionary (CSV)](disease_tracking_data_dictionary.csv) - Reference table of all fields and valid values
- [Validation Rules](validation.md) - Complete validation requirements
- [CSTE CCCD Guidelines](https://cdn.ymaws.com/www.cste.org/resource/resmgr/2015weston/DSWG_BestPracticeGuidelines_.pdf)
- [CSTE Residency Guidelines](https://learn.cste.org/images/dH42Qhmof6nEbdvwIIL6F4zvNjU1NzA0MjAxMTUy/Course_Content/Case_based_Surveillance_for_Syphilis/CSTE_Revised_Guidelines_for_Determining_Residency_for_Disease_Reporting_Purposes.pdf)
- [MMWR Week Calendar](https://ndc.services.cdc.gov/wp-content/uploads/MMWR-Weeks-Calendar_2024-2025.pdf)
- [Data dictionary and examples (SharePoint)](https://cste.sharepoint.com/:x:/g/EYIPI-VSAaJAqJlUfPpwoagBrjHTQaM862FGjLfhoPjXsA?e=OtN9Ql)

## Questions

For questions about these technical specifications, see the [Data Submission Guide](../DATA-SUBMISSION-GUIDE.md) or contact the project team through your jurisdiction's liaison.
