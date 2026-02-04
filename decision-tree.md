---
layout: default
title: USDT Data Standards Tool
---

# USDT Data Standards Tool

This tool helps you understand the valid data options for disease tracking submissions. Select values from the dropdowns to see which options are available for other fields based on the validation rules.

<div id="decision-tree-container">
  <style>
    .field-group {
      margin: 20px 0;
      padding: 15px;
      background-color: #f5f5f5;
      border-radius: 5px;
      border-left: 4px solid #159957;
    }
    
    .field-group label {
      display: block;
      font-weight: bold;
      margin-bottom: 5px;
      color: #333;
    }
    
    .field-group select {
      width: 100%;
      padding: 8px;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 14px;
      background-color: white;
    }
    
    .field-group select:disabled {
      background-color: #e9ecef;
      cursor: not-allowed;
    }
    
    .field-group input {
      width: 100%;
      padding: 8px;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 14px;
    }
    
    .field-help {
      margin-top: 5px;
      font-size: 12px;
      color: #666;
      font-style: italic;
    }
    
    .info-box {
      margin: 20px 0;
      padding: 15px;
      background-color: #d1ecf1;
      border-left: 4px solid #0c5460;
      border-radius: 5px;
    }
    
    .info-box h4 {
      margin-top: 0;
      color: #0c5460;
    }
    
    .example-value {
      font-family: monospace;
      background-color: #fff;
      padding: 2px 6px;
      border-radius: 3px;
      border: 1px solid #ddd;
    }
    
    .reset-button {
      margin: 20px 0;
      padding: 10px 20px;
      background-color: #159957;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 14px;
    }
    
    .reset-button:hover {
      background-color: #138f4f;
    }
  </style>

  <div class="info-box">
    <h4>How to Use This Tool</h4>
    <p>Start by selecting a disease from the dropdown below. Based on your selection, the tool will automatically update the available options for other fields according to the validation rules. Fields marked with an asterisk (*) are required.</p>
  </div>

  <button class="reset-button" onclick="resetForm()">Reset All Selections</button>

  <div class="field-group">
    <label for="disease_name">Disease Name *</label>
    <select id="disease_name" onchange="updateFields()">
      <option value="">-- Select a disease --</option>
      <option value="measles">measles</option>
      <option value="pertussis">pertussis</option>
      <option value="meningococcus">meningococcus</option>
    </select>
    <div class="field-help">The disease being reported</div>
  </div>

  <div class="field-group">
    <label for="time_unit">Time Unit *</label>
    <select id="time_unit" onchange="updateFields()">
      <option value="">-- Select time unit --</option>
    </select>
    <div class="field-help">Time aggregation unit for the report period</div>
  </div>

  <div class="field-group">
    <label for="confirmation_status">Confirmation Status *</label>
    <select id="confirmation_status" onchange="updateFields()">
      <option value="">-- Select confirmation status --</option>
    </select>
    <div class="field-help">Case confirmation level</div>
  </div>

  <div class="field-group">
    <label for="disease_subtype">Disease Subtype</label>
    <select id="disease_subtype" onchange="updateFields()">
      <option value="">-- Select disease subtype --</option>
    </select>
    <div class="field-help">Subtype of the disease (e.g., meningococcal serogroup). Use 'total' for non-subtype-stratified aggregations</div>
  </div>

  <div class="field-group">
    <label for="outcome">Outcome *</label>
    <select id="outcome" onchange="updateFields()">
      <option value="">-- Select outcome --</option>
      <option value="cases">cases</option>
      <option value="hospitalizations">hospitalizations</option>
      <option value="deaths">deaths</option>
    </select>
    <div class="field-help">Type of outcome being reported (currently only "cases" is accepted for pilot)</div>
  </div>

  <div class="field-group">
    <label for="date_type">Date Type *</label>
    <select id="date_type" onchange="updateFields()">
      <option value="">-- Select date type --</option>
      <option value="cccd">cccd</option>
      <option value="jurisdiction date hierarchy">jurisdiction date hierarchy</option>
    </select>
    <div class="field-help">Method used to assign cases to reporting periods (CCCD = Calculated Case Counting Date)</div>
  </div>

  <div class="field-group">
    <label for="state">State *</label>
    <select id="state" onchange="updateFields()">
      <option value="">-- Select state --</option>
      <option value="AL">AL - Alabama</option>
      <option value="AK">AK - Alaska</option>
      <option value="AZ">AZ - Arizona</option>
      <option value="AR">AR - Arkansas</option>
      <option value="AS">AS - American Samoa</option>
      <option value="CA">CA - California</option>
      <option value="CO">CO - Colorado</option>
      <option value="CT">CT - Connecticut</option>
      <option value="DE">DE - Delaware</option>
      <option value="DC">DC - District of Columbia</option>
      <option value="FL">FL - Florida</option>
      <option value="GA">GA - Georgia</option>
      <option value="GU">GU - Guam</option>
      <option value="HI">HI - Hawaii</option>
      <option value="ID">ID - Idaho</option>
      <option value="IL">IL - Illinois</option>
      <option value="IN">IN - Indiana</option>
      <option value="IA">IA - Iowa</option>
      <option value="KS">KS - Kansas</option>
      <option value="KY">KY - Kentucky</option>
      <option value="LA">LA - Louisiana</option>
      <option value="ME">ME - Maine</option>
      <option value="MD">MD - Maryland</option>
      <option value="MA">MA - Massachusetts</option>
      <option value="MI">MI - Michigan</option>
      <option value="MN">MN - Minnesota</option>
      <option value="MS">MS - Mississippi</option>
      <option value="MO">MO - Missouri</option>
      <option value="MT">MT - Montana</option>
      <option value="NE">NE - Nebraska</option>
      <option value="NV">NV - Nevada</option>
      <option value="NH">NH - New Hampshire</option>
      <option value="NJ">NJ - New Jersey</option>
      <option value="NM">NM - New Mexico</option>
      <option value="NY">NY - New York</option>
      <option value="NC">NC - North Carolina</option>
      <option value="ND">ND - North Dakota</option>
      <option value="MP">MP - Northern Mariana Islands</option>
      <option value="OH">OH - Ohio</option>
      <option value="OK">OK - Oklahoma</option>
      <option value="OR">OR - Oregon</option>
      <option value="PA">PA - Pennsylvania</option>
      <option value="PR">PR - Puerto Rico</option>
      <option value="RI">RI - Rhode Island</option>
      <option value="SC">SC - South Carolina</option>
      <option value="SD">SD - South Dakota</option>
      <option value="TN">TN - Tennessee</option>
      <option value="TX">TX - Texas</option>
      <option value="TT">TT - Trust Territories</option>
      <option value="UT">UT - Utah</option>
      <option value="VT">VT - Vermont</option>
      <option value="VA">VA - Virginia</option>
      <option value="VI">VI - Virgin Islands</option>
      <option value="WA">WA - Washington</option>
      <option value="WV">WV - West Virginia</option>
      <option value="WI">WI - Wisconsin</option>
      <option value="WY">WY - Wyoming</option>
    </select>
    <div class="field-help">State or territory containing the geographic unit</div>
  </div>

  <div class="field-group">
    <label for="reporting_jurisdiction">Reporting Jurisdiction *</label>
    <select id="reporting_jurisdiction" onchange="updateFields()">
      <option value="">-- Select reporting jurisdiction --</option>
    </select>
    <div class="field-help">Jurisdiction submitting the data (usually same as state, or NYC for New York City)</div>
  </div>

  <div class="field-group">
    <label for="geo_unit">Geographic Unit *</label>
    <select id="geo_unit" onchange="updateFields()">
      <option value="">-- Select geographic unit --</option>
      <option value="county">county</option>
      <option value="state">state</option>
      <option value="region">region</option>
      <option value="planning area">planning area</option>
      <option value="hsa">hsa</option>
      <option value="NA">NA</option>
    </select>
    <div class="field-help">Type of geographic unit (use 'NA' for international residents)</div>
  </div>

  <div class="field-group">
    <label for="geo_name">Geographic Name *</label>
    <select id="geo_name" onchange="updateFields()">
      <option value="">-- Select or provide geographic name --</option>
    </select>
    <div class="field-help">Name of the geographic unit (or special values: 'international resident', 'unknown', 'unspecified')</div>
  </div>

  <div class="field-group">
    <label for="age_group">Age Group *</label>
    <select id="age_group" onchange="updateFields()">
      <option value="">-- Select age group --</option>
      <option value="<1 y">&lt;1 y</option>
      <option value="1-4 y">1-4 y</option>
      <option value="5-11 y">5-11 y</option>
      <option value="12-18 y">12-18 y</option>
      <option value="19-22 y">19-22 y</option>
      <option value="23-44 y">23-44 y</option>
      <option value="45-64 y">45-64 y</option>
      <option value=">=65 y">&gt;=65 y</option>
      <option value="total">total</option>
      <option value="unknown">unknown</option>
      <option value="unspecified">unspecified</option>
    </select>
    <div class="field-help">Age group of cases (use 'total' for non-age-stratified aggregations)</div>
  </div>

  <div class="field-group">
    <label for="report_period_start">Report Period Start *</label>
    <input type="date" id="report_period_start" placeholder="YYYY-MM-DD">
    <div class="field-help">Example: <span class="example-value">2025-01-05</span> (YYYY-MM-DD format, must align with MMWR week/month boundaries)</div>
  </div>

  <div class="field-group">
    <label for="report_period_end">Report Period End *</label>
    <input type="date" id="report_period_end" placeholder="YYYY-MM-DD">
    <div class="field-help">Example: <span class="example-value">2025-01-11</span> (YYYY-MM-DD format, must be after or equal to start date)</div>
  </div>

  <div class="field-group">
    <label for="count">Count *</label>
    <input type="number" id="count" placeholder="Enter count" min="1">
    <div class="field-help">Example: <span class="example-value">5</span> (positive integer, only non-zero counts should be submitted)</div>
  </div>

  <button class="reset-button" onclick="generateExample()" style="margin-top: 20px;">Generate Example</button>

  <div id="example-table" class="info-box" style="display: none; margin-top: 30px;">
    <h4>Example Data Table</h4>
    <div style="overflow-x: auto;">
      <table id="data-table" style="width: 100%; border-collapse: collapse; margin-top: 10px;">
        <thead>
          <tr style="background-color: #159957; color: white;">
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">report_period_start</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">report_period_end</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">date_type</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">time_unit</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">disease_name</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">disease_subtype</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">state</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">reporting_jurisdiction</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">geo_name</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">geo_unit</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">age_group</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">confirmation_status</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">outcome</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">count</th>
          </tr>
        </thead>
        <tbody id="data-table-body">
          <!-- Table rows will be inserted here -->
        </tbody>
      </table>
    </div>
    <p style="margin-top: 10px; font-size: 12px; color: #666;">
      <strong>Note:</strong> This is how your data should be formatted for submission. Copy this table format to create your CSV file.
    </p>
  </div>

  <script>
    // Validation rules based on schema and documentation
    const validationRules = {
      disease_name: ['measles', 'pertussis', 'meningococcus'],
      
      time_unit: {
        measles: ['week', 'month'],
        pertussis: ['month'],
        meningococcus: ['month']
      },
      
      confirmation_status: {
        measles: ['confirmed'],
        pertussis: ['confirmed and probable'],
        meningococcus: ['confirmed and probable']
      },
      
      disease_subtype: {
        measles: ['NA', 'unknown'],
        pertussis: ['NA', 'unknown'],
        meningococcus: ['A', 'B', 'C', 'W', 'X', 'Y', 'Z', 'unknown', 'unspecified']
      },
      
      geo_unit: ['county', 'state', 'region', 'planning area', 'hsa', 'NA'],
      
      geo_name_special: ['international resident', 'unknown', 'unspecified'],
      
      age_group: ['<1 y', '1-4 y', '5-11 y', '12-18 y', '19-22 y', '23-44 y', '45-64 y', '>=65 y', 'total', 'unknown', 'unspecified']
    };

    function updateFields() {
      const disease = document.getElementById('disease_name').value;
      const state = document.getElementById('state').value;
      const geoUnit = document.getElementById('geo_unit').value;
      
      // Update time_unit based on disease
      updateTimeUnit(disease);
      
      // Update confirmation_status based on disease
      updateConfirmationStatus(disease);
      
      // Update disease_subtype based on disease
      updateDiseaseSubtype(disease);
      
      // Update reporting_jurisdiction based on state
      updateReportingJurisdiction(state);
      
      // Update geo_name based on geo_unit
      updateGeoName(geoUnit, state);
    }

    function updateTimeUnit(disease) {
      const select = document.getElementById('time_unit');
      const currentValue = select.value;
      
      select.innerHTML = '<option value="">-- Select time unit --</option>';
      
      if (disease && validationRules.time_unit[disease]) {
        validationRules.time_unit[disease].forEach(value => {
          const option = document.createElement('option');
          option.value = value;
          option.textContent = value;
          if (value === currentValue) {
            option.selected = true;
          }
          select.appendChild(option);
        });
        select.disabled = false;
      } else {
        select.disabled = true;
      }
    }

    function updateConfirmationStatus(disease) {
      const select = document.getElementById('confirmation_status');
      const currentValue = select.value;
      
      select.innerHTML = '<option value="">-- Select confirmation status --</option>';
      
      if (disease && validationRules.confirmation_status[disease]) {
        validationRules.confirmation_status[disease].forEach(value => {
          const option = document.createElement('option');
          option.value = value;
          option.textContent = value;
          if (value === currentValue) {
            option.selected = true;
          }
          select.appendChild(option);
        });
        select.disabled = false;
      } else {
        select.disabled = true;
      }
    }

    function updateDiseaseSubtype(disease) {
      const select = document.getElementById('disease_subtype');
      const currentValue = select.value;
      
      select.innerHTML = '<option value="">-- Select disease subtype --</option>';
      
      if (disease && validationRules.disease_subtype[disease]) {
        validationRules.disease_subtype[disease].forEach(value => {
          const option = document.createElement('option');
          option.value = value;
          option.textContent = value;
          if (value === currentValue) {
            option.selected = true;
          }
          select.appendChild(option);
        });
        select.disabled = false;
      } else {
        select.disabled = true;
      }
    }

    function updateReportingJurisdiction(state) {
      const select = document.getElementById('reporting_jurisdiction');
      const currentValue = select.value;
      
      select.innerHTML = '<option value="">-- Select reporting jurisdiction --</option>';
      
      if (state) {
        // Most jurisdictions are the same as the state
        const option1 = document.createElement('option');
        option1.value = state;
        option1.textContent = state;
        if (state === currentValue) {
          option1.selected = true;
        }
        select.appendChild(option1);
        
        // NYC is special for New York
        if (state === 'NY') {
          const option2 = document.createElement('option');
          option2.value = 'NYC';
          option2.textContent = 'NYC';
          if ('NYC' === currentValue) {
            option2.selected = true;
          }
          select.appendChild(option2);
        }
        
        select.disabled = false;
      } else {
        select.disabled = true;
      }
    }

    function updateGeoName(geoUnit, state) {
      const select = document.getElementById('geo_name');
      const currentValue = select.value;
      
      select.innerHTML = '<option value="">-- Select or provide geographic name --</option>';
      
      if (geoUnit === 'NA') {
        // For NA geo_unit, only allow "international resident"
        const option = document.createElement('option');
        option.value = 'international resident';
        option.textContent = 'international resident';
        option.selected = true;
        select.appendChild(option);
        select.disabled = false;
      } else if (geoUnit === 'state' && state) {
        // For state-level reporting, use the state abbreviation
        const option = document.createElement('option');
        option.value = state;
        option.textContent = state;
        option.selected = true;
        select.appendChild(option);
        select.disabled = false;
      } else if (geoUnit) {
        // For other geo_units, provide special values and an example
        validationRules.geo_name_special.forEach(value => {
          const option = document.createElement('option');
          option.value = value;
          option.textContent = value;
          if (value === currentValue) {
            option.selected = true;
          }
          select.appendChild(option);
        });
        
        // Add example based on geo_unit
        const examples = {
          'county': 'King County',
          'region': 'Region 1',
          'planning area': 'Planning Area A',
          'hsa': 'HSA 1'
        };
        
        if (examples[geoUnit]) {
          const option = document.createElement('option');
          option.value = examples[geoUnit];
          option.textContent = examples[geoUnit] + ' (example)';
          select.appendChild(option);
        }
        
        select.disabled = false;
      } else {
        select.disabled = true;
      }
    }

    function resetForm() {
      const selects = document.querySelectorAll('select');
      selects.forEach(select => {
        select.selectedIndex = 0;
        if (select.id !== 'disease_name' && select.id !== 'outcome' && 
            select.id !== 'date_type' && select.id !== 'state' && 
            select.id !== 'geo_unit' && select.id !== 'age_group') {
          select.disabled = true;
          select.innerHTML = '<option value="">-- Select --</option>';
        }
      });
      
      // Clear input fields
      document.getElementById('report_period_start').value = '';
      document.getElementById('report_period_end').value = '';
      document.getElementById('count').value = '';
      
      document.getElementById('example-table').style.display = 'none';
    }

    function generateExample() {
      const fields = {
        report_period_start: document.getElementById('report_period_start').value,
        report_period_end: document.getElementById('report_period_end').value,
        date_type: document.getElementById('date_type').value,
        time_unit: document.getElementById('time_unit').value,
        disease_name: document.getElementById('disease_name').value,
        disease_subtype: document.getElementById('disease_subtype').value,
        reporting_jurisdiction: document.getElementById('reporting_jurisdiction').value,
        state: document.getElementById('state').value,
        geo_name: document.getElementById('geo_name').value,
        geo_unit: document.getElementById('geo_unit').value,
        age_group: document.getElementById('age_group').value,
        confirmation_status: document.getElementById('confirmation_status').value,
        outcome: document.getElementById('outcome').value,
        count: document.getElementById('count').value
      };

      // Check if all required fields are filled
      const requiredFields = ['disease_name', 'disease_subtype', 'time_unit', 'confirmation_status', 'outcome', 
                              'date_type', 'state', 'reporting_jurisdiction', 'geo_unit', 
                              'geo_name', 'age_group', 'report_period_start', 'report_period_end', 'count'];
      
      const missingFields = [];
      requiredFields.forEach(field => {
        if (!fields[field]) {
          missingFields.push(field.replace(/_/g, ' '));
        }
      });

      if (missingFields.length > 0) {
        alert('Please fill in all required fields before generating an example:\n\n' + 
              missingFields.map(f => '- ' + f).join('\n'));
        return;
      }

      // Create the table row safely to prevent XSS
      const tableBody = document.getElementById('data-table-body');
      tableBody.innerHTML = '';
      
      const row = document.createElement('tr');
      const fieldOrder = [
        fields.report_period_start,
        fields.report_period_end,
        fields.date_type,
        fields.time_unit,
        fields.disease_name,
        fields.disease_subtype || 'NA',
        fields.reporting_jurisdiction,
        fields.state,
        fields.geo_name,
        fields.geo_unit,
        fields.age_group,
        fields.confirmation_status,
        fields.outcome,
        fields.count
      ];
      
      fieldOrder.forEach(value => {
        const cell = document.createElement('td');
        cell.style.padding = '8px';
        cell.style.border = '1px solid #ddd';
        cell.textContent = value;
        row.appendChild(cell);
      });
      
      tableBody.appendChild(row);
      
      // Show the example table
      document.getElementById('example-table').style.display = 'block';
      
      // Scroll to the table
      document.getElementById('example-table').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  </script>
</div>

## Additional Resources

For complete technical specifications and validation rules, see:
- [Data Technical Specifications](guides/DATA-TECHNICAL-SPECS.md)
- [Validation Rules](guides/VALIDATION.md)
- [Data dictionary (CSV)](examples-and-templates/disease_tracking_data_dictionary.csv)
