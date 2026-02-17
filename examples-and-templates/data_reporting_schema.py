from datetime import date
from typing import List, Literal
from collections import defaultdict
from pydantic import RootModel
from pydantic import BaseModel, ValidationInfo, field_validator, model_validator

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
}

class DiseaseReport(BaseModel):
    disease_name: Literal["measles", "pertussis", "meningococcus"]
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
    outcome: Literal["cases", "hospitalizations", "deaths"]
    count: int
    
    class Config:
        """
        forbid extra data columns
        """
        extra = "forbid"
    
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
        validate disease_subtype based on disease_name
        """
        disease_name = info.data.get('disease_name')
        
        if disease_name == "meningococcus":
            if v not in ["A", "B", "C", "W", "X", "Y", "Z", "unknown", "unspecified", "total"]:
                raise ValueError(
                    f"for meningococcus, disease_subtype must be one of: A, B, C, W, X, Y, Z, unknown, unspecified, total. got: {v}"
                )
        elif disease_name in ["measles", "pertussis"]:
            if v not in ["total"]:
                raise ValueError(
                    f"for {disease_name}, disease_subtype must be 'total'. got: {v}"
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
        enforces age_group and disease_subtype breakdown rules based on geo_unit and disease_name.

        sub-state level (geo_unit != 'state'):
            - disease_subtype must be 'total'
            - age_group must be 'total'

        state level (geo_unit == 'state') — disease_name == 'measles' or 'pertussis':
            - disease_subtype must be 'total' (already enforced by field validator)
            - age_group must be anything except 'total'

        state level (geo_unit == 'state') — disease_name == 'meningococcus':
            - age breakdown:  disease_subtype == 'total', and age_group != 'total'
            - subtype breakdown:  age_group == 'total', and disease_subtype != 'total'
        """
        disease_name = self.disease_name
        disease_subtype = self.disease_subtype
        geo_unit = self.geo_unit
        age_group = self.age_group

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
        if disease_name in ["measles", "pertussis"]:
            if age_group == "total":
                raise ValueError(
                    f"at state level, age_group must not be 'total' for {disease_name}."
                    f"\ngot age_group = '{age_group}'"
                )
        elif disease_name == "meningococcus":
            age_is_total = age_group == "total"
            subtype_is_total = disease_subtype == "total"

            if age_is_total and subtype_is_total:
                raise ValueError(
                    "for meningococcus at state level, age_group and disease_subtype cannot both be 'total'."
                    "\nuse age_group = 'total' for subtype breakdowns, or disease_subtype = 'total' for age breakdowns."
                )
            if not age_is_total and not subtype_is_total:
                raise ValueError(
                    "for meningococcus at state level, exactly one of age_group or disease_subtype must be 'total'."
                    f"\ngot age_group = '{age_group}' and disease_subtype = '{disease_subtype}'"
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
        validate confirmation_status based on disease_name:
            - measles: 'confirmed' only
            - pertussis, meningococcus: 'confirmed and probable' only
        """
        disease_name = info.data.get('disease_name')
        
        if disease_name == 'measles' and v != 'confirmed':
            raise ValueError(
                f"for measles, confirmation_status must be 'confirmed'."
                f"\ngot: '{v}'"
            )
        elif disease_name in ['pertussis', 'meningococcus'] and v != 'confirmed and probable':
            raise ValueError(
                f"for {disease_name}, confirmation_status must be 'confirmed and probable'."
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
        verify that counts match across levels:

        measles/pertussis:
            - sum of state-level rows (age breakdown) == sum of sub-state rows

        meningococcus:
            -    sum of state-level age breakdown rows (disease_subtype == 'total')
              == sum of state-level disease subtype breakdown rows (age_group == 'total')
              == sum of sub-state rows

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

            if disease_name in ["measles", "pertussis"]:
                state_sum = sum(r.count for r in state_rows)

                if state_sum != substate_sum:
                    errors.append(
                        f"count mismatch for [{period_str} | {disease_name} | {outcome}]:"
                        f"\nstate-level sum ({state_sum}) != sub-state sum ({substate_sum})"
                    )
            elif disease_name == "meningococcus":
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

        if errors:
            raise ValueError(
                f"count mismatch(es) found:"
                + "".join(f"\n - {e}" for e in errors)
            )

        return self