
# This script is designed to build an example dataset for the disease tracking report, using publicly available data on measles, pertussis, and meningococcal disease. 
# The script will pull data from the CDC, process it to fit the desired format, and save it as CSV files for specific states.


library(readr)
library(tidyverse)
library(MMWRweek)
library(lubridate)


# MEASLES DATA ------------------------------------------------------------

measles_dat <- read_csv("https://raw.githubusercontent.com/CSSEGISandData/measles_data/refs/heads/main/measles_county_all_updates.csv")

# agregate data to MMWR week
measles_dat <- measles_dat %>%
    mutate(year = MMWRweek::MMWRweek(date)$MMWRyear,
           week = MMWRweek::MMWRweek(date)$MMWRweek) %>%
    mutate(report_period_end = MMWRweek::MMWRweek2Date(year, week, 7)) %>%
    mutate(report_period_start = report_period_end - days(6)) %>%
    separate(location_name, into = c("geo_name", "state"), sep = ", ") %>%
    mutate(date_type = "cccd",
           disease_name = "measles",
           outcome = "cases",
           age_group = "total",
           disease_subtype = "total",
           time_unit = "week") %>%
    rename(count = value,
           geo_unit = location_type) %>%
    mutate(confirmation_status = case_when(
        grepl("confirm", tolower(outcome_type)) ~ "confirmed",
        TRUE ~ NA
    )) %>%
    # convert state names to abbreviations
    mutate(state = state.abb[match(state, state.name)]) %>%
    mutate(state = ifelse(is.na(state), "DC", state)) %>%
    mutate(reporting_jurisdiction = state)

measles_dat_weekly <- measles_dat %>%
    group_by(report_period_start,report_period_end,date_type, time_unit, disease_name, 
             reporting_jurisdiction, state, geo_name, geo_unit, age_group, disease_subtype, confirmation_status, outcome) %>%
    summarize(count = sum(count, na.rm = TRUE)) %>%
    ungroup() %>%
    mutate(geo_name = ifelse(geo_unit == "county" & !grepl("city", geo_name,ignore.case = TRUE), paste0(geo_name, " County"), geo_name))



# ~ Make Age-Specific Measles Data --------------------------------------------------

# distribute data to age groups assuming the following distributions. These distributions are just examples and can be adjusted as needed. 
# The "pert" distribution is more heavily weighted towards younger ages, while the "meas" distribution is more balanced across age groups.
#                     "<1 y" : 0.2
#                     "1-4 y" : 0.3
#                     "5-11 y" : 0.2
#                     "12-18 y" : 0.1
#                     "19-22 y" : 0.05
#                     "23-44 y" : 0.1
#                     "45-64 y" : 0.03
#                     ">=65 y" : 0.02
#                     "Unknown" : 0.0
age_groups <- c("<1 y",
                "1-4 y",
                "5-11 y",
                "12-18 y",
                "19-22 y",
                "23-44 y",
                "45-64 y",
                ">=65 y",
                "unknown")
age_dist_pert <- c(0, 0.3, 0.45, 0.0, 0.15, 0.1, 0.0, 0.0, 0.0)
age_df_pert <- data.frame(age_group = age_groups, age_dist = age_dist_pert)
age_dist_meas <- c(0.2, 0.2, 0.4, 0.1, 0.1, 0, 0.0, 0.0, 0.0)
age_df_meas <- data.frame(age_group = age_groups, age_dist = age_dist_meas)


dat_state <- measles_dat_weekly %>%
    group_by(report_period_start, report_period_end, state, 
             time_unit, disease_name, outcome, confirmation_status) %>%
    summarise(count = sum(count, na.rm = TRUE)) %>%
    ungroup() %>%
    mutate(reporting_jurisdiction = state,
           geo_unit = "state",
           disease_subtype = "total",
           geo_name = state,
           date_type = "cccd") 

set.seed(123) # for reproducibility

library(purrr)
# Example multinomial expansion
measles_dat_weekly_age <- dat_state %>%
    rowwise() %>%
    mutate(age_split = list({
        # sample counts across age groups
        counts <- as.vector(rmultinom(
            n = 1, 
            size = count, 
            prob = age_df_pert$age_dist
        ))
        tibble(
            age_group = age_df_pert$age_group,
            age_count = counts
        )
    })) %>%
    unnest(age_split) %>%
    ungroup() %>%
    dplyr::select(-count) %>%
    rename(count = age_count) %>%
    filter(count > 0)





