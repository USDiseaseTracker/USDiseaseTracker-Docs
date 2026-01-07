## Description

<!-- Provide a brief description of your changes -->

## Type of Change

<!-- Check all that apply -->

- [ ] New data standard
- [ ] Update to existing standard
- [ ] New template
- [ ] New example data
- [ ] New validation script
- [ ] Documentation update
- [ ] Bug fix
- [ ] Other (please describe):

## Checklist

<!-- Check all that apply to your contribution -->

### For New Standards

- [ ] Standard definition document created in `standards/`
- [ ] At least one complete example in `examples-and-templates/`
- [ ] Validation script created in `data-raw/`
- [ ] Entry added to `INDEX.md`
- [ ] Version number and change log included
- [ ] All fields have clear definitions and data types
- [ ] Validation rules documented

### For Standard Updates

- [ ] Version number incremented
- [ ] Change log updated
- [ ] Examples updated (if applicable)
- [ ] Validation script updated (if applicable)
- [ ] Breaking changes documented

### General

- [ ] All example data files are valid CSV format
- [ ] Validation scripts tested and working
- [ ] Markdown files properly formatted
- [ ] No sensitive or confidential data included
- [ ] Documentation is clear and complete

## Testing

<!-- Describe how you tested your changes -->

```r
# Example test code
source("data-raw/validate_your_standard.R")
result <- validate_your_standard(example_data)
# result$valid should be TRUE
```

## Related Issues

<!-- Link any related issues using #issue_number -->

Closes #

## Additional Notes

<!-- Any additional information reviewers should know -->
