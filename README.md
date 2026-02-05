# USDiseaseTracker-Docs

📖 **[View this documentation as a website](https://usdiseasetracker.github.io/USDiseaseTracker-Docs/)**

| Version | Changes from previous version |   
|---------|---------|
|  1.1.0 (updated 2026-01-07) | - Initial version of documentation repository <br>- Fixed contradictions between files |

---

## Project Goals

The goal of the US Disease Tracker project is to provide consolidated epidemiologically sound data, analytics, and insights for monitoring and responding to disease threats across the United States. To accomplish this, this project aims to produce data that are as standardized as possible, while recognizing individual variations in how and when data are collected and made available to participating health departments. 
<br>

#### ***The USDiseaseTracker-Docs repository***
This repository houses the data standards, templates, examples, and validation documentation for the US Disease Tracker project. It provides a centralized location for standardized formats and guidelines for disease surveillance data. The goal of this repository is to establish the processes, standards, and data formats that will enable construction of a consolidated database and dashboard to track infectious diseases across the US in real-time. 
<br>

While we aim to limit changes once data standards and processes are established, they may change intermittently as this project evolves. All changes will be reflected and described here.
<br>
<br>

## Quick Reference

**🛠️ Interactive Tool:**
- **[USDT Data Standards Tool](https://usdiseasetracker.github.io/USDiseaseTracker-Docs/data-standards-tool/)** - Interactive tool to explore valid data field options and generate example data

**Key Dates:**
- **Data Start:** December 29, 2024 (MMWR week 1, 2025)
- **Submission Frequency:** Weekly (preferred)

**Current Diseases Collected:**

| Disease | Time Aggregation | Confirmation Status | Outcomes |
|---------|------------------|---------------------|----------|
| Measles | Weekly | Confirmed only | Cases |
| Pertussis | Weekly | Confirmed and probable (combined) | Cases |
| Invasive Meningococcal Disease | Weekly | Confirmed and probable (combined) | Cases |

**Guides and Specifications**
1. **[Data Submission Guide](guides/DATA-SUBMISSION-GUIDE.md)** - High-level overview of what and when to submit
2. **[Data Technical Specifications](guides/DATA-TECHNICAL-SPECS.md)** - Detailed field specifications and requirements
3. **[Data Transfer Guide](guides/DATA-TRANSFER-GUIDE.md)** - Technical transfer methods
4. **[Validation Rules](guides/VALIDATION.md)** - Data validation requirements

**Templates and Examples:**
- [Data submission template](examples-and-templates/disease_tracking_report_{jurisdiction}_{report_date}.csv)
- [Example data file](examples-and-templates/disease_tracking_report_WA_2025-09-30.csv)
- [Data dictionary (CSV)](examples-and-templates/disease_tracking_data_dictionary.csv) - Reference table of all fields and valid values
- [Data dictionary and additional examples (SharePoint)](https://cste.sharepoint.com/:x:/g/EYIPI-VSAaJAqJlUfPpwoagBrjHTQaM862FGjLfhoPjXsA?e=OtN9Ql)
<br>


## Data Validation

Data are validated upon submission for completeness, format, and errors. See the [Validation Rules](guides/VALIDATION.md) for detailed validation requirements.

***Coming Soon:*** Tools to perform validation prior to submission are currently under development.
<br>
<br>


## Key Principles

#### 1. Voluntary Participation
- Provision of data is voluntary and based on individual jurisdiction capabilities and policies.

#### 2. Aggregate Data Only
- No line-level data will be collected
- Data are subject to suppression in accordance with individual jurisdiction policies, regulations, and laws
- Ensures patient privacy and minimizes reidentification risk

#### 3. Data Updates and Versioning
- Data should be updated and back-populated on a regular basis
- Records of prior versions will be maintained
- Recent data may be incomplete as investigations proceed

#### 4. Data Integrity
- We do not manipulate or suppress data once received
- Jurisdictions submit only data they are comfortable posting publicly
- Only data supplied by jurisdictions will be posted publicly

*NOTE: Data for the pilot will **not** be released publicly. Once the pilot is completed and additional states are invited to participate, the dashboard and reported data are intended to become public.*
<br>
<br>


## Repository Structure

This repository is organized as follows:

- **`webpage/`** - All website-related files (Jekyll site, published at https://usdiseasetracker.github.io/USDiseaseTracker-Docs/)
- **`guides/`** - Documentation guides (DATA-SUBMISSION-GUIDE.md, DATA-TECHNICAL-SPECS.md, etc.)
- **`examples-and-templates/`** - Data templates, examples, and the data dictionary
- **`scripts/`** - Validation scripts and schema generators

For more information about the website structure, see [webpage/README.md](webpage/README.md).
<br>
<br>


## Contributing

We welcome contributions to the data standards! Please see our [Contributing Guide](CONTRIBUTING.md) for detailed instructions.
<br>
<br>


This project is licensed under the GNU General Public License v3.0 or later. See [LICENSE](LICENSE) for details.
