# Data Submission Guide

**Version:** 1.0.0  
**Last Updated:** 2026-01-06  
**Status:** Draft

## Overview

This guide provides a high-level overview of the data submission requirements for the US Disease Tracker project. For detailed technical specifications, including specific field requirements and validation rules, please refer to the [Data Technical Specifications](Data-Technical-Specifications.md).

## Purpose

The US Disease Tracker project maintains standardized data formats to ensure consistent, reliable disease surveillance across jurisdictions. This guide helps data submitters understand what information is required and how to submit it correctly.

## What Data is Required?

### Disease Tracking Reports

Disease tracking reports are the primary data submission format for the US Disease Tracker system. These reports capture essential information about disease cases including:

- **Case Identification**: Unique identifiers for each case
- **Timing Information**: When the case was reported and when symptoms began
- **Disease Information**: What disease is being reported using standard codes
- **Geographic Information**: Where the case is being reported from
- **Demographic Information**: Basic patient demographics (age, sex, race, ethnicity)
- **Clinical Information**: Hospitalization status and other health outcomes

See the [Disease Tracking Report Standard](standards/disease-tracking-report-standard.md) for specific field definitions.

## Required vs. Optional Fields

### Required Fields

All disease tracking reports **must** include:
- Case ID
- Report date
- Disease code
- Reporting jurisdiction
- Patient age
- Patient sex

Without these required fields, a report cannot be processed.

### Optional Fields

Additional fields that enhance data quality and analysis capabilities:
- Race
- Ethnicity
- Symptom onset date
- Hospitalization status

While optional, submitting these fields is strongly encouraged as they provide valuable epidemiological context.

## Data Formats

All data should be submitted following standardized formats:

- **Dates**: ISO 8601 format (YYYY-MM-DD)
- **Jurisdiction codes**: Two-letter state codes
- **Disease codes**: Must match the approved disease list
- **Demographic codes**: Standard categories as defined in the technical specifications

For complete data type definitions and validation rules, see the [Data Technical Specifications](Data-Technical-Specifications.md).

## Submission Process

### 1. Prepare Your Data

Ensure your data includes all required fields and follows the standard formats. Use the example files in the `examples/` directory as templates:

- `examples/disease_tracking_report_example.csv` - Complete example with all fields
- `examples/disease_tracking_report_minimal.csv` - Minimal example with only required fields

### 2. Validate Your Data

**Coming Soon**: Validation scripts will be available to check your data before submission.

### 3. Submit Your Data

**Coming Soon**: Submission instructions and endpoints will be provided.

## Getting Help

### Documentation Resources

- **[Data Technical Specifications](Data-Technical-Specifications.md)**: Detailed field-level specifications
- **[Disease Tracking Report Standard](standards/disease-tracking-report-standard.md)**: Current standard definition
- **[Example Data Files](examples/)**: Sample data files demonstrating compliance
- **[Templates](templates/)**: Templates for creating new standards

### Support

For questions or issues with data submission:
- Open an issue in the [GitHub repository](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/issues)
- Review the [Contributing Guide](CONTRIBUTING.md) for contribution guidelines

## Future Standards

The following data standards are planned for future development:

- **Laboratory Data Standard**: Formats for laboratory test results and interpretations
- **Demographic Data Standard**: Detailed demographic information for case tracking
- **Outbreak Investigation Standard**: Data requirements for outbreak investigations
- **Contact Tracing Standard**: Information needed for contact tracing activities

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2026-01-06 | Initial consolidated data submission guide | US Disease Tracker Team |
