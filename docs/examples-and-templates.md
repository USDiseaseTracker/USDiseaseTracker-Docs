# Examples & Templates

This section provides templates, examples, and reference materials to help you prepare and submit data.

## Data Templates

### CSV Submission Template

The standard template for submitting disease tracking data:

**📄 [disease_tracking_report_{jurisdiction}_{report_date}.csv](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/blob/main/examples-and-templates/disease_tracking_report_{jurisdiction}_{report_date}.csv)**

This template includes:
- All required column headers
- Placeholder values showing the expected format
- Comments explaining each field

### Example Data File

A complete example showing real data submission:

**📄 [disease_tracking_report_WA-EXAMPLE_2026-02-09.csv](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/blob/main/examples-and-templates/disease_tracking_report_WA-EXAMPLE_2026-02-09.csv)**

This example demonstrates:
- Proper formatting for each field
- Multiple disease entries
- Different stratification levels
- Age group and demographic data
- Suppressed data handling

## Reference Materials

### Data Dictionary

The comprehensive data dictionary defines all fields and their valid values:

**📄 [disease_tracking_data_dictionary.csv](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/blob/main/examples-and-templates/disease_tracking_data_dictionary.csv)**

The data dictionary includes:
- Field names and descriptions
- Data types and formats
- Valid values for each field
- Required vs. optional fields
- Validation rules

### MMWR Week Crosswalk

A reference table mapping MMWR weeks to calendar months:

**📄 [MMWR_week_to_month_crosswalk.csv](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/blob/main/examples-and-templates/MMWR_week_to_month_crosswalk.csv)**

This crosswalk helps you:
- Convert between MMWR weeks and calendar dates
- Understand week boundaries (Sunday to Saturday)
- Plan your reporting schedule

## Schema Files

### JSON Schema

The formal JSON schema defining the data structure:

**📄 [data_reporting_schema.json](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/blob/main/examples-and-templates/data_reporting_schema.json)**

Use this schema for:
- Automated validation
- Integration with validation tools
- Understanding field relationships
- Building your own tools

### Python Schema

The Python Pydantic schema used for validation:

**📄 [data_reporting_schema.py](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/blob/main/examples-and-templates/data_reporting_schema.py)**

This schema includes:
- Field definitions with types
- Validation logic
- Custom validators
- Helper functions

## Additional Resources

### SharePoint Data Dictionary

An enhanced version of the data dictionary with additional examples:

**🔗 [Data Dictionary and Examples (SharePoint)](https://cste.sharepoint.com/:x:/g/EYIPI-VSAaJAqJlUfPpwoagBrjHTQaM862FGjLfhoPjXsA?e=OtN9Ql)**

This SharePoint resource provides:
- Extended examples
- Additional use cases
- Collaborative updates
- Supplementary documentation

## How to Use These Resources

1. **Start with the Template**: Download the CSV template to understand the structure
2. **Review the Example**: Look at the example data file to see proper formatting
3. **Consult the Data Dictionary**: Use this as your primary reference for field specifications
4. **Validate with Schema**: Use the JSON or Python schema to validate your data
5. **Check MMWR Crosswalk**: Reference this when converting dates to MMWR weeks

## Related Guides

- [Data Technical Specifications](guides/data-technical-specs.md) - Detailed field requirements
- [Data Submission Guide](guides/data-submission-guide.md) - Submission process
- [Validation Rules](guides/validation.md) - Validation requirements
- [Data Standards Tool](data-standards-tool.md) - Interactive tool

---

For questions about templates or examples, please see our [Contributing Guide](CONTRIBUTING.md).
