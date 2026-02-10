# US Disease Tracker Documentation

Welcome to the US Disease Tracker Documentation site. This repository houses the data standards, templates, examples, and validation documentation for the US Disease Tracker project.

!!! info "Version"
    **Version 1.1.0** (updated 2026-02-09)
    
    - Updated version of documentation to clarify new standards 
    - Serogrouping for meningococcus: Report only at the state/reporting jurisdiction level as reporting at smaller geographies would likely lead to data suppression; report separately from age.
    - Age Groups: Reported at the state/reporting jurisdiction level; Combined the <1 year age groups (currently 0-6 months and 6-12 months) for current diseases (measles, pertussis, meningococcus) into a single “<1 year” category.
    - Removed “YTD” value as a valid option for time_unit.
    - Removed monthly aggregations; only weekly aggregation of cases by MMWR week for all diseases.
    - New value uses implemented: `total`, `unknown`, `unspecified` have specified meaning and uses, `NA` is only valid if `geo_name = "international resident"`.


---

## Project Goals

The goal of the US Disease Tracker project is to provide consolidated epidemiologically sound data, analytics, and insights for monitoring and responding to disease threats across the United States. To accomplish this, this project aims to produce data that are as standardized as possible, while recognizing individual variations in how and when data are collected and made available to participating health departments.

### The USDiseaseTracker-Docs Repository

This repository provides a centralized location for standardized formats and guidelines for disease surveillance data. The goal of this repository is to establish the processes, standards, and data formats that will enable construction of a consolidated database and dashboard to track infectious diseases across the US in real-time.

While we aim to limit changes once data standards and processes are established, they may change intermittently as this project evolves. All changes will be reflected and described here.

---

## Quick Reference

### 🛠️ Interactive Tool

- **[USDT Data Standards Tool](data-standards-tool.md)** - Interactive tool to explore valid data field options and generate example data

### 📅 Key Dates

- **Data Start:** December 29, 2024 (MMWR week 1, 2025)
- **Submission Frequency:** Weekly (preferred)

### 🦠 Current Diseases Collected

| Disease | Time Aggregation | Confirmation Status | Outcomes |
|---------|------------------|---------------------|----------|
| Measles | Weekly | Confirmed only | Cases |
| Pertussis | Weekly | Confirmed and probable (combined) | Cases |
| Invasive Meningococcal Disease | Weekly | Confirmed and probable (combined) | Cases |

### 📚 Guides and Specifications

1. **[Data Submission Guide](guides/data-submission-guide.md)** - High-level overview of what and when to submit
2. **[Data Technical Specifications](guides/data-technical-specs.md)** - Detailed field specifications and requirements
3. **[Data Transfer Guide](guides/data-transfer-guide.md)** - Technical transfer methods
4. **[Validation Rules](guides/validation.md)** - Data validation requirements
5. **[Pilot Overview](guides/pilot-overview.md)** - Overview of the pilot program

### 📄 Templates and Examples

- [Data submission template](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/blob/main/examples-and-templates/disease_tracking_report_{jurisdiction}_{report_date}.csv)
- [Example data file](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/blob/main/examples-and-templates/disease_tracking_report_WA_2025-09-30.csv)
- [Data dictionary (CSV)](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/blob/main/examples-and-templates/disease_tracking_data_dictionary.csv) - Reference table of all fields and valid values
- [Data dictionary and additional examples (SharePoint)](https://cste.sharepoint.com/:x:/g/EYIPI-VSAaJAqJlUfPpwoagBrjHTQaM862FGjLfhoPjXsA?e=OtN9Ql)

---

## Data Validation

Data are validated upon submission for completeness, format, and errors. See the [Validation Rules](guides/validation.md) for detailed validation requirements.

!!! note "Coming Soon"
    Tools to perform validation prior to submission are currently under development.

---

## Key Principles

### 1. Voluntary Participation
- Provision of data is voluntary and based on individual jurisdiction capabilities and policies.

### 2. Aggregate Data Only
- No line-level data will be collected
- Data are subject to suppression in accordance with individual jurisdiction policies, regulations, and laws
- Ensures patient privacy and minimizes reidentification risk

### 3. Data Updates and Versioning
- Data should be updated and back-populated on a regular basis
- Records of prior versions will be maintained
- Recent data may be incomplete as investigations proceed

### 4. Data Integrity
- We do not manipulate or suppress data once received
- Jurisdictions submit only data they are comfortable posting publicly
- Only data supplied by jurisdictions will be posted publicly

!!! warning "Pilot Program"
    Data for the pilot will **not** be released publicly. Once the pilot is completed and additional states are invited to participate, the dashboard and reported data are intended to become public.

---

## Repository Structure

This repository is organized as follows:

- **`guides/`** - Documentation guides (data-submission-guide.md, data-technical-specs.md, etc.)
- **`examples-and-templates/`** - Data templates, examples, and the data dictionary
- **`scripts/`** - Validation scripts and schema generators
- **`data_standards_tool/`** - Interactive data standards tool

---

## Contributing

We welcome contributions to the data standards! Please see our [Contributing Guide](CONTRIBUTING.md) for detailed instructions.

---

## License

This project is licensed under the GNU General Public License v3.0 or later. See [LICENSE](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/blob/main/LICENSE) for details.
