# US Disease Tracker Documentation Index

This is the comprehensive index for all data standards, templates, and examples in the US Disease Tracker documentation repository.

## Quick Links

- [Disease Tracking Report Standard](standards/disease-tracking-report-standard.md)

## Pilot Program Documentation

### For Participating Jurisdictions

1. **[Pilot Phase Overview](PILOT-OVERVIEW.md)** - Background and project information
2. **[Data Submission Guide](DATA-SUBMISSION-GUIDE.md)** - High-level overview of what and when to submit
3. **[Data Technical Specifications](standards/disease-tracking-report-standard.md)** - Detailed field requirements and valid values
4. **[Data Transfer Guide](DATA-TRANSFER-GUIDE.md)** - Technical transfer methods
5. **[Validation Rules](standards/validation.md)** - Data validation requirements

## Data Standards

### Active Standards

1. **[Data Technical Specifications](standards/disease-tracking-report-standard.md)** (v1.0.0)
   - Status: Draft
   - Last Updated: 2026-01-06
   - Complete technical specifications including field definitions, data types, and valid value sets
   - [Template file](examples-and-templates/disease_tracking_report_{state}_{report_date}.csv)
   - [Example data file](examples-and-templates/disease_tracking_report_WA_2025-09-30.csv)
2. **[Validation Rules](standards/validation.md)**
   - Comprehensive validation requirements for data submissions
   - Includes format, data type, logical, and cross-field validation

### Planned Standards

- TBD


## Examples and Templates

All example and template data files are located in the `examples-and-templates/` directory:

- [disease_tracking_report_WA_2025-09-30.csv](examples-and-templates/disease_tracking_report_WA_2025-09-30.csv) - Sample data file with measles and pertussis data from Washington state
- [disease_tracking_report_{state}_{report_date}.csv](examples-and-templates/disease_tracking_report_{state}_{report_date}.csv) - Empty template with correct field structure

## Validation Scripts

Validation scripts are coming soon. Check back for updates.

## Contributing

To contribute, Please see our [Contributing Guide](CONTRIBUTING.md) for detailed instructions.

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-05 | 0.1.0 | Initial repository setup with disease tracking report standard |

## Contact

For questions or suggestions, please [open an issue](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/issues).
