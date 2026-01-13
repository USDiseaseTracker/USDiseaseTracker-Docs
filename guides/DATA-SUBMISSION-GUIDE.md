# Data Submission Guide

| Version | Changes from previous version |   
|---------|---------|
|  1.0.0 (updated 2026-01-07) | - Initial version of documentation repository <br>- Fixed contradictions between files |


---

**Status:** Work in Progress


This guide provides detailed specifications for state, tribal, local, and territorial health departments participating in the US Disease Tracker project to contribute reportable disease count data. 

## Overview

1. [Reportable Data Specifications](#reportable-data-specifications)
2. [Data Elements](#data-elements)
3. [Data Suppression](#data-suppression)
4. [Data Format](#data-format)
5. [Metadata Requirements](#metadata-requirements)
6. [Validation](#validation)
<br>

## Reportable Data Specifications


### Time Period

**Start Date:** December 29, 2024 (start of MMWR week 1, 2025)  
**End Date:** Through present
<br>

### Time Aggregation

| Disease | Weekly | Monthly |
|---------|--------|---------|
| Measles | ✓ | ✓ |
| Pertussis | | ✓ |
| Invasive Meningococcal Disease | | ✓ |
<br>

### Confirmation Status

Required **case** confirmation status by disease:

| Disease | Confirmation Status |
|---------|-------------------|
| Measles | Confirmed only |
| Pertussis | Confirmed and probable combined |
| Invasive Meningococcal Disease | Confirmed and probable combined |
<br>


### Required Data Aggregations

Each aggregation stream should provide complete data from December 29, 2024 through the present. See [Case Classification by Time](#case-classification-by-time) below for details on assignment of cases to time periods.

#### Measles (confirmed only)
- Cases × week × jurisdiction (state, DC, NYC, or territory)
- Cases × week × sub-jurisdiction unit (county, planning area, sub-state region, etc.)
- Cases × week × jurisdiction × age group
- Cases × month × jurisdiction (state, DC, NYC, or territory)
- Cases × month × sub-jurisdiction unit (county, planning area, sub-state region, etc.)
- Cases × month × jurisdiction × age group

#### Pertussis (confirmed and probable)
- Cases × month × jurisdiction (state, DC, NYC, or territory)
- Cases × month × sub-jurisdiction unit (county, planning area, sub-state region, etc.)
- Cases × month × jurisdiction × age group

#### Invasive Meningococcal Disease (confirmed and probable)
- Cases × month × jurisdiction (state, DC, NYC, or territory)
- Cases × month × sub-jurisdiction unit (county, planning area, sub-state region, etc.)
- Cases × month × jurisdiction × age group
- Cases × month × jurisdiction × serogroup
<br>

### Reporting Frequency

Data should be reported **weekly** during non-emergency periods.

Weekly reports can follow one of two formats. In both formats, all diseases and aggregations should be included, but differ based on update frequency of monthly reporting. Choice of format is at the jurisdiction's discretion.

1. **Continuously Updated Report**
   - Includes a refresh of all historic weekly and monthly data
   - Includes the new week's data for <u>current week and month for weekly reported diseases</u>
   - Includes the new week's data for <u>current month for monthly reported diseases</u>

2. **Reporting Period Updated Report** - Full report once per month, with interim weekly reports
   - Includes a refresh of all <u>prior</u> historic weekly and monthly data
   - Includes the new week's data for <u>current week and month for weekly reported diseases</u> (must update both so totals match)
   - <u>Does not</u> include the new week's data for <u>current month for monthly reported diseases</u>
   - Includes the new month's data for monthly reported diseases <u>only when month is complete</u>

*Note: During large outbreaks or public health emergencies, more frequent updates may be requested to improve situational awareness.*
<br> <br>

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
<br>

### Data Lags and Incompleteness

- Jurisdictions should share all cases as soon as they are adjudicated as confirmed or probable
- Data from recent weeks/months may be incomplete
- The project team will clearly indicate provisional data through:
  - Dashed lines on epidemic curves
  - Asterisks and notes detailing data completeness limitations
- The project team will **not** censor data reported by jurisdictions
- All data will be displayed as reported
- The project team will work with jurisdictions to ensure completeness details are understood and portrayed correctly
<br>


### Geographic Assignment

Cases should be included in aggregated counts according to their **place of residence**, in accordance with standard epidemiologic practice in the US (see [CSTE Position Statement 11-SI-04](https://learn.cste.org/images/dH42Qhmof6nEbdvwIIL6F4zvNjU1NzA0MjAxMTUy/Course_Content/Case_based_Surveillance_for_Syphilis/CSTE_Revised_Guidelines_for_Determining_Residency_for_Disease_Reporting_Purposes.pdf)).

#### Sub-jurisdiction Reporting

Sub-jurisdiction level reporting (below state, territory, or city level) is optimal to maximize usefulness for preparedness and response.

- Each jurisdiction should decide the geographic unit to use and provide a list of geographic units as metadata
- Individual jurisdictions will work with the project team to determine geographic granularity
<br>

## Data Elements

For complete field definitions, data types, valid values, and detailed validation rules, see the [Data Technical Specifications](DATA-TECHNICAL-SPECS.md).

### Summary of Required Fields

All data submissions must include the following types of information:

- **Time fields:** When the cases occurred (report period dates and time unit)
- **Disease fields:** What disease is being reported and case confirmation status
- **Geographic fields:** Where the cases occurred (jurisdiction and geographic unit)
- **Count field:** Number of cases for this combination
- **Demographic fields:** Age group (for age-stratified aggregations)

### Summary of Optional Fields

- **disease_subtype:** For meningococcal serogroup reporting

For detailed specifications of each field including exact field names, data types, and valid value sets, see the [Data Technical Specifications](DATA-TECHNICAL-SPECS.md).
<br>


### Age Groups

Age groups are defined to be relevant to both disease epidemiology and vaccine schedules. The same age groupings are used for all diseases to simplify visualizations.

| Age Group | Description |
|-----------|-------------|
| 0-5 m | From birth up to but not including 6 months |
| 6-11 m | From 6 months up to but not including 1 year birthday |
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
<br>

### International Residents

International residents (international travelers who are not residents of the reporting jurisdiction but were identified in that jurisdiction) can be included in reported data but should be:

- Designated as "international resident" using:
  - `geo_name = "international resident"`
  - `geo_unit = "NA"`
- Excluded from jurisdiction total counts and age group stratifications
- Excluded from displayed totals, epidemic curves, etc. for the jurisdiction
<br>

## Data Suppression
<br>

### Small Count Suppression

Jurisdictions should work with the project team to ensure visualized data do not risk reidentification of individual patients. In general, jurisdictions can leverage their existing policies regarding suppression of small numerators or where underlying populations are small enough to risk reidentification. All <u>data should have suppression applied by the jurisdiction prior to submission</u>, in accordance with their institutional policies. To ensure clear understanding of the data and transparency, jurisdictions should share applicable documentation of small count suppression policies with the project team if possible. Specific reporting rules are to be followed when data are suppressed to limit uncertainty and incompleteness in the data.
<br>

### Handling Suppressed Data

To ensure total counts add to 100% of cases:

1. Cases that cannot be assigned to specific disaggregations should be aggregated in an "unspecified" category
      For example, if county counts in a week are too low to release for particular counties but for other counties are sufficient:
      - Aggregate suppressed county counts together
      - Report as `geo_name = "unspecified"`
2. Perform allocation of suppression rules and "unspecified" aggregation prior to data release
3. Share all suppression rules with the project team for accurate description/footnoting
<br>

### Measles Exception

For measles, the project team recommends **not suppressing data** as a default and releasing any cases that have already been publicly released. This is to ensure comparability with counts being produced through various "web-scraping" efforts that exist, which often capture cases reported individually through press releases. Individual requests to suppress data can be discussed with the project team.
<br>

## Data Format
<br>

### No Zero Reporting

- Report only non-zero counts
- If a jurisdiction or age group had no reported outcome during a timeframe, no entry is required
- The database system will automatically add 0s at higher spatial aggregations
<br>

### File Format

Data should be submitted in CSV format following the standard template structure. 

**Template and Example Files:**
- [Data submission template](../examples-and-templates/disease_tracking_report_{state}_{report_date}.csv) - Empty template with correct field structure
- [Example data file](../examples-and-templates/disease_tracking_report_WA_2025-09-30.csv) - Sample data demonstrating proper format

**File Submission Requirements:**
- Submit a file with all incident disease counts since December 29, 2024
- Add new rows each week/month for new cases
- Files will be date-stamped by the system for version control
- Changes to prior observation counts will be taken as revisions

**File Naming:** Jurisdictions should name files following the pattern:
```
disease_tracking_report_{state}_{report_date}.csv
```
Example: `disease_tracking_report_WA_2025-09-30.csv`

See the [Data Transfer Guide](DATA-TRANSFER-GUIDE.md) for technical details on data submission methods and the [Data Technical Specifications](DATA-TECHNICAL-SPECS.md) for complete field requirements.
<br>

## Metadata Requirements

Jurisdictions should provide metadata including:

- Date classification algorithm used (CCCD or alternative)
- List of geographic units used for reporting
- Data suppression policies and rules
- Any jurisdiction-specific notes or caveats
<br>

## Validation

All submitted data must meet validation requirements to ensure data quality and consistency.

**What is validated:**
- Field formats and data types
- Values are within acceptable ranges and valid value sets
- Logical consistency across fields
- Required fields are present

**Resources:**
- [Data Technical Specifications](DATA-TECHNICAL-SPECS.md) - Complete field definitions and valid value sets
- [Data dictionary (CSV)](../examples-and-templates/disease_tracking_data_dictionary.csv) - Reference table of all fields and valid values
- [Validation Rules](VALIDATION.md) - Comprehensive validation requirements
- [Data dictionary and examples (SharePoint)](https://cste.sharepoint.com/:x:/g/EYIPI-VSAaJAqJlUfPpwoagBrjHTQaM862FGjLfhoPjXsA?e=OtN9Ql) - External reference with detailed specifications

Values submitted must align with valid value sets. Values not in alignment may result in validation errors. The [Data Transfer Guide](DATA-TRANSFER-GUIDE.md) describes what happens when validation succeeds or fails.
<br>

## Questions

For questions about data submission requirements, contact the project team.
