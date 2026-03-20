# USDiseaseTracker-Docs

📖 **[View this documentation as a website](https://usdiseasetracker.github.io/USDiseaseTracker-Docs/)**

**Version 1.1.0 (updated 2026-02-09)**
    
    - Updated version of documentation to clarify new standards 
    - Serogrouping for meningococcus: Report only at the state/reporting jurisdiction level as reporting at smaller geographies would likely lead to data suppression; report separately from age.
    - Age Groups: Reported at the state/reporting jurisdiction level; Combined the <1 year age groups (currently 0-6 months and 6-12 months) for current diseases (measles, pertussis, meningococcus) into a single “<1 year” category.
    - Removed “YTD” value as a valid option for `time_unit`.
    - Removed monthly aggregations; only weekly aggregation of cases by MMWR week for all diseases.
    - New value uses implemented: `total`, `unknown`, `unspecified` have specified meaning and uses, `NA` is only valid if `geo_name = "international resident"`.


---

## About This Project 

The goal of the US Disease Tracker project is to provide consolidated epidemiologically sound data, analytics, and insights for monitoring and responding to disease threats across the United States. This project aims to produce data that are as standardized as possible, while recognizing individual variations in how and when data are collected and made available to participating health departments. 
<br>

#### ***The USDiseaseTracker-Docs Repository***
This repository houses the data standards, templates, examples, and validation documentation for the US Disease Tracker project. It provides a centralized location for standardized formats and guidelines for disease surveillance data. The goal of this repository is to establish the processes, standards, and data formats that will enable construction of a consolidated database and dashboard to track infectious diseases across the US in real-time. 
<br>

While we aim to limit changes once data standards and processes are established, they may change intermittently as this project evolves. All changes will be reflected and described here.
<br>
<br>

This repository is organized as follows:

- **`guides/`** - Documentation guides on data submission, technical specifications, data transfer, and data validation
- **`examples-and-templates/`** - Submission templates, examples, and the data dictionary
- **`data_standards_tool/`** - Interactive data standards tool
- **`scripts/`** - Validation scripts and schema generators
- **`docs/`** - MkDocs documentation source files (website content)
<br>

Our **Key Principles** are:
1. Provision of data is voluntary.
2. Only aggregate data will be collected to minimize the risk of reidentification.
3. Data should be updated and back-populated on a regular basis, acknowledging that recent data may be incomplete as investigations proceed. Records of prior versions will be maintained.
4. We do not suppress (except in accordance with individual jurisdiction policies, regulations, or laws) or manipulate data once received; jurisdictions should submit only data they are comfortable posting publicly.

*NOTE: Data for the pilot will **not** be released publicly. Once the pilot is completed and additional states are invited to participate, the dashboard and reported data are intended to become public.*

<br>

## Quick Reference

**🛠️ Interactive Tool:**
- ***NEW!!!*** **[USDT Data Standards Tool](https://usdiseasetracker.github.io/USDiseaseTracker-Docs/data-standards-tool/)** - Interactive tool to explore valid data field options and generate example data

**Key Dates:**
- **Data Start:** December 29, 2024 (MMWR week 1, 2025)
- **Submission Frequency:** Weekly (preferred)

**Current Diseases Collected:**

| Disease | Time Aggregation | Confirmation Status | Outcomes | Age groups | Disease Subtypes |
|---------|------------------|---------------------|----------|------------|------------------|
| Measles | Weekly | Confirmed only | Cases | *multiple* | *not collected* |
| Pertussis | Weekly | Confirmed and probable (combined) | Cases | *multiple* | *not collected* |
| Invasive Meningococcal Disease | Weekly | Confirmed and probable (combined) | Cases | *multiple* | *collected* |

**Guides and Specifications**
1. **[Data Submission Guide](guides/data-submission-guide.md)** - High-level overview of what and when to submit
2. **[Data Technical Specifications](guides/data-technical-specs.md)** - Detailed field specifications and requirements
3. **[Data Transfer Guide](guides/data-transfer-guide.md)** - Technical transfer methods
4. **[Validation Rules](guides/validation.md)** - Data validation requirements

**Templates and Examples:**
- [Data submission template](examples-and-templates/disease_tracking_report_{jurisdiction}_{report_date}.csv)
- [Example data file](examples-and-templates/disease_tracking_report_CA-EXAMPLE_2026-02-09.csv)
- [Data dictionary (CSV)](examples-and-templates/disease_tracking_data_dictionary.csv) - Reference table of all fields and valid values
<br>


## Data Validation

Data are validated upon submission for completeness, format, and errors. See the [Validation Rules](guides/validation.md) for detailed validation requirements. Data can be submitted to the dashboard at any time to check the validation.

To check what combinations of values are valid, check out the [USDT Data Standards Tool](https://usdiseasetracker.github.io/USDiseaseTracker-Docs/data-standards-tool/).

<br>
<br>

## Repository Structure

This repository is organized as follows:

- **`guides/`** - Documentation guides (data-submission-guide.md, data-technical-specs.md, etc.)
- **`examples-and-templates/`** - Data templates, examples, and the data dictionary
- **`data_standards_tool/`** - Interactive data standards tool
- **`scripts/`** - Validation scripts and schema generators
- **`docs/`** - MkDocs documentation source files (website content)
<br>
<br>

## Contributing

We welcome new jurisdictions to contribute data! Please see our [Contributing Guide](CONTRIBUTING.md) for detailed instructions.
<br>
<br>


This project is licensed under the GNU General Public License v3.0 or later. See [LICENSE](LICENSE) for details.
