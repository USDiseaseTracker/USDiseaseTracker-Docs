
# This script builds an example dataset for the disease tracking report using publicly
# available data. It improves on v1.1.0 in two key ways:
#
#   1. NNDSS weekly data are pulled DIRECTLY from the CDC Socrata API — no manual
#      download required. The raw API response is normalised so its columns match the
#      format used in the rest of the script.
#
#   2. ALL diseases listed in disease_metadata.csv are processed from NNDSS using the
#      same generic pipeline introduced for pertussis/meningococcus in v1.1.0.
#      Measles is the sole exception and continues to be pulled from the separate
#      CSSEGISandData GitHub repository.
#
# Prerequisites
#   - A Census API key saved via tidycensus::census_api_key("YOUR_KEY", install = TRUE)
#     (needed for county population weights).  Sign up at:
#     https://api.census.gov/data/key_signup.html
#
# Output
#   examples-and-templates/disease_tracking_report_CA-SIMULATED-EXAMPLE_<date>.csv


library(readr)
library(tidyverse)
library(MMWRweek)
library(lubridate)
library(purrr)
library(tidycensus)
library(httr)


# =========================================================================
# CONFIGURATION
# =========================================================================

# Path to disease metadata file (relative to working directory / project root)
disease_meta_path <- "examples-and-templates/disease_metadata.csv"

# Only retain data at or after this MMWR week start date
filter_start_date <- as.Date("2024-12-29")

# Random seed for reproducibility of multinomial splits
random_seed <- 123

# NNDSS Socrata API base URL (CDC dataset x9gk-5huc).
# Query parameters ($where, $limit, $order) are set via httr::GET() below so
# that they are properly URL-encoded. Raise $limit if the dataset grows larger.
nndss_api_base <- "https://data.cdc.gov/resource/x9gk-5huc.csv"

# Age-group definitions and probability distributions
age_groups    <- c("<1 y", "1-4 y", "5-11 y", "12-18 y",
                   "19-22 y", "23-44 y", "45-64 y", ">=65 y", "unknown")

# Distribution used for pertussis and most NNDSS diseases
age_dist_pert <- c(0, 0.3, 0.45, 0.0, 0.15, 0.1, 0.0, 0.0, 0.0)
age_df_pert   <- data.frame(age_group = age_groups, age_dist = age_dist_pert)

# Distribution used for measles
age_dist_meas <- c(0.2, 0.2, 0.4, 0.1, 0.1, 0.0, 0.0, 0.0, 0.0)
age_df_meas   <- data.frame(age_group = age_groups, age_dist = age_dist_meas)


# =========================================================================
# LOAD DISEASE METADATA
# =========================================================================

disease_meta <- read_csv(disease_meta_path, show_col_types = FALSE)

# Derive the NNDSS label map from disease_meta.
# The nndss_label column stores the substring to match against the NNDSS
# "Label" field for each disease.  Measles has NA (uses GitHub instead).
nndss_label_map <- disease_meta %>%
    filter(!is.na(nndss_label)) %>%
    select(disease, nndss_pattern = nndss_label)


# =========================================================================
# PULL NNDSS DATA DIRECTLY FROM CDC SOCRATA API
# =========================================================================

message("Pulling NNDSS weekly data from CDC Socrata API...")
nndss_response <- httr::GET(
    url   = nndss_api_base,
    query = list(
        `$where` = "current_mmwr_year >= 2024",
        `$limit` = 500000,
        `$order` = ":id"
    )
)
httr::stop_for_status(nndss_response)
state_nndss_raw <- read_csv(
    httr::content(nndss_response, as = "text", encoding = "UTF-8"),
    show_col_types = FALSE
)

# The Socrata CSV endpoint returns lowercase-underscore field names rather than
# the display names that appear in a manually-downloaded CSV file.  Normalise
# to the display names so the rest of the script is consistent with v1.1.0.
#
# Socrata field name  →  display name used in this script
# ─────────────────────────────────────────────────────
# label               →  Label
# reporting_area      →  Reporting Area
# mmwr_week           →  MMWR WEEK
# current_mmwr_year   →  Current MMWR Year
# current_week        →  Current week
#
# If the endpoint ever changes column naming, adjust the rename() call below.