# PERTUSSIS DATA ----------------------------------------------------------

# Download NNDSS from here: https://data.cdc.gov/NNDSS/NNDSS-Weekly-Data/x9gk-5huc/about_data

# load state-level pertussis data
# state_nndss <- read_csv("sandbox/NNDSS_Weekly_Data_20250919.csv")
# state_nndss <- read_csv("sandbox/NNDSS_Weekly_Data_20260210.csv")
# arrow::write_parquet(state_nndss, "sandbox/NNDSS_Weekly_Data_20260210.parquet")
state_nndss <- arrow::read_parquet("sandbox/NNDSS_Weekly_Data_20260210.parquet")


pertussis_dat_weekly_state <- state_nndss %>%
    filter(Label == "Pertussis") %>%
    mutate(state = c(state.abb, "DC")[match(`Reporting Area`, c(state.name, "District of Columbia"))]) %>%
    filter(!is.na(state)) %>%
    rename(week = `MMWR WEEK`,
           year = `Current MMWR Year`) %>%
    mutate(report_period_end = MMWRweek::MMWRweek2Date(year, week, 7)) %>%
    mutate(report_period_start = report_period_end - days(6)) %>%
    # rename(state = `Reporting Area`) %>%
    rename(count = `Current week`) %>%
    mutate(date_type = "cccd",
           disease_name = "pertussis",
           outcome = "cases",
           age_group = "total",
           disease_subtype = "total",
           time_unit = "week",
           geo_unit = "state",
           confirmation_status = "confirmed and probable") %>%
    # convert state names to abbreviations
    # mutate(state = ifelse(is.na(state), "DC", state)) %>%
    mutate(geo_name = state) %>%
    mutate(reporting_jurisdiction = state) %>%
    dplyr::select(report_period_start, report_period_end, date_type, time_unit, disease_name, 
                  reporting_jurisdiction, state, geo_name, geo_unit, age_group, disease_subtype, confirmation_status, outcome, count) %>%
    filter(!is.na(count))

pertussis_dat_weekly_state <- pertussis_dat_weekly_state %>%
    group_by(report_period_start,report_period_end,date_type, time_unit, disease_name, 
             reporting_jurisdiction, state, geo_name, geo_unit, age_group, disease_subtype, confirmation_status, outcome) %>%
    summarize(count = sum(count, na.rm = TRUE)) %>%
    ungroup() 




# ~ Pertussis by Age ------------------------------------------------------

set.seed(123) # for reproducibility

library(purrr)
# Example multinomial expansion
pertussis_dat_weekly_age <- pertussis_dat_weekly_state %>%
    dplyr::select(-age_group) %>%
    rowwise() %>%
    mutate(age_split = list({
        # sample counts across age groups
        counts <- as.vector(rmultinom(
            n = 1, 
            size = count, 
            prob = age_df_pert$age_dist
        ))
        tibble(
            age_group = age_df_pert$age_group,
            age_count = counts
        )
    })) %>%
    unnest(age_split) %>%
    ungroup() %>%
    dplyr::select(-count) %>%
    rename(count = age_count) %>%
    filter(count > 0)



# ~ distribute pertussis to counties --------------------------------------

library(tidycensus)
library(dplyr)
library(purrr)

# install if needed
# install.packages("tidycensus")

# You need a Census API key (get one at https://api.census.gov/data/key_signup.html)
# Once you have it, set it once per session:
# census_api_key("YOUR_KEY_HERE", install = TRUE)

# pull latest county-level population (here, 2020 Decennial Census total population)
county_pops <- get_decennial(
    geography = "county",
    variables = "P1_001N",  # total population
    year = 2020,
    sumfile = "pl"
) %>%
    rename(population = value) %>%
    separate(NAME, into = c("county", "state"), sep = ", ") %>%
    mutate(state = state.abb[match(state, state.name)])  # make state abbrev match dat

head(county_pops)

county_pops <- county_pops %>%
    filter(!is.na(state)) %>%  # remove territories not in dat
    select(state, geo_name=county, population) 


# function to split one state-level row into county-level rows
split_to_counties <- function(state_name, count, county_pops) {
    # filter counties for this state
    county_df <- county_pops %>%
        filter(state == state_name)
    
    # if no counties available, return original row with NA county
    if (nrow(county_df) == 0) {
        return(tibble(geo_name = NA_character_, county_obs = count))
    }
    
    # probability vector based on population
    probs <- county_df$population / sum(county_df$population)
    
    # multinomial draw
    counts <- as.vector(rmultinom(1, size = count, prob = probs))
    
    tibble(
        geo_name = county_df$geo_name,
        county_obs = counts
    )
}

