# Data Standards Overview

**Last Updated:** January 5, 2026  
**Status:** Work in Progress

## Introduction

This document provides an overview of the data standards for the US Disease Data Project pilot phase. The specifications have been developed with input from the Joint Data Dashboard Steering Committee (SC) and Technical Advisory Group (TAG) to provide guidance for state, tribal, local, and territorial health departments participating in the pilot.

## Document Organization

The data standards documentation is organized into several focused documents:

### 1. [Pilot Phase Overview](../PILOT-OVERVIEW.md)
Background information about the US Disease Data Project, including:
- Project goals and principles
- Pilot scope and timeline
- Key stakeholders
- Participating diseases

### 2. [Data Submission Guide](../DATA-SUBMISSION-GUIDE.md)
Comprehensive guide for jurisdictions on submitting data, including:
- Submission frequency and requirements
- Required data aggregations by disease
- Case classification methods
- Geographic assignment rules
- Age group definitions
- Data suppression guidelines
- Metadata requirements

### 3. [Data Transfer Guide](../DATA-TRANSFER-GUIDE.md)
Technical details on data transfer methods, including:
- Transfer frequency and timing
- Manual upload via web portal
- Automated pull by JHU from jurisdiction portals
- Automated push by jurisdictions to JHU API
- File naming conventions
- Validation processes
- Security and authentication

### 4. [Disease Tracking Report Standard](disease-tracking-report-standard.md)
Detailed technical specification of the data standard, including:
- Required and optional fields
- Data types and formats
- Validation rules
- Valid value sets
- Example data
- Version history

## Quick Reference

### Key Dates
- **Data Start:** December 29, 2024 (MMWR week 1, 2025)
- **Submission Frequency:** Weekly (preferred)

### Pilot Diseases

| Disease | Time Aggregation | Confirmation Status |
|---------|------------------|---------------------|
| Measles | Weekly + Monthly | Confirmed only |
| Pertussis | Monthly | Confirmed and probable |
| Invasive Meningococcal Disease | Monthly | Confirmed and probable |

### Required Aggregations

**Measles (confirmed only):**
- Cases × week × jurisdiction
- Cases × week × sub-jurisdiction
- Cases × month × jurisdiction
- Cases × month × sub-jurisdiction
- Cases × month × jurisdiction × age group

**Pertussis (confirmed and probable):**
- Cases × month × jurisdiction
- Cases × month × sub-jurisdiction
- Cases × month × jurisdiction × age group

**Invasive Meningococcal Disease (confirmed and probable):**
- Cases × month × jurisdiction
- Cases × month × sub-jurisdiction
- Cases × month × jurisdiction × age group
- Cases × month × jurisdiction × serogroup

## Key Principles

### Data Privacy
- **Aggregate data only** - No line-level data
- Apply jurisdiction suppression policies before submission
- Use "unspecified" category to maintain totals after suppression

### Data Integrity
- JHU does not manipulate or suppress data once received
- Jurisdictions submit only data they are comfortable posting publicly
- Data clearly marked as provisional during lag periods

### Flexibility
- Voluntary participation
- Accommodates jurisdictional variations in data collection
- Regular updates and back-population supported

## Resources

### Templates and Tools
- [Data Submission Template](https://cste.sharepoint.com/:x:/g/EYIPI-VSAaJAqJlUfPpwoagBrjHTQaM862FGjLfhoPjXsA?e=2Xea8R)
- [Data Dictionary and Sample Data](https://cste.sharepoint.com/:x:/g/EYIPI-VSAaJAqJlUfPpwoagBrjHTQaM862FGjLfhoPjXsA?e=OtN9Ql)
- [MMWR Week Calendar 2024-2025](https://ndc.services.cdc.gov/wp-content/uploads/MMWR-Weeks-Calendar_2024-2025.pdf)
- [MMWR Week to Month Crosswalk](https://cste.sharepoint.com/:x:/g/EYIPI-VSAaJAqJlUfPpwoagBrjHTQaM862FGjLfhoPjXsA?rtime=8l2fm2Ig3kg&ActiveCell=MMWR%20week%20to%20month)

### Reference Documents
- [Data Dashboard Project Charter](https://cste.sharepoint.com/:w:/g/ERDgYNKaMUxNrk3eK0EZsXkB2z87SC7OVTASmf_Jk-t07Q?e=FAcBJE)
- [Joint Data Dashboard Project Technical Workgroup](https://cste.sharepoint.com/:w:/g/Eeo56Obf66dKg5RfOpE3UBEB0-Bn4wYKN8UGBvclV37jyw?e=y2dTIk)
- [CSTE CCCD Guidelines](https://cdn.ymaws.com/www.cste.org/resource/resmgr/2015weston/DSWG_BestPracticeGuidelines_.pdf)
- [CSTE Residency Guidelines](https://learn.cste.org/images/dH42Qhmof6nEbdvwIIL6F4zvNjU1NzA0MjAxMTUy/Course_Content/Case_based_Surveillance_for_Syphilis/CSTE_Revised_Guidelines_for_Determining_Residency_for_Disease_Reporting_Purposes.pdf)

## Getting Started

For jurisdictions interested in participating in the pilot:

1. Review the [Pilot Phase Overview](../PILOT-OVERVIEW.md) to understand project goals
2. Read the [Data Submission Guide](../DATA-SUBMISSION-GUIDE.md) for submission requirements
3. Review the [Disease Tracking Report Standard](disease-tracking-report-standard.md) for technical specifications
4. Consult the [Data Transfer Guide](../DATA-TRANSFER-GUIDE.md) to select a transfer method
5. Contact the project team through your jurisdiction's liaison to discuss participation

## Updates and Versioning

These standards are living documents that will be updated based on:
- Lessons learned during the pilot phase
- Feedback from participating jurisdictions
- Guidance from the Steering Committee and Technical Advisory Group
- Evolving public health needs

Check the "Last Updated" date at the top of each document for the most recent version.

## Questions and Support

For questions about the data standards or participation in the pilot, contact the project team through your jurisdiction's liaison or established communication channels.

## Document History

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-05 | 1.0.0 | Reorganized documentation into focused guides |
| 2025-10-13 | 0.1.0 | Initial draft (consolidated document) |