normalize_nndss_columns <- function(df) {
    # Collapse all names to lowercase-underscore for a consistent starting point
    names(df) <- tolower(gsub("[^a-zA-Z0-9]+", "_", names(df)))
    names(df) <- gsub("_+", "_", names(df))
    names(df) <- gsub("^_|_$", "", names(df))

    rename_map <- c(
        label               = "Label",
        reporting_area      = "Reporting Area",
        mmwr_week           = "MMWR WEEK",
        current_mmwr_year   = "Current MMWR Year",
        current_week        = "Current week"
    )
    for (old in names(rename_map)) {
        if (old %in% names(df)) {
            names(df)[names(df) == old] <- rename_map[[old]]
        }
    }
    df
}

state_nndss <- normalize_nndss_columns(state_nndss_raw)

# Filter to only the diseases we need (those present in disease_metadata.csv)
nndss_patterns <- nndss_label_map %>%
    semi_join(disease_meta, by = "disease") %>%
    pull(nndss_pattern)

state_nndss_filtered <- state_nndss %>%
    filter(rowSums(
        sapply(nndss_patterns, function(p) grepl(p, Label, ignore.case = TRUE))
    ) > 0)

message(sprintf("NNDSS rows retained after disease filter: %d", nrow(state_nndss_filtered)))


# =========================================================================
# SHARED HELPERS  (defined once, reused across all diseases)
# =========================================================================

# --- County population weights (2020 Decennial Census) -------------------

county_pops <- get_decennial(
    geography = "county",
    variables = "P1_001N",
    year      = 2020,
    sumfile   = "pl"
) %>%
    rename(population = value) %>%
    separate(NAME, into = c("county", "state"), sep = ", ") %>%
    mutate(state = state.abb[match(state, state.name)]) %>%
    filter(!is.na(state)) %>%
    select(state, geo_name = county, population)


# --- Multinomial split: state count → county counts ----------------------

split_to_counties <- function(state_name, count, county_pops) {
    county_df <- county_pops %>% filter(state == state_name)
    if (nrow(county_df) == 0) {
        return(tibble(geo_name = NA_character_, county_obs = count))
    }
    probs  <- county_df$population / sum(county_df$population)
    counts <- as.vector(rmultinom(1, size = count, prob = probs))
    tibble(geo_name = county_df$geo_name, county_obs = counts)
}


# --- Age expansion -------------------------------------------------------
# Takes a state-level dataset (with an `age_group` column set to "total") and
# returns age-stratified rows drawn from a multinomial distribution.

age_expand <- function(dat, age_df, seed = random_seed) {
    set.seed(seed)
    dat %>%
        dplyr::select(-age_group) %>%
        rowwise() %>%
        mutate(age_split = list({
            counts <- as.vector(rmultinom(
                n    = 1,
                size = count,
                prob = age_df$age_dist
            ))
            tibble(age_group = age_df$age_group, age_count = counts)
        })) %>%
        unnest(age_split) %>%
        ungroup() %>%
        dplyr::select(-count) %>%
        rename(count = age_count) %>%
        filter(count > 0)
}


# --- County expansion ----------------------------------------------------
# Takes a state-level dataset and returns county-level rows distributed by
# population weight.

county_expand <- function(dat, county_pops, seed = random_seed) {
    set.seed(seed)
    dat %>%
        dplyr::select(-geo_name, -geo_unit) %>%
        rowwise() %>%
        mutate(county_split = list(
            split_to_counties(state, count, county_pops)
        )) %>%
        unnest(county_split) %>%
        ungroup() %>%
        dplyr::select(-count) %>%
        rename(count = county_obs) %>%
        filter(count > 0) %>%
        mutate(age_group = "total", geo_unit = "county")
}


# =========================================================================
# GENERIC NNDSS DISEASE PROCESSOR
# =========================================================================
# Converts raw NNDSS rows for one disease into the standard state-level weekly
# tibble format used throughout this script.

