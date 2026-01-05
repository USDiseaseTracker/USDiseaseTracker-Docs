# Contributing to US Disease Tracker Docs

Thank you for your interest in contributing to the US Disease Tracker documentation! This document provides guidelines for contributing data standards, templates, examples, and validation scripts.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and collaborative environment.

## How to Contribute

### Reporting Issues

If you find an error in the documentation or have a suggestion:

1. Check if the issue already exists in [GitHub Issues](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/issues)
2. If not, create a new issue with a clear title and description
3. Include relevant examples or references

### Proposing New Standards

To propose a new data standard:

1. Open an issue describing the proposed standard
2. Discuss the scope and requirements with maintainers
3. Once approved, follow the contribution workflow below

## Contribution Workflow

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR-USERNAME/USDiseaseTracker-Docs.git
cd USDiseaseTracker-Docs
```

### 2. Create a Branch

```bash
git checkout -b feature/your-standard-name
```

### 3. Make Your Changes

#### Creating a New Standard

1. **Copy the template:**
   ```bash
   cp templates/standard-definition-template.md standards/your-standard-name.md
   ```

2. **Fill in all sections:**
   - Overview and scope
   - Required and optional fields
   - Data types and validation rules
   - Examples
   - Change log

3. **Create example data:**
   ```bash
   # Create at least one complete example and one minimal example
   touch examples/your_standard_example.json
   touch examples/your_standard_minimal.json
   ```

4. **Create a validation script:**
   ```bash
   touch data-raw/validate_your_standard.R
   ```
   
   (Coming soon: validation script templates will be provided)

5. **Update the index:**
   Add your standard to `INDEX.md`

#### Updating an Existing Standard

1. Update the standard document in `standards/`
2. Increment the version number
3. Add entry to the Change Log section
4. Update examples if needed
5. Update validation script if validation rules changed

### 4. Test Your Changes

```r
# Source your validation script
source("data-raw/validate_your_standard.R")

# Test with example data
# Ensure validation passes for valid examples
# Ensure validation fails appropriately for invalid data
```

### 5. Document Your Changes

- Update `INDEX.md` with your new standard
- Ensure all markdown files are properly formatted

### 6. Commit and Push

```bash
git add .
git commit -m "Add [standard name] data standard"
git push origin feature/your-standard-name
```

### 7. Create a Pull Request

1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill in the PR template with:
   - Description of changes
   - Motivation for the standard
   - Any breaking changes
   - Checklist of requirements

## Standard Requirements

All data standards must include:

- [ ] Complete standard definition document
- [ ] At least one complete example
- [ ] At least one minimal example (required fields only)
- [ ] Validation script
- [ ] Entry in `INDEX.md`
- [ ] Version number and change log
- [ ] Clear field definitions with data types
- [ ] Validation rules

## Style Guidelines

### Markdown

- Use ATX-style headers (`#` instead of underlining)
- Include blank lines before and after headers
- Use tables for field definitions
- Include code blocks with language specifiers

### R Code

- Follow the [tidyverse style guide](https://style.tidyverse.org/)
- Use meaningful variable names
- Include comments for complex logic
- Provide examples in function documentation

### JSON Examples

- Use 2-space indentation
- Include all required fields
- Use realistic example values
- Follow the standard field names exactly

## Review Process

1. **Automated checks:** GitHub Actions will build and deploy the documentation site
2. **Maintainer review:** A maintainer will review your contribution for:
   - Completeness
   - Accuracy
   - Consistency with existing standards
   - Documentation quality
3. **Revisions:** You may be asked to make changes
4. **Approval:** Once approved, your contribution will be merged

## Questions?

If you have questions about contributing:

1. Check the [Setup Guide](SETUP.md)
2. Review existing standards in `standards/`
3. Open an issue with the `question` label

## License

By contributing, you agree that your contributions will be licensed under the GNU General Public License v3.0 or later.

Thank you for contributing to US Disease Tracker!
