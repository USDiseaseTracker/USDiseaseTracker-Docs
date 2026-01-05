#' Validate Case Report Data
#'
#' This function validates case report data against the case reporting standard.
#'
#' @param data A list or data frame containing case report data
#' @return A list with components 'valid' (logical) and 'errors' (character vector)
#' @examples
#' \dontrun{
#' # Read example data
#' data <- jsonlite::fromJSON("inst/examples/case_report_example.json")
#' 
#' # Validate
#' result <- validate_case_report(data)
#' print(result)
#' }
validate_case_report <- function(data) {
  errors <- character()
  
  # Check required fields
  required_fields <- c("case_id", "report_date", "disease_code", 
                       "jurisdiction", "age", "sex")
  
  for (field in required_fields) {
    if (!field %in% names(data) || is.null(data[[field]]) || 
        (is.character(data[[field]]) && nchar(data[[field]]) == 0)) {
      errors <- c(errors, paste("Missing required field:", field))
    }
  }
  
  # Validate data types and formats
  if ("age" %in% names(data)) {
    if (!is.numeric(data$age) || data$age < 0 || data$age > 120) {
      errors <- c(errors, "Age must be between 0 and 120")
    }
  }
  
  if ("sex" %in% names(data)) {
    if (!data$sex %in% c("M", "F", "U", "O")) {
      errors <- c(errors, "Sex must be M, F, U, or O")
    }
  }
  
  if ("jurisdiction" %in% names(data)) {
    if (nchar(data$jurisdiction) != 2) {
      errors <- c(errors, "Jurisdiction must be a two-letter state code")
    }
  }
  
  # Validate date format
  if ("report_date" %in% names(data)) {
    tryCatch({
      as.Date(data$report_date)
    }, error = function(e) {
      errors <<- c(errors, "report_date must be in ISO 8601 format (YYYY-MM-DD)")
    })
  }
  
  # Return validation result
  list(
    valid = length(errors) == 0,
    errors = if (length(errors) > 0) errors else NULL
  )
}
