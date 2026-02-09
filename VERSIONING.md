# Versioning Documentation

This repository uses two tools for versioning:

## Release Drafter

Release Drafter automatically creates draft releases based on merged pull requests. When PRs are merged to the `main` branch, they are automatically added to a draft release.

### Usage

1. **Label your PRs**: Add labels to your pull requests to categorize them:
   - `feature` or `enhancement` - For new features
   - `bug` or `fix` - For bug fixes
   - `documentation` or `docs` - For documentation changes
   - `chore` or `dependencies` - For maintenance tasks
   - `major`, `minor`, or `patch` - For version bumping (default is `patch`)

2. **Review the draft release**: Check the automatically generated draft release in the [Releases](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/releases) page.

3. **Publish the release**: Edit the draft release, update the title and description if needed, and publish it with a version tag (e.g., `v1.0.0`).

## MkDocs Versioning with Mike

Mike manages versioned documentation on the MkDocs site. Each tagged release creates a new version of the documentation.

### How it works

- **Development version**: Commits to the `main` branch deploy to the `dev` version
- **Tagged releases**: When you create a tag (e.g., `v1.0.0`), the documentation is deployed to that version and marked as `latest`
- **Version selector**: Users can switch between documentation versions using the version selector in the site header

### Workflow

1. **Automatic deployment on push to main**: Documentation is built and deployed as `dev` version
2. **Automatic deployment on tag creation**: When a release tag is created (e.g., `v1.0.0`):
   - Documentation is built and deployed with that version number
   - The version is aliased as `latest`
   - The `latest` alias is set as the default version

### Manual deployment

To manually deploy a version (requires write access):

```bash
# Install dependencies
pip install mkdocs-material mike

# Deploy a new version
mike deploy --push --update-aliases v1.0.0 latest

# Set default version
mike set-default --push latest

# List all versions
mike list

# Delete a version
mike delete --push version-name
```

### Version management commands

```bash
# Serve locally to preview versions
mike serve

# Deploy without pushing
mike deploy v1.0.0

# Update aliases
mike alias v1.0.0 stable
```

## Creating a new release

1. Merge your PRs to `main` with appropriate labels
2. Review the auto-generated draft release
3. Edit and publish the release with a version tag (e.g., `v1.0.0`)
4. The GitHub Action will automatically deploy the versioned documentation
5. Users can now view the documentation for this specific version

## Configuration Files

- `.github/release-drafter.yml` - Release Drafter configuration
- `.github/workflows/release-drafter.yml` - Release Drafter workflow
- `.github/workflows/deploy-pages.yml` - MkDocs deployment workflow with mike
- `mkdocs.yml` - MkDocs configuration with mike plugin
