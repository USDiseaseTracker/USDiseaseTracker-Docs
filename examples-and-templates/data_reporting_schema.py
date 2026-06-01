import csv as _csv
from datetime import date
from pathlib import Path as _Path
from typing import List, Literal
from collections import defaultdict
from pydantic import RootModel
from pydantic import BaseModel, ValidationInfo, field_validator, model_validator


def _load_disease_metadata() -> list[dict]:
    """Load disease metadata from disease_metadata.csv at module import time."""
    csv_path = _Path(__file__).parent / 'disease_metadata.csv'
    diseases = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = _csv.DictReader(f)
        for row in reader:
            if not row or not any(v.strip() for v in row.values() if isinstance(v, str)):
                continue
            disease = row.get('disease', '').strip()
            if not disease:
                continue
            subtypes_raw = row.get('disease_subtype', '').strip() or 'total'
            subtypes = [s.strip() for s in subtypes_raw.split(',') if s.strip()]
            age_groups_raw = row.get('age_group', '').strip() or 'total'
            age_groups = [a.strip() for a in age_groups_raw.split(',') if a.strip()]
            def _parse_bool_flag(column: str, default: str) -> str:
                raw = row.get(column, default)
                normalized = raw.strip().upper() if isinstance(raw, str) else default
                if normalized not in ('TRUE', 'FALSE'):
                    raise ValueError(
                        f"Invalid value {raw!r} for column '{column}' in disease_metadata.csv "
                        f"(disease={disease!r}). Expected 'TRUE' or 'FALSE'."
                    )
                return normalized

            diseases.append({
                'disease': disease,
                'confirmation_status': row.get('confirmation_status', '').strip(),
                'disease_subtype': subtypes,
                'age_group': age_groups,
                'aggregation_agegroups': _parse_bool_flag('aggregation_agegroups', 'TRUE'),
                'aggregations_diseasesubtype': _parse_bool_flag('aggregations_diseasesubtype', 'FALSE'),
            })
    return diseases


_DISEASE_METADATA: list[dict] = _load_disease_metadata()

# Lookup tables derived from disease_metadata.csv (authoritative source)
DISEASE_NAMES: list[str] = [d['disease'] for d in _DISEASE_METADATA]
DISEASE_SUBTYPES: dict[str, list[str]] = {d['disease']: d['disease_subtype'] for d in _DISEASE_METADATA}
DISEASE_CONFIRMATION: dict[str, str] = {d['disease']: d['confirmation_status'] for d in _DISEASE_METADATA}
DISEASE_AGE_GROUPS: dict[str, list[str]] = {d['disease']: d['age_group'] for d in _DISEASE_METADATA}
# diseases where aggregation_agegroups = 'TRUE' (state-level age breakdown is reported)
DISEASES_WITH_AGE_BREAKDOWN: set[str] = {
    d['disease'] for d in _DISEASE_METADATA if d['aggregation_agegroups'] == 'TRUE'
}
# diseases where aggregations_diseasesubtype = 'TRUE' (state-level subtype breakdown is reported)
DISEASES_WITH_SUBTYPE_BREAKDOWN: set[str] = {
    d['disease'] for d in _DISEASE_METADATA if d['aggregations_diseasesubtype'] == 'TRUE'
}


"""
# add new states here as needed. only states present in this dictionary
# will have their geo_name validated; all others are unchecked.
"""
sub_state_jurisdictions: dict[str, list[str]] = {
    "ID": [
        "Public Health District 1", "Public Health District 2", "Public Health District 3", "Public Health District 4",
        "Public Health District 5", "Public Health District 6", "Public Health District 7"
    ],
    "MA": [
        "Berkshire", "Bristol", "Essex", "Franklin", "Hampden", "Hampshire", "Middlesex", "Norfolk", "Plymouth", "Suffolk",
        "Worcester", "Dukes/Nantucket/Barnstable" 
    ],
    "MI": [
        "1", "2 North", "2 South", "3", "5", "6", "7", "8"
    ],
    "MN": [
        "Aitkin County", "Anoka County", "Becker County", "Beltrami County", "Benton County", "Big Stone County", "Blue Earth County", "Brown County",
        "Carlton County", "Carver County", "Cass County", "Chippewa County", "Chisago County", "Clay County", "Clearwater County", "Cook County", "Cottonwood County",
        "Crow Wing County", "Dakota County", "Dodge County", "Douglas County", "Faribault County", "Fillmore County", "Freeborn County", "Goodhue County", "Grant County",
        "Hennepin County", "Houston County", "Hubbard County", "Isanti County", "Itasca County", "Jackson County", "Kanabec County", "Kandiyohi County", "Kittson County",
        "Koochiching County", "Lake County", "Lake of the Woods County", "Lac qui Parle County", "Le Sueur County", "Lincoln County", "Lyon County", "Mahnomen County",
        "Marshall County", "Martin County", "McLeod County", "Meeker County", "Mille Lacs County", "Morrison County", "Mower County", "Murray County", "Nicollet County",
        "Nobles County", "Norman County", "Olmsted County", "Otter Tail County", "Pennington County", "Pine County", "Pipestone County", "Polk County", "Pope County",
        "Ramsey County", "Red Lake County", "Redwood County", "Renville County", "Rice County", "Rock County", "Roseau County", "Scott County", "Sherburne County", "Sibley County",
        "St. Louis County", "Stearns County", "Steele County", "Stevens County", "Swift County", "Todd County", "Traverse County", "Wabasha County", "Wadena County", "Waseca County",
        "Washington County", "Watonwan County", "Wilkin County", "Winona County", "Wright County", "Yellow Medicine County"
    ],
}
# add "unspecified" as a valid sub-state jurisdiction for each state to handle suppression rules.
sub_state_jurisdictions = {k: v + ["unspecified"] for k, v in sub_state_jurisdictions.items()}

