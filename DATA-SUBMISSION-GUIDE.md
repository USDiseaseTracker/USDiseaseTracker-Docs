# Data Submission Guide

**Last Updated:** January 5, 2026  
**Status:** Work in Progress

## Overview

This guide provides detailed specifications for state, tribal, local, and territorial health departments participating in the US Disease Data Project pilot phase.

## Submission Summary

### Frequency
**Weekly** submission is preferred (monthly can be arranged if weekly is not possible, in coordination with the project team)

### Required Data Aggregations

Each aggregation stream should provide complete data from December 29, 2024 through the present.

#### Measles (confirmed only)
- Cases × week × jurisdiction (state, DC, NYC, or territory)
- Cases × week × sub-jurisdiction unit (county, planning area, etc.)
- Cases × month × jurisdiction (state, DC, NYC, or territory)
- Cases × month × sub-jurisdiction unit (county, planning area, etc.)
- Cases × month × jurisdiction × age group

#### Pertussis (confirmed and probable)
- Cases × month × jurisdiction (state, DC, NYC, or territory)
- Cases × month × sub-jurisdiction unit (county, planning area, etc.)
- Cases × month × jurisdiction × age group

#### Invasive Meningococcal Disease (confirmed and probable)
- Cases × month × jurisdiction (state, DC, NYC, or territory)
- Cases × month × sub-jurisdiction unit (county, planning area, etc.)
- Cases × month × jurisdiction × age group
- Cases × month × jurisdiction × serogroup

## Reportable Data Specifications

### Time Period

**Start Date:** December 29, 2024* (start of MMWR week 1, 2025)  
**End Date:** Through present

*This start date provides a reasonable baseline of data for visualization during the pilot.

### Time Aggregation

| Disease | Weekly | Monthly |
|---------|--------|---------|
| Measles | ✓ | ✓ |
| Pertussis | | ✓ |
| Invasive Meningococcal Disease | | ✓ |

Measles requires both weekly and monthly aggregation to allow for more timely updates and enhanced situational awareness.

### Reporting Frequency

Data should be reported **weekly** during non-emergency periods.

Weekly reports can follow one of two formats:

