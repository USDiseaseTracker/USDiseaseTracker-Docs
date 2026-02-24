---
title: Validation
permalink: /docs/validation/
---

# Validation

!!! info "**Version 1.1.0** (updated 2026-02-09)"
    
    - Updated version of documentation to clarify new standards 
    - Serogrouping for meningococcus: Report only at the state/reporting jurisdiction level as reporting at smaller geographies would likely lead to data suppression; report separately from age.
    - Age Groups: Reported at the state/reporting jurisdiction level; Combined the <1 year age groups (currently 0-6 months and 6-12 months) for current diseases (measles, pertussis, meningococcus) into a single “<1 year” category.
    - Removed “YTD” value as a valid option for time_unit.
    - Removed monthly aggregations; only weekly aggregation of cases by MMWR week for all diseases.
    - New value uses implemented: `total`, `unknown`, `unspecified` have specified meaning and uses, `NA` is only valid if `geo_name = "international resident"`.


---

The validation process checks:

- File format and structure
- Required field presence
- Data type compliance
- Valid value adherence
- Logical consistency
- Cross-field rules

Validation errors will be reported back to submitters with specific error descriptions.

<br>

## Validation Rules

### Format Validation

- File must be valid CSV format
- Required fields must be present in all rows
- Field names must match specification exactly (case-sensitive)

### Data Type Validation

- Dates must be in YYYY-MM-DD format
- Counts must be positive integers
- String fields must use exact valid values (case-sensitive)

### Logical Validation

- `report_period_end` must be after `report_period_start`
- Date ranges must align with MMWR week boundaries
- Geographic units must be consistent with reporting jurisdiction
- Age group required for age-stratified aggregations
- Disease subtype only valid for applicable diseases

### Cross-Field Validation

- Measles confirmation_status must be `confirmed`
- Pertussis and meningococcus confirmation_status must be `confirmed and probable`
- All diseases require weekly time_unit submissions