# apply across dat
pertussis_dat_weekly_county <- pertussis_dat_weekly_state %>%
    dplyr::select(-geo_name, -geo_unit) %>%  # remove state-level geo info
    rowwise() %>%
    mutate(county_split = list(
        split_to_counties(state, count, county_pops)
    )) %>%
    unnest(county_split) %>%
    ungroup() %>%
    dplyr::select(-count) %>%
    rename(count = county_obs) %>%
    filter(count > 0) %>%
    mutate(age_group="total",
           geo_unit = "county")



# BUILD MENINGICOCCUS -----------------------------------------------------

mening_dat_weekly_state <- state_nndss %>%
    filter(grepl("Mening", Label)) %>%
    mutate(state = c(state.abb, "DC")[match(tolower(`Reporting Area`), tolower(c(state.name, "DISTRICT OF COLUMBIA")))]) %>%
    filter(!is.na(state)) %>%
    rename(week = `MMWR WEEK`,
           year = `Current MMWR Year`) %>%
    mutate(report_period_end = MMWRweek::MMWRweek2Date(year, week, 7)) %>%
    mutate(report_period_start = report_period_end - days(6)) %>%
    # rename(state = `Reporting Area`) %>%
    rename(count = `Current week`) %>%
    mutate(date_type = "cccd",
           disease_name = "meningicoccus",
           outcome = "cases",
           age_group = "total",
           disease_subtype = "total",
           time_unit = "week",
           geo_unit = "state",
           confirmation_status = "confirmed and probable") %>%
    # convert state names to abbreviations
    # mutate(state = ifelse(is.na(state), "DC", state)) %>%
    mutate(geo_name = state) %>%
    mutate(reporting_jurisdiction = state) %>%
    dplyr::select(report_period_start, report_period_end, date_type, time_unit, disease_name, 
                  reporting_jurisdiction, state, geo_name, geo_unit, age_group, disease_subtype, confirmation_status, outcome, count, Label) %>%
    filter(!is.na(count))

# Separate out serogroups of menning
mening_dat_weekly_state_serogroups <- mening_dat_weekly_state %>%
    mutate(disease_type_temp = gsub("Meningococcal disease, ", "", Label)) %>%
    mutate(disease_subtype = case_when(
        grepl("All serogroups", disease_type_temp) ~ "total",
        grepl("Serogroup B", disease_type_temp) ~ "B",
        grepl("Serogroups ACWY", disease_type_temp) ~ "ACWY",
        grepl("Unknown|Other", disease_type_temp) ~ "unknown",
        TRUE ~ NA
    )) %>%
    select(-disease_type_temp, -Label)


mening_dat_weekly_state_serogroups <- mening_dat_weekly_state_serogroups %>%
    group_by(report_period_start,report_period_end,date_type, time_unit, disease_name, 
             reporting_jurisdiction, state, geo_name, geo_unit, age_group, disease_subtype, confirmation_status, outcome) %>%
    summarize(count = sum(count, na.rm = TRUE)) %>%
    ungroup() 

# Replace the ACWY subtype with specific values to improve the example

acwy <- which(mening_dat_weekly_state_serogroups$disease_subtype == "ACWY")
n_acwy <- length(acwy)
mening_dat_weekly_state_serogroups$disease_subtype[acwy] <- sample(c("A", "C", "W", "Y"), size = n_acwy, replace = TRUE) 



# ~ Mening by Age ------------------------------------------------------

set.seed(123) # for reproducibility

library(purrr)
# Example multinomial expansion
mening_dat_weekly_state_age <- mening_dat_weekly_state_serogroups %>%
    filter(disease_subtype == "total") %>%  # only split the total rows, keep serogroup-specific rows as is")
    dplyr::select(-age_group) %>%
    rowwise() %>%
    mutate(age_split = list({
        # sample counts across age groups
        counts <- as.vector(rmultinom(
            n = 1, 
            size = count, 
            prob = age_df_pert$age_dist
        ))
        tibble(
            age_group = age_df_pert$age_group,
            age_count = counts
        )
    })) %>%
    unnest(age_split) %>%
    ungroup() %>%
    dplyr::select(-count) %>%
    rename(count = age_count) %>%
    filter(count > 0)

