process_nndss_disease <- function(nndss_data,
                                  nndss_pattern,
                                  disease_name_out,
                                  confirmation_status_out,
                                  outcome_out = "cases") {
    nndss_data %>%
        filter(grepl(nndss_pattern, Label, ignore.case = TRUE)) %>%
        mutate(state = c(state.abb, "DC")[match(
            tolower(`Reporting Area`),
            tolower(c(state.name, "DISTRICT OF COLUMBIA"))
        )]) %>%
        filter(!is.na(state)) %>%
        rename(
            week = `MMWR WEEK`,
            year = `Current MMWR Year`
        ) %>%
        mutate(
            report_period_end   = MMWRweek::MMWRweek2Date(year, week, 7),
            report_period_start = report_period_end - days(6)
        ) %>%
        rename(count = `Current week`) %>%
        mutate(
            date_type              = "cccd",
            disease_name           = disease_name_out,
            outcome                = outcome_out,
            age_group              = "total",
            disease_subtype        = "total",
            time_unit              = "week",
            geo_unit               = "state",
            confirmation_status    = confirmation_status_out,
            geo_name               = state,
            reporting_jurisdiction = state
        ) %>%
        dplyr::select(
            report_period_start, report_period_end, date_type, time_unit,
            disease_name, reporting_jurisdiction, state, geo_name, geo_unit,
            age_group, disease_subtype, confirmation_status, outcome, count
        ) %>%
        filter(!is.na(count)) %>%
        group_by(
            report_period_start, report_period_end, date_type, time_unit,
            disease_name, reporting_jurisdiction, state, geo_name, geo_unit,
            age_group, disease_subtype, confirmation_status, outcome
        ) %>%
        summarize(count = sum(count, na.rm = TRUE), .groups = "drop")
}


# =========================================================================
# MEASLES DATA  (pulled from separate GitHub repository)
# =========================================================================

message("Pulling measles data from GitHub...")
measles_raw <- read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/measles_data/refs/heads/main/measles_county_all_updates.csv",
    show_col_types = FALSE
)

measles_dat <- measles_raw %>%
    mutate(
        year = MMWRweek::MMWRweek(date)$MMWRyear,
        week = MMWRweek::MMWRweek(date)$MMWRweek
    ) %>%
    mutate(
        report_period_end   = MMWRweek::MMWRweek2Date(year, week, 7),
        report_period_start = report_period_end - days(6)
    ) %>%
    separate(location_name, into = c("geo_name", "state"), sep = ", ") %>%
    mutate(
        date_type       = "cccd",
        disease_name    = "measles",
        outcome         = "cases",
        age_group       = "total",
        disease_subtype = "total",
        time_unit       = "week"
    ) %>%
    rename(count = value, geo_unit = location_type) %>%
    mutate(confirmation_status = case_when(
        grepl("confirm", tolower(outcome_type)) ~ "confirmed",
        TRUE ~ NA
    )) %>%
    mutate(
        state                  = state.abb[match(state, state.name)],
        state                  = ifelse(is.na(state), "DC", state),
        reporting_jurisdiction = state
    )

# Aggregate to MMWR week
measles_dat_weekly <- measles_dat %>%
    group_by(
        report_period_start, report_period_end, date_type, time_unit,
        disease_name, reporting_jurisdiction, state, geo_name, geo_unit,
        age_group, disease_subtype, confirmation_status, outcome
    ) %>%
    summarize(count = sum(count, na.rm = TRUE), .groups = "drop") %>%
    mutate(
        geo_name = ifelse(
            geo_unit == "county" & !grepl("city|county", geo_name, ignore.case = TRUE),
            paste0(geo_name, " County"),
            geo_name
        ),
        geo_name = ifelse(
            geo_unit == "county" & grepl("unknown", geo_name, ignore.case = TRUE),
            "unknown",
            geo_name
        )
    )

# ~ Measles age expansion (state level) -----------------------------------

measles_state_total <- measles_dat_weekly %>%
    group_by(
        report_period_start, report_period_end, state, time_unit,
        disease_name, outcome, confirmation_status
    ) %>%
    summarise(count = sum(count, na.rm = TRUE), .groups = "drop") %>%
    mutate(
        reporting_jurisdiction = state,
        geo_unit               = "state",
        disease_subtype        = "total",
        geo_name               = state,
        date_type              = "cccd",
        age_group              = "total"
    )

measles_dat_weekly_age <- age_expand(measles_state_total, age_df_meas)


# =========================================================================
# PERTUSSIS DATA  (from NNDSS)
# =========================================================================

