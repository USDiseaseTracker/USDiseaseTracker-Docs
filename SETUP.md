# Setup Guide for US Disease Tracker Docs

This guide will help you set up and use the US Disease Tracker documentation repository.

## Prerequisites

- R (>= 4.0.0)
- Git
- GitHub account

## Installation

### Option 1: Install as an R Package

```r
# Install from GitHub
install.packages("remotes")
remotes::install_github("USDiseaseTracker/USDiseaseTracker-Docs")
```

### Option 2: Clone the Repository

```bash
git clone https://github.com/USDiseaseTracker/USDiseaseTracker-Docs.git
cd USDiseaseTracker-Docs
```

## Building the Documentation Website

The repository uses `pkgdown` to generate a documentation website. To build it locally:

```r
# Install pkgdown if you haven't already
install.packages("pkgdown")

# Build the site
pkgdown::build_site()

# Preview the site
pkgdown::preview_site()
```

The site will be built in the `docs/` directory and automatically deployed to GitHub Pages when changes are pushed to the main branch.

## Using the Data Standards

### Viewing Standards

All data standards are located in `inst/standards/`. Each standard document includes:

- Field definitions
- Data types and validation rules
- Examples
- Version history

### Validating Data

Use the validation scripts in `data-raw/`:

```r
# Source the validation function
source("data-raw/validate_case_report.R")

# Load your data
my_data <- list(
  case_id = "CASE-2026-001-TX",
  report_date = "2026-01-05",
  disease_code = "COVID-19",
  jurisdiction = "TX",
  age = 42,
  sex = "F"
)

# Validate
result <- validate_case_report(my_data)

if (result$valid) {
  message("Data is valid!")
} else {
  print(result$errors)
}
```

### Using Example Data

Example data files demonstrate proper formatting:

```r
# Read example using jsonlite
library(jsonlite)
example <- fromJSON("inst/examples/case_report_example.json")
```

## Creating New Standards

1. **Copy the template**
   ```bash
   cp inst/templates/standard-definition-template.md inst/standards/my-new-standard.md
   ```

2. **Fill in the template** with your standard details

3. **Create example data** in `inst/examples/`

4. **Create a validation script** in `data-raw/`

5. **Update the index** in `inst/INDEX.md`

6. **Submit a pull request**

## GitHub Actions

This repository includes two GitHub Actions workflows:

### R-CMD-check

Runs on every push and pull request to validate the R package structure across multiple platforms (Ubuntu, macOS, Windows) and R versions.

### pkgdown

Automatically builds and deploys the documentation website to GitHub Pages when changes are pushed to the main branch.

## Troubleshooting

### Package Check Fails

If `R CMD check` fails:

1. Make sure all required fields in `DESCRIPTION` are filled
2. Ensure all examples in documentation are valid
3. Check that all dependencies are listed

### Website Build Fails

If `pkgdown::build_site()` fails:

1. Install all suggested packages: `install.packages(c("knitr", "rmarkdown"))`
2. Check that `_pkgdown.yml` is valid YAML
3. Ensure vignettes build correctly

### Validation Script Issues

If validation scripts don't work:

1. Check that the script is properly sourced
2. Ensure data is in the correct format (list or data frame)
3. Verify required fields match the standard

## Contributing

See the main [README.md](README.md) for contribution guidelines.

## Support

- [Report Issues](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/issues)
- [View Documentation](https://usdiseasetracker.github.io/USDiseaseTracker-Docs/)

## License

This project is licensed under the GNU General Public License v3.0 or later.