# ~ distribute mening to counties --------------------------------------

library(tidycensus)
library(dplyr)
library(purrr)

# install if needed
# install.packages("tidycensus")

# You need a Census API key (get one at https://api.census.gov/data/key_signup.html)
# Once you have it, set it once per session:
# census_api_key("YOUR_KEY_HERE", install = TRUE)

# pull latest county-level population (here, 2020 Decennial Census total population)
county_pops <- get_decennial(
    geography = "county",
    variables = "P1_001N",  # total population
    year = 2020,
    sumfile = "pl"
) %>%
    rename(population = value) %>%
    separate(NAME, into = c("county", "state"), sep = ", ") %>%
    mutate(state = state.abb[match(state, state.name)])  # make state abbrev match dat

head(county_pops)

county_pops <- county_pops %>%
    filter(!is.na(state)) %>%  # remove territories not in dat
    select(state, geo_name=county, population) 


# function to split one state-level row into county-level rows
split_to_counties <- function(state_name, count, county_pops) {
    # filter counties for this state
    county_df <- county_pops %>%
        filter(state == state_name)
    
    # if no counties available, return original row with NA county
    if (nrow(county_df) == 0) {
        return(tibble(geo_name = NA_character_, county_obs = count))
    }
    
    # probability vector based on population
    probs <- county_df$population / sum(county_df$population)
    
    # multinomial draw
    counts <- as.vector(rmultinom(1, size = count, prob = probs))
    
    tibble(
        geo_name = county_df$geo_name,
        county_obs = counts
    )
}

# apply across dat
mening_dat_weekly_county <-  mening_dat_weekly_state_serogroups %>%
    filter(disease_subtype == "total") %>%  # only split the total rows, keep serogroup-specific rows as is")
    dplyr::select(-geo_name, -geo_unit) %>%  # remove state-level geo info
    rowwise() %>%
    mutate(county_split = list(
        split_to_counties(state, count, county_pops)
    )) %>%
    unnest(county_split) %>%
    ungroup() %>%
    dplyr::select(-count) %>%
    rename(count = county_obs) %>%
    filter(count > 0) %>%
    mutate(age_group="total",
           geo_unit = "county")






















# BUILD COMPLETE DATA SET -------------------------------------------------

reported_data <- bind_rows(
    measles_dat_weekly,           # weekly measles data by county, no age
    measles_dat_weekly_age,       # weekly measles data by state, with age
    pertussis_dat_weekly_county,  # weekly pertussis data by county, no age  ---> duplicative of the age data
    pertussis_dat_weekly_age,   # weekly pertussis data by state, with age  ---> not being reported at this time
    mening_dat_weekly_county,
    mening_dat_weekly_state_age,
    mening_dat_weekly_state_serogroups %>% filter(disease_subtype != "total")
) %>%
    arrange(disease_name, report_period_start, report_period_end, 
            state, geo_unit, reporting_jurisdiction, 
            age_group, disease_subtype, confirmation_status) %>%
    dplyr::select(report_period_start, report_period_end, date_type, time_unit, 
                  disease_name, reporting_jurisdiction, state, geo_unit, geo_name,  
                  age_group, disease_subtype, confirmation_status, outcome, count) %>%
    filter(count > 0) %>%
    filter(report_period_start >= as.Date("2024-12-29"))




# Check totals


total_check <- reported_data %>%
    group_by(disease_name, disease_subtype=="total", age_group=="total", state) %>%
    summarize(total_count = sum(count)) %>%
    ungroup() %>%
    arrange(disease_name, state) %>% 
  group_by(disease_name, state) %>%
    summarise(equal_counts = n_distinct(total_count) == 1,
              total_count = paste(unique(total_count), collapse = ", ")) %>%
    ungroup() %>%
    arrange(disease_name, state)

total_check %>%
    filter(!equal_counts)


# Cases by state, mening subtype
reported_data %>%
  filter(disease_subtype != "total") %>%
  View()







# save as disease_tracking_report_{state}_{report_date}

# write_csv(reported_data %>% filter(state == "MA"), "examples-and-templates/disease_tracking_report_MA-EXAMPLE_2026-02-09.csv")
write_csv(reported_data %>% filter(state == "WA"), "examples-and-templates/disease_tracking_report_WA-EXAMPLE_2026-02-09.csv")
write_csv(reported_data %>% filter(state == "CA"), "examples-and-templates/disease_tracking_report_CA-EXAMPLE_2026-02-09.csv")







