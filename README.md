# USDiseaseTracker-Docs

[![Deploy GitHub Pages](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/workflows/Deploy%20GitHub%20Pages/badge.svg)](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/actions)

This repository houses the data standards, templates, examples, and validation documentation for the US Disease Tracker project. It provides a centralized location for standardized formats and guidelines for disease surveillance data.

The documentation website is available at: <a href="https://usdiseasetracker.github.io/USDiseaseTracker-Docs/" target="_blank">USDiseaseTracker.GitHub.io/USDiseaseTracker-Docs</a>


## Project Goals

The goal of this project is establish the processes, standards, data formats and build a preliminary database and dashboard, with the aim of producing epidemiologically sound data that is as standardized as possible, while recognizing individual variations in how and when data are collected and made available to participating health departments. Some differences can be accommodated during the pilot phase.


## Program Documentation

For jurisdictions participating or interested in participating, the following pages provide detailed information about the project, data formatting and standards, and how to submit data:

1. **[Pilot Phase Overview](PILOT-OVERVIEW.md)** - Background and project information
2. **[Data Submission Guide](DATA-SUBMISSION-GUIDE.md)** - High-level overview of what and when to submit
3. **[Data Technical Specifications](standards/disease-tracking-report-standard.md)** - Detailed field specifications and requirements
4. **[Data Transfer Guide](DATA-TRANSFER-GUIDE.md)** - Technical transfer methods
5. **[Validation Rules](standards/validation.md)** - Data validation requirements

See also:
- **[Data Standards Overview](standards/data-standards.md)** - Quick reference and navigation guide


## Examples and Templates

- **Example data:** See `examples/` directory
  - [disease_tracking_report_WA_2025-09-30.csv](examples/disease_tracking_report_WA_2025-09-30.csv) - Sample data file with measles and pertussis data
- **Templates:** See `templates/` directory
  - [disease_tracking_report_{state}_{report_date}.csv](templates/disease_tracking_report_{state}_{report_date}.csv) - Empty template with correct field structure
- **Data dictionary:**
  - [disease_tracking_data_dictionary.csv](standards/disease_tracking_data_dictionary.csv) - Reference table of all fields and valid values
- **External resources:**
  - [Data dictionary and additional examples (SharePoint)](https://cste.sharepoint.com/:x:/g/EYIPI-VSAaJAqJlUfPpwoagBrjHTQaM862FGjLfhoPjXsA?e=OtN9Ql)


## Data Validation

Data are validated upon submission for completeness, format, and errors. See the [Validation Rules](standards/validation.md) for detailed validation requirements.

***Coming Soon:*** Tools to perform validation prior to submission are currently under development.


## Key Principles

#### 1. Voluntary Participation
- Provision of data is voluntary and based on individual jurisdiction capabilities and policies.

#### 2. Aggregate Data Only
- No line-level data will be collected
- Data are subject to suppression in accordance with individual jurisdiction policies, regulations, and laws
- Ensures patient privacy and minimizes reidentification risk

#### 3. Data Updates and Versioning
- Data should be updated and back-populated on a regular basis
- Records of prior versions will be maintained
- Recent data may be incomplete as investigations proceed

#### 4. Data Integrity
- We do not manipulate or suppress data once received
- Jurisdictions submit only data they are comfortable posting publicly
- Only data supplied by jurisdictions will be posted publicly

*NOTE: Data for the pilot will **not** be released publicly. Once the pilot is completed and additional states are invited to participate, the dashboard and reported data are intended to become public.*


## Contributing

We welcome contributions to the data standards! Please see our [Contributing Guide](CONTRIBUTING.md) for detailed instructions.


This project is licensed under the GNU General Public License v3.0 or later. See [LICENSE](LICENSE) for details.
