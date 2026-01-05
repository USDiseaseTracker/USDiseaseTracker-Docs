# Setup Guide for US Disease Tracker Docs

This guide will help you set up and use the US Disease Tracker documentation repository.

## Prerequisites

- Git
- GitHub account

## Installation

### Clone the Repository

```bash
git clone https://github.com/USDiseaseTracker/USDiseaseTracker-Docs.git
cd USDiseaseTracker-Docs
```

## Viewing the Documentation Website

The documentation website is automatically built and deployed to GitHub Pages:

**Website URL:** https://usdiseasetracker.github.io/USDiseaseTracker-Docs/

The site is built using Jekyll and updates automatically when changes are pushed to the main branch.

## Using the Data Standards

### Viewing Standards

All data standards are located in `standards/`. Each standard document includes:

- Field definitions
- Data types and validation rules
- Examples
- Version history

### Validating Data

**Coming Soon:** Validation scripts are currently under development.

### Using Example Data

Example data files demonstrate proper formatting:

```bash
# View example using cat
cat examples/disease_tracking_report_example.csv
```

## Creating New Standards

1. **Copy the template**
   ```bash
   cp templates/standard-definition-template.md standards/my-new-standard.md
   ```

2. **Fill in the template** with your standard details

3. **Create example data** in `examples/`

4. **Update the index** in `INDEX.md`

5. **Submit a pull request**

## GitHub Actions

This repository includes a GitHub Actions workflow that automatically builds and deploys the documentation website to GitHub Pages when changes are pushed to the main branch.

## Troubleshooting

### Website Build Fails

If the GitHub Pages deployment fails:

1. Check the Actions tab in GitHub for error messages
2. Ensure `_config.yml` is valid YAML
3. Verify all markdown files are properly formatted

## Contributing

See the main [README.md](README.md) for contribution guidelines.

## Support

- [Report Issues](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/issues)
- [View Documentation](https://usdiseasetracker.github.io/USDiseaseTracker-Docs/)

## License

This project is licensed under the GNU General Public License v3.0 or later.