class DiseaseReport(BaseModel):
    disease_name: str
    report_period_start: date
    report_period_end: date
    date_type: Literal["cccd", "jurisdiction date hierarchy"]
    time_unit: Literal["week"]
    disease_subtype: str
    reporting_jurisdiction: str
    state: Literal[
        "AL", "AK", "AZ", "AR", "AS",
        "CA", "CO", "CT", "DE", "DC",
        "FL", "GA", "GU", "HI", "ID",
        "IL", "IN", "IA", "KS", "KY",
        "LA", "ME", "MD", "MA", "MI",
        "MN", "MS", "MO", "MT", "NE",
        "NV", "NH", "NJ", "NM", "NY",
        "NC", "ND", "MP", "OH", "OK",
        "OR", "PA", "PR", "RI", "SC",
        "SD", "TN", "TX", "TT", "UT",
        "VT", "VA", "VI", "WA", "WV",
        "WI", "WY"
    ]
    geo_unit: Literal["county", "state", "region", "planning area", "hsa", "NA"]
    geo_name: str
    age_group: Literal[
        "<1 y", "1-4 y", "5-11 y", "12-18 y",
        "19-22 y", "23-44 y", "45-64 y", ">=65 y",
        "total", "unknown", "unspecified"
    ]
    confirmation_status: Literal["confirmed", "confirmed and probable"]
    outcome: Literal["cases", "deaths"]
    count: int
    
    class Config:
        """
        forbid extra data columns
        """
        extra = "forbid"
    
    @field_validator('disease_name')
    @classmethod
    def validate_disease_name(cls, v):
        """
        validate disease_name against the authoritative list in disease_metadata.csv
        """
        if v not in DISEASE_NAMES:
            raise ValueError(
                f"disease_name must be one of: {DISEASE_NAMES}. got: '{v}'"
            )
        return v

    @field_validator('count')
    @classmethod
    def count_must_be_non_negative(cls, v):
        if v <= 0:
            raise ValueError('count must be > 0')
        return v
    
    @field_validator('disease_subtype')
    @classmethod
    def validate_disease_subtype(cls, v, info: ValidationInfo):
        """
        validate disease_subtype based on disease_name, using valid subtypes from disease_metadata.csv
        """
        disease_name = info.data.get('disease_name')
        valid_subtypes = DISEASE_SUBTYPES.get(disease_name)
        if valid_subtypes is None:
            # disease_name failed its own validation; nothing to check here.
            return v
        
        if v not in valid_subtypes:
            raise ValueError(
                f"for {disease_name}, disease_subtype must be one of: {valid_subtypes}. got: '{v}'"
            )
        
        return v
    
    @model_validator(mode = 'after')
    def validate_reporting_jurisdiction(self):
        """
        validate reporting_jurisdiction to match either the state or the geo_name column. for 'international resident' rows, reporting_jurisdiction must
        match the state only.
        """
        if self.geo_name == 'international resident':
            if self.reporting_jurisdiction != self.state:
                raise ValueError(
                    f"for 'international resident' rows, reporting_jurisdiction must match the state."
                    f"\ngot reporting_jurisdiction = '{self.reporting_jurisdiction}' but state = '{self.state}'"
                )
            
            return self
        
        if self.reporting_jurisdiction not in (self.state, self.geo_name):
            raise ValueError(
                f"reporting_jurisdiction must match either state or geo_name."
                f"\ngot reporting_jurisdiction = '{self.reporting_jurisdiction}', "
                f"state = '{self.state}', geo_name = '{self.geo_name}'"
            )
        
        return self
    
    @model_validator(mode = 'after')
    def validate_breakdown_rules(self):
        """
        enforces age_group and disease_subtype breakdown rules based on geo_unit and disease_name,
        using aggregation flags from disease_metadata.csv.

        sub-state level (geo_unit != 'state'):
            - disease_subtype must be 'total'
            - age_group must be 'total'

        state level (geo_unit == 'state') — diseases with age breakdown only
        (aggregation_agegroups=TRUE, aggregations_diseasesubtype=FALSE, e.g. measles, pertussis,
        hepatitis a, mumps, mpox, varicella, pediatric flu mortality, acute hepatitis b):
            - disease_subtype must be 'total' (already enforced by field validator)
            - age_group must not be 'total'

        state level (geo_unit == 'state') — diseases with subtype breakdown
        (aggregations_diseasesubtype=TRUE, e.g. meningococcus):
            - age breakdown rows:     disease_subtype == 'total', age_group != 'total'
            - subtype breakdown rows: age_group == 'total', disease_subtype != 'total'
            i.e. exactly one of age_group or disease_subtype must be 'total'
            (the other must not be 'total')

        diseases with no age breakdown (aggregation_agegroups=FALSE, e.g. perinatal hepatitis b):
            - age_group must always be 'total' at all geo levels
        """
        disease_name = self.disease_name
        disease_subtype = self.disease_subtype
        geo_unit = self.geo_unit
        age_group = self.age_group

        has_age_breakdown = disease_name in DISEASES_WITH_AGE_BREAKDOWN
        has_subtype_breakdown = disease_name in DISEASES_WITH_SUBTYPE_BREAKDOWN

        # Validate age_group against disease-specific allowed values (all geo levels).
        valid_age_groups = DISEASE_AGE_GROUPS.get(disease_name)
        if valid_age_groups and age_group not in valid_age_groups:
            raise ValueError(
                f"for {disease_name}, age_group must be one of: {valid_age_groups}."
                f"\ngot age_group = '{age_group}'"
            )

        # sub-state level: both must be 'total'.
        if geo_unit != "state":
            if age_group != "total":
                raise ValueError(
                    f"at sub-state level, age_group must be 'total'."
                    f"\ngot geo_unit = '{geo_unit}' and age_group = '{age_group}'"
                )
            
            if disease_subtype != "total":
                raise ValueError(
                    f"at sub-state level, disease_subtype must be 'total'."
                    f"\ngot geo_unit = '{geo_unit}' and disease_subtype = '{disease_subtype}'"
                )
            
            return self

        # state level.
        if not has_age_breakdown:
            # diseases with no age breakdown (e.g. perinatal hepatitis b):
            # age_group must always be 'total'.
            if age_group != "total":
                raise ValueError(
                    f"for {disease_name}, age_group must be 'total' (no age breakdown reported)."
                    f"\ngot age_group = '{age_group}'"
                )
        elif has_subtype_breakdown:
            # diseases with subtype breakdown (e.g. meningococcus):
            # exactly one of age_group or disease_subtype must be 'total'.
            age_is_total = age_group == "total"
            subtype_is_total = disease_subtype == "total"

            if age_is_total and subtype_is_total:
                raise ValueError(
                    f"for {disease_name} at state level, age_group and disease_subtype cannot both be 'total'."
                    "\nuse age_group = 'total' for subtype breakdowns, or disease_subtype = 'total' for age breakdowns."
                )
            if not age_is_total and not subtype_is_total:
                raise ValueError(
                    f"for {disease_name} at state level, exactly one of age_group or disease_subtype must be 'total'."
                    f"\ngot age_group = '{age_group}' and disease_subtype = '{disease_subtype}'"
                )
        else:
            # diseases with age breakdown only (e.g. measles, pertussis, hepatitis a, etc.):
            # age_group must not be 'total' at state level.
            if age_group == "total":
                raise ValueError(
                    f"at state level, age_group must not be 'total' for {disease_name}."
                    f"\ngot age_group = '{age_group}'"
                )

        return self
    
    @field_validator('geo_name')
    @classmethod
    def validate_geo_name(cls, v, info: ValidationInfo):
        """
        validate geo_name for sub-state jurisdictions of the states that are participating in the USDT project.
        """
        state = info.data.get('state')
        geo_unit = info.data.get('geo_unit')
        
        if v == 'international resident':
            # handles 'international resident' case.
            if geo_unit != 'NA':
                raise ValueError(
                    f"when geo_name is 'international resident', geo_unit must be 'NA'."
                    f"\ngot geo_name = '{v}' but geo_unit = '{geo_unit}'"
                )
            
            return v
        elif geo_unit == 'NA':
            raise ValueError(
                f"geo_unit must not be 'NA', unless geo_name is 'international resident'."
                f"\ngot geo_unit = '{geo_unit}' but geo_name = '{v}'"
            )

        if geo_unit == "state":
            if v != state:
                raise ValueError(
                    f"when geo_unit is 'state', geo_name must match state."
                    f"\ngot geo_name = '{v}' but state = '{state}'"
                )
            
            return v
        else:
            known_jurisdictions = sub_state_jurisdictions.get(state)
            if known_jurisdictions is None:
                # state not yet registered in the schema, so accept any jurisdiction name.
                return v

            if v not in known_jurisdictions:
                raise ValueError(
                    f"'{v}' is not a recognized sub-state jurisdiction for {state}."
                    f"\nexpected one of: {known_jurisdictions}"
                )
            
            return v
        
    @field_validator('confirmation_status')
    @classmethod
    def validate_confirmation_status(cls, v, info: ValidationInfo):
        """
        validate confirmation_status based on disease_name, using the expected status from
        disease_metadata.csv.
        """
        disease_name = info.data.get('disease_name')
        expected = DISEASE_CONFIRMATION.get(disease_name)
        if expected is None:
            # disease_name failed its own validation; nothing to check here.
            return v
        
        if v != expected:
            raise ValueError(
                f"for {disease_name}, confirmation_status must be '{expected}'."
                f"\ngot: '{v}'"
            )
        
        return v

