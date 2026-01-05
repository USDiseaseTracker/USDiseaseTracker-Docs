# USDiseaseTracker-Docs

[![Deploy GitHub Pages](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/workflows/Deploy%20GitHub%20Pages/badge.svg)](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/actions)

Data standards and public documentation of the US Disease Tracker project.

## Overview

This repository houses the data standards, templates, examples, and validation documentation for the US Disease Tracker project. It provides a centralized location for standardized formats and guidelines for disease surveillance data.

## Repository Structure

```
USDiseaseTracker-Docs/
├── standards/             # Data standard definitions
├── templates/             # Templates for creating new standards
├── examples/              # Example data files
├── data-raw/              # Data validation scripts
├── .github/
│   ├── workflows/         # GitHub Actions workflows
│   └── ISSUE_TEMPLATE/    # Issue templates
├── INDEX.md               # Comprehensive index of all standards
├── README.md              # This file
├── SETUP.md               # Setup and usage guide
├── CONTRIBUTING.md        # Contribution guidelines
└── _config.yml            # Jekyll configuration for GitHub Pages
```

## Data Standards

The repository includes the following data standards:

- **Case Reporting Standard**: Defines required and optional fields for disease case reports
- Templates for creating additional standards

See the [full documentation](https://usdiseasetracker.github.io/USDiseaseTracker-Docs/) for details.

## Quick Start

### Viewing Documentation

The documentation website is available at: https://usdiseasetracker.github.io/USDiseaseTracker-Docs/

### Using Examples

Example data files are provided in `examples/`:

```bash
# View example case report
cat examples/case_report_example.json
```

Or in R:
```r
jsonlite::fromJSON("examples/case_report_example.json")
```

### Validating Data

Validation scripts are available in `data-raw/`:

```r
# Source validation function
source("data-raw/validate_case_report.R")

# Validate your data
result <- validate_case_report(your_data)
if (result$valid) {
  message("Data is valid!")
} else {
  print(result$errors)
}
```

## Contributing

We welcome contributions to the data standards! Please see our [Contributing Guide](CONTRIBUTING.md) for detailed instructions.

Quick overview:

1. Review existing standards in `standards/`
2. Use templates from `templates/` for new standards
3. Include example data in `examples/`
4. Provide validation scripts in `data-raw/`
5. Submit a pull request

See the [Setup Guide](SETUP.md) for more information on using and contributing to this repository.

## GitHub Actions

This repository uses GitHub Actions to automatically build and deploy the documentation website to GitHub Pages whenever changes are pushed to the main branch.

## License

This project is licensed under the GNU General Public License v3.0 or later. See [LICENSE](LICENSE) for details.