meta_pert <- disease_meta %>% filter(disease == "pertussis")

pertussis_dat_weekly_state <- process_nndss_disease(
    nndss_data              = state_nndss_filtered,
    nndss_pattern           = "Pertussis",
    disease_name_out        = "pertussis",
    confirmation_status_out = meta_pert$confirmation_status
)

# ~ Pertussis age expansion -----------------------------------------------
pertussis_dat_weekly_age <- age_expand(pertussis_dat_weekly_state, age_df_pert)

# ~ Pertussis county expansion --------------------------------------------
pertussis_dat_weekly_county <- county_expand(pertussis_dat_weekly_state, county_pops)


# =========================================================================
# MENINGOCOCCAL DISEASE DATA  (from NNDSS, with serogroup subtypes)
# =========================================================================

meta_mening <- disease_meta %>% filter(disease == "meningococcus")

mening_dat_weekly_state_raw <- state_nndss_filtered %>%
    filter(grepl("Meningococcal disease", Label, ignore.case = TRUE)) %>%
    mutate(state = c(state.abb, "DC")[match(
        tolower(`Reporting Area`),
        tolower(c(state.name, "DISTRICT OF COLUMBIA"))
    )]) %>%
    filter(!is.na(state)) %>%
    rename(
        week = `MMWR WEEK`,
        year = `Current MMWR Year`
    ) %>%
    mutate(
        report_period_end   = MMWRweek::MMWRweek2Date(year, week, 7),
        report_period_start = report_period_end - days(6)
    ) %>%
    rename(count = `Current week`) %>%
    mutate(
        date_type              = "cccd",
        disease_name           = "meningococcus",
        outcome                = "cases",
        age_group              = "total",
        disease_subtype        = "total",
        time_unit              = "week",
        geo_unit               = "state",
        confirmation_status    = meta_mening$confirmation_status,
        geo_name               = state,
        reporting_jurisdiction = state
    ) %>%
    dplyr::select(
        report_period_start, report_period_end, date_type, time_unit,
        disease_name, reporting_jurisdiction, state, geo_name, geo_unit,
        age_group, disease_subtype, confirmation_status, outcome, count, Label
    ) %>%
    filter(!is.na(count))

# Parse serogroup subtypes from NNDSS Label
mening_dat_weekly_state_serogroups <- mening_dat_weekly_state_raw %>%
    mutate(disease_type_temp = gsub("Meningococcal disease, ", "", Label)) %>%
    mutate(disease_subtype = case_when(
        grepl("All serogroups",  disease_type_temp) ~ "total",
        grepl("Serogroup B",     disease_type_temp) ~ "B",
        grepl("Serogroups ACWY", disease_type_temp) ~ "ACWY",
        grepl("Unknown|Other",   disease_type_temp) ~ "unknown",
        TRUE ~ NA
    )) %>%
    select(-disease_type_temp, -Label) %>%
    group_by(
        report_period_start, report_period_end, date_type, time_unit,
        disease_name, reporting_jurisdiction, state, geo_name, geo_unit,
        age_group, disease_subtype, confirmation_status, outcome
    ) %>%
    summarize(count = sum(count, na.rm = TRUE), .groups = "drop")

# Replace the combined ACWY category with specific serogroup values to enrich
# the example data
set.seed(random_seed)
acwy_idx <- which(mening_dat_weekly_state_serogroups$disease_subtype == "ACWY")
mening_dat_weekly_state_serogroups$disease_subtype[acwy_idx] <-
    sample(c("A", "C", "W", "Y"), size = length(acwy_idx), replace = TRUE)

# Total-subtype rows used for age and county expansion
mening_state_total <- mening_dat_weekly_state_serogroups %>%
    filter(disease_subtype == "total")

# ~ Meningococcus age expansion -------------------------------------------
mening_dat_weekly_state_age <- age_expand(mening_state_total, age_df_pert)

# ~ Meningococcus county expansion ----------------------------------------
mening_dat_weekly_county <- county_expand(mening_state_total, county_pops)


# =========================================================================
# ALL OTHER NNDSS DISEASES  (generic pipeline)
# =========================================================================
# For every disease in disease_metadata.csv that is neither measles nor
# meningococcus, run the generic NNDSS processor and then apply county and
# (where relevant) age expansion.

