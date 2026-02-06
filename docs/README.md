# MkDocs Documentation Setup

This directory contains the MkDocs documentation source files for the US Disease Tracker Documentation website.

## Structure

```
docs/
├── index.md                    # Homepage
├── data-standards-tool.md      # Data Standards Tool page
├── data-standards-tool.html    # Interactive Data Standards Tool (HTML)
├── examples-and-templates.md   # Examples and Templates page
├── CONTRIBUTING.md             # Symlink to ../CONTRIBUTING.md
└── guides/                     # Symlink to ../guides/
```

## Building the Documentation

### Prerequisites

- Python 3.x
- pip

### Installation

Install MkDocs and the Material theme:

```bash
pip install mkdocs-material
```

### Local Development

To preview the documentation locally:

```bash
mkdocs serve
```

This will start a development server at `http://127.0.0.1:8000/USDiseaseTracker-Docs/`

### Building for Production

To build the static site:

```bash
mkdocs build
```

The built site will be in the `site/` directory.

## Configuration

The site configuration is in `mkdocs.yml` at the repository root. Key settings:

- **Theme**: Material for MkDocs
- **Navigation**: Organized into Guides, Tools, Examples, and Contributing sections
- **Features**: Search, syntax highlighting, code copying, dark mode
- **Base URL**: `/USDiseaseTracker-Docs/` for GitHub Pages

## Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the `main` branch. See `.github/workflows/deploy-pages.yml` for the deployment workflow.

## Adding New Content

### Adding a New Guide

1. Create a new Markdown file in the `guides/` directory
2. Add it to the navigation in `mkdocs.yml` under the `Guides` section

### Adding a New Page

1. Create a new Markdown file in the `docs/` directory
2. Add it to the navigation in `mkdocs.yml`

### Linking to Files

- **Internal documentation links**: Use relative paths (e.g., `guides/data-submission-guide.md`)
- **External files in repository**: Use full GitHub URLs (e.g., `https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/blob/main/examples-and-templates/...`)
- **Images**: Store in `docs/assets/images/` and reference with relative paths

## Theme Customization

The Material theme supports extensive customization. See the [Material for MkDocs documentation](https://squidfunk.github.io/mkdocs-material/) for options.

Current customizations:
- Primary and accent colors: Teal
- Light and dark mode support
- Navigation tabs and sections
- Search with suggestions
- Code copy buttons

## Notes

- The `guides/` directory is a symbolic link to `../guides/` to avoid duplication
- The `data-standards-tool.html` is copied from `../data_standards_tool/` during build
- The site uses the `/USDiseaseTracker-Docs/` base URL for GitHub Pages deployment