class DiseaseReportDataset(RootModel[List[DiseaseReport]]):
    @model_validator(mode = 'after')
    def validate_single_state(self):
        """
        check that the submitted file only contains data for a single state.
        """
        states = {row.state for row in self.root}
        if len(states) > 1:
            raise ValueError(
                f"dataset must contain data for a single state only."
                f"\nfound multiple states: {sorted(states)}"
            )
        
        return self

    @model_validator(mode = 'after')
    def validate_count_totals(self):
        """
        for each (report_period_start, report_period_end, disease_name, outcome) grouping,
        verify that counts match across levels, using aggregation flags from disease_metadata.csv:

        diseases with subtype breakdown (aggregations_diseasesubtype=TRUE, e.g. meningococcus):
            -    sum of state-level age breakdown rows (disease_subtype == 'total')
              == sum of state-level disease subtype breakdown rows (age_group == 'total')
              == sum of sub-state rows

        all other diseases (including age-breakdown-only and no-age-breakdown diseases):
            - sum of state-level rows == sum of sub-state rows

        international resident rows (geo_unit == 'NA') are excluded from all sums.
        """
        # filter out international resident rows.
        rows = [r for r in self.root if r.geo_name != 'international resident']

        # group rows by (report_period_start, report_period_end, disease_name, outcome).
        groups = defaultdict(list)
        for row in rows:
            key = (row.report_period_start, row.report_period_end, row.disease_name, row.outcome)
            groups[key].append(row)

        errors = []
        for (start, end, disease_name, outcome), group_rows in groups.items():
            period_str = f"{start} to {end}"

            state_rows = [r for r in group_rows if r.geo_unit == 'state']
            substate_rows = [r for r in group_rows if r.geo_unit != 'state']

            substate_sum = sum(r.count for r in substate_rows)

            if disease_name in DISEASES_WITH_SUBTYPE_BREAKDOWN:
                # diseases with subtype breakdown (e.g. meningococcus): verify both
                # state-level age breakdown and subtype breakdown sums equal the sub-state sum.
                age_breakdown_sum = sum(
                    r.count for r in state_rows if r.disease_subtype == 'total'
                )
                subtype_breakdown_sum = sum(
                    r.count for r in state_rows if r.age_group == 'total'
                )

                if not (age_breakdown_sum == subtype_breakdown_sum == substate_sum):
                    errors.append(
                        f"count mismatch for [{period_str} | {disease_name} | {outcome}]:"
                        f"\nstate-level age breakdown sum = {age_breakdown_sum}"
                        f"\nstate-level disease subtype breakdown sum = {subtype_breakdown_sum}"
                        f"\nsub-state sum = {substate_sum}"
                    )
            else:
                # all other diseases: state-level sum must equal sub-state sum.
                state_sum = sum(r.count for r in state_rows)

                if state_sum != substate_sum:
                    errors.append(
                        f"count mismatch for [{period_str} | {disease_name} | {outcome}]:"
                        f"\nstate-level sum ({state_sum}) != sub-state sum ({substate_sum})"
                    )

        if errors:
            raise ValueError(
                f"count mismatch(es) found:"
                + "".join(f"\n - {e}" for e in errors)
            )

        return self