1. **Full Report** - All requested diseases aggregated by week and month
   - Includes a refresh of all historic weekly and monthly data
   - Includes the new week's data
   - May or may not include counts to date for the current month (at jurisdiction's discretion)

2. **Variable Report** - Full report once per month, with interim weekly reports
   - Full report sent once per month
   - Weekly reports include only diseases aggregated by week (i.e., measles only)

*Note: During large outbreaks or public health emergencies, more frequent updates may be requested to improve situational awareness.*

### Case Classification by Time

Cases should be classified according to a hierarchical date algorithm. 

**Recommended:** Use the **Calculated Case Counting Date (CCCD)** ([CSTE Data Standardization Guidelines](https://cdn.ymaws.com/www.cste.org/resource/resmgr/2015weston/DSWG_BestPracticeGuidelines_.pdf)).

The CCCD employs a hierarchy and assigns the case to the earliest of:
1. Symptom onset date
2. Clinical diagnosis date
3. Earliest specimen collection date associated with a positive lab result
4. Earliest result date for a positive lab result
5. Date first received by a public health agency
6. Date entered/record initiated

**Alternative:** If CCCD is not implemented, use a similar hierarchical algorithm or an existing case classification date such as Event Date in your system.

**Required:** Provide metadata on the algorithm used for each jurisdiction.

#### Time Period Assignment

- **Weekly counts:** Classify by MMWR week (see [MMWR week table](https://ndc.services.cdc.gov/wp-content/uploads/MMWR-Weeks-Calendar_2024-2025.pdf))
- **Monthly counts:** Use groupings of 4-5 corresponding MMWR weeks (see [MMWR week to month crosswalk](https://cste.sharepoint.com/:x:/g/EYIPI-VSAaJAqJlUfPpwoagBrjHTQaM862FGjLfhoPjXsA?rtime=8l2fm2Ig3kg&ActiveCell=MMWR%20week%20to%20month))
  - Month start = start of first MMWR week that includes at least four days of the new calendar month
- **Year-to-date counts:** Start of MMWR week 1 (2024-12-29) through end of last included MMWR week

### Data Lags and Incompleteness

- Jurisdictions should share all cases as soon as they are adjudicated as confirmed or probable
- Data from recent weeks/months may be incomplete
- The project team will clearly indicate provisional data through:
  - Dashed lines on epidemic curves
  - Asterisks and notes detailing data completeness limitations
- The project team will **not** censor data reported by jurisdictions
- All data will be displayed as reported
- The project team will work with jurisdictions to ensure completeness details are understood and portrayed correctly

### Confirmation Status

Required confirmation status by disease:

| Disease | Confirmation Status |
|---------|-------------------|
| Measles | Confirmed only |
| Pertussis | Confirmed and probable combined |
| Invasive Meningococcal Disease | Confirmed and probable combined |

### Geographic Assignment

Cases should be included in aggregated counts according to their **place of residence**, in accordance with standard epidemiologic practice in the US (see [CSTE Position Statement 11-SI-04](https://learn.cste.org/images/dH42Qhmof6nEbdvwIIL6F4zvNjU1NzA0MjAxMTUy/Course_Content/Case_based_Surveillance_for_Syphilis/CSTE_Revised_Guidelines_for_Determining_Residency_for_Disease_Reporting_Purposes.pdf)).

#### Sub-jurisdiction Reporting

Sub-jurisdiction level reporting (below state, territory, or city level) is optimal to maximize usefulness for preparedness and response.

- Health departments decide the geographic unit to use
- Geographic units may vary by disease
- Each jurisdiction should provide a list of geographic units as metadata
- Individual jurisdictions will work with the project team to determine geographic granularity

## Data Elements

For complete field definitions, data types, and validation rules, see the [Disease Tracking Report Standard](standards/disease-tracking-report-standard.md).

### Required Data Fields

- **Time fields:** time_unit, report_period_start, report_period_end, date_type
- **Disease fields:** disease_name, outcome, confirmation_status
- **Geographic fields:** reporting_jurisdiction, state, geo_unit, geo_name
- **Demographic fields:** age_group (for applicable aggregations)
- **Count field:** count

### Optional Data Fields

- **disease_subtype** - For meningococcal serogroup reporting

### Age Groups

Age groups are defined to be relevant to both disease epidemiology and vaccine schedules. The same age groupings are used for all diseases to simplify visualizations.

| Age Group | Description |
|-----------|-------------|
| 0-11 m | From birth up to but not including 1 year birthday |
| 1-4 y | From 1 year birthday up to but not including 5 year birthday |
| 5-11 y | From 5 year birthday up to but not including 12 year birthday |
| 12-18 y | From 12 year birthday up to but not including 19 year birthday |
| 19-22 y | From 19 year birthday up to but not including 23 year birthday |
| 23-44 y | From 23 year birthday up to but not including 45 year birthday |
| 45-64 y | From 45 year birthday up to but not including 65 year birthday |
| >=65 y | From 65 year birthday and older |
| total | Total counts, all ages |
| unknown | Counts of individuals with unknown age |

**Important:** Age groups will only be shared and displayed at the jurisdiction level, not at sub-jurisdiction level, unless otherwise agreed to by individual jurisdictions.

### International Residents

International residents (international travelers who are not residents of the reporting jurisdiction but were identified in that jurisdiction) can be included in reported data but should be:

- Designated as "international resident" using:
  - `geo_name = "international resident"`
  - `geo_unit = "NA"`
- Excluded from jurisdiction total counts and age group stratifications
- Excluded from displayed totals, epidemic curves, etc. for the jurisdiction

## Data Suppression

### Small Count Suppression

Jurisdictions should work with the project team to ensure visualized data do not risk reidentification of individual patients.

- Leverage existing jurisdiction policies regarding suppression of small numerators
- Consider underlying populations small enough to risk reidentification
- Suppress counts prior to sharing data

### Handling Suppressed Data

To ensure total counts add to 100% of cases:

1. Cases that cannot be assigned to specific disaggregations should be aggregated in an "unspecified" category
2. For example, if county counts in a week are too low to release but other counties are sufficient:
   - Aggregate suppressed county counts together
   - Report as `geo_name = "unspecified"`
3. Perform allocation prior to data release
4. Share all suppression rules with the project team for accurate description/footnoting

### Measles Exception

For measles, the project team recommends **not suppressing data** as a default and releasing any cases that have already been publicly released. Individual requests to suppress data can be discussed with the project team.

## Data Format

### No Zero Reporting

- Report only non-zero counts
- If a jurisdiction or age group had no reported outcome during a timeframe, no entry is required
- The database system will automatically add 0s at higher spatial aggregations

### File Format

Each jurisdiction will use the template provided ([download template](https://cste.sharepoint.com/:x:/g/EYIPI-VSAaJAqJlUfPpwoagBrjHTQaM862FGjLfhoPjXsA?e=2Xea8R)) to report data.

- Submit a file with all incident disease counts since December 29, 2024
- Add new rows each week/month for new cases
- Files will be date-stamped by the system for version control
- Changes to prior observation counts will be taken as revisions

See the [Data Transfer Guide](DATA-TRANSFER-GUIDE.md) for technical details on data submission methods.

## Metadata Requirements

Jurisdictions should provide metadata including:

- Date classification algorithm used (CCCD or alternative)
- List of geographic units used for reporting
- Data suppression policies and rules
- Any jurisdiction-specific notes or caveats

## Validation

Values submitted must align with valid value sets defined in the [Disease Tracking Report Standard](standards/disease-tracking-report-standard.md). Values not in alignment may result in validation errors.

See the [data dictionary and sample data file](https://cste.sharepoint.com/:x:/g/EYIPI-VSAaJAqJlUfPpwoagBrjHTQaM862FGjLfhoPjXsA?e=OtN9Ql) for complete data element definitions and valid value sets.

## Questions

For questions about data submission requirements, contact the project team through your jurisdiction's liaison.
