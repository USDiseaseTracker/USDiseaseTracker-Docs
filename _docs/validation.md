---
title: Validation
permalink: /docs/validation/
---

# Validation

| Version | Changes from previous version |   
|---------|---------|
|  1.1.0 (updated 2026-01-07) | - Initial version of documentation repository |


---

The validation process checks:

- File format and structure
- Required field presence
- Data type compliance
- Valid value adherence
- Logical consistency
- Cross-field rules

Validation errors will be reported back to submitters with specific error descriptions.

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
