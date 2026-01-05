# USDiseaseTracker-Docs

<!-- badges: start -->
[![R-CMD-check](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/workflows/R-CMD-check/badge.svg)](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/actions)
[![pkgdown](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/workflows/pkgdown/badge.svg)](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/actions)
<!-- badges: end -->

Data standards and public documentation of the US Disease Tracker project.

## Overview

This repository houses the data standards, templates, examples, and validation documentation for the US Disease Tracker project. It is structured as an R package to leverage pkgdown for documentation and provide a standardized format for data standard management.

## Repository Structure

```
USDiseaseTracker-Docs/
├── inst/
│   ├── standards/          # Data standard definitions
│   ├── templates/          # Templates for creating new standards
│   └── examples/           # Example data files
├── data-raw/              # Data validation scripts
├── vignettes/             # Documentation articles
├── man/                   # R documentation
├── .github/
│   └── workflows/         # GitHub Actions workflows
├── DESCRIPTION            # R package metadata
├── NAMESPACE              # R package namespace
└── _pkgdown.yml          # pkgdown configuration
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

Example data files are provided in `inst/examples/`:

```r
# View example case report
jsonlite::fromJSON("inst/examples/case_report_example.json")
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

1. Review existing standards in `inst/standards/`
2. Use templates from `inst/templates/` for new standards
3. Include example data in `inst/examples/`
4. Provide validation scripts in `data-raw/`
5. Submit a pull request

## Installation and Setup

While this is primarily a documentation repository, you can install it as an R package. See the [Setup Guide](SETUP.md) for detailed instructions.

```r
# install.packages("remotes")
remotes::install_github("USDiseaseTracker/USDiseaseTracker-Docs")
```

## GitHub Actions

This repository uses GitHub Actions for:

- **R-CMD-check**: Validates the R package structure across multiple platforms
- **pkgdown**: Automatically builds and deploys the documentation website

## License

This project is licensed under the GNU General Public License v3.0 or later. See [LICENSE](LICENSE) for details.
