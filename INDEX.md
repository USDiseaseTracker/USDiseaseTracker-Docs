# US Disease Tracker Documentation Index

This is the comprehensive index for all data standards, templates, and examples in the US Disease Tracker documentation repository.

## Quick Links

- [Getting Started Guide](SETUP.md)
- [Pilot Phase Overview](PILOT-OVERVIEW.md)
- [Data Submission Guide](DATA-SUBMISSION-GUIDE.md)
- [Data Transfer Guide](DATA-TRANSFER-GUIDE.md)
- [Data Standards Overview](standards/data-standards.md)
- [Disease Tracking Report Standard](standards/disease-tracking-report-standard.md)
- [Standard Definition Template](templates/standard-definition-template.md)

## Pilot Program Documentation

### For Participating Jurisdictions

1. **[Pilot Phase Overview](PILOT-OVERVIEW.md)** - Background and project information
2. **[Data Submission Guide](DATA-SUBMISSION-GUIDE.md)** - How to prepare and submit data
3. **[Data Transfer Guide](DATA-TRANSFER-GUIDE.md)** - Technical transfer methods
4. **[Data Standards Overview](standards/data-standards.md)** - Overview of all standards documentation

## Data Standards

### Active Standards

1. **[Disease Tracking Report Standard](standards/disease-tracking-report-standard.md)** (v1.0.0)
   - Status: Draft
   - Last Updated: 2026-01-05
   - Defines required and optional fields for aggregate disease tracking reports
   - [Example Data](examples/disease_tracking_report_example.csv)
   - Validation: Coming Soon

### Planned Standards

- Laboratory Data Standard
- Demographic Data Standard
- Outbreak Investigation Standard
- Contact Tracing Standard

## Templates

- **[Standard Definition Template](templates/standard-definition-template.md)**
  - Use this template to create new data standard documents
  - Includes all required sections for a complete standard definition

## Examples

All example data files are located in the `examples/` directory:

- [disease_tracking_report_example.csv](examples/disease_tracking_report_example.csv) - Complete disease tracking report with all fields
- [disease_tracking_report_minimal.csv](examples/disease_tracking_report_minimal.csv) - Minimal valid disease tracking report

## Validation Scripts

Validation scripts are coming soon. Check the `data-raw/` directory for updates.

## Contributing

To contribute a new data standard:

1. Copy the [standard definition template](templates/standard-definition-template.md)
2. Fill in all required sections
3. Create example data files in `examples/`
4. Create a validation script in `data-raw/`
5. Update this index
6. Submit a pull request

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-05 | 0.1.0 | Initial repository setup with disease tracking report standard |

## Contact

For questions or suggestions, please [open an issue](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/issues).
