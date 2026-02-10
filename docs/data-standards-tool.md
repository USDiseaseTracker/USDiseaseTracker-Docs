# Data Standards Tool

The USDT Data Standards Tool is an interactive web application that helps you explore valid data field options and generate example data for submission.

## Access the Tool

<div style="text-align: center; margin: 2em 0;">
    <a href="../data-standards-tool.html" style="display: inline-block; padding: 12px 24px; background-color: #009688; color: white; text-decoration: none; border-radius: 4px; font-weight: bold;">
        🛠️ Open Data Standards Tool
    </a>
</div>

## Features

- **Explore Valid Options**: View all valid values for each data field
- **Interactive Form**: Select values interactively to see how they work together
- **Generate Example Data**: Create example CSV records based on your selections
- **Validation Rules**: See validation rules applied to each field
- **Export Examples**: Download example data in the correct format

## How to Use

1. **Select a Disease**: Choose the disease you want to report data for
2. **Choose Time Period**: Select the MMWR week for your report
3. **Fill in Data Fields**: Enter or select values for each required field
4. **Review Validation**: Check that your data meets all validation rules
5. **Generate Example**: Click to generate example CSV data

## Field Specifications

The tool includes all valid options for:

- **Diseases**: Measles, Pertussis, Invasive Meningococcal Disease
- **Jurisdictions**: All US states and territories
- **Time Periods**: MMWR weeks from 2025 onwards
- **Age Groups**: Standard age group categories
- **Demographics**: Sex, race, and ethnicity categories
- **Geographic Levels**: State and county level reporting

## Validation

The tool applies the same validation rules used in the actual data submission process:

- Required fields must be filled
- Values must match allowed options
- MMWR week validation
- Stratification requirements

## Related Resources

- [Data Technical Specifications](guides/data-technical-specs.md) - Detailed field specifications
- [Validation Rules](guides/validation.md) - Complete validation requirements
- [Data Submission Guide](guides/data-submission-guide.md) - Submission process overview

---

*Note: The Data Standards Tool is designed to help you understand the data requirements. For actual data submission, please follow the procedures outlined in the [Data Transfer Guide](guides/data-transfer-guide.md).*
