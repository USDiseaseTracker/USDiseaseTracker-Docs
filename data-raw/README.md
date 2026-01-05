# Data Validation Scripts

This directory contains scripts for validating data against the defined standards.

## Available Validation Scripts

### validate_case_report.R
Validates case report data against the case reporting standard.

## Planned Validation Scripts

- validate_lab_data.R - For laboratory data (when standard is completed)
- validate_demographic_data.R - For demographic data (when standard is completed)

## Usage

```r
# Source the validation script
source("data-raw/validate_case_report.R")

# Validate a data file
result <- validate_case_report("path/to/data.json")

# Check validation results
if (result$valid) {
  message("Data is valid!")
} else {
  print(result$errors)
}
```

## Adding New Validation Scripts

1. Create a new R script in this directory
2. Follow the naming convention: `validate_[standard_name].R`
3. Include clear documentation and examples
4. Test thoroughly before committing