simple_nndss_meta <- nndss_label_map %>%
    filter(!disease %in% c("pertussis", "meningococcus")) %>%
    left_join(
        disease_meta %>% select(disease, confirmation_status, outcome,
                                aggregation_agegroups),
        by = "disease"
    ) %>%
    filter(!is.na(nndss_pattern))

# Process each disease to state-level weekly totals
simple_nndss_state_list <- pmap(
    list(
        nndss_pattern           = simple_nndss_meta$nndss_pattern,
        disease_name_out        = simple_nndss_meta$disease,
        confirmation_status_out = simple_nndss_meta$confirmation_status,
        outcome_out             = simple_nndss_meta$outcome
    ),
    function(nndss_pattern, disease_name_out, confirmation_status_out, outcome_out) {
        process_nndss_disease(
            nndss_data              = state_nndss_filtered,
            nndss_pattern           = nndss_pattern,
            disease_name_out        = disease_name_out,
            confirmation_status_out = confirmation_status_out,
            outcome_out             = outcome_out
        )
    }
)
names(simple_nndss_state_list) <- simple_nndss_meta$disease

# County expansion for all simple NNDSS diseases
simple_nndss_county_list <- lapply(
    simple_nndss_state_list,
    county_expand,
    county_pops = county_pops
)

# Age expansion only for diseases where disease_metadata flags aggregation_agegroups = TRUE
diseases_with_age <- simple_nndss_meta %>%
    filter(aggregation_agegroups == TRUE) %>%
    pull(disease)

simple_nndss_age_list <- lapply(
    simple_nndss_state_list[diseases_with_age],
    age_expand,
    age_df = age_df_pert
)


# =========================================================================
# BUILD COMPLETE DATASET
# =========================================================================

reported_data <- bind_rows(
    # Measles: GitHub source
    measles_dat_weekly,           # county-level, no age
    measles_dat_weekly_age,       # state-level, with age
    # Pertussis: NNDSS
    pertussis_dat_weekly_county,  # county-level, no age
    pertussis_dat_weekly_age,     # state-level, with age
    # Meningococcus: NNDSS, with serogroup subtypes
    mening_dat_weekly_county,
    mening_dat_weekly_state_age,
    mening_dat_weekly_state_serogroups %>% filter(disease_subtype != "total"),
    # All other NNDSS diseases
    bind_rows(simple_nndss_county_list),
    bind_rows(simple_nndss_age_list)
) %>%
    arrange(
        disease_name, report_period_start, report_period_end,
        state, geo_unit, reporting_jurisdiction,
        age_group, disease_subtype, confirmation_status
    ) %>%
    dplyr::select(
        report_period_start, report_period_end, date_type, time_unit,
        disease_name, reporting_jurisdiction, state, geo_unit, geo_name,
        age_group, disease_subtype, confirmation_status, outcome, count
    ) %>%
    filter(count > 0) %>%
    filter(report_period_start >= filter_start_date)


# =========================================================================
# VALIDATION CHECKS
# =========================================================================

total_check <- reported_data %>%
    group_by(disease_name, disease_subtype == "total", age_group == "total", state) %>%
    summarize(total_count = sum(count), .groups = "drop") %>%
    arrange(disease_name, state) %>%
    group_by(disease_name, state) %>%
    summarise(
        equal_counts = n_distinct(total_count) == 1,
        total_count  = paste(unique(total_count), collapse = ", "),
        .groups      = "drop"
    ) %>%
    arrange(disease_name, state)

message("States with mismatched total counts (should be empty):")
print(total_check %>% filter(!equal_counts))


# =========================================================================
# SAVE OUTPUT FILES
# =========================================================================

# write_csv(reported_data %>% filter(state == "MA"), "examples-and-templates/disease_tracking_report_MA-EXAMPLE_2026-02-09.csv")
# write_csv(reported_data %>% filter(state == "WA"), "examples-and-templates/disease_tracking_report_WA-SIMULATED-EXAMPLE_2026-02-09.csv")
write_csv(reported_data %>% filter(state == "CA"), "examples-and-templates/disease_tracking_report_CA-SIMULATED-EXAMPLE_2026-02-09.csv")
