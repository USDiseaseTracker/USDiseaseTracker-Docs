# Data Transfer Guide

| Version | Changes from previous version |   
|---------|---------|
|  1.0.0 (updated 2026-01-07) | - Initial version of documentation repository |


---

**Status:** Work in Progress

## Overview

This guide describes the technical methods for transferring data from participating jurisdictions to the Johns Hopkins University (JHU) project database.

- [Transfer Frequency](#transfer-frequency)
- [Transfer Methods](#transfer-methods)
- [Pilot Phase Implementation](#pilot-phase-implementation)
- [File Format Specifications](#file-format-specifications)
- [Validation](#validation)
- [Retry Policy](#retry-policy)
- [Security and Authentication](#security-and-authentication)
- [Troubleshooting](#troubleshooting)
- [Support](#support)
- [Version Control](#version-control)
- [Future Enhancements](#future-enhancements)



## Transfer Frequency

**Recommended:** Weekly

Data should be transferred to the project database on a weekly basis unless an exception has been agreed to by the project team.

### Weekly Transfer Requirements

- Submit a single file with all diseases and cases aggregated by week or month
- Use the calculated case counting date (or alternative hierarchical date)
- Update file each week with new data and changes to previous aggregate values
- If no updates are available, submit either:
  - A statement: "No data updates for this week"
  - The current file with no changes (to ensure data are not assumed missing)

### Monthly Disease Updates

For diseases reported on monthly timescales, jurisdictions can:
- Update monthly totals each week, OR
- Update month counts following completion of the reporting month

Counts will be marked as "provisional" for a specified lag period on visualizations.

### Monthly Transfer Option

Individual jurisdictions may request monthly data transfer instead of weekly. This must be discussed and agreed upon with the project team. Weekly data sharing is strongly preferred.

## Transfer Methods

The project team is working with submitting jurisdictions to provide multiple mechanisms for data transfer. During the pilot, mechanisms matching current capabilities of jurisdictions will be prioritized.

### Option 1: Manual File Upload (Web Portal)

**Best for:** Jurisdictions without automated data export capabilities

#### Process

1. User opens the USDT data upload website in a web browser
2. User logs in with credentials (includes 2-factor authentication)
3. User uploads data file
4. System validates file (format, data types, data reasonableness checks)

#### Success Scenario

- File is uploaded successfully
- Success message displayed to user
- Log entry created recording successful upload
- Email confirmation sent to jurisdiction's registered email address

#### Error Scenario

- File is not stored
- Error message displayed with description of problems
- Log entry created recording unsuccessful attempt and errors
- Email notification sent to jurisdiction's registered email address

### Option 2: Scheduled Pull by JHU (Automated)

**Best for:** Jurisdictions with existing public data portals

#### Requirements

- Jurisdiction has an existing data portal with accessible data
- Jurisdiction provides example script/documentation for data access
- Jurisdiction provides point of contact for troubleshooting

#### Process

1. JHU connects to jurisdiction's data portal on scheduled basis using provided script
2. JHU retrieves data file automatically
3. System validates file (format, data types, data reasonableness checks)

#### Success Scenario

- File retrieved and stored successfully
- Log entry created recording successful retrieval
- Email confirmation sent to jurisdiction's registered email address

#### Error Scenarios

**Connection Failure:**
- Logged to extent possible
- Log contents emailed to monitored JHU email address

**Validation Failure:**
- File not stored
- Log entry created recording unsuccessful attempt and errors
- Email notification sent to jurisdiction's registered email address

#### Implementation Notes

- Requires separate script/connector for each participating jurisdiction
- Some commonality possible if states use same data portal software (e.g., Socrata with published API)
- Each script requires ongoing maintenance
- Assumes jurisdiction has defined process and schedule for storing data in their portal

### Option 3: Scheduled Push by Jurisdiction (Automated)

**Best for:** Jurisdictions with IT capability to implement automated uploads

#### Requirements

- Jurisdiction can implement and troubleshoot provided script
- Jurisdiction has scheduling capability for automated execution
- Jurisdiction provides point of contact for coordination

#### Process

1. Jurisdiction connects to JHU portal on scheduled basis using JHU-provided script
2. Jurisdiction pushes data file to JHU's data portal
3. System validates file (format, data types, data reasonableness checks)

#### Success Scenario

- File stored successfully
- Log entry created recording successful push
- Email confirmation sent to jurisdiction's registered email address

#### Error Scenarios

**Connection Failure:**
- Jurisdiction monitors/logs connection failures
- Jurisdiction notifies JHU if warranted

**Validation Failure:**
- File not stored
- Log entry created recording unsuccessful attempt and errors
- Email notification sent to jurisdiction's registered email address

#### Implementation Notes

- Jurisdiction responsible for implementing script (with JHU support)
- Jurisdiction responsible for ongoing troubleshooting
- Jurisdiction should have automated scheduling capability
- Without automated scheduling, provides no benefit over manual upload

## Pilot Phase Implementation

For the production environment, JHU intends to provide all three transfer methods. However, the pilot timeline may not allow development of all three methods.

### Jurisdiction Input Needed

To prioritize development efforts, jurisdictions should indicate preferences for the pilot phase:

**Ranking Instructions:**
- Rank methods 1-3 based on your preference
- Omit methods that are not possible for your jurisdiction
- If only one method is possible, provide only that ranking

**Important:** These rankings are for pilot phase only. Production system will have all methods available.

### Data Portal Information

If your jurisdiction has a data portal, please provide:
- Software/platform name
- Link to developer documentation (if available)
- Point of contact for technical coordination

## File Format Specifications

### Naming Convention

Jurisdictions should name submitted files according to the following convention:

```
disease_tracking_report_{jurisdiction}_{report_date}.csv
```

Where:
- `{state}` = Two-letter state/territory code or NYC (e.g., WA, CA, NYC, PR)
- `{report_date}` = Date of submission in YYYY-MM-DD format

**Examples:**
```
disease_tracking_report_WA_2025-09-30.csv
disease_tracking_report_CA_2025-10-15.csv
disease_tracking_report_NYC_2025-11-01.csv
```

JHU may add additional metadata to filenames for internal tracking purposes (e.g., submission timestamp, username) but will preserve the original file content.

### File Content

Files should not be altered after generation. JHU will not modify file contents, only may add metadata to filenames for internal tracking.

For detailed field specifications, see the [Data Technical Specifications](DATA-TECHNICAL-SPECS.md).

### Template and Examples

Use the official data submission template and examples:
- [Empty template](../examples-and-templates/disease_tracking_report_{jurisdiction}_{report_date}.csv) - Template with correct field structure
- [Example data file](../examples-and-templates/disease_tracking_report_WA_2025-09-30.csv) - Sample data demonstrating proper format
- [Data dictionary (CSV)](../examples-and-templates/disease_tracking_data_dictionary.csv) - Reference table of all fields and valid values
- [Data dictionary and additional resources (SharePoint)](https://cste.sharepoint.com/:x:/g/EYIPI-VSAaJAqJlUfPpwoagBrjHTQaM862FGjLfhoPjXsA?e=OtN9Ql) - Complete field definitions and external resources

## Validation

### Automated Validation Checks

All submitted files undergo automated validation:

- **Format checks:** File structure, CSV formatting
- **Data type checks:** Field data types match specifications
- **Value checks:** Values within acceptable ranges/enumerations
- **Reasonableness checks:** Logical consistency (dates, counts, etc.)

See the [Validation Rules](VALIDATION.md) for detailed validation requirements.

### Validation Errors

If validation fails:
1. File is not imported into the system
2. Detailed error report is generated
3. Error report is provided to submitting user
4. Email notification sent to jurisdiction
5. Jurisdiction should correct errors and resubmit

### Validation Success

If validation succeeds:
1. File is imported into the system
2. Data becomes available for dashboard
3. Confirmation message provided to user
4. Email notification sent to jurisdiction

## Retry Policy

### Overview

The system implements automatic retry mechanisms for transient failures during data transfer. This section describes retry behavior for each transfer method and provides guidance on when manual intervention is required.

### Automatic Retry Behavior

#### Manual File Upload (Web Portal)

**Automatic Retries:** Not applicable - user initiates retry manually

**User Action Required:**
- If upload fails due to transient errors (network issues, server timeouts), users should retry the upload
- Wait 5-10 minutes before retrying if server is experiencing high load
- If errors persist after 3 attempts, contact technical support

**When NOT to Retry:**
- Validation failures (fix data errors first)
- Authentication failures (verify credentials)
- File format errors (correct file format first)

#### Scheduled Pull by JHU (Automated)

**Automatic Retries:** Yes

**Retry Configuration:**
- **Maximum attempts:** 3 retries per scheduled pull
- **Retry delay:** Exponential backoff starting at 5 minutes
  - 1st retry: 5 minutes after initial failure
  - 2nd retry: 15 minutes after 1st retry
  - 3rd retry: 30 minutes after 2nd retry
- **Total retry window:** Approximately 50 minutes

**Transient Failures (Automatic Retry):**
- Network connectivity issues
- Temporary server unavailability (HTTP 503, 504)
- DNS resolution failures
- Connection timeouts
- SSL/TLS handshake failures

**Permanent Failures (No Retry - Requires Intervention):**
- Authentication failures (HTTP 401, 403)
- Resource not found (HTTP 404)
- Validation failures in retrieved data
- Malformed response data
- Certificate validation failures

**Notifications:**
- After all retries exhausted: Email sent to jurisdiction and JHU monitoring team
- Email includes error details and timestamp of attempts
- Jurisdiction should investigate and resolve underlying issue

#### Scheduled Push by Jurisdiction (Automated)

**Automatic Retries:** Yes (if implemented in jurisdiction's script)

**Recommended Configuration:**
- **Maximum attempts:** 3 retries per scheduled push
- **Retry delay:** Exponential backoff starting at 5 minutes
  - 1st retry: 5 minutes after initial failure
  - 2nd retry: 15 minutes after 1st retry
  - 3rd retry: 30 minutes after 2nd retry

**Implementation Notes:**
- Jurisdictions implementing automated push should include retry logic in their scripts
- JHU-provided example scripts include retry functionality
- Jurisdictions using custom scripts should implement similar retry mechanisms

**Transient Failures (Should Retry):**
- Network connectivity issues
- JHU server temporarily unavailable (HTTP 503, 504)
- Connection timeouts
- Rate limiting (HTTP 429) - implement longer backoff

**Permanent Failures (Should Not Retry):**
- Authentication failures (HTTP 401, 403) - verify credentials
- Validation failures - fix data errors
- File format errors - correct file format

**Monitoring:**
- Jurisdictions should monitor their push logs for failures
- After retries exhausted, notify JHU technical support
- Maintain local logs of all transfer attempts

### Retry Best Practices

#### For Manual Uploads

1. **First Attempt Fails:**
   - Check error message for specific issue
   - For transient errors (timeouts, server errors), wait 5 minutes and retry
   - For validation errors, fix data and resubmit

2. **Second Attempt Fails:**
   - Wait 10-15 minutes before third attempt
   - Verify network connectivity
   - Check system status page (if available)

3. **Third Attempt Fails:**
   - Contact technical support with error details
   - Include timestamps and error messages from all attempts
   - Have the data file ready for troubleshooting

#### For Automated Transfers

1. **Monitor Logs:**
   - Review automated transfer logs regularly
   - Set up alerts for failed transfers
   - Track retry patterns to identify systematic issues

2. **Investigate Patterns:**
   - Multiple retries needed regularly? Investigate root cause
   - Consistent failures at same time? Check scheduled maintenance windows
   - Authentication failures? Verify credential rotation schedule

3. **Escalation:**
   - If automated retries consistently fail, escalate to technical support
   - Provide log excerpts showing failure pattern
   - Include configuration details for troubleshooting

### Rate Limiting

To ensure fair resource allocation and system stability:

**Manual Uploads:**
- Maximum 10 upload attempts per hour per jurisdiction
- Rate limit resets every hour
- Exceeding limit results in temporary 1-hour restriction

**Automated Transfers:**
- Scheduled transfers subject to jurisdiction-specific quotas
- Default: 1 transfer per 15 minutes (accounts for retries)
- Higher frequency can be negotiated with JHU team

**Rate Limit Exceeded:**
- HTTP 429 (Too Many Requests) returned
- Retry-After header indicates when to retry
- Implement exponential backoff with longer delays

### Emergency Procedures

#### Critical Data Submission

For time-sensitive data during public health emergencies:

1. **Priority Support:**
   - Contact emergency support line (contact information provided through your jurisdiction's project liaison)
   - Identify as emergency/urgent submission
   - Support team may bypass standard retry procedures

2. **Manual Override:**
   - Support team can manually process failed submissions
   - Requires coordination with jurisdiction contact
   - Used only for critical, time-sensitive data

3. **Alternative Transfer:**
   - If all automated methods fail, secure email transfer available
   - Must be encrypted and approved by JHU security team
   - Contact technical support for instructions

### Monitoring and Alerts

#### JHU Monitoring

- All transfer attempts logged and monitored
- Automated alerts for consecutive failures
- Regular reports on transfer success rates by jurisdiction

#### Jurisdiction Monitoring

**Recommended:**
- Monitor confirmation emails for successful uploads
- Track upload attempt logs (for automated transfers)
- Set up alerts for transfer failures
- Review weekly summary of transfer status

**Alert Thresholds:**
- 2 consecutive failures: Monitor situation
- 3 consecutive failures: Investigate and contact support
- Missing scheduled transfer: Verify automation is running

### Support and Escalation

**For Retry-Related Issues:**

1. **First Contact:** Technical support email/phone (see Support section)
2. **Provide:**
   - Jurisdiction identifier
   - Timestamps of all attempts
   - Error messages received
   - Transfer method used
3. **Response Time:**
   - Standard: Within 24 hours
   - Urgent/emergency: Within 2 hours

**Self-Service Resources (Planned for Future Releases):**
- System status dashboard
- Known issues page
- Automated retry log viewer

These tools are under development and will be made available as the system matures beyond the pilot phase.

## Security and Authentication

### Authentication Requirements

All data transfer methods require secure authentication:

- **Username/password** for system access
- **Two-factor authentication (2FA)** for added security
- **Secure credentials** for automated transfers (API keys, tokens)

### Data Security

- All transfers use encrypted connections (HTTPS/TLS)
- Files stored securely on JHU servers
- Access limited to authorized project team members
- Audit logs maintained for all data access

## Troubleshooting

### Common Issues

**For retry-specific guidance, see the [Retry Policy](#retry-policy) section.**

**File Upload Fails:**
- Check file format (must be CSV)
- Verify file follows template structure
- Check for special characters or encoding issues
- Ensure file size is within limits
- See [Retry Best Practices](#retry-best-practices) for manual upload retry guidance

**Validation Errors:**
- Review error message for specific issues
- Check field values against valid value sets
- Verify date formats (YYYY-MM-DD)
- Ensure required fields are populated
- **Note:** Do not retry until validation errors are fixed

**Authentication Issues:**
- Verify username and password
- Check 2FA device/app is working
- Contact JHU support for account issues
- **Note:** Authentication failures are permanent - do not retry without fixing credentials

**Automated Transfer Failures:**
- Verify network connectivity
- Check credentials/API keys are valid
- Review firewall/security settings
- Check retry logs to see if automatic retries are exhausted
- See [Retry Policy](#retry-policy) for automatic retry behavior
- Contact JHU technical support if retries are exhausted

## Support

### Technical Support

For technical issues with data transfer:
- Email: [to be provided]
- Phone: [to be provided]
- Support hours: [to be provided]

### Escalation

For urgent issues or escalation:
- Contact your jurisdiction's project liaison
- Liaison will coordinate with JHU project team

## Version Control

### Data Versioning

- Each file submission is timestamped
- Previous versions are retained
- Changes to historical data are tracked
- Revision history available for review

### Metadata Tracking

For each submission, the system records:
- Submission date/time
- Submitting jurisdiction
- Submitting user
- File name
- Validation status
- Any errors or warnings

## Future Enhancements

Post-pilot enhancements may include:

- Additional transfer methods based on jurisdiction needs
- Enhanced validation with more detailed feedback
- Real-time data quality dashboards for submitters
- Automated data quality reports
- API access for jurisdictions to retrieve their own data

## Questions

For questions about data transfer methods or technical requirements, contact the project team through your jurisdiction's liaison.
