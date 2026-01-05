# US Disease Tracker Documentation Index

This is the comprehensive index for all data standards, templates, and examples in the US Disease Tracker documentation repository.

## Quick Links

- [Getting Started Guide](SETUP.md)
- [Case Reporting Standard](standards/case-reporting-standard.md)
- [Standard Definition Template](templates/standard-definition-template.md)

## Data Standards

### Active Standards

1. **[Case Reporting Standard](standards/case-reporting-standard.md)** (v1.0.0)
   - Status: Draft
   - Last Updated: 2026-01-05
   - Defines required and optional fields for disease case reports
   - [Example Data](examples/case_report_example.json)
   - [Validation Script](data-raw/validate_case_report.R)

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

- [case_report_example.json](examples/case_report_example.json) - Complete case report with all fields
- [case_report_minimal.json](examples/case_report_minimal.json) - Minimal valid case report

## Validation Scripts

Validation scripts are available in the `data-raw/` directory:

- [validate_case_report.R](../data-raw/validate_case_report.R) - Validates case report data

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
| 2026-01-05 | 0.1.0 | Initial repository setup with case reporting standard |

## Contact

For questions or suggestions, please [open an issue](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/issues).
