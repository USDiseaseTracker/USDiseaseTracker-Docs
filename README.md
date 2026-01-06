# USDiseaseTracker-Docs

[![Deploy GitHub Pages](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/workflows/Deploy%20GitHub%20Pages/badge.svg)](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/actions)

Data standards and public documentation of the US Disease Tracker project.

## Overview

This repository houses the data standards, templates, examples, and validation documentation for the US Disease Tracker project. It provides a centralized location for standardized formats and guidelines for disease surveillance data.

## Data Standards

The repository includes the following data standards:

- **Disease Tracking Report Standard**: Defines required and optional fields for disease tracking reports
- Templates for creating additional standards

See the [full documentation](https://usdiseasetracker.github.io/USDiseaseTracker-Docs/) for details.

## Quick Start

### Viewing Documentation

The documentation website is available at: https://usdiseasetracker.github.io/USDiseaseTracker-Docs/

### Using Examples

Example data files are provided in `examples/`:

```bash
# View example disease tracking report
cat examples/disease_tracking_report_example.csv
```

### Validating Data

**Coming Soon:** Validation scripts are currently under development.

## Contributing

We welcome contributions to the data standards! Please see our [Contributing Guide](CONTRIBUTING.md) for detailed instructions.

Quick overview:

1. Review existing standards in `standards/`
2. Use templates from `templates/` for new standards
3. Include example data in `examples/`
4. Submit a pull request

## GitHub Actions

This repository uses GitHub Actions to automatically build and deploy the documentation website to GitHub Pages whenever changes are pushed to the main branch.

## License

This project is licensed under the GNU General Public License v3.0 or later. See [LICENSE](LICENSE) for details.
