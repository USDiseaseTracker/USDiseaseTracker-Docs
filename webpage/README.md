# Webpage Directory

This directory contains all files related to the US Disease Tracker documentation website that is published at:
**https://usdiseasetracker.github.io/USDiseaseTracker-Docs/**

## Contents

This directory contains the complete Jekyll-based documentation website, including:

- **`_config.yml`** - Jekyll configuration file
- **`Gemfile`** - Ruby dependencies for Jekyll
- **`index.html`** - Homepage/landing page
- **`_data/`** - Site data files (navigation structure)
- **`_docs/`** - Documentation pages (markdown files)
- **`_includes/`** - Reusable HTML components (header, footer, navigation)
- **`_layouts/`** - Page layout templates
- **`_sass/`** - SASS/SCSS stylesheets
- **`assets/`** - Static assets (CSS, JavaScript, images, fonts)
- **`data-standards-tool.html`** - Interactive data standards tool
- **`decision-tree.md`** - Decision tree tool page
- **`favicon.ico`** - Website favicon

## Local Development

To preview the website locally:

```bash
# Navigate to this directory
cd webpage

# Install dependencies
bundle install

# Serve the site locally
bundle exec jekyll serve

# View at http://localhost:4000/USDiseaseTracker-Docs/
```

## Deployment

The website is automatically built and deployed via GitHub Actions when changes are pushed to the `main` branch. See `.github/workflows/deploy-pages.yml` for the deployment configuration.

## More Information

For detailed setup and customization instructions, see:
- [GitHub Pages Setup Guide](../GITHUB-PAGES-SETUP.md)
- [Theme Summary](../NEW-THEME-SUMMARY.md)
