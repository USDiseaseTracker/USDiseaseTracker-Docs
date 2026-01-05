# Disease Tracking Report Data Standard

**Version:** 1.0.0  
**Last Updated:** 2026-01-05  
**Status:** Draft

## Overview

This document defines the data standard for disease tracking reports in the US Disease Tracker system.

## Required Fields

| Field Name | Data Type | Description | Validation Rules |
|------------|-----------|-------------|------------------|
| case_id | String | Unique identifier for the case | Must be unique, alphanumeric |
| report_date | Date | Date the case was reported | ISO 8601 format (YYYY-MM-DD) |
| disease_code | String | Standard disease code | Must match approved disease list |
| jurisdiction | String | Reporting jurisdiction | Two-letter state code |
| age | Integer | Patient age in years | 0-120 |
| sex | String | Patient sex | M, F, U (Unknown), O (Other) |

## Optional Fields

| Field Name | Data Type | Description | Validation Rules |
|------------|-----------|-------------|------------------|
| race | String | Patient race | Standard race categories |
| ethnicity | String | Patient ethnicity | Hispanic/Non-Hispanic/Unknown |
| symptom_onset_date | Date | Date of symptom onset | ISO 8601 format |
| hospitalized | Boolean | Hospitalization status | true/false |

## Example

See `examples/disease_tracking_report_example.csv` for a complete example.

## Validation

Validation scripts are coming soon.
